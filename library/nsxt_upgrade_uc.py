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
module: nsxt_upgrade_uc
short_description: 'Upgrade the upgrade coordinator'
description: "Upgrade the upgrade coordinator"
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
'''

EXAMPLES = '''
- name: Upgrade UC
  nsxt_upgrade_uc:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils.common_utils import wait_for_operation_to_execute, get_upgrade_orchestrator_node
from ansible.module_utils._text import to_native


def main():
  argument_spec = vmware_argument_spec()

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']

  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'

  mgr_hostname = get_upgrade_orchestrator_node(module, mgr_hostname, mgr_username, 
                                            mgr_password, headers, validate_certs)

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  # Upgrade UC
  if module.check_mode:
    module.exit_json(changed=False, debug_out='Upgrade Coordinator '
                     'will be upgraded.', id=mgr_hostname)

  try:
    (rc, resp) = request(manager_url+ '/upgrade?action=upgrade_uc', data='',
                         headers=headers, method='POST', url_username=mgr_username,
                         url_password=mgr_password, validate_certs=validate_certs,
                         ignore_errors=True)
  except Exception as err:
    module.fail_json(msg='Failed to upgrade UC. Error[%s].' % to_native(err))

  time.sleep(5)

  try:
    wait_for_operation_to_execute(manager_url, '/upgrade/uc-upgrade-status', 
                                  mgr_username, mgr_password, validate_certs, 
                                  ['state'], ['SUCCESS'], ['FAILED'])
  except Exception as err:
    module.fail_json(msg='Error while upgrading UC. Error [%s]' % to_native(err))
  module.exit_json(changed=True, result=resp, message='UC is upgraded'
                                                      ' successfully.')

if __name__ == '__main__':
    main()
