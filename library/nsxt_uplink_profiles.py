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
module: nsxt_uplink_profiles
short_description: Create a Hostswitch Profile
description: Creates a hostswitch profile. The resource_type is required. For uplink
              profiles, the teaming and policy parameters are required. By default, the
              mtu is 1600 and the transport_vlan is 0. The supported MTU range is 1280
              through 9000.

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
    display_name:
        description: Display name
        required: true
        type: str
    description:
        description: Description of the resource
        required: false
        type: str
    enabled:
        description: 'The enabled property specifies the status of NIOC feature.
                      When enabled is set to true, NIOC feature is turned on and
                      the bandwidth allocations specified for the traffic resources
                      are enforced. When enabled is set to false, NIOC feature
                      is turned off and no bandwidth allocation is guaranteed.
                      By default, enabled will be set to true.'
        required: false
        type: boolean
    extra_configs:
        description: list of extra configs
        required: false
        type: array of ExtraConfig
    host_infra_traffic_res:
        description: 'host_infra_traffic_res specifies bandwidth allocation for
                      various traffic resources.'
        required: false
        type: array of ResourceAllocation
    lags:
        description: list of LACP group
        required: false
        type: array of Lag
    mtu:
        description: Maximum Transmission Unit used for uplinks
        required: false
        type: int
    named_teamings:
        description: List of named uplink teaming policies that can be used by logical switches
        required: false
        type: array of NamedTeamingPolicy
    overlay_encap:
        description: The protocol used to encapsulate overlay traffic
        required: false
        type: str
    required_capabilities:
        description: None
        required: false
        type: list
    resource_type:
        choices:
        - UplinkHostSwitchProfile
        description: Supported HostSwitch profiles.
        required: true
        type: str
    send_enabled:
        description: Enabled or disabled sending LLDP packets
        required: false
        type: boolean
    tags:
        description: Opaque identifier meaninful to API user
        required: false
        type: Array of Tag
    state:
        choices:
        - present
        - absent
        description: "State can be either 'present' or 'absent'. 
                    'present' is used to create or update resource. 
                    'absent' is used to delete resource."
        required: true
    teaming:
        active_list:
            description: List of Uplinks used in active list
            required: true
            type: array of Uplink
        description: Default TeamingPolicy associated with this UplinkProfile
        policy:
            description: Teaming policy
            required: true
            type: str
        required: true
        standby_list:
            description: List of Uplinks used in standby list
            required: false
            type: array of Uplink
        type: dict
    transport_vlan:
        description: VLAN used for tagging Overlay traffic of associated HostSwitch
        required: false
        type: int
    
'''

EXAMPLES = '''
- name: Create a Hostswitch Profile
  nsxt_uplink_profiles:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      display_name: "uplinkProfile1",
      mtu: 1600,
      resource_type: "UplinkHostSwitchProfile",
      teaming:
        active_list:
        - uplink_name: "uplink-1"
          uplink_type: PNIC
        policy: FAILOVER_ORDER
      transport_vlan: 0,
      state: "present",
'''

RETURN = '''# '''


import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def get_profile_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_host_switch_profiles(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/host-switch-profiles', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing host profiles. Error [%s]' % (to_native(err)))
    return resp

