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
module: nsxt_upgrade_eula_accept_facts
short_description: 'Gets EULA acceptance status and contents'
description: "Returns EULA acceptance status and the contents."
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
    required_info:
        choices:
            - acceptance
            - contents
        description: "required_info can be either 'acceptance' or 'contents'.
                      'acceptance' returns the acceptance status of end user license agreement .
                      'contents' Return the content of end user license agreement in the specified format. 
                       By default, it's pure string without line break. "
        required: true
'''

EXAMPLES = '''
- name: Gets EULA acceptance status and contents
  nsxt_upgrade_eula_accept_facts:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      required_info: "acceptance"
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils.common_utils import get_id_from_display_name_results
from ansible.module_utils._text import to_native

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(required_info=dict(required=True, type='str', 
                       choices=['acceptance', 'contents']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  required_info = module.params['required_info']

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  if required_info == 'acceptance':
    try:
      (rc, resp) = request(manager_url + '/upgrade/eula/acceptance',
                           headers=dict(Accept='application/json'), url_username=mgr_username,
                           url_password=mgr_password, validate_certs=validate_certs,
                           ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing upgrade EULA acceptance '
                                    'status. Error [%s]' % (to_native(err)))
    module.exit_json(changed=False, **resp)
  elif required_info == 'contents':
    try:
      (rc, resp) = request(manager_url + '/upgrade/eula/content',
                           headers=dict(Accept='application/json'), url_username=mgr_username,
                           url_password=mgr_password, validate_certs=validate_certs,
                           ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing upgrade EULA contents '
                                    'status. Error [%s]' % (to_native(err)))

    module.exit_json(changed=False, **resp)
  else:
    module.fail_json(msg='Invalid value passed for required_info.')

if __name__ == '__main__':
    main()
