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
module: nsxt_transport_node_profiles
short_description: Create a Transport Node Profile
description: Transport node profile captures the configuration needed to create
a transport node. A transport node profile can be attached to
compute collections for automatic TN creation of member hosts.

version_added: "2.7"
author: Rahul Raghuvanshi
options:
    hostname:
        description: Deployed NSX manager hostname.
        required: true
        type: str
    username:
        description: The username to authenticate with the NSX manager.
        required: true
        type: str
    password:
        description: The password to authenticate with the NSX manager.
        required: true
        type: str
    description:
        description: Description of the pre/post-upgrade check
        required: false
        type: str
    display_name:
        description: Display name
        required: true
        type: str
    host_switch_spec:
        description: 'The HostSwitchSpec is the base class for standard and preconfigured
                      host switch specifications. Only standard host switches are supported
                      in the transport node profile.'
        host_switches:
            description: Transport Node host switches
            required: true
            type: array of HostSwitch
        required: false
        resource_type:
            description: Selects the type of the transport zone profile
            required: true
            type: str
        type: dict
    resource_type:
        description: Selects the type of the transport zone profile
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
    transport_zone_endpoints:
        description: Transport zone endpoints.
        required: False
        type: array of TransportZoneEndPoint
    
'''

EXAMPLES = '''
- name: Create transport node profile
  nsxt_transport_node_profiles:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    resource_type: "TransportNodeProfile"
    display_name: "NSX Configured TNP"
    description: "NSX configured Test Transport Node Profile"
    host_switch_spec:
      resource_type: "StandardHostSwitchSpec"
      host_switches:
      - host_switch_profiles:
        - name: "uplinkProfile1"
          type: "UplinkHostSwitchProfile"
        host_switch_name: "hostswitch1"
        host_switch_mode: "STANDARD"
        pnics:
        - device_name: "vmnic1"
          uplink_name: "uplink-1"
        ip_assignment_spec:
          resource_type: "StaticIpPoolSpec"
          ip_pool_name: "IPPool-IPV4-1"
        transport_zone_endpoints:
        - transport_zone_name: "TZ1"
        vmk_install_migration:
        - device_name: vmk0
          destination_network_name: "ls_vmk_Mgmt"
    state: "present"

'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native


FAILED_STATES = ["failed"]
IN_PROGRESS_STATES = ["pending", "in_progress"]
SUCCESS_STATES = ["partial_success", "success"]
FABRIC_VIRTUAL_SWITCH_TYPE = ["VDS"]

def get_transport_node_profile_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_transport_node_profiles(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/transport-node-profiles', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing transport node profiles. Error [%s]' % (to_native(err)))
    return resp

def get_host_switch_id_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, endpoint, display_name, exit_if_not_found=True):
    try:
      (rc, resp) = request(manager_url+ endpoint, headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing id for display name %s. Error [%s]' % (display_name, to_native(err)))

    for result in resp['results']:
        if result.__contains__('display_name') and result['display_name'] == display_name:
            return result['uuid']
    if exit_if_not_found:
        module.fail_json(msg='No id exist with display name %s' % display_name)

def get_id_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, endpoint, display_name, exit_if_not_found=True):
    try:
      (rc, resp) = request(manager_url+ endpoint, headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing id for display name %s. Error [%s]' % (display_name, to_native(err)))

    for result in resp['results']:
        if result.__contains__('display_name') and result['display_name'] == display_name:
            return result['id']
    if exit_if_not_found:
        module.fail_json(msg='No id exist with display name %s' % display_name)

def get_tnp_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    transport_node_profiles = get_transport_node_profiles(module, manager_url, mgr_username, mgr_password, validate_certs)
    for transport_node_profile in transport_node_profiles['results']:
        if transport_node_profile.__contains__('display_name') and transport_node_profile['display_name'] == display_name:
            return transport_node_profile
    return None


def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_profile_params ):
    for host_switch in transport_node_profile_params['host_switch_spec']['host_switches']:
        if host_switch.__contains__('host_switch_type') and host_switch['host_switch_type'] in FABRIC_VIRTUAL_SWITCH_TYPE:
            if host_switch.__contains__('host_switch_name'):
                host_switch['host_switch_id'] = get_host_switch_id_from_display_name(module, manager_url, mgr_username, 
                                                                     mgr_password, validate_certs,
                                                                     '/fabric/virtual-switches', host_switch['host_switch_name'])
            else:
                module.fail_json(msg='Failing as host_switch_name is not provided for host switch of type: %s' % host_switch['host_switch_type'])
        host_switch_profiles = host_switch.pop('host_switch_profiles', None)
        host_switch_profile_ids = []
        for host_switch_profile in host_switch_profiles:
            profile_obj = {}
            profile_obj['value'] = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                                                    "/host-switch-profiles?include_system_owned=true", host_switch_profile['name'])
            profile_obj['key'] = host_switch_profile['type']
            host_switch_profile_ids.append(profile_obj)
        host_switch['host_switch_profile_ids'] = host_switch_profile_ids
        ip_pool_id = None
        if host_switch.__contains__('ip_assignment_spec'):
            if host_switch['ip_assignment_spec'].__contains__('ip_pool_name'):
                ip_pool_name = host_switch['ip_assignment_spec'].pop('ip_pool_name', None)
                host_switch['ip_assignment_spec']['ip_pool_id'] = get_id_from_display_name (module, manager_url,
                                                                                        mgr_username, mgr_password, validate_certs,
                                                                                        "/pools/ip-pools", ip_pool_name)
        if host_switch.__contains__('transport_zone_endpoints'):
            for transport_zone_endpoint in host_switch['transport_zone_endpoints']:
                transport_zone_name = transport_zone_endpoint.pop('transport_zone_name', None)
                transport_zone_endpoint['transport_zone_id'] = get_id_from_display_name (module, manager_url,
                                                                                    mgr_username, mgr_password, validate_certs,
                                                                                    "/transport-zones", transport_zone_name)
        if host_switch.__contains__('vmk_install_migration'):
            for vmk_install_migration in host_switch['vmk_install_migration']:
                if vmk_install_migration.__contains__('destination_network_name'):
                    destination_network_name = vmk_install_migration.pop('destination_network_name', None)
                    vmk_install_migration['destination_network'] = get_id_from_display_name (module, manager_url,
                                                                                        mgr_username, mgr_password, validate_certs,
                                                                                        "/logical-switches", destination_network_name)
    if transport_node_profile_params.__contains__('transport_zone_endpoints'):
        for transport_zone_endpoint in transport_node_profile_params['transport_zone_endpoints']:
            transport_zone_name = transport_zone_endpoint.pop('transport_zone_name', None)
            transport_zone_endpoint['transport_zone_id'] = get_id_from_display_name (module, manager_url,
                                                                                    mgr_username, mgr_password, validate_certs,
                                                                                    "/transport-zones", transport_zone_name)
    transport_node_profile_params['display_name'] = transport_node_profile_params.pop('display_name', None)
    return transport_node_profile_params