def get_uplink_profile_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    host_switch_profiles = get_host_switch_profiles(module, manager_url, mgr_username, mgr_password, validate_certs)
    for host_switch_profile in host_switch_profiles['results']:
        if host_switch_profile.__contains__('display_name') and host_switch_profile['display_name'] == display_name:
            return host_switch_profile
    return None

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
def cmp_dict(dict1, dict2): # dict1 contain dict2
    #print dict2
    for k2, v2 in dict2.items():
        found = False
        if k2 not in dict1:
            continue
        if type(v2) != list and dict1[k2] != dict2[k2]:
            return False
            
        for obj2 in v2:
            for obj1 in dict1[k2]:
                if all(item in obj1.items() for item in obj2.items()):
                           found = True
        if not found:
            return False
    return True

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, profile_params):
    existing_profile = get_uplink_profile_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, profile_params['display_name'])
    if existing_profile is None:
        return False
    if existing_profile.__contains__('mtu') and profile_params.__contains__('mtu') and \
        existing_profile['mtu'] != profile_params['mtu']:
        return True
    if existing_profile.__contains__('transport_vlan') and profile_params.__contains__('transport_vlan') and \
        existing_profile['transport_vlan'] != profile_params['transport_vlan']:
        return True
    if profile_params.__contains__('lags') and profile_params['lags']:
       existing_lags = existing_profile['lags']
       new_lags = profile_params['lags']
       sorted_existing_lags = sorted(existing_lags, key = lambda i: i['name'])
       sorted_new_lags = sorted(new_lags, key = lambda i: i['name'])
       if len(sorted_existing_lags) != len(sorted_new_lags):
          return True
       both_lags_same = True
       for i in range(len(sorted_existing_lags)):
           diff_obj = {k: sorted_existing_lags[i][k] for k in sorted_existing_lags[i] if k in sorted_new_lags[i] and sorted_existing_lags[i][k] != sorted_new_lags[i][k]}
           del diff_obj['uplinks']
           if not cmp_dict(diff_obj, sorted_new_lags[i]):
              both_lags_same = False
       if not both_lags_same:
          return True
    if profile_params.__contains__('named_teamings'):
       existing_teamings = existing_profile['named_teamings']
       new_teamings = profile_params['named_teamings']
       sorted_existing_teamings = sorted(existing_teamings, key = lambda i: i['name'])
       sorted_new_teamings = sorted(new_teamings, key = lambda i: i['name'])
       if len(sorted_existing_teamings) != len(sorted_new_teamings):
          return False
       both_teamings_same = True
       for i in range(len(sorted_existing_teamings)):
           diff_obj = {k: sorted_existing_teamings[i][k] for k in sorted_existing_teamings[i] if k in sorted_new_teamings[i] and sorted_existing_teamings[i][k] != sorted_new_teamings[i][k]}
           if not cmp_dict(diff_obj, sorted_new_teamings[i]):
              both_teamings_same = False
       if not both_teamings_same:
          return True
    return False
  

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                        transport_vlan=dict(required=False, type='int'),
                        description=dict(required=False, type='str'),
                        enabled=dict(required=False, type='boolean'),
                        host_infra_traffic_res=dict(required=False, type='list'),
                        overlay_encap=dict(required=False, type='str'),
                        named_teamings=dict(required=False, type='list'),
                        mtu=dict(required=False, type='int'),
                        required_capabilities=dict(required=False, type='list'),
                        send_enabled=dict(required=False, type='boolean'),
                        extra_configs=dict(required=False, type='list'),
                        teaming=dict(required=True, type='dict',
                        policy=dict(required=True, type='str'),
                        standby_list=dict(required=False, type='list'),
                        active_list=dict(required=True, type='list')),
                        lags=dict(required=False, type='list'),
                        tags=dict(required=False, type='list'),
                        resource_type=dict(required=True, type='str', choices=['UplinkHostSwitchProfile']),
                        state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  profile_params = get_profile_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  host_switch_profile_dict = get_uplink_profile_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  host_switch_profile_id, revision = None, None
  if host_switch_profile_dict:
    host_switch_profile_id = host_switch_profile_dict['id']
    revision = host_switch_profile_dict['_revision']

  if state == 'present':
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, profile_params)

    if not updated:
      # add the block
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(profile_params)), id='12345')
      request_data = json.dumps(profile_params)
      try:
          if host_switch_profile_id:
              module.exit_json(changed=False, id=host_switch_profile_id, message="Uplink profile with display_name %s already exist."% module.params['display_name'])

          (rc, resp) = request(manager_url+ '/host-switch-profiles', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to add host profile. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="host profile with display name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(profile_params)), id=host_switch_profile_id)

      profile_params['_revision'] = revision # update current revision
      request_data = json.dumps(profile_params)
      id = host_switch_profile_id
      try:
          (rc, resp) = request(manager_url+ '/host-switch-profiles/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update host profile with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="host profile with id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = host_switch_profile_id
    if id is None:
        module.exit_json(changed=False, msg='No host switch profile exist with display name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(profile_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/host-switch-profiles/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete host profile with id %s. Error[%s]." % (id, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=id, message="host profile with id %s deleted." % id)


if __name__ == '__main__':
    main()
