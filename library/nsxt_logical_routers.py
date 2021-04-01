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
module: nsxt_logical_routers
short_description: Create a Logical Router
description: Creates a logical router. The required parameters are router_type (TIER0 or
             TIER1) and edge_cluster_id (TIER0 only). Optional parameters include
             internal and external transit network addresses.

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
    advanced_config:
        description: Contains config properties for tier0 routers
        external_transit_networks:
            description: CIDR block defining tier0 to tier1 links
            required: false
            type: list
        ha_vip_configs:
            description: This configuration can be defined only for Active-Standby LogicalRouter
                          to provide redundancy. For mulitple uplink ports, multiple HaVipConfigs 
                          must be defined and each config will pair exactly two uplink ports. 
                          The VIP will move and will always be owned by the Active node. 
                          Note - when HaVipConfig[s] are defined, configuring dynamic-routing is 
                          disallowed.
            required: false
            type: array of HaVipConfig
        internal_routing_network:
            description: Internal Routing Name
            required: false
            type: str
        internal_transit_networks:
            description: CIDR block defining service router to distributed router links
            required: false
            type: list
        required: false
        transport_zone_name:
            description: Name of transport zone
            required: false
            type: str
        type: dict
    allocation_profile:
        allocation_pool:
            allocation_pool_type:
                description: Types of logical router allocation pool based on services
                required: true
                type: str
            allocation_size:
                description: "To address varied customer performance and scalability 
                              requirements, different sizes for load balancer service are 
                              supported: SMALL, MEDIUM and LARGE, each with its own set of 
                              resource and performance. Specify size of load balancer service
                              which you will bind to TIER1 router."
                required: true
                type: str
            description: "Logical router allocation can be tracked for specific services and
                          services may have their own hard limits and allocation sizes. For
                          example load balancer pool should be specified if load balancer
                          service will be attached to logical router."
            required: false
            type: dict
        description: 'Configurations options to auto allocate edge cluster members for
                      logical router. Auto allocation is supported only for TIER1 and pick
                      least utilized member post current assignment for next allocation.'
        enable_standby_relocation:
            description: 'Flag to enable the auto-relocation of standby service router running
                          on edge cluster and node associated with the logical router. Only
                          manually placed service contexts for tier1 logical routers are
                          considered for the relocation.'
            required: false
            type: boolean
        required: false
        type: dict
    description:
        description: Description of the resource
        required: false
        type: str
    display_name:
        description: Display name
        required: true
        type: str
    edge_cluster_member_indices:
        description: 'For stateful services, the logical router should be associated with
                      edge cluster. For TIER 1 logical router, for manual placement of
                      service router within the cluster, edge cluster member indices needs
                      to be provided else same will be auto-allocated. You can provide
                      maximum two indices for HA ACTIVE_STANDBY. For TIER0 logical router
                      this property is no use and placement is derived from logical router
                      uplink or loopback port.'
        required: false
        type: list
    edge_cluster_name:
        description: Name of edge cluster
        required: false
        type: str
    failover_mode:
        description: 'Determines the behavior when a logical router instance restarts after
                      a failure. If set to PREEMPTIVE, the preferred node will take over,
                      even if it causes another failure. If set to NON_PREEMPTIVE, then the
                      instance that restarted will remain secondary.
                      This property must not be populated unless the high_availability_mode 
                      property is set to ACTIVE_STANDBY.
                      If high_availability_mode property is set to ACTIVE_STANDBY and this 
                      property is not specified then default will be NON_PREEMPTIVE.'
        required: false
        type: str
    high_availability_mode:
        description: High availability mode
        required: false
        type: str
    preferred_edge_cluster_member_index:
        description: Used for tier0 routers only
        required: false
        type: int
    resource_type:
        choices:
        - LogicalRouter
        description: "A Policy Based VPN requires to define protect rules that match local
                     and peer subnets. IPSec security associations is negotiated for each pair
                     of local and peer subnet.
                     A Route Based VPN is more flexible, more powerful
                     and recommended over policy based VPN. IP Tunnel port is created and all
                     traffic routed via tunnel port is protected. Routes can be configured 
                     statically or can be learned through BGP. A route based VPN is must for 
                     establishing redundant VPN session to remote site."
        required: false
        type: str
    router_type:
        description: Type of Logical Router
        required: true
        type: str
    ipv6_profiles:
        description: IPv6 Profiles
        required: false
        type: dict
        dad_profile_id:
            description: DAD profile id
            required: False
            type: str
        ndra_profile_id:
            description: NDRA profile id
            required: False
            type: str
    tags:
        description: Opaque identifiers meaningful to the API user
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
- name: Create a Logical Router
  nsxt_logical_routers:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      resource_type: LogicalRouter
      description: "Router West"
      display_name: "tier-0"
      edge_cluster_name: edge-cluster-1
      router_type: TIER0
      high_availability_mode: ACTIVE_ACTIVE
      state: present
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def get_logical_router_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
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

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, logical_router_params ):

    if logical_router_params.__contains__('edge_cluster_name'):
        edge_cluster_name = logical_router_params.pop('edge_cluster_name', None)
        logical_router_params['edge_cluster_id'] = get_id_from_display_name (module, manager_url,
                                                                                mgr_username, mgr_password, validate_certs,
                                                                                "/edge-clusters", edge_cluster_name)
    if logical_router_params.__contains__('ipv6_profiles'):
        if logical_router_params['ipv6_profiles'].__contains__('dad_profile_name'):
            dad_profile_name = logical_router_params['ipv6_profiles'].pop('dad_profile_name')
            logical_router_params['ipv6_profiles']['dad_profile_id'] = get_id_from_display_name (module, manager_url,
                                                                                                   mgr_username, mgr_password, 
                                                                                                   validate_certs,
                                                                                                   "/ipv6/dad-profiles", dad_profile_name)
        if logical_router_params['ipv6_profiles'].__contains__('ndra_profile_name'):
            ndra_profile_name = logical_router_params['ipv6_profiles'].pop('ndra_profile_name')
            logical_router_params['ipv6_profiles']['ndra_profile_id'] = get_id_from_display_name (module, manager_url,
                                                                                                   mgr_username, mgr_password, 
                                                                                                   validate_certs,
                                                                                                   "/ipv6/nd-ra-profiles",
                                                                                                  ndra_profile_name)
    if logical_router_params.__contains__('advanced_config') and logical_router_params['advanced_config'].__contains__('transport_zone_name'):
        transport_zone_name= logical_router_params['advanced_config'].pop('transport_zone_name', None)
        logical_router_params['advanced_config']['transport_zone_id'] = get_id_from_display_name (module, manager_url,
                                                                                mgr_username, mgr_password, validate_certs,
                                                                                "/transport-zones", transport_zone_name)
    return logical_router_params

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, logical_router_with_ids):
    existing_logical_router = get_lr_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, logical_router_with_ids['display_name'])
    if existing_logical_router is None:
        return False
    if existing_logical_router.__contains__('edge_cluster_id') and logical_router_with_ids.__contains__('edge_cluster_id') and \
        existing_logical_router['edge_cluster_id'] != logical_router_with_ids['edge_cluster_id']:
        return True
    if existing_logical_router.__contains__('advanced_config') and logical_router_with_ids.__contains__('advanced_config'):
        if existing_logical_router['advanced_config'].__contains__('internal_transit_networks') and logical_router_with_ids['advanced_config'].__contains__('internal_transit_networks') and \
            existing_logical_router['advanced_config']['internal_transit_networks'] != logical_router_with_ids['advanced_config']['internal_transit_networks']:
            return True
        if existing_logical_router['advanced_config'].__contains__('external_transit_networks') and logical_router_with_ids['advanced_config'].__contains__('external_transit_networks') and \
            existing_logical_router['advanced_config']['external_transit_networks'] != logical_router_with_ids['advanced_config']['external_transit_networks']:
            return True
        if existing_logical_router['advanced_config'].__contains__('ha_vip_configs') is False and \
            logical_router_with_ids['advanced_config'].__contains__('ha_vip_configs') is True:
            return True
    return False


