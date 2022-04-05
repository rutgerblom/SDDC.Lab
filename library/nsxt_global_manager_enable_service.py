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
module: nsxt_global_manager_enable_service
short_description: 'Enables global manager service first time after deployment and makes it active'
description: "Enables global manager service first time after deployment  and makes it active'"
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
    display_name:
        description: "Identifier to use when displaying entity in logs or GUI. Defaults to ID if not set'
        required: false
        type: str
    id:
        description: 'Unique identifier of this global manager'
        required: true
        type: str        
'''

EXAMPLES = '''
- name: Enables global manager service first time after deployment and makes it active
  nsxt_global_manager_enable_service:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    display_name: "GM First"
    id: "GM-1"
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native
import ssl
import socket
import hashlib


def get_global_manager_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args


def get_global_managers(module, url, mgr_username, mgr_password, validate_certs):
    try:
        (rc, resp) = request(url, headers=dict(Accept='application/json'),
                             url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs,
                             ignore_errors=True)
    except Exception as err:
        module.fail_json(msg='Error accessing global manager. Error [%s]' % (to_native(err)))
    return resp


def get_global_manager_from_id(module, url, mgr_username, mgr_password, validate_certs, id):
    global_managers = get_global_managers(module, url, mgr_username, mgr_password, validate_certs)
    for global_manager in global_managers['results']:
        if global_manager.__contains__('id') and global_manager['id'] == id:
            return global_manager
    return None

def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(username=dict(required=False, type='str'),
                         password=dict(required=False, type='str'),
                         hostname=dict(required=True, type='str'),
                         display_name=dict(required=False, type='str'),
                         id=dict(required=True, type='str'))

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    global_manager_params = get_global_manager_params(module.params.copy())
    mgr_hostname = module.params['hostname']
    mgr_username = module.params['username']
    mgr_password = module.params['password']
    validate_certs = module.params['validate_certs']
    id = module.params['id']
    manager_url = 'https://{}/global-manager/api/v1'.format(mgr_hostname)
    global_manager_api_url = manager_url + '/global-infra/global-managers'

    existing_global_manager = get_global_manager_from_id(module, global_manager_api_url, mgr_username, mgr_password,
                                                     validate_certs, id)
    global_manager_id, revision = None, None

    if existing_global_manager:
        if existing_global_manager['mode'] == 'ACTIVE':
            module.exit_json(changed=False, message="Global manager with id %s already exists in ACTIVE mode." % module.params['id'])
        else:
            module.fail_json(msg="Global manager with id %s as a standby mode. Use other module to make it active " % module.params['id'])
    else:
        headers = dict(Accept="application/json")
        headers['Content-Type'] = 'application/json'

        global_manager_params["mode"] = "ACTIVE"
        # add the global_manager
        request_data = json.dumps(global_manager_params)

        if module.check_mode:
            module.exit_json(changed=True, debug_out=str(request_data), id=module.params['id'])

        try:
            (rc, resp) = request(global_manager_api_url + '/%s' % module.params['id'], data=request_data,
                                     headers=headers, method='PATCH',
                                     url_username=mgr_username, url_password=mgr_password,
                                     validate_certs=validate_certs, ignore_errors=True)
        except Exception as err:
            module.fail_json(
                    msg="Failed to activate global manager service. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

        module.exit_json(changed=True, id=module.params['id'], body=str(resp),
                         message="Global manager with id %s is activated." % module.params['id'])

if __name__ == '__main__':
    main()
