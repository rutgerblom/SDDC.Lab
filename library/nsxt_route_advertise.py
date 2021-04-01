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


ANSIBLE_METADATA = {'metadata_version': 'xx',
                    'status': ['preview'],
                    'supported_by': 'community'}
DOCUMENTATION = '''
---
module: nsxt_route_advertise
short_description: 'Toggle tier 1 route advertisement'
description: "Toggle route advertisement on Tier 1 routers"

version_added: '2.7'
author: 'Matt Proud'
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
        description: 'Display name of Tier 1 router'
        required: true
        type: str
    enabled:
        description: 'Flag to enable this configuration'
        type: boolean
        required: false
    advertise_static_routes:
        description: 'Flag to advertise all static routes'
        required: false
        type: boolean
    advertise_dns_forwarder:
        description: 'Flag to advertise all routes of dns forwarder listener ips and source ips'
        required: false
        type: boolean
    advertise_lb_snat_ip:
        description: 'Flag to advertise all lb SNAT ips'
        required: false
        type: boolean
    advertise_lb_vip:
        description: 'Flag to advertise lb vips'
        required: false
        type: boolean
    advertise_nat_routes:
        description: 'Flag to advertise all routes of nat'
        required: false
        type: boolean
    advertise_nsx_connected_routes:
        description: 'Flag to advertise all connected routes'
        required: false
        type: boolean
    
'''

EXAMPLES = '''
- name: Toggle tier 1 route advertisement
  nsxt_route_advertise:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    enabled: True
    advertise_static_routes: True
    advertise_dns_forwarder: True
    advertise_lb_snat_ip: True
    advertise_lb_vip: True
    advertise_nat_routes: True
    advertise_nsx_connected_routes: True
'''

RETURN = '''# '''


import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def get_advertise_params(args=None):
    args_to_remove = ['username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_logical_routers(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/logical-routers', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing logical routers. Error [%s]' % (to_native(err)))
    return resp

def get_lr_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    logical_routers = get_logical_routers(module, manager_url, mgr_username, mgr_password, validate_certs)
    for logical_router in logical_routers['results']:
        if logical_router.__contains__('display_name') and logical_router['display_name'] == display_name:
            return logical_router
    return None

def get_revision(module, manager_url, mgr_username, mgr_password, validate_certs, logical_router_id):
  try:
    (rc, resp) = request(manager_url+ '/logical-routers/%s/routing/advertisement' % logical_router_id, headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    return resp['_revision']
  except Exception as err:
    module.fail_json(msg='Error accessing current advertisement. Error [%s]' % (to_native(err)))
    

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                        enabled=dict(required=False, type='bool'),
                        advertise_static_routes=dict(required=False, type='bool'),
                        advertise_dns_forwarder=dict(required=False, type='bool'),
                        advertise_lb_snat_ip=dict(required=False, type='bool'),
                        advertise_lb_vip=dict(required=False, type='bool'),
                        advertise_nat_routes=dict(required=False, type='bool'),
                        advertise_nsx_connected_routes=dict(required=False, type='bool')
                        )

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  advertise_params = get_advertise_params(module.params.copy())
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  logical_router_dict = get_lr_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  logical_router_id = None
  if logical_router_dict:
    logical_router_id = logical_router_dict['id']
  
  advertise_params['_revision'] = get_revision(module, manager_url, mgr_username, mgr_password, 
                                              validate_certs, logical_router_id) # update current revision

  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'
   
  # add the pool
  if module.check_mode:
    module.exit_json(changed=True, debug_out=str(json.dumps(advertise_params)), id='12345')
  request_data = json.dumps(advertise_params)
  try:
    (rc, resp) = request(manager_url+ '/logical-routers/%s/routing/advertisement' % logical_router_id, data=request_data, headers=headers, method='PUT',
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
  except Exception as err:
      module.fail_json(msg="Failed to toggle config. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

  time.sleep(5)
  module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Router advertisement set for display name %s." % module.params['display_name'])


if __name__ == '__main__':
    main()
