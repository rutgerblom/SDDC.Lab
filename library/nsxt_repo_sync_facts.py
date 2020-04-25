#!/usr/bin/env python
#
# Copyright 2019 VMware, Inc.
# SPDX-License-Identifier: BSD-2-Clause OR GPL-3.0-only
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: nsxt_repo_sync_facts
short_description: 'Get synchronize status of a manager node'
description: "Returns the synchronization status for the manager represented by given ."
version_added: '2.7'
author: 'Kommireddy Akhilesh'
options:
    hostname:
        description: 'Deployed NSX manager hostname.'
        required: true
        type: str
    username:
        description: 'The username to authenticate with the NSX manager.'
        required: true
        type: str
    password:
        description: 'The password to authenticate with the NSX manager.'
        required: true
        type: str
    node_name:
        description: 'Name of auto-deployment node'
        required: true
        type: str
'''

EXAMPLES = '''
- name: Get repo sync status of an auto deployed node
  nsxt_repo_sync_facts:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      node_name: "Manager-01"
      state: present
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils.common_utils import get_id_from_display_name_results
from ansible.module_utils._text import to_native

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(node_name=dict(required=True, type='str'))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  manager_node_name = module.params['node_name']

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  manager_node_id = get_id_from_display_name_results(module, manager_url, 
    '/cluster/nodes/deployments', mgr_username, mgr_password, validate_certs,
    ['deployment_config','hostname'], ['vm_id'], manager_node_name)

  changed = False
  try:
    (rc, resp) = request(manager_url + '/cluster/nodes/%s/repo_sync/status' % manager_node_id,
                         headers=dict(Accept='application/json'), url_username=mgr_username,
                         url_password=mgr_password, validate_certs=validate_certs,
                         ignore_errors=True)
  except Exception as err:
    module.fail_json(msg='Error accessing manager node repo sync '
                                  'status. Error [%s]' % (to_native(err)))

  module.exit_json(changed=changed, **resp)

if __name__ == '__main__':
    main()
