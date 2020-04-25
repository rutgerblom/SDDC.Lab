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
module: nsxt_logical_router_ports
short_description: Create a Logical Router Port
description: Creates a logical router port. The required parameters include resource_type
(LogicalRouterUpLinkPort, LogicalRouterDownLinkPort, LogicalRouterLinkPort,
LogicalRouterLoopbackPort, LogicalRouterCentralizedServicePort); and
logical_router_id (the router to which each logical router port is assigned).
The service_bindings parameter is optional.

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
    admin_state:
        description: Admin state of port.
        required: false
        type: str
    display_name:
        description: Display name
        required: true
        type: str
    edge_cluster_member_index:
        description: Member index of the edge node on the cluster
        required: false
        type: list
    enable_netx:
        description: Port is exclusively used for N-S service insertion
        required: false
        type: boolean
    linked_logical_router_port_id:
        description: Identifier of connected LogicalRouterLinkPortOnTIER1 of TIER1 logical
                     router
        is_valid:
            description: Will be set to false if the referenced NSX resource has been deleted.
            required: false
            type: boolean
        profile_type:
            description: Profile type of the ServiceConfig
            required: true
            type: str
        required: false
        selected:
            description: Set to true if this resource has been selected to be acted upon
            required: true
            type: boolean
        service:
            alg:
                description: "The Application Layer Gateway (ALG) protocol.
                              Please note, protocol NBNS_BROADCAST and NBDG_BROADCAST are  
                              deprecated.Please use UDP protocol and create L4 Port Set type 
                              of service instead."
                required: true
                type: str
            description: Service which registered the ip.
            destination_ports:
                description: Destination ports
                required: false
                type: list
            ether_type:
                description: Type of the encapsulated protocol
                required: true
                type: int
            icmp_code:
                description: 'Code of the IPv4 ICMP message.'
                required: false
                type: int
            icmp_type:
                description: ICMP message type
                required: false
                type: int
            l4_protocol:
                description: L4 protocol
                required: true
                type: str
            protocol:
                description: Export protocol
                required: true
                type: str
            protocol_number:
                description: The IP protocol number
                required: true
                type: int
            required: false
            resource_type:
                description: "LogicalRouterUpLinkPort is allowed only on TIER0 logical router.
                              It is the north facing port of the logical router. 
                              LogicalRouterLinkPortOnTIER0 is allowed only on TIER0 logical 
                              router.
                              This is the port where the LogicalRouterLinkPortOnTIER1
                              of TIER1 logical router connects to. LogicalRouterLinkPortOnTIER1
                              is allowed only on TIER1 logical router.
                              This is the port using which the user connected to TIER1 logical
                              router for upwards connectivity via TIER0 logical router.

                              Connect this port to the LogicalRouterLinkPortOnTIER0 of the TIER0
                              logical router. LogicalRouterDownLinkPort is for the connected 
                              subnets on the logical router. LogicalRouterLoopbackPort is a 
                              loopback port for logical router component which is placed on c
                              hosen edge cluster member. LogicalRouterIPTunnelPort is a IPSec VPN
                              tunnel port created on logical router when route based VPN session 
                              configured.
                              LogicalRouterCentralizedServicePort is allowed only on Active/Standby 
                              TIER0 and TIER1 logical router. Port can be connected to VLAN or 
                              overlay logical switch. Unlike downlink port it does not participate
                              in distributed routing and hosted on all edge cluster members 
                              associated with logical router.
                              Stateful services can be applied on this port."
                required: true
                type: str
            source_ports:
                description: Source ports
                required: false
                type: list
            type: dict
        target_display_name:
            description: Display name of the NSX resource.
            required: false
            type: str
        target_id:
            description: Identifier of the NSX resource.
            required: false
            type: str
        target_type:
            description: Type of the Policy object corresponding to the source type (e.g. Segment).
            required: false
            type: str
        type: dict
    linked_logical_switch_port_id:
        description: Reference to the logical switch port to connect to
        is_valid:
            description: Will be set to false if the referenced NSX resource has been deleted.
            required: false
            type: boolean
        profile_type:
            description: Profile type of the ServiceConfig
            required: true
            type: str
        required: false
        selected:
            description: Set to true if this resource has been selected to be acted upon
            required: true
            type: boolean
        service:
            alg:
                description: "The Application Layer Gateway (ALG) protocol.
                              Please note, protocol NBNS_BROADCAST and 
                              NBDG_BROADCAST are  deprecated.
                              Please use UDP protocol and create L4 Port 
                              Set type of service instead."
                required: true
                type: str
            description: Service which registered the ip.
            destination_ports:
                description: Destination ports
                required: false
                type: list
            ether_type:
                description: Type of the encapsulated protocol
                required: true
                type: int
            icmp_code:
                description: 'Code of the IPv4 ICMP message.'
                required: false
                type: int
            icmp_type:
                description: ICMP Type
                required: false
                type: int
            l4_protocol:
                description: L4 Protocol
                required: true
                type: str
            protocol:
                description: Export protocol
                required: true
                type: str
            protocol_number:
                description: The IP protocol number
                required: true
                type: int
            required: false
            resource_type:
                description: "LogicalRouterUpLinkPort is allowed only on TIER0 logical router.
                              It is the north facing port of the logical router. 
                              LogicalRouterLinkPortOnTIER0 is allowed only on TIER0 logical 
                              router.
                              This is the port where the LogicalRouterLinkPortOnTIER1
                              of TIER1 logical router connects to. LogicalRouterLinkPortOnTIER1
                              is allowed only on TIER1 logical router.
                              This is the port using which the user connected to TIER1 logical
                              router for upwards connectivity via TIER0 logical router.

                              Connect this port to the LogicalRouterLinkPortOnTIER0 of the TIER0
                              logical router. LogicalRouterDownLinkPort is for the connected 
                              subnets on the logical router. LogicalRouterLoopbackPort is a 
                              loopback port for logical router component which is placed on c
                              hosen edge cluster member. LogicalRouterIPTunnelPort is a IPSec VPN
                              tunnel port created on logical router when route based VPN session 
                              configured.
                              LogicalRouterCentralizedServicePort is allowed only on Active/Standby 
                              TIER0 and TIER1 logical router. Port can be connected to VLAN or 
                              overlay logical switch. Unlike downlink port it does not participate
                              in distributed routing and hosted on all edge cluster members 
                              associated with logical router.
                              Stateful services can be applied on this port."
                required: true
                type: str
            source_ports:
                description: Source ports
                required: false
                type: list
            type: dict
        target_display_name:
            description: Display name of the NSX resource.
            required: false
            type: str
        target_id:
            description: Identifier of the NSX resource.
            required: false
            type: str
        target_type:
            description: Type of the Policy object corresponding to the source type 
                         (e.g. Segment).
            required: false
            type: str
        type: dict
    logical_router_name:
        description: Name of the logical router
        required: true
        type: str
    mac_address:
        description: MAC address
        required: false
        type: str
    mtu:
        description: 'Maximum transmission unit specifies the size of the largest packet
                      that a network protocol can transmit. If not specified, the global logical
                      MTU set in the /api/v1/global-configs/RoutingGlobalConfig API will be
                      used.'
        required: false
        type: int
    resource_type:
        description: "LogicalRouterUpLinkPort is allowed only on TIER0 logical router.
                    It is the north facing port of the logical router. 
                    LogicalRouterLinkPortOnTIER0 is allowed only on TIER0 logical 
                    router.
                    This is the port where the LogicalRouterLinkPortOnTIER1
                    of TIER1 logical router connects to. LogicalRouterLinkPortOnTIER1
                    is allowed only on TIER1 logical router.
                    This is the port using which the user connected to TIER1 logical
                    router for upwards connectivity via TIER0 logical router.

                    Connect this port to the LogicalRouterLinkPortOnTIER0 of the TIER0
                    logical router. LogicalRouterDownLinkPort is for the connected 
                    subnets on the logical router. LogicalRouterLoopbackPort is a 
                    loopback port for logical router component which is placed on c
                    hosen edge cluster member. LogicalRouterIPTunnelPort is a IPSec VPN
                    tunnel port created on logical router when route based VPN session 
                    configured.
                    LogicalRouterCentralizedServicePort is allowed only on Active/Standby 
                    TIER0 and TIER1 logical router. Port can be connected to VLAN or 
                    overlay logical switch. Unlike downlink port it does not participate
                    in distributed routing and hosted on all edge cluster members 
                    associated with logical router.
                    Stateful services can be applied on this port."
        required: true
        type: str
    service_bindings:
        description: Service Bindings
        required: false
        type: array of ServiceBinding
    state:
        choices:
        - present
        - absent
        description: "State can be either 'present' or 'absent'. 
                      'present' is used to create or update resource. 
                      'absent' is used to delete resource."
        required: true
    subnets:
        description: Logical router port subnets
        required: false
        type: array of IPSubnet
    urpf_mode:
        description: Unicast Reverse Path Forwarding mode
        required: false
        type: str
    vpn_session_id:
        description: Associated VPN session identifier.
        required: false
        type: str
    description:
        description: Description of the resou
        required: False
        type: 'str'
    ndra_profile_id:
        description: NDRA Profile id
        required: False
        type: 'str'
    enable_multicast:
        description: Flag to enable/disable Multicast
        required: False
        type: 'bool'
    routing_policies:
        description: Routing policies used to specify how the traffic, which matches the
                     policy routes, will be processed.
        required: False
        type: 'list'
    ndra_prefix_config:
        description: Configuration to override the neighbor discovery router advertisement
                      prefix time parameters at the subnet level. Note that users are allowed
                      to override the prefix time only for IPv6 subnets which are configured
                      on the port.
        required: False
        type: 'list'
    pim_config:
        description: PIM configuration parameters
        required: False
        type: 'dict'
        enabled:
            description: Flag to enable/disable PIM
            required: False
            type: 'bool'
            default: False
    tags:
        description: Opaque identifiers meaningful to the API user
        required: False
        type: list
    