def id_exist_in_list_dict_obj(key, list_obj1, list_obj2):
    all_id_presents = False
    if len(list_obj1) != len(list_obj2):
        return all_id_presents
    for dict_obj1 in list_obj1:
        if dict_obj1.__contains__(key):
            for dict_obj2 in list_obj2:
                if dict_obj2.__contains__(key) and dict_obj1[key] == dict_obj2[key]:
                    all_id_presents = True
                    continue
            if not all_id_presents:
                return False
    return True


def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_profile_with_ids):
    existing_transport_node_profile = get_tnp_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_profile_with_ids['display_name'])
    if existing_transport_node_profile is None:
        return False
    if existing_transport_node_profile.__contains__('transport_zone_endpoints') and transport_node_profile_with_ids.__contains__('transport_zone_endpoints'):
        return not id_exist_in_list_dict_obj('transport_zone_id', existing_transport_node_profile['transport_zone_endpoints'], transport_node_profile_with_ids['transport_zone_endpoints'])
    if existing_transport_node_profile.__contains__('host_switch_spec') and existing_transport_node_profile['host_switch_spec'].__contains__('host_switches') and \
        transport_node_profile_with_ids.__contains__('host_switch_spec') and transport_node_profile_with_ids['host_switch_spec'].__contains__('host_switches') and \
        existing_transport_node_profile['host_switch_spec']['host_switches'] != transport_node_profile_with_ids['host_switch_spec']['host_switches']:
        return True
    return False


def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                description=dict(required=False, type='str'),
                host_switch_spec=dict(required=False, type='dict',
                host_switches=dict(required=True, type='list'),
                resource_type=dict(required=True, type='str')),
                resource_type=dict(required=True, type='str'),
                transport_zone_endpoints=dict(required=False, type='list'),
                state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  transport_node_profile_params = get_transport_node_profile_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  transport_node_profile_dict = get_tnp_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  transport_node_profile_id, revision = None, None
  if transport_node_profile_dict:
    transport_node_profile_id = transport_node_profile_dict['id']
    revision = transport_node_profile_dict['_revision']

  if state == 'present':
    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_profile_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'

    if not updated:
      # add the node
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(logical_switch_params)), id='12345')
      request_data = json.dumps(body)
      try:
          if not transport_node_profile_id:
              transport_node_profile_id = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, '/transport-node-profiles', display_name, exit_if_not_found=False)
          if transport_node_profile_id:
              module.exit_json(changed=False, id=transport_node_profile_id, message="Transport node profile with display_name %s already exist."% module.params['display_name'])

          (rc, resp) = request(manager_url+ '/transport-node-profiles', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
           module.fail_json(msg="Failed to add transport node profile. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="transport node profile with display name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(body)), id=transport_node_profile_id)

      body['_revision'] = revision # update current revision
      request_data = json.dumps(body)
      id = transport_node_profile_id
      try:
          (rc, resp) = request(manager_url+ '/transport-node-profiles/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update transport node profile with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="transport node profile with node id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = transport_node_profile_id
    if id is None:
        module.exit_json(changed=False, msg='No transport node profile exist with display name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(transport_node_profile_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/transport-node-profiles/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete transport node profile with id %s. Error[%s]." % (id, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=id, message="transport node profile with node id %s deleted." % id)



if __name__ == '__main__':
    main()
