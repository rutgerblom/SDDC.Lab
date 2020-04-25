#!/usr/bin/env python
#
# Copyright 2018 VMware, Inc.
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
module: nsxt_licenses
short_description: 'Add a new license key'
description: "This will add a license key to the system.
              The API supports adding only one license key for each license edition
              type - Standard, Advanced or Enterprise. If a new license key is tried
              to add for an edition for which the license key already exists,
              then this API will return an error."
version_added: '2.7'
author: 'Rahul Raghuvanshi'
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
    license_key:
        description: 'license key'
        no_log: 'True'
        required: true
        type: str
    state:
        choices:
            - present
            - absent
        description: "State can be either 'present' or 'absent'.
                      'present' is used to create or update resource.
                      'absent' is used to delete resource."
        required: true   
'''

EXAMPLES = '''
- name: Add license
  nsxt_licenses:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      license_key: "11111-22222-33333-44444-55555"
      state: present
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def get_license_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def check_license_exist(module, manager_url, mgr_username, mgr_password, validate_certs):
    id = module.params['license_key']
    try:
      (rc, resp) = request(manager_url+ '/licenses/%s' % id, headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      return False
    return True

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(license_key=dict(required=True, type='str', no_log=True),
                    state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  license_params = get_license_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'
  request_data = json.dumps(license_params)

  if state == 'present':
    # add the license
    if check_license_exist(module, manager_url, mgr_username, mgr_password, validate_certs):
        module.exit_json(changed=False, message="license with license key %s already exist."% module.params['license_key'])
    if module.check_mode:
       module.exit_json(changed=True, debug_out=str(request_data), id=module.params['license_key'])
    try:
        (rc, resp) = request(manager_url+ '/licenses', data=request_data, headers=headers, method='POST',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
        module.fail_json(msg="Failed to add license. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, result=resp, message="license with license key %s created." % module.params['license_key'])

  elif state == 'absent':
    # delete the license key
    id = module.params['license_key']
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(request_data), id=id)
    try:
       (rc, resp) = request(manager_url+ '/licenses/' + id, method='DELETE',
                            url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg="Failed to delete license with id %s. Error[%s]." % (id, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=id, message="license with license key %s deleted." % id)


if __name__ == '__main__':
    main()
