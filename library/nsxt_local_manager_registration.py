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
module: nsxt_local_manager_registration
short_description: 'Register a local manager with the global manager'
description: "Registers a local manager with the global manager"
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
    description:
        description: 'Description of this resource'
        required: false
        type: str
    fail_if_rtt_exceeded:
        description: 'Fail onboarding if maximum RTT exceeded.'
        required: false
        type: bool
    id:
        description: 'Unique identifier of this resource'
        required: true
        type: str
    maximum_rtt:
        description: "Maximum acceptable packet round trip time (RTT). 
                If provided and fail_if_rtt_exceeded is true, onboarding of the site will
                fail if measured RTT is greater than this value.
                Minimum: 0
                Maximum: 1000
                Default: 250"
        required: false
        type: int                  
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
- name: Register local manager with NSX
  nsxt_local_manager_registration:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    id: "LM-Mumbai"
    display_name: "Mumbai LM"
    site_connection_info:
      fqdn: "10.161.244.213"
      username: "admin"
      password: "Admin!23"
      thumbprint: "31a4eeaef05ad711c84d688cfb72001d17a4965a963611d9af63fb86ff55276cf"
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

def get_local_manager_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)

#   site_connection_info is an array
    args["site_connection_info"] = [args["site_connection_info"]]
    return args

def get_local_managers(module, url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(url, headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing local manager. Error [%s]' % (to_native(err)))
    return resp

def get_local_manager_by_id(module, url, mgr_username, mgr_password, validate_certs, id):
    local_managers = get_local_managers(module, url, mgr_username, mgr_password, validate_certs)
    for local_manager in local_managers['results']:
        if local_manager.__contains__('id') and local_manager['id'] == id:
            return local_manager
    return None

def check_for_update(module, url, mgr_username, mgr_password, validate_certs, local_manager_params):
    existing_local_manager = get_local_manager_by_id(module, url, mgr_username, mgr_password, validate_certs, local_manager_params['id'])
    if existing_local_manager is None:
        return False
    if existing_local_manager['site_connection_info'][0]['fqdn'] != local_manager_params['site_connection_info'][0]['fqdn'] or \
        existing_local_manager['site_connection_info'][0]['thumbprint'] != local_manager_params['site_connection_info'][0]['thumbprint'] :
        return True
    return False

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                        id=dict(required=True, type='str'),
                        site_connection_info=dict(required=False, type='dict', no_log=True,
                        username=dict(required=False, type='str'),
                        password=dict(required=False, type='str'),
                        thumbprint=dict(required=False, type='str'),
                        fqdn=dict(required=True, type='str')),
                        state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  local_manager_params = get_local_manager_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  id = module.params['id']
  manager_url = 'https://{}/global-manager/api/v1'.format(mgr_hostname)
  sites_api_url = manager_url + '/global-infra/sites/'
  local_manager_dict = get_local_manager_by_id (module, sites_api_url, mgr_username, mgr_password, validate_certs, id)
  local_manager_id, revision = None, None
  if local_manager_dict:
    local_manager_id = local_manager_dict['id']
    revision = local_manager_dict['_revision']

  if state == 'present':
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    updated = check_for_update(module, sites_api_url, mgr_username, mgr_password, validate_certs, local_manager_params)
    if not updated:
      # add the local_manager
      request_data = json.dumps(local_manager_params)
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(request_data), id='12345')
      try:
          if local_manager_id:
              module.exit_json(changed=False, id=local_manager_id, message="Local manager with id %s already exist."% module.params['id'])

          (rc, resp) = request(sites_api_url + '%s' % module.params['id'], data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
                module.fail_json(msg="Failed to add local_manager. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      module.exit_json(changed=True, id=None, body= str(resp), message="Local manager with id %s created." % module.params['id'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(local_manager_params)), id=local_manager_id)
      local_manager_params['_revision'] = revision # update current revision
      request_data = json.dumps(local_manager_params)
      id = local_manager_id
      try:
          (rc, resp) = request(sites_api_url + '%s' % id, data=request_data, headers=headers, method='PATCH',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update local_manager with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))
      module.exit_json(changed=True, id=None, body= str(resp), message="Local manager with id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = local_manager_id
    if id is None:
        module.exit_json(changed=False, msg='No local manager exist with id %s' % id)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(local_manager_params)), id=id)
    try:
        (rc, resp) = request(sites_api_url + "%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete local manager with id %s. Error[%s]." % (id, to_native(err)))

    module.exit_json(changed=True, id=id, message="Local manager with id %s deleted." % id)


if __name__ == '__main__':
    main()