'''

EXAMPLES = '''
- name: Create a Logical Router Port
  nsxt_logical_routers_ports:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      resource_type: LogicalRouterDownLinkPort
      logical_router_name: "lr-1"
      linked_logical_switch_port_id:
        target_type: LogicalPort
        target_id: "18691381-b08f-4d90-8c0c-98d0e449b141"
      subnets:
      - ip_addresses:
        - "172.16.40.1"
        prefix_length: 24
      state: present
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def get_logical_router_port_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_logical_router_ports(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/logical-router-ports', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing logical router ports. Error [%s]' % (to_native(err)))
    return resp

def get_lr_port_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    logical_router_ports = get_logical_router_ports(module, manager_url, mgr_username, mgr_password, validate_certs)
    for logical_router_port in logical_router_ports['results']:
        if logical_router_port.__contains__('display_name') and logical_router_port['display_name'] == display_name:
            return logical_router_port
    return None

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

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, logical_router_port_params ):
    logical_router_port_params['logical_router_id'] = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                '/logical-routers', logical_router_port_params.pop('logical_router_name', None))
    if logical_router_port_params.__contains__('linked_logical_switch_port_id') and \
        logical_router_port_params['linked_logical_switch_port_id'].__contains__('target_display_name'):
        if not logical_router_port_params['linked_logical_switch_port_id'].__contains__('target_id'):
            logical_router_port_params['linked_logical_switch_port_id']['target_id'] = get_id_from_display_name(module, manager_url, mgr_username,
                  mgr_password, validate_certs, '/logical-ports', logical_router_port_params['linked_logical_switch_port_id']['target_display_name'])
    return logical_router_port_params

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, logical_router_port_params):
    existing_lr_port = get_lr_port_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, logical_router_port_params['display_name'])
    if existing_lr_port is None:
        return False
    if existing_lr_port.__contains__('description') and logical_router_port_params.__contains__('description') and\
       existing_lr_port['description'] != logical_router_port_params['description']:
       return True
    if existing_lr_port.__contains__('description') and not logical_router_port_params.__contains__('description'):
        return True
    if not existing_lr_port.__contains__('description') and logical_router_port_params.__contains__('description'):
        return True
    if existing_lr_port['resource_type'] != logical_router_port_params['resource_type']:
        return True
    if existing_lr_port['logical_router_id'] != logical_router_port_params['logical_router_id']:
        return True
    if existing_lr_port.__contains__('service_bindings') and logical_router_port_params.__contains__('service_bindings') and \
        existing_lr_port['service_bindings'] != logical_router_port_params['service_bindings']:
        return True
    if existing_lr_port.__contains__('subnets') and logical_router_port_params.__contains__('subnets') and \
        existing_lr_port['subnets'] != logical_router_port_params['subnets']:
        return True
    return False

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                        description=dict(required=False, type='str'),
                        ndra_profile_id=dict(required=False, type='str'),
                        enable_multicast=dict(required=False, type='bool'),
                        routing_policies=dict(required=False, type='list'),
                        ndra_prefix_config=dict(required=False, type='list'),
                        pim_config=dict(required=False, type='dict',
                        enabled=dict(required=False, type='bool', default=False)),
                        subnets=dict(required=False, type='list'),
                        urpf_mode=dict(required=False, type='str'),
                        mac_address=dict(required=False, type='str'),
                        linked_logical_switch_port_id=dict(required=False, type='dict',
                        profile_type=dict(required=True, type='str'),
                        selected=dict(required=True, type='bool'),
                        service=dict(required=False, type='dict',
                        ether_type=dict(required=True, type='int'),
                        destination_ports=dict(required=False, type='list'),
                        l4_protocol=dict(required=True, type='str'),
                        source_ports=dict(required=False, type='list'),
                        icmp_code=dict(required=False, type='int'),
                        icmp_type=dict(required=False, type='int'),
                        protocol=dict(required=True, type='str'),
                        protocol_number=dict(required=True, type='int'),
                        alg=dict(required=True, type='str'),
                        resource_type=dict(required=True, type='str')),
                        target_display_name=dict(required=False, type='str'),
                        is_valid=dict(required=False, type='bool'),
                        target_id=dict(required=False, type='str'),
                        target_type=dict(required=False, type='str')),
                        admin_state=dict(required=False, type='str'),
                        vpn_session_id=dict(required=False, type='str'),
                        enable_netx=dict(required=False, type='bool'),
                        edge_cluster_member_index=dict(required=False, type='list'),
                        mtu=dict(required=False, type='int'),
                        linked_logical_router_port_id=dict(required=False, type='dict',
                        profile_type=dict(required=True, type='str'),
                        selected=dict(required=True, type='bool'),
                        service=dict(required=False, type='dict',
                        ether_type=dict(required=True, type='int'),
                        destination_ports=dict(required=False, type='list'),
                        l4_protocol=dict(required=True, type='str'),
                        source_ports=dict(required=False, type='list'),
                        icmp_code=dict(required=False, type='int'),
                        icmp_type=dict(required=False, type='int'),
                        protocol=dict(required=True, type='str'),
                        protocol_number=dict(required=True, type='int'),
                        alg=dict(required=True, type='str'),
                        resource_type=dict(required=True, type='str')),
                        target_display_name=dict(required=False, type='str'),
                        is_valid=dict(required=False, type='bool'),
                        target_id=dict(required=False, type='str'),
                        target_type=dict(required=False, type='str')),
                        logical_router_name=dict(required=True, type='str'),
                        service_bindings=dict(required=False, type='list'),
                        resource_type=dict(required=True, type='str'),
                        tags=dict(required=False, type='list'),
                        state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  logical_router_port_params = get_logical_router_port_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  logical_router_port_dict = get_lr_port_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  logical_router_port_id, revision = None, None
  if logical_router_port_dict:
    logical_router_port_id = logical_router_port_dict['id']
    revision = logical_router_port_dict['_revision']

  if state == 'present':
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, logical_router_port_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)

    if not updated:
      # add the logical_router_port
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(logical_router_port_params)), id='12345')
      request_data = json.dumps(logical_router_port_params)
      try:
          if logical_router_port_id:
              module.exit_json(changed=False, id=logical_router_port_id, message="Logical router port with display_name %s already exist."% module.params['display_name'])

          (rc, resp) = request(manager_url+ '/logical-router-ports', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to add logical router port. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Logical router port with displayname %s created." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(logical_router_port_params)), id=logical_router_port_id)
      logical_router_port_params['_revision'] = revision # update current revision
      request_data = json.dumps(logical_router_port_params)
      id = logical_router_port_id
      try:
          (rc, resp) = request(manager_url+ '/logical-router-ports/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update logical router port with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="logical router port with id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = logical_router_port_id
    if id is None:
        module.exit_json(changed=False, msg='No logical router port exist with display name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(logical_router_port_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/logical-router-ports/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete logical router port with id %s. Error[%s]." % (id, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=id, message="Logical router port with id %s deleted." % id)


if __name__ == '__main__':
    main()
