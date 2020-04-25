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
module: nsxt_logical_switches
short_description: Create a Logical Switch
description: Creates a new logical switch. The request must include the
             transport_zone_id, display_name, and admin_state (UP or DOWN). The
             replication_mode (MTEP or SOURCE) is required for overlay logical
             switches, but not for VLAN-based logical switches. A vlan needs to be
             provided for VLAN-based logical switches

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
    address_bindings:
        description: Address bindings for the Logical switch
        required: false
        type: array of PacketAddressClassifier
    admin_state:
        description: Represents Desired state of the Logical Switch
        required: true
        type: str
    display_name:
        description: Display name
        required: true
        type: str
    extra_configs:
        description: 'This property could be used for vendor specific configuration in key 
                      value string pairs, the setting in extra_configs will be automatically
                      inheritted by logical ports in the logical switch.'
        required: false
        type: array of ExtraConfig
    hybrid:
        description: 'If this flag is set to true, then all the logical switch ports attached
                      to this logical switch will behave in a hybrid fashion. The hybrid 
                      logical switch port indicates to NSX that the VM intends to operate in 
                      underlay mode, but retains the ability to forward egress traffic to the
                      NSX overlay network.
                  
                      This flag can be enabled only for the logical switches in the overlay 
                      type transport zone which has host switch mode as STANDARD and also has 
                      either CrossCloud or CloudScope tag scopes.
                  
                      Only the NSX public cloud gateway (PCG) uses this flag, other host agents 
                      like ESX, KVM and Edge will ignore it. This property cannot be modified 
                      once the logical switch is created.'
        required: false
        type: boolean
    ip_pool_name:
        description: IP pool name
        required: false
        type: str
    lswitch_id:
        description: LSwitch ID
        required: false
        type: str
    mac_pool_id:
        description: Mac pool id that associated with a LogicalSwitch.
        required: false
        type: str
    mac_pool_name:
        description: Mac pool name that associated with a LogicalSwitch.
        required: false
        type: str
    replication_mode:
        description: Replication mode of the Logical Switch
        required: false
        type: str
    description:
        description: Description of the resource
        required: False
        type: str
    span:
        description: List of Local Manager IDs the logical switch extends
        required: False
        type: list
    tags:
        description: Opaque identifiers meaningful to the API user
        required: False
        type: list
    state:
        choices:
        - present
        - absent
        description: "State can be either 'present' or 'absent'. 
                    'present' is used to create or update resource. 
                    'absent' is used to delete resource."
        required: true
    switch_type:
        description: 'This readonly field indicates purpose of a LogicalSwitch. It is set
                      by manager internally and any user provided values will not be honored.
                      DEFAULT type LogicalSwitches are created for basic L2 connectivity by API
                      users.
                      SERVICE_PLANE type LogicalSwitches are system created service plane 
                      LogicalSwitches
                      Service Insertion service.'
        required: false
        type: str
    switching_profiles:
        description: List of Switching Profile Names and type
        required: false
        type: list
    transport_zone_name:
        description: Transport Zone Name
        required: true
        type: str
    uplink_teaming_policy_name:
        description: This name has to be one of the switching uplink teaming policy names
                     listed inside the logical switch's TransportZone. If this field is not 
                     specified, the logical switch will not have a teaming policy associated 
                     with it and the host switch's default teaming policy will be used.
        required: false
        type: str
    vlan:
        description: 'This property is dedicated to VLAN based network, to set VLAN of logical
                      network. It is mutually exclusive with ''vlan_trunk_spec''.'
        required: false
        type: int
    vlan_trunk_spec:
        description: 'This property is used for VLAN trunk specification of logical switch.
                      It''s mutually exclusive with ''vlan''. Also it could be set to do guest 
                      VLAN tagging in overlay network.'
        required: false
        type: dict
        vlan_ranges:
            description: Trunk VLAN id ranges
            required: true
            type: array of TrunkVlanRange
    vni:
        description: 'Only for OVERLAY network. A VNI will be auto-allocated from the
                      default VNI pool if not given; otherwise the given VNI has to be
                      inside the default pool and not used by any other LogicalSwitch.'
        required: false
        type: int
    
'''

EXAMPLES = '''
- name: Create logical switch
  nsxt_logical_switches:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    display_name: "test_lswitch"
    replication_mode: "SOURCE"
    admin_state: "UP"
    transport_zone_name: "TZ1"
    state: "present"
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def get_logical_switch_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs', 'lswitch_id']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_logical_switches(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/logical-switches', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing logical switches. Error [%s]' % (to_native(err)))
    return resp

def get_lswitch_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    logical_switchs = get_logical_switches(module, manager_url, mgr_username, mgr_password, validate_certs)
    for logical_switch in logical_switchs['results']:
        if logical_switch.__contains__('display_name') and logical_switch['display_name'] == display_name:
            return logical_switch
    return None

