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
module: nsxt_vidm
short_description: 'Register a vIDM with NSX'
description: "Register a vIDM with NSX"
version_added: '3.2'
author: 'Kaushik Lele'
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
    client_id:
        description: 'vIDM client id'
        required: true
        type: str
    client_secret:
        description: 'vIDM client secret'
        required: false
        type: str
    host_name:
        description: 'Fully Qualified Domain Name(FQDN) of vIDM'
        required: false
        type: str                
    lb_enable:
        description: 'Load Balancer enable flag'
        required: false
        type: bool
    node_host_name:
        description: "Host name of the node redirected to
            host name to use when creating the redirect URL for clients to follow after authenticating to vIDM"
        required: true
        type: bool    
    thumbprint:
        description: "vIDM certificate thumbprint
            Hexadecimal SHA256 hash of the vIDM server's X.509 certificate"
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
- name: Register vIDM with NSX
  nsxt_vidm:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    client_id: "OAuth2Client_NsxClientId",
    client_secret: "23424234234234"
    host_name: "lbhost_vidm.eng.vmware.com",
    lb_enable: False
    node_host_name: "jt-vidm.eng.vmware.com"
    thumbprint: "898b75618e3e56615d53f987a720ff22b6381f4b85bec1eb973214ff7361f8b8"
    state: present
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native
import ssl
import socket
import hashlib


def get_vidm_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args


def get_vidm(module, url, mgr_username, mgr_password, validate_certs):
    try:
        (rc, resp) = request(url, headers=dict(Accept='application/json'),
                             url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs,
                             ignore_errors=True)
    except Exception as err:
        module.fail_json(msg='Error accessing vidm details. Error [%s]' % (to_native(err)))
    return resp


def get_vidm_from_client_id(module, url, mgr_username, mgr_password, validate_certs, client_id):
    vidm = get_vidm(module, url, mgr_username, mgr_password, validate_certs)
    if vidm['client_id'] == client_id:
        return vidm
    return None


def wait_till_create(module, url, mgr_username, mgr_password, validate_certs):
    retry_counter = 0
    try:
        while True:

            try:
                (rc, resp) = request(url + '/status', headers=dict(Accept='application/json'),
                                     url_username=mgr_username, url_password=mgr_password,
                                     validate_certs=validate_certs, ignore_errors=True)
                if resp['runtime_state'] != "ALL_OK":
                    if retry_counter < 6:
                        time.sleep(5)
                        retry_counter = retry_counter + 1
                    else:
                        module.fail_json(
                            msg='Failed to register vIDM. runtime state is : %s' % (str(resp["runtime_state"])))
                else:
                    break;
            except Exception as err:
                # When registration is in progress and status is not yet accessible then it can throw error.
                #  {'error_code': 36514, 'error_message': 'Error when requesting to verify VMware Identity Manager user access client',
                # So retry is needed in error case as well.
                if retry_counter < 6:
                    retry_counter = retry_counter + 1
                    time.sleep(5)
                else:
                    module.fail_json(msg='Failed to register vIDM. runtime state is : %s' % (to_native(err)))
    except Exception as err:
        module.fail_json(msg='Error accessing vIDM status. Error [%s]' % (to_native(err)))
    return


def wait_till_delete(module, url, mgr_username, mgr_password, validate_certs):
    retry_counter = 0
    try:
        while True:
            (rc, resp) = request(url + '/status', headers=dict(Accept='application/json'),
                                 url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs,
                                 ignore_errors=True)
            if resp['runtime_state'] != "NOT_OK" or resp['vidm_enable'] is not False:
                if retry_counter < 6:
                    time.sleep(10)
                    retry_counter = retry_counter + 1
                else:
                    module.fail_json(msg='Failed to unregister vIDM. runtime state is : %s registration flag is : %s'
                                         % (str(resp["runtime_state"]), str(resp["vidm_enable"])))
            else:
                break;
    except Exception as err:
        module.fail_json(msg='Error accessing vIDM status. Error [%s]' % (to_native(err)))
    return


def check_for_update(existing_vidm, vidm_params):
    if existing_vidm['client_id'] != vidm_params['client_id'] or \
            existing_vidm['host_name'] != vidm_params['host_name'] or \
            existing_vidm['client_id'] != vidm_params['client_id'] or \
            existing_vidm['lb_enable'] != vidm_params['lb_enable'] or \
            existing_vidm['node_host_name'] != vidm_params['node_host_name'] or \
            existing_vidm['thumbprint'] != vidm_params['thumbprint'] or \
            existing_vidm['vidm_enable'] != vidm_params['vidm_enable']:
        return True

    return False


def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(client_id=dict(required=True, type='str'),
                         client_secret=dict(required=False, type='str'),
                         host_name=dict(required=True, type='str'),
                         lb_enable=dict(required=False, type='bool'),
                         node_host_name=dict(required=True, type='str'),
                         thumbprint=dict(required=True, type='str'),
                         state=dict(required=True, choices=['present', 'absent']))

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    vidm_params = get_vidm_params(module.params.copy())
    state = module.params['state']
    mgr_hostname = module.params['hostname']
    mgr_username = module.params['username']
    mgr_password = module.params['password']
    validate_certs = module.params['validate_certs']
    client_id = module.params['client_id']

    manager_url = 'https://{}/api/v1'.format(mgr_hostname)
    vidm_api_url = manager_url + '/node/aaa/providers/vidm'
    existing_vidm = get_vidm_from_client_id(module, vidm_api_url, mgr_username, mgr_password, validate_certs,
                                            vidm_params['client_id'])
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'

    if state == 'present':
        vidm_params["vidm_enable"] = True
        if existing_vidm is not None:
            updated = check_for_update(existing_vidm, vidm_params)
            if not updated:
                module.exit_json(changed=False, id=vidm_params['client_id'],
                                 message="vIDM with id %s is already enabled." % vidm_params['client_id'])

        # vIDM not present or update. So call PUT API which is same for add and update vIDM
        request_data = json.dumps(vidm_params)
        if module.check_mode:
            module.exit_json(changed=True, debug_out=str(request_data), id='12345')
        try:
            (rc, resp) = request(vidm_api_url, data=request_data, headers=headers, method='PUT',
                                 url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs,
                                 ignore_errors=True)
        except Exception as err:
            module.fail_json(
                msg="Failed to register vIDM. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

        wait_till_create(module, vidm_api_url, mgr_username, mgr_password, validate_certs)

        module.exit_json(changed=True, id=resp["client_id"], body=str(resp),
                         message="vIDM with client id %s registered." % resp["client_id"])

    elif state == 'absent':
        if module.check_mode:
            module.exit_json(changed=True, debug_out=str(json.dumps(vidm_params)), id=vidm_params['client_id'])

        if existing_vidm is None:
            module.exit_json(changed=False, id=vidm_params['client_id'],
                             message="vIDM with client id %s was not registered." % vidm_params['client_id'])

        # vIDM with given client_id is registered so unregister it
        vidm_params['vidm_enable'] = False
        request_data = json.dumps(vidm_params)

        try:
            (rc, resp) = request(vidm_api_url, data=request_data, headers=headers, method='PUT',
                                 url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs,
                                 ignore_errors=True)
        except Exception as err:
            module.fail_json(
                msg="Failed to un-register vIDM. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

        wait_till_delete(module, vidm_api_url, mgr_username, mgr_password, validate_certs)
        module.exit_json(changed=True, id=vidm_params['client_id'], body=str(resp),
                         message="vIDM with id %s is unregistered." % vidm_params['client_id'])


if __name__ == '__main__':
    main()
