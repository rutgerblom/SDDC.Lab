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
module: nsxt_ip_pools
short_description: 'Create an IP Pool'
description: "Creates a new IPv4 or IPv6 address pool. Required parameters are
              allocation_ranges and cidr. Optional parameters are display_name,
              description, dns_nameservers, dns_suffix, and gateway_ip."
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
    display_name:
        description: 'Display name'
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
    subnets:
        description: "Subnets can be IPv4 or IPv6 and they should not overlap. The maximum
                      number will not exceed 5 subnets."
        required: false
        type: 'array of IpPoolSubnet'
    tags:
        description: 'Opaque identifiers meaningful to the API user'
        required: false
        type: str
    description:
        description: 'description of the resource'
        required: false
        type: str
    ip_release_delay:
        description: 'IP address release delay'
        required: false
        type: int

    
'''

EXAMPLES = '''
- name: Create ip pool
  nsxt_ip_pools:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    display_name: IPPool-IPV4-1
    subnets:
    - allocation_ranges:
      - start: "10.112.201.28"
        end: "10.112.201.29"
      cidr: "10.112.201.0/24"
    state: "present"
'''

RETURN = '''# '''


import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def get_ip_pool_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_ip_pools(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/pools/ip-pools', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing ip pools. Error [%s]' % (to_native(err)))
    return resp

def get_ip_pool_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    ip_pools = get_ip_pools(module, manager_url, mgr_username, mgr_password, validate_certs)
    for ip_pool in ip_pools['results']:
        if ip_pool.__contains__('display_name') and ip_pool['display_name'] == display_name:
            return ip_pool
    return None

# def ordered(obj):
#     if isinstance(obj, dict):
#         return sorted((k, ordered(v)) for k, v in obj.items())
#     if isinstance(obj, list):
#         return sorted(ordered(x) for x in obj)
#     else:
#         return obj

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, ip_pool_params):
    existing_ip_pool = get_ip_pool_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, ip_pool_params['display_name'])
    if existing_ip_pool is None:
        return False
    if  existing_ip_pool.__contains__('subnets') and ip_pool_params.__contains__('subnets') and existing_ip_pool['subnets'] != ip_pool_params['subnets']:
        return True
    return False

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                        subnets=dict(required=False, type='list'),
                        tags=dict(required=False, type='list'),
                        description=dict(required=False, type='str'),
                        ip_release_delay=dict(required=False, type='int'),
                        state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  ip_pool_params = get_ip_pool_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  pool_dict = get_ip_pool_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  pool_id, revision = None, None
  if pool_dict:
    pool_id = pool_dict['id']
    revision = pool_dict['_revision']

  if state == 'present':
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, ip_pool_params)

    if not updated:
      # add the pool
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(ip_pool_params)), id='12345')
      request_data = json.dumps(ip_pool_params)
      try:
          if pool_id:
              module.exit_json(changed=False, id=pool_id, message="IP pool with display_name %s already exist."% module.params['display_name'])
          (rc, resp) = request(manager_url+ '/pools/ip-pools', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to add ip pool. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="IP pool with display name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(ip_pool_params)), id=pool_id)
      ip_pool_params['_revision']=revision # update current revision
      request_data = json.dumps(ip_pool_params)
      id = pool_id
      try:
          (rc, resp) = request(manager_url+ '/pools/ip-pools/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update ip pool with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))
      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="ip pool with pool id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = pool_id
    if id is None:
        module.exit_json(changed=False, msg='No ip pool exist with display name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(ip_pool_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/pools/ip-pools/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete ip pool with id %s. Error[%s]." % (id, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=id, message="ip pool with pool id %s deleted." % id)


if __name__ == '__main__':
    main()