def get_id_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, endpoint, display_name):
    try:
      (rc, resp) = request(manager_url+ endpoint, headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing id for display name %s. Error [%s]' % (display_name, to_native(err)))

    for result in resp['results']:
        if result.__contains__('display_name') and result['display_name'] == display_name:
            return result['id']
    module.fail_json(msg='No id existe with display name %s' % display_name)

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, logical_switch_params ):
    if 'ip_pool_name' in logical_switch_params:
        logical_switch_params['ip_pool_id'] = get_id_from_display_name (module, manager_url,
                                                                mgr_username, mgr_password, validate_certs,
                                                                "/pools/ip-pools", logical_switch_params.pop('ip_pool_name', None))
    if 'mac_pool_name' in logical_switch_params and 'mac_pool_id' not in logical_switch_params:
        logical_switch_params['mac_pool_id'] = get_id_from_display_name (module, manager_url,
                                                                mgr_username, mgr_password, validate_certs,
                                                                "/pools/mac-pools", logical_switch_params.pop('mac_pool_name', None))
    if 'mac_pool_name' in logical_switch_params and 'mac_pool_id' in logical_switch_params:
        logical_switch_params.pop('mac_pool_name', None)
    logical_switch_params['transport_zone_id'] = get_id_from_display_name (module, manager_url,
                                                                mgr_username, mgr_password, validate_certs,
                                                                "/transport-zones", logical_switch_params.pop('transport_zone_name', None))
    switch_profiles = logical_switch_params.pop('switching_profiles', None)

    switch_profile_ids = []
    for switch_profile in switch_profiles or []:
        profile_obj = {}
        profile_obj['value'] = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                                                "/switching-profiles", switch_profile['name'])
        profile_obj['key'] = switch_profile['type']
        switch_profile_ids.append(profile_obj)
    logical_switch_params['switching_profile_ids'] = switch_profile_ids
    return logical_switch_params

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, logical_switch_with_ids):
    existing_logical_switch = get_lswitch_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, logical_switch_with_ids['display_name'])
    if existing_logical_switch is None:
        return False
    if existing_logical_switch.__contains__('vlan') and logical_switch_with_ids.__contains__('vlan') and \
        existing_logical_switch['vlan'] != logical_switch_with_ids['vlan']:
        return True

    if logical_switch_with_ids.__contains__('vlan_trunk_spec') and existing_logical_switch.__contains__('vlan_trunk_spec') and \
        existing_logical_switch['vlan_trunk_spec']['vlan_ranges'] != logical_switch_with_ids['vlan_trunk_spec']['vlan_ranges']:
        return True
    if existing_logical_switch.__contains__('switching_profile_ids') and logical_switch_with_ids.__contains__('switching_profile_ids') and \
        existing_logical_switch['switching_profile_ids'] != logical_switch_with_ids['switching_profile_ids']:
        return True
    if existing_logical_switch['admin_state'] != logical_switch_with_ids['admin_state']:
        return True
    if existing_logical_switch.__contains__('replication_mode') and logical_switch_with_ids.__contains__('replication_mode') and \
        existing_logical_switch['replication_mode'] != logical_switch_with_ids['replication_mode']:
        return True
    if existing_logical_switch.__contains__('hybrid') and logical_switch_with_ids.__contains__('hybrid') and \
        existing_logical_switch['hybrid'] != logical_switch_with_ids['hybrid']:
        return True
    return False

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                        switch_type=dict(required=False, type='str'),
                        replication_mode=dict(required=False, type='str'),
                        extra_configs=dict(required=False, type='list'),
                        uplink_teaming_policy_name=dict(required=False, type='str'),
                        transport_zone_name=dict(required=True, type='str'),
                        ip_pool_name=dict(required=False, type='str'),
                        vlan=dict(required=False, type='int'),
                        hybrid=dict(required=False, type='bool'),
                        mac_pool_id=dict(required=False, type='str'),
                        mac_pool_name=dict(required=False, type='str'),
                        vni=dict(required=False, type='int'),
                        vlan_trunk_spec=dict(required=False, type='dict',
                        vlan_ranges=dict(required=True, type='list')),
                        admin_state=dict(required=True, type='str'),
                        address_bindings=dict(required=False, type='list'),
                        switching_profiles=dict(required=False, type='list'),
                        lswitch_id=dict(required=False, type='str'),
                        description=dict(required=False, type='str'),
                        span=dict(required=False, type='list'),
                        tags=dict(required=False, type='list'),
                        state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  logical_switch_params = get_logical_switch_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  changed = True
  lswitch_dict = get_lswitch_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  lswitch_id, revision = None, None
  if lswitch_dict:
    lswitch_id = lswitch_dict['id']
    revision = lswitch_dict['_revision']

  if state == 'present':
    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, logical_switch_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'

    if lswitch_id is None:
      # add the logical_switch
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(body)), id=lswitch_id)
      request_data = json.dumps(body)
      try:
          if lswitch_id:
              module.exit_json(changed=False, id=lswitch_id, message="Logical switch with display_name %s already exist."% module.params['display_name'])

          (rc, resp) = request(manager_url+ '/logical-switches', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to add logical switch. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Logical switch with display name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(body)), id=lswitch_id)

      body['_revision'] = revision # update current revision
      request_data = json.dumps(body)
      id = lswitch_id
      try:
          (rc, resp) = request(manager_url+ '/logical-switches/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update logical switch with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="logical switch with lswitch id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = lswitch_id
    if id is None:
        module.exit_json(changed=False, msg='No logical switch exist with display name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(logical_switch_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/logical-switches/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete logical switch with id %s. Error[%s]." % (id, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=id, message="Logical switch with zone id %s deleted." % id)


if __name__ == '__main__':
    main()
