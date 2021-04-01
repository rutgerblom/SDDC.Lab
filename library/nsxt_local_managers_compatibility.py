#!/usr/bin/env python
#
# Copyright 2021 VMware, Inc.
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
module: nsxt_local_managers_compatibility
short_description: 'Checks the compatibility of a local manager for registration with a global manager'
description: "Checks the compatibility of a local manager for registration with a global manager"
version_added: '3.2'
author: 'Kaushik Lele'
options:
    hostname:
        description: 'Deployed NSX Global manager hostname.'
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
    site_connection_info:
        fqdn:
            description: 'IP address or hostname of local manager'
            required: true
            type: str
        password:
            description: "Password for the user"
            no_log: 'True'
            required: false
            type: str
        required: false
        thumbprint:
            description: 'Thumbprint of local manager in the form of a SHA-256 hash represented in lower case HEX'
            no_log: 'True'
            required: false
            type: str
        username:
            description: 'Username value of the local manager'
            required: false
            type: str   
'''

EXAMPLES = '''
- name: Checks the compatibility of a local manager for registration with a global manager
  nsxt_local_managers_compatibility:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    site_connection_info:
      fqdn: "10.161.244.213"
      username: "admin"
      password: "Admin!23"
      thumbprint: "1a4eeaef05ad711c84d688cfb72001d17a4965a963611d9af63fb86ff55276cf"
'''

RETURN = '''
version_compatible:
    description: Specifies whether local manager version is compatible with global manager.
    type: bool
    returned: when API invocation is successful
'''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native
import ssl
import socket
import hashlib

def get_local_manager_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)

    return args

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(site_connection_info=dict(required=False, type='dict', no_log=True,
                    username=dict(required=False, type='str'),
                    password=dict(required=False, type='str'),
                    thumbprint=dict(required=False, type='str'),
                    fqdn=dict(required=True, type='str')))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  local_manager_params = get_local_manager_params(module.params.copy())
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  manager_url = 'https://{}/global-manager/api/v1'.format(mgr_hostname)
  check_copmatibility_api_url = manager_url + '/global-infra/onboarding-check-compatibility'
  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'


  request_data = json.dumps(local_manager_params['site_connection_info'])
  try:
    (rc, resp) = request(check_copmatibility_api_url, data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
  except Exception as err:
    module.fail_json(msg='Error accessing local manager. Error [%s]' % (to_native(err)))

  module.exit_json(changed=False, **resp)

if __name__ == '__main__':
    main()
