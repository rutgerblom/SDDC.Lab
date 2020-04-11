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
module: nsxt_ip_blocks
short_description: 'Create a new IP address block.'
description: "Creates a new IPv4 address block using the specified cidr. cidr is a
              required parameter. display_name & description are optional parameters"
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
    cidr:
        description: "Represents network address and the prefix length which will be                 associated\nwith a layer-2 broadcast domain"
        required: true
        type: str
    display_name:
        description: 'Display name'
        required: true
        type: str
    description:
        description: 'Description of the resource'
        required: false
        type: str
    tags:
        description: 'Opaque identifier meaningful to the API user'
        required: false
        type: list
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
- name: Create a new IP address block
  nsxt_ip_blocks:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    display_name: "IPBlock-Tenant-1"
    description: "IPBlock-Tenant-1 Description"
    cidr: "192.168.0.0/16"
    state: present
'''

RETURN = '''# '''


import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def get_ip_block_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_ip_blocks(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/pools/ip-blocks', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing ip blocks. Error [%s]' % (to_native(err)))
    return resp

def get_ip_block_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    ip_blocks = get_ip_blocks(module, manager_url, mgr_username, mgr_password, validate_certs)
    for ip_block in ip_blocks['results']:
        if ip_block.__contains__('display_name') and ip_block['display_name'] == display_name:
            return ip_block
    return None

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, ip_block_params):
    existing_ip_block = get_ip_block_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, ip_block_params['display_name'])
    if existing_ip_block is None:
        return False
    if existing_ip_block['cidr'] != ip_block_params['cidr']:
        return True
    return False

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                        cidr=dict(required=True, type='str'),
                        description=dict(required=False, type='str'),
                        tags=dict(required=False, type='list'),
                        state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  ip_block_params = get_ip_block_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  block_dict = get_ip_block_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  block_id, revision = None, None
  if block_dict:
      block_id = block_dict['id']
      revision = block_dict['_revision']

  if state == 'present':
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, ip_block_params)

    if not updated:
      # add the block
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(ip_block_params)), id='12345')
      request_data = json.dumps(ip_block_params)
      try:
          if block_id:
              module.exit_json(changed=False, id=block_id, message="IP block with display_name %s already exist."% module.params['display_name'])
          (rc, resp) = request(manager_url+ '/pools/ip-blocks', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to add ip block. Request body [%s]. Error[%s]." % (request_data, to_native(err)))
      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="IP block with display name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(ip_block_params)), id=block_id)

      ip_block_params['_revision'] = revision # update current revision
      request_data = json.dumps(ip_block_params)
      id = block_id
      try:
          (rc, resp) = request(manager_url+ '/pools/ip-blocks/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update ip block with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="ip block with block id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = block_id
    if id is None:
        module.exit_json(changed=False, msg='No ip block exist with display name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(ip_block_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/pools/ip-blocks/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete ip block with id %s. Error[%s]." % (id, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=id, message="ip block with block id %s deleted." % id)


if __name__ == '__main__':
    main()