def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                        description=dict(required=False, type='str'),
                        edge_cluster_member_indices=dict(required=False, type='list'),
                        allocation_profile=dict(required=False, type='dict',
                        allocation_pool=dict(required=False, type='dict',
                        allocation_size=dict(required=True, type='str'),
                        allocation_pool_type=dict(required=True, type='str')),
                        enable_standby_relocation=dict(required=False, type='boolean')),
                        failover_mode=dict(required=False, type='str'),
                        advanced_config=dict(required=False, type='dict',
                            transport_zone_name=dict(required=False, type='str'),
                            internal_transit_networks=dict(required=False, type='list'),
                            internal_routing_network=dict(required=False, type='str'),
                            ha_vip_configs=dict(required=False, type='list'),
                            external_transit_networks=dict(required=False, type='list')),
                        router_type=dict(required=True, type='str'),
                        preferred_edge_cluster_member_index=dict(required=False, type='int'),
                        high_availability_mode=dict(required=False, type='str'),
                        edge_cluster_name=dict(required=False, type='str'),
                        tags=dict(required=False, type='list'),
                        ipv6_profiles=dict(required=False, type='dict',
                        dad_profile_name=dict(required=False, type='str'),
                        ndra_profile_name=dict(required=False, type='str')),
                        resource_type=dict(required=False, type='str', choices=['LogicalRouter']),
                        state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  logical_router_params = get_logical_router_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  logical_router_dict = get_lr_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  logical_router_id, revision = None, None
  if logical_router_dict:
    logical_router_id = logical_router_dict['id']
    revision = logical_router_dict['_revision']

  if state == 'present':
    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, logical_router_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'

    if not updated:
      # add the router
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(body)), id='12345')
      request_data = json.dumps(body)
      try:
          if logical_router_id:
              module.exit_json(changed=False, id=logical_router_id, message="Logical router with display_name %s already exist."% module.params['display_name'])

          (rc, resp) = request(manager_url+ '/logical-routers', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to add logical router. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Logical router with display_name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(body)), id=logical_router_id)

      body['_revision'] = revision # update current revision
      request_data = json.dumps(body)
      id = logical_router_id
      try:
          (rc, resp) = request(manager_url+ '/logical-routers/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update logical router with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="logical router with id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = logical_router_id
    if id is None:
        module.exit_json(changed=False, msg='No logical router exist with display name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(logical_router_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/logical-routers/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete logical router with id %s. Error[%s]." % (id, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=id, message="logical router with id %s deleted." % id)


if __name__ == '__main__':
    main()
