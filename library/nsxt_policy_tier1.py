#!/usr/bin/env python
#
# Copyright 2018 VMware, Inc.
# SPDX-License-Identifier: BSD-2-Clause OR GPL-3.0-only
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
module: nsxt_policy_tier1
short_description: 'Create/Update/Delete a Tier-1 and associated resources'
description: Creates/Updates/Deletes a Tier-1 resource using the Policy API.
             Assocaited resources include 'Tier-1 Locale Service' and
             'Tier-1 Interface'. 'Tier-1 Locale Service' and 'Tier-1 Interface'
             attributes must be prepended with 't1ls' and 't1iface'
             respectively.
version_added: '2.8'
author: 'Gautam Verma'
options:
    hostname:
        description: Deployed NSX manager hostname.
        required: true
        type: str
    username:
        description: The username to authenticate with the NSX manager.
        type: str
    password:
        description:
            - The password to authenticate with the NSX manager.
            - Must be specified if username is specified
        type: str
    ca_path:
        description: Path to the CA bundle to be used to verify host's SSL
                     certificate
        type: str
    nsx_cert_path:
        description: Path to the certificate created for the Principal
                     Identity using which the CRUD operations should be
                     performed
        type: str
    nsx_key_path:
        description:
            - Path to the certificate key created for the Principal Identity
              using which the CRUD operations should be performed
            - Must be specified if nsx_cert_path is specified
        type: str
    request_headers:
        description: HTTP request headers to be sent to the host while making
                     any request
        type: dict
    display_name:
        description:
            - Display name.
            - If resource ID is not specified, display_name will be used as ID.
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
    validate_certs:
        description: Enable server certificate verification.
        type: bool
        default: False
    tags:
        description: Opaque identifiers meaningful to the API user.
        type: dict
        suboptions:
            scope:
                description: Tag scope.
                required: true
                type: str
            tag:
                description: Tag value.
                required: true
                type: str
    create_or_update_subresource_first:
        type: bool
        default: false
        description:
            - Can be used to create subresources first.
            - Can be specified for each subresource.
    delete_subresource_first:
        type: bool
        default: true
        description:
            - Can be used to delete subresources first.
            - Can be specified for each subresource.
    achieve_subresource_state_if_del_parent:
        type: bool
        default: false
        description:
            - Can be used to achieve the state of subresources even if
              the parent(base) resource's state is absent.
            - Can be specified for each subresource.
    do_wait_till_create:
        type: bool
        default: false
        description:
            - Can be used to wait for the realization of subresource before the
              request to create the next resource is sent to the Manager.
            - Can be specified for each subresource.
    id:
        description: Tier-1 ID
        required: false
        type: str
    description:
        description: Tier-1 description
        type: str
    default_rule_logging:
        description: Enable logging for whitelisted rule.
                     Indicates if logging should be enabled for the default
                     whitelisting rule.
        default: false
    disable_firewall:
        description: Disable or enable gateway fiewall.
        default: False
        type: bool
    failover_mode:
        description: Determines the behavior when a Tier-1 instance in
                     ACTIVE-STANDBY high-availability mode restarts
                     after a failure. If set to PREEMPTIVE, the preferred node
                     will take over, even if it causes
                     another failure. If set to NON_PREEMPTIVE, then
                     the instance that restarted will remain secondary.
                     This property must not be populated unless the
                     ha_mode property is set to ACTIVE_STANDBY.
        choices:
            - 'NON_PREEMPTIVE'
            - 'PREEMPTIVE'
        default: 'NON_PREEMPTIVE'
        type: str
    enable_standby_relocation:
        description:
            - Flag to enable standby service router relocation.
            - Standby relocation is not enabled until edge cluster is
              configured for Tier1.
        type: bool
        default: false
    force_whitelisting:
        description: Flag to add whitelisting FW rule during
                     realization.
        default: False
        type: bool
    intersite_config:
        description: Inter site routing configuration when the gateway is
                     streched.
        type: dict
        suboptions:
            fallback_sites:
                description: Fallback site to be used as new primary
                             site on current primary site failure.
                             Disaster recovery must be initiated via
                             API/UI. Fallback site configuration is
                             supported only for T0 gateway. T1 gateway
                             will follow T0 gateway's primary site
                             during disaster recovery
                type: list
            intersite_transit_subnet:
                description:
                    - Transit subnet in CIDR format
                    - IPv4 subnet for inter-site transit segment
                      connecting service routers across sites for
                      stretched gateway. For IPv6 link local subnet is
                      auto configured
                type: str
                default: "169.254.32.0/20"
            last_admin_active_epoch:
                description:
                    - Epoch of last time admin changing active
                      LocaleServices
                    - Epoch(in seconds) is auto updated based on
                      system current timestamp when primary locale
                      service is updated. It is used for resolving
                      conflict during site failover. If system clock
                      not in sync then User can optionally override
                      this. New value must be higher than the current
                      value.
                type: int
            primary_site_path:
                description:
                    - Primary egress site for gateway.
                    - Primary egress site for gateway. T0/T1 gateway in
                      Active/Standby mode supports stateful services on primary
                      site. In this mode primary site must be set if gateway is
                      stretched to more than one site. For T0 gateway in
                      Active/Active primary site is optional field. If set then
                      secondary site prefers routes learned from primary over
                      locally learned routes. This field is not applicable for
                      T1 gateway with no services
                type: str
    ipv6_ndra_profile_id:
        description: IPv6 NDRA profile configuration on Tier1.
                     Either or both NDRA and/or DAD profiles can be
                     configured. Related attribute ipv6_dad_profile_id.
        type: str
    ipv6_ndra_profile_display_name:
        description: Same as ipv6_ndra_profile_id. Either one can be specified.
                     If both are specified, ipv6_ndra_profile_id takes
                     precedence.
        type: str
    ipv6_dad_profile_id:
        description: IPv6 DRA profile configuration on Tier1.
                     Either or both NDRA and/or DAD profiles can be
                     configured. Related attribute ipv6_ndra_profile_id.
        type: str
    ipv6_dad_profile_display_name:
        description: Same as ipv6_dad_profile_id. Either one can be specified.
                     If both are specified, ipv6_dad_profile_id takes
                     precedence.
        type: str
    dhcp_config_id:
        description: DHCP configuration for Segments connected to
                     Tier-1. DHCP service is configured in relay mode.
        type: str
    dhcp_config_display_name:
        description: Same as dhcp_config_id. Either one can be specified.
                     If both are specified, dhcp_config_id takes precedence.
        type: str
    pool_allocation:
        description:
            - Edge node allocation size
            - Supports edge node allocation at different sizes for routing and
              load balancer service to meet performance and scalability
              requirements.
            - ROUTING - Allocate edge node to provide routing services.
            - LB_SMALL, LB_MEDIUM, LB_LARGE, LB_XLARGE - Specify size of load
              balancer service that will be configured on TIER1 gateway.
        type: str
        choices:
            - ROUTING
            - LB_SMALL
            - LB_MEDIUM
            - LB_LARGE
            - LB_XLARGE
        default: ROUTING
    qos_profile:
        description: QoS Profile configuration for Tier1 router link connected
                     to Tier0 gateway.
        type: dict
        suboptions:
            egress_qos_profile_path:
                description: Policy path to gateway QoS profile in egress
                             direction.
                type: str
            ingress_qos_profile_path:
                description: Policy path to gateway QoS profile in ingress
                             direction.
                type: str
    route_advertisement_rules:
        description: Route advertisement rules and filtering
        type: list
        suboptions:
            action:
                description:
                    - Action to advertise filtered routes to the connected
                      Tier0 gateway.
                choices:
                    - PERMIT: Enables the advertisment
                    - DENY: Disables the advertisement
                type: str
                required: true
            name:
                description: Display name for rule
                type: str
                required: true
            prefix_operator:
                description:
                    - Prefix operator to filter subnets.
                    - GE prefix operator filters all the routes with prefix
                      length greater than or equal to the subnets configured.
                    - EQ prefix operator filter all the routes with prefix
                      length equal to the subnets configured.
                type: str
                choices:
                    - GE
                    - EQ
            route_advertisement_types:
                description:
                    - Enable different types of route advertisements.
                    - By default, Routes to IPSec VPN local-endpoint subnets
                      (TIER1_IPSEC_LOCAL_ENDPOINT) are advertised if no value
                      is supplied here.
                type: list
                choices:
                    - 'TIER1_STATIC_ROUTES'
                    - 'TIER1_CONNECTED'
                    - 'TIER1_NAT'
                    - 'TIER1_LB_VIP'
                    - 'TIER1_LB_SNAT'
                    - 'TIER1_DNS_FORWARDER_IP'
                    - 'TIER1_IPSEC_LOCAL_ENDPOINT'
            subnets:
                description: Network CIDRs to be routed.
                type: list
    route_advertisement_types:
        description:
            - Enable different types of route advertisements.
            - By default, Routes to IPSec VPN local-endpoint subnets
              (TIER1_IPSEC_LOCAL_ENDPOINT) are advertised if no value is
              supplied here.
        type: list
        choices:
            - 'TIER1_STATIC_ROUTES'
            - 'TIER1_CONNECTED'
            - 'TIER1_NAT'
            - 'TIER1_LB_VIP'
            - 'TIER1_LB_SNAT'
            - 'TIER1_DNS_FORWARDER_IP'
            - 'TIER1_IPSEC_LOCAL_ENDPOINT'
    tier0_id:
        description: Tier-1 connectivity to Tier-0
        type: str
    tier0_display_name:
        description: Same as tier0_id. Either one can be specified.
                    If both are specified, tier0_id takes precedence.
        type: str
    static_routes:
        type: list
        element: dict
        description: This is a list of Static Routes that need to be created,
                     updated, or deleted
        suboptions:
            id:
                description: Tier-1 Static Route ID.
                required: false
                type: str
            display_name:
                description:
                    - Tier-1 Static Route display name.
                    - Either this or id must be specified. If both are
                      specified, id takes precedence.
                required: false
                type: str
            description:
                description:
                    - Tier-1 Static Route description.
                type: str
            state:
                description:
                    - State can be either 'present' or 'absent'. 'present' is
                      used to create or update resource. 'absent' is used to
                      delete resource.
                    - Must be specified in order to modify the resource
                choices:
                    - present
                    - absent
            network:
                description: Network address in CIDR format
                required: true
                type: str
            next_hops:
                description: Next hop routes for network
                type: list
                elements: dict
                suboptions:
                    admin_distance:
                        description: Cost associated with next hop route
                        type: int
                        default: 1
                ip_address:
                    description: Next hop gateway IP address
                    type: str
                scope:
                    description:
                        - Interface path associated with current route
                        - For example, specify a policy path referencing the
                          IPSec VPN Session
                    type: list
            tags:
                description: Opaque identifiers meaningful to the API user
                type: dict
                suboptions:
                    scope:
                        description: Tag scope.
                        required: true
                        type: str
                    tag:
                        description: Tag value.
                        required: true
                        type: str
            achieve_subresource_state_if_del_parent:
                type: bool
                default: false
                description:
                    - Can be used to achieve the state of subresources even if
                      the parent(base) resource's state is absent.
                    - Can be specified for each subresource.
            do_wait_till_create:
                type: bool
                default: false
                description:
                    - Can be used to wait for the realization of subresource
                      before the request to create the next resource is sent to
                      the Manager
    locale_services:
        type: list
        element: dict
        description: This is a list of Locale Services that need to be created,
                     updated, or deleted
        suboptions:
            id:
                description: Tier-1 Locale Service ID
                type: str
            display_name:
                description:
                    - Tier-1 Locale Service display name.
                    - Either this or id must be specified. If both are
                      specified, id takes precedence.
                required: false
                type: str
            description:
                description: Tier-1 Locale Service  description
                type: str
            state:
                description:
                    - State can be either 'present' or 'absent'. 'present' is
                      used to create or update resource. 'absent' is used to
                      delete resource.
                    - Required if I(segp_id != null)
                choices:
                    - present
                    - absent
            tags:
                description: Opaque identifiers meaningful to the API user.
                type: dict
                suboptions:
                    scope:
                        description: Tag scope.
                        required: true
                        type: str
                    tag:
                        description: Tag value.
                        required: true
                        type: str
            achieve_subresource_state_if_del_parent:
                type: bool
                default: false
                description:
                    - Can be used to achieve the state of subresources even if
                      the parent(base) resource's state is absent.
                    - Can be specified for each subresource.
            do_wait_till_create:
                type: bool
                default: false
                description:
                    - Can be used to wait for the realization of subresource
                      before the request to create the next resource is sent to
                      the Manager
            edge_cluster_info:
                description: Used to create path to edge cluster. Auto-assigned
                             if associated enforcement-point has only one edge
                             cluster.
                type: dict
                suboptions:
                    site_id:
                        description: site_id where edge cluster is located
                        default: default
                        type: str
                    enforcementpoint_id:
                        description: enforcementpoint_id where edge cluster is
                                     located
                        default: default
                        type: str
                    edge_cluster_id:
                        description: ID of the edge cluster
                        required: true
                        type: str
                    edge_cluster_display_name:
                        description:
                            - display name of the edge cluster.
                            - Either this or edge_cluster_id must be specified.
                              If both are specified, edge_cluster_id takes
                              precedence
                        type: str
            preferred_edge_nodes_info:
                description: Used to create paths to edge nodes. Specified edge
                             is used as preferred edge cluster member when
                             failover mode is set to PREEMPTIVE, not
                             applicable otherwise.
                type: list
                suboptions:
                    site_id:
                        description: site_id where edge node is located
                        default: default
                        type: str
                    enforcementpoint_id:
                        description: enforcementpoint_id where edge node is
                                     located
                        default: default
                        type: str
                    edge_cluster_id:
                        description: edge_cluster_id where edge node is
                                     located
                        required: true
                        type: str
                    edge_cluster_display_name:
                        description:
                            - display name of the edge cluster.
                            - either this or edge_cluster_id must be specified.
                              If both are specified, edge_cluster_id takes
                              precedence
                        type: str
                    edge_node_id:
                        description: ID of the edge node
                        type: str
                    edge_node_display_name:
                        description:
                            - Display name of the edge node.
                            - either this or edge_node_id must be specified. If
                              both are specified, edge_node_id takes precedence
                        type: str
            route_redistribution_types:
                description:
                    - Enable redistribution of different types of routes on
                      Tier-0.
                    - This property is only valid for locale-service under
                      Tier-0.
                    - This property is deprecated, please use
                      "route_redistribution_config" property to configure
                      redistribution rules.
                choices:
                    - TIER0_STATIC - Redistribute user added
                        static routes.
                    - TIER0_CONNECTED - Redistribute all
                        subnets configured on Interfaces and
                        routes related to TIER0_ROUTER_LINK,
                        TIER0_SEGMENT, TIER0_DNS_FORWARDER_IP,
                        TIER0_IPSEC_LOCAL_IP, TIER0_NAT types.
                    - TIER1_STATIC - Redistribute all subnets
                        and static routes advertised by Tier-1s.
                    - TIER0_EXTERNAL_INTERFACE - Redistribute
                        external interface subnets on Tier-0.
                    - TIER0_LOOPBACK_INTERFACE - Redistribute
                        loopback interface subnets on Tier-0.
                    - TIER0_SEGMENT - Redistribute subnets
                        configured on Segments connected to
                        Tier-0.
                    - TIER0_ROUTER_LINK - Redistribute router
                        link port subnets on Tier-0.
                    - TIER0_SERVICE_INTERFACE - Redistribute
                        Tier0 service interface subnets.
                    - TIER0_DNS_FORWARDER_IP - Redistribute DNS
                        forwarder subnets.
                    - TIER0_IPSEC_LOCAL_IP - Redistribute IPSec
                        subnets.
                    - TIER0_NAT - Redistribute NAT IPs owned by
                        Tier-0.
                    - TIER0_EVPN_TEP_IP - Redistribute EVPN
                        local endpoint subnets on Tier-0.
                    - TIER1_NAT - Redistribute NAT IPs
                        advertised by Tier-1 instances.
                    - TIER1_LB_VIP - Redistribute LB VIP IPs
                        advertised by Tier-1 instances.
                    - TIER1_LB_SNAT - Redistribute LB SNAT IPs
                        advertised by Tier-1 instances.
                    - TIER1_DNS_FORWARDER_IP - Redistribute DNS
                        forwarder subnets on Tier-1 instances.
                    - TIER1_CONNECTED - Redistribute all
                        subnets configured on Segments and
                        Service Interfaces.
                    - TIER1_SERVICE_INTERFACE - Redistribute
                        Tier1 service interface subnets.
                    - TIER1_SEGMENT - Redistribute subnets
                        configured on Segments connected to
                        Tier1.
                    - TIER1_IPSEC_LOCAL_ENDPOINT - Redistribute
                        IPSec VPN local-endpoint subnets
                        advertised by TIER1.
                type: list
            route_redistribution_config:
                description: Configure all route redistribution properties like
                             enable/disable redistributon, redistribution rule
                             and so on.
                type: dict
                suboptions:
                    bgp_enabled:
                        description: Flag to enable route redistribution.
                        type: bool
                        default: false
                    redistribution_rules:
                        description: List of redistribution rules.
                        type: list
                        elements: dict
                        suboptions:
                            name:
                                description: Rule name
                                type: str
                            route_map_path:
                                description: Route map to be associated with
                                             the redistribution rule
                                type: str
                            route_redistribution_types:
                                description: Tier-0 route redistribution types
                                choices:
                                    - TIER0_STATIC - Redistribute user added
                                      static routes.
                                    - TIER0_CONNECTED - Redistribute all
                                      subnets configured on Interfaces and
                                      routes related to TIER0_ROUTER_LINK,
                                      TIER0_SEGMENT, TIER0_DNS_FORWARDER_IP,
                                      TIER0_IPSEC_LOCAL_IP, TIER0_NAT types.
                                    - TIER1_STATIC - Redistribute all subnets
                                      and static routes advertised by Tier-1s.
                                    - TIER0_EXTERNAL_INTERFACE - Redistribute
                                      external interface subnets on Tier-0.
                                    - TIER0_LOOPBACK_INTERFACE - Redistribute
                                      loopback interface subnets on Tier-0.
                                    - TIER0_SEGMENT - Redistribute subnets
                                      configured on Segments connected to
                                      Tier-0.
                                    - TIER0_ROUTER_LINK - Redistribute router
                                      link port subnets on Tier-0.
                                    - TIER0_SERVICE_INTERFACE - Redistribute
                                      Tier0 service interface subnets.
                                    - TIER0_DNS_FORWARDER_IP - Redistribute DNS
                                      forwarder subnets.
                                    - TIER0_IPSEC_LOCAL_IP - Redistribute IPSec
                                      subnets.
                                    - TIER0_NAT - Redistribute NAT IPs owned by
                                      Tier-0.
                                    - TIER0_EVPN_TEP_IP - Redistribute EVPN
                                      local endpoint subnets on Tier-0.
                                    - TIER1_NAT - Redistribute NAT IPs
                                      advertised by Tier-1 instances.
                                    - TIER1_LB_VIP - Redistribute LB VIP IPs
                                      advertised by Tier-1 instances.
                                    - TIER1_LB_SNAT - Redistribute LB SNAT IPs
                                      advertised by Tier-1 instances.
                                    - TIER1_DNS_FORWARDER_IP - Redistribute DNS
                                      forwarder subnets on Tier-1 instances.
                                    - TIER1_CONNECTED - Redistribute all
                                      subnets configured on Segments and
                                      Service Interfaces.
                                    - TIER1_SERVICE_INTERFACE - Redistribute
                                      Tier1 service interface subnets.
                                    - TIER1_SEGMENT - Redistribute subnets
                                      configured on Segments connected to
                                      Tier1.
                                    - TIER1_IPSEC_LOCAL_ENDPOINT - Redistribute
                                      IPSec VPN local-endpoint subnets
                                      advertised by TIER1.
                                type: list
            ha_vip_configs:
                type: list
                elements: dict
                description:
                    - Array of HA VIP Config.
                    - This configuration can be defined only for Active-Standby
                      Tier0 gateway to provide redundancy. For mulitple
                      external interfaces, multiple HA VIP configs must be
                      defined and each config will pair exactly two external
                      interfaces. The VIP will move and will always be owned by
                      the Active node. When this property is configured,
                      configuration of dynamic-routing is not allowed.
                suboptions:
                    enabled:
                        description: Flag to enable this HA VIP config.
                        default: true
                        type: bool
                    external_interface_paths:
                        description:
                            - Policy paths to Tier0 external interfaces for
                              providing redundancy
                            - Policy paths to Tier0 external interfaces which
                              are to be paired to provide redundancy. Floating
                              IP will be owned by one of these interfaces
                              depending upon which edge node is Active.
                        type: list
                    vip_subnets:
                        description:
                            - VIP floating IP address subnets
                            - Array of IP address subnets which will be used as
                              floating IP addresses.
                        type: list
                        suboptions:
                            ip_addresses:
                                description: IP addresses assigned to interface
                                type: list
                                required: true
                            prefix_len:
                                description: Subnet prefix length
                                type: int
                                required: true
            interfaces:
                type: list
                element: dict
                description: Specify the interfaces associated with the Gateway
                             in this section that need to be created, updated,
                             or deleted
                suboptions:
                    id:
                        description: Tier-1 Interface ID
                        required: false
                        type: str
                    description:
                        description: Tier-1 Interface  description
                        type: str
                    display_name:
                        description:
                            - Tier-1 Interface display name
                            - Either this or id must be specified. If both are
                              specified, id takes precedence.
                        required: false
                        type: str
                    state:
                        description:
                            - State can be either 'present' or 'absent'.
                              'present' is used to create or update resource.
                              'absent' is used to delete resource.
                            - Required if I(segp_id != null).
                        choices:
                            - present
                            - absent
                    tags:
                        description: Opaque identifiers meaningful to the API
                                     user
                        type: dict
                        suboptions:
                            scope:
                                description: Tag scope.
                                required: true
                                type: str
                            tag:
                                description: Tag value.
                                required: true
                                type: str
                    achieve_subresource_state_if_del_parent:
                        type: bool
                        default: false
                        description:
                            - Can be used to achieve the state of subresources
                              even if the parent(base) resource's state is
                              absent.
                            - Can be specified for each subresource.
                    do_wait_till_create:
                        type: bool
                        default: false
                        description:
                            - Can be used to wait for the realization of
                              subresource before the request to create the next
                              resource is sent to the Manager
                    ipv6_ndra_profile_id:
                        description:
                            - Configrue IPv6 NDRA profile. Only one NDRA
                              profile can be configured
                            - Required if I(id != null)
                        type: str
                    mtu:
                        description:
                            - MTU size
                            - Maximum transmission unit (MTU) specifies the
                              size of the largest packet that a network
                              protocol can transmit.
                        type: int
                    segment_id:
                        description:
                            - Specify Segment to which this interface is
                              connected to.
                            - Required if I(id != null)
                        type: str
                    segment_display_name:
                        description:
                            - Same as segment_id
                            - Either this or segment_id must be specified. If
                              both are specified, segment_id takes precedence.
                        type: str
                    subnets:
                        description:
                            - IP address and subnet specification for interface
                            - Specify IP address and network prefix for
                              interface
                            - Required if I(id != null)
                        type: list
                        elements: dict
                        suboptions:
                            ip_addresses:
                                description: IP addresses assigned to interface
                                type: str
                            prefix_len:
                                description: Subnet prefix length
                                type: str
                    urpf_mode:
                        description: Unicast Reverse Path Forwarding mode
                        type: str
                        choices:
                            - NONE
                            - STRICT
                        default: STRICT
'''

EXAMPLES = '''
- name: create Tier1
  nsxt_policy_tier1:
    hostname: "10.10.10.10"
    nsx_cert_path: /root/com.vmware.nsx.ncp/nsx.crt
    nsx_key_path: /root/com.vmware.nsx.ncp/nsx.key
    validate_certs: False
    display_name: test-tier22222
    state: present
    failover_mode: "PREEMPTIVE"
    disable_firewall: True
    force_whitelisting: True
    enable_standby_relocation: False
    tags:
      - scope: "a"
        tag: "b"
    route_advertisement_rules:
      - name: "test-route-advertisement-rules"
        route_advertisement_types: ['TIER1_STATIC_ROUTES', 'TIER1_CONNECTED']
        subnets: ["35.1.1.1/23"]
    route_advertisement_types:
        - "TIER1_STATIC_ROUTES"
        - "TIER1_CONNECTED"
        - "TIER1_NAT"
    tier0_display_name: "node-t0"
    locale_services:
      - state: present
        display_name: test-t1ls-2
        route_redistribution_config:
          redistribution_rules:
            - name: abc
              route_redistribution_types: ["TIER0_STATIC", "TIER0_NAT"]
        interfaces:
          - id: "test-t1-t1ls-iface-2"
            display_name: "test-t1-t1ls-iface"
            state: present
            subnets:
              - ip_addresses: ["35.1.1.1"]
                prefix_len: 24
            segment_id: "test-seg-2"
            ipv6_ndra_profile_id: test
            mtu: 1400
            urpf_mode: NONE
'''

RETURN = '''# '''

import json
import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import _ANSIBLE_ARGS as ANSIBLE_ARGS
from ansible.module_utils._text import to_native
from ansible.module_utils.nsxt_base_resource import NSXTBaseRealizableResource
from ansible.module_utils.nsxt_resource_urls import (
    TIER_0_URL, TIER_1_URL, IPV6_DAD_PROFILE_URL, IPV6_NDRA_PROFILE_URL,
    DHCP_RELAY_CONFIG_URL, EDGE_CLUSTER_URL, EDGE_NODE_URL, SEGMENT_URL,
    TIER_1_STATIC_ROUTE_URL, TIER_1_LOCALE_SERVICE_URL,
    TIER_1_LS_INTERFACE_URL, TIER_0_LOCALE_SERVICE_URL,
    TIER_0_LS_INTERFACE_URL)


class NSXTTier1(NSXTBaseRealizableResource):
    @staticmethod
    def get_resource_spec():
        tier1_arg_spec = {}
        tier1_arg_spec.update(
            default_rule_logging=dict(
                required=False,
                type='bool'
            ),
            dhcp_config_id=dict(
                required=False,
                type='str'
            ),
            dhcp_config_display_name=dict(
                required=False,
                type='str'
            ),
            disable_firewall=dict(
                required=False,
                type='bool',
                default=False
            ),
            enable_standby_relocation=dict(
                required=False,
                type='bool',
                default=False
            ),
            failover_mode=dict(
                required=False,
                type='str',
                default='NON_PREEMPTIVE',
                choices=['NON_PREEMPTIVE', 'PREEMPTIVE']
            ),
            force_whitelisting=dict(
                required=False,
                type='bool',
                default=False
            ),
            intersite_config=dict(
                required=False,
                type='dict',
                options=dict(
                    fallback_sites=dict(
                        required=False,
                        type='list'
                    ),
                    intersite_transit_subnet=dict(
                        default="169.254.32.0/20",
                        type='str'
                    ),
                    last_admin_active_epoch=dict(
                        required=False,
                        type='int'
                    ),
                    primary_site_path=dict(
                        required=False,
                        type='str'
                    ),
                )
            ),
            ipv6_ndra_profile_id=dict(
                required=False,
                type='str'
            ),
            ipv6_ndra_profile_display_name=dict(
                required=False,
                type='str'
            ),
            ipv6_dad_profile_id=dict(
                required=False,
                type='str'
            ),
            ipv6_dad_profile_display_name=dict(
                required=False,
                type='str'
            ),
            pool_allocation=dict(
                type='str',
                choices=['ROUTING', 'LB_SMALL', 'LB_MEDIUM', 'LB_LARGE',
                         'LB_XLARGE'],
                default='ROUTING'
            ),
            qos_profile=dict(
                type='dict',
                options=dict(
                    egress_qos_profile_path=dict(
                        type='str'
                    ),
                    ingress_qos_profile_path=dict(
                        type='str'
                    )
                )
            ),
            route_advertisement_rules=dict(
                required=False,
                type='list',
                options=dict(
                    action=dict(
                        required=False,
                        type='str',
                        default='PERMIT',
                        choices=['PERMIT', 'DENY']
                    ),
                    name=dict(
                        required=True,
                        type='str'
                    ),
                    prefix_operator=dict(
                        required=False,
                        type='str',
                        default='GE',
                        choices=['GE', 'EQ']
                    ),
                    route_advertisement_types=dict(
                        required=False,
                        type='list',
                        choices=['TIER1_STATIC_ROUTES', 'TIER1_CONNECTED',
                                 'TIER1_NAT', 'TIER1_LB_VIP', 'TIER1_LB_SNAT',
                                 'TIER1_DNS_FORWARDER_IP',
                                 'TIER1_IPSEC_LOCAL_ENDPOINT']
                    ),
                    subnets=dict(
                        required=True,
                        type='list'
                    )
                )
            ),
            route_advertisement_types=dict(
                required=False,
                type='list',
                choices=['TIER1_STATIC_ROUTES', 'TIER1_CONNECTED', 'TIER1_NAT',
                         'TIER1_LB_VIP', 'TIER1_LB_SNAT',
                         'TIER1_DNS_FORWARDER_IP', 'TIER1_IPSEC_LOCAL_ENDPOINT'
                         ]
            ),
            tier0_id=dict(
                required=False,
                type='str'
            ),
            tier0_display_name=dict(
                required=False,
                type='str'
            )
        )
        return tier1_arg_spec

    @staticmethod
    def get_resource_base_url(baseline_args=None):
        return TIER_1_URL

    def update_resource_params(self, nsx_resource_params):
        ipv6_profile_paths = []
        if self.do_resource_params_have_attr_with_id_or_display_name(
                "ipv6_ndra_profile"):
            ipv6_ndra_profile_id = self.get_id_using_attr_name_else_fail(
                    "ipv6_ndra_profile", nsx_resource_params,
                    IPV6_NDRA_PROFILE_URL, "Ipv6NdraProfile")
            ipv6_profile_paths.append(
                IPV6_NDRA_PROFILE_URL + "/" + ipv6_ndra_profile_id)
        if self.do_resource_params_have_attr_with_id_or_display_name(
                "ipv6_dad_profile"):
            ipv6_dad_profile_id = self.get_id_using_attr_name_else_fail(
                    "ipv6_dad_profile", nsx_resource_params,
                    IPV6_DAD_PROFILE_URL, "Ipv6DadProfile")
            ipv6_profile_paths.append(
                IPV6_DAD_PROFILE_URL + "/" + ipv6_dad_profile_id)
        if ipv6_profile_paths:
            nsx_resource_params["ipv6_profile_paths"] = ipv6_profile_paths

        if self.do_resource_params_have_attr_with_id_or_display_name(
                "dhcp_config"):
            dhcp_config_id = self.get_id_using_attr_name_else_fail(
                "dhcp_config", nsx_resource_params,
                DHCP_RELAY_CONFIG_URL, "DhcpRelayConfig")
            nsx_resource_params["dhcp_config_paths"] = [
                DHCP_RELAY_CONFIG_URL + "/" + dhcp_config_id]

        if self.do_resource_params_have_attr_with_id_or_display_name(
                "tier0"):
            tier0_id = self.get_id_using_attr_name_else_fail(
                "tier0", nsx_resource_params,
                TIER_0_URL, "Tier0")
            nsx_resource_params["tier0_path"] = (
                TIER_0_URL + "/" + tier0_id)

    def update_parent_info(self, parent_info):
        parent_info["tier1_id"] = self.id

    class NSXTTier1StaticRoutes(NSXTBaseRealizableResource):
        def get_spec_identifier(self):
            return NSXTTier1.NSXTTier1StaticRoutes.get_spec_identifier()

        @classmethod
        def get_spec_identifier(cls):
            return "static_routes"

        @staticmethod
        def get_resource_spec():
            tier1_sr_arg_spec = {}
            tier1_sr_arg_spec.update(
                network=dict(
                    required=True,
                    type='str'
                ),
                next_hops=dict(
                    required=True,
                    type='list',
                    elements='dict',
                    options=dict(
                        admin_distance=dict(
                            type='int',
                            default=1
                        ),
                        ip_address=dict(
                            type='str'
                        ),
                        scope=dict(
                            type='list',
                            elements='str'
                        )
                    )
                ),
            )
            return tier1_sr_arg_spec

        @staticmethod
        def get_resource_base_url(parent_info):
            tier1_id = parent_info.get("tier1_id", 'default')
            return TIER_1_STATIC_ROUTE_URL.format(tier1_id)

    class NSXTTier1LocaleService(NSXTBaseRealizableResource):
        def get_spec_identifier(self):
            return NSXTTier1.NSXTTier1LocaleService.get_spec_identifier()

        @classmethod
        def get_spec_identifier(cls):
            return "locale_services"

        def infer_resource_id(self, parent_info):
            all_locale_services = self.get_all_resources_from_nsx()
            if len(all_locale_services) == 0:
                self.module.fail_json(
                    msg="No {} found under Tier1 gateway {}. Please specify "
                        "the id or display_name of the LocaleService to be "
                        "created".format(
                            self.get_spec_identifier(),
                            parent_info.get("tier1_id", 'default')))
            if len(all_locale_services) > 1:
                ls_ids = [ls['id'] for ls in all_locale_services]
                self.module.fail_json(
                    msg="Multiple {} found under Tier1 gateway {} with IDs "
                        "{}. Please specify the id of the LocaleService "
                        "to be updated".format(
                            self.get_spec_identifier(),
                            parent_info.get("tier1_id", 'default'), ls_ids))
            return all_locale_services[0]['id']

        @staticmethod
        def get_resource_spec():
            tier1_ls_arg_spec = {}
            tier1_ls_arg_spec.update(
                edge_cluster_info=dict(
                    required=False,
                    type='dict',
                    options=dict(
                        # Note that only default site_id and
                        # enforcementpoint_id are used
                        site_id=dict(
                            type='str',
                            default="default"
                        ),
                        enforcementpoint_id=dict(
                            type='str',
                            default="default"
                        ),
                        edge_cluster_id=dict(
                            type='str'
                        ),
                        edge_cluster_display_name=dict(
                            type='str'
                        )
                    )
                ),
                preferred_edge_nodes_info=dict(
                    required=False,
                    type='list',
                    options=dict(
                        # Note that only default site_id and
                        # enforcementpoint_id are used
                        site_id=dict(
                            type='str',
                            default="default"
                        ),
                        enforcementpoint_id=dict(
                            type='str',
                            default="default"
                        ),
                        edge_cluster_id=dict(
                            type='str'
                        ),
                        edge_cluster_display_name=dict(
                            type='str'
                        ),
                        edge_node_id=dict(
                            type='str'
                        ),
                        edge_node_display_name=dict(
                            type='str'
                        )
                    )
                ),
                route_redistribution_types=dict(
                    required=False,
                    type='list',
                    elements='str',
                ),
                route_redistribution_config=dict(
                    type='dict',
                    required=False,
                    options=dict(
                        bgp_enabled=dict(
                            type='bool',
                            default=False
                        ),
                        redistribution_rules=dict(
                            type='list',
                            required=False,
                            elements='dict',
                            options=dict(
                                name=dict(
                                    type='str',
                                    required=False
                                ),
                                route_map_path=dict(
                                    type='str',
                                    required=False
                                ),
                                route_redistribution_types=dict(
                                    type='list',
                                    elements='str',
                                    required=False
                                ),
                            )
                        )
                    )
                ),
                ha_vip_configs=dict(
                    type='list',
                    elements='dict',
                    options=dict(
                        enabled=dict(
                            default=True,
                            type='bool'
                        ),
                        external_interface_info=dict(
                            required=True,
                            type='list',
                            elements='dict',
                            options=dict(
                                tier0_id=dict(
                                    type='str',
                                ),
                                tier0_display_name=dict(
                                    type='str',
                                ),
                                tier0_ls_id=dict(
                                    type='str',
                                ),
                                tier0_ls_display_name=dict(
                                    type='str',
                                ),
                                tier0_ls_interface_id=dict(
                                    type='str',
                                ),
                                tier0_ls_interface_display_name=dict(
                                    type='str',
                                ),
                                external_interface_path=dict(
                                    type='str'
                                )
                            )
                        ),
                        vip_subnets=dict(
                            type='list',
                            elements='dict',
                            required=True,
                            options=dict(
                                ip_addresses=dict(
                                    type='list',
                                    required=True
                                ),
                                prefix_len=dict(
                                    type='int',
                                    rqeuired=True
                                )
                            )
                        ),
                    )
                )
            )
            return tier1_ls_arg_spec

        @staticmethod
        def get_resource_base_url(parent_info):
            tier1_id = parent_info.get("tier1_id", 'default')
            return TIER_1_LOCALE_SERVICE_URL.format(tier1_id)

        def update_resource_params(self, nsx_resource_params):
            if "edge_cluster_info" in nsx_resource_params:
                edge_cluster_info = nsx_resource_params.pop(
                    "edge_cluster_info")
                site_id = edge_cluster_info["site_id"]
                enforcementpoint_id = edge_cluster_info["enforcementpoint_id"]
                edge_cluster_base_url = (
                    EDGE_CLUSTER_URL.format(site_id, enforcementpoint_id))
                edge_cluster_id = self.get_id_using_attr_name_else_fail(
                    "edge_cluster", edge_cluster_info, edge_cluster_base_url,
                    "Edge Cluster")
                nsx_resource_params["edge_cluster_path"] = (
                    edge_cluster_base_url + "/" + edge_cluster_id)

            if "preferred_edge_nodes_info" in nsx_resource_params:
                preferred_edge_nodes_info = nsx_resource_params.pop(
                    "preferred_edge_nodes_info")
                nsx_resource_params["preferred_edge_paths"] = []
                for preferred_edge_node_info in preferred_edge_nodes_info:
                    site_id = preferred_edge_node_info.get(
                        "site_id", "default")
                    enforcementpoint_id = preferred_edge_node_info.get(
                        "enforcementpoint_id", "default")
                    edge_cluster_base_url = (
                        EDGE_CLUSTER_URL.format(site_id, enforcementpoint_id))
                    edge_cluster_id = self.get_id_using_attr_name_else_fail(
                        "edge_cluster", preferred_edge_node_info,
                        edge_cluster_base_url, 'Edge Cluster')
                    edge_node_base_url = EDGE_NODE_URL.format(
                        site_id, enforcementpoint_id, edge_cluster_id)
                    edge_node_id = self.get_id_using_attr_name_else_fail(
                        "edge_node", preferred_edge_node_info,
                        edge_node_base_url, "Edge Node")
                    nsx_resource_params["preferred_edge_paths"].append(
                        edge_node_base_url + "/" + edge_node_id)

            if 'ha_vip_configs' in nsx_resource_params:
                for ha_vip_config in nsx_resource_params['ha_vip_configs']:
                    external_interface_info = ha_vip_config.pop(
                        'external_interface_info')
                    external_interface_paths = []
                    for external_interface in (
                            external_interface_info):
                        external_interface_path = external_interface.get(
                            'external_interface_path')
                        if not external_interface_path:
                            tier0_id = self.get_id_using_attr_name_else_fail(
                                'tier0', external_interface, TIER_0_URL,
                                "Tier 0")
                            tier0_ls_id = (
                                self.get_id_using_attr_name_else_fail(
                                    'tier0_ls', external_interface,
                                    TIER_0_LOCALE_SERVICE_URL,
                                    "Tier 0 Locale Service"))
                            tier0_ls_inf_id = (
                                self.get_id_using_attr_name_else_fail(
                                    'tier0_ls_interface', external_interface,
                                    TIER_0_LS_INTERFACE_URL,
                                    "Tier 0 Interface"))
                            external_interface_path = (
                                TIER_0_LS_INTERFACE_URL.format(
                                    tier0_id, tier0_ls_id) + "/" +
                                tier0_ls_inf_id)
                        external_interface_paths.append(
                            external_interface_path)
                    ha_vip_config[
                        'external_interface_paths'] = external_interface_paths

        def update_parent_info(self, parent_info):
            parent_info["ls_id"] = self.id

        class NSXTTier1Interface(NSXTBaseRealizableResource):
            def get_spec_identifier(self):
                return (NSXTTier1.NSXTTier1LocaleService.NSXTTier1Interface
                        .get_spec_identifier())

            @classmethod
            def get_spec_identifier(cls):
                return "interfaces"

            @staticmethod
            def get_resource_spec():
                tier1_ls_int_arg_spec = {}
                tier1_ls_int_arg_spec.update(
                    ipv6_ndra_profile_id=dict(
                        required=False,
                        type='str'
                    ),
                    mtu=dict(
                        type='int'
                    ),
                    segment_id=dict(
                        required=False,
                        type='str'
                    ),
                    segment_display_name=dict(
                        required=False,
                        type='str'
                    ),
                    subnets=dict(
                        required=True,
                        type='list',
                        elements='dict',
                        options=dict(
                            ip_addresses=dict(
                                type='list',
                                elements='str'
                            ),
                            prefix_len=dict(
                                type='int'
                            )
                        )
                    ),
                    urpf_mode=dict(
                        type='str',
                        default='STRICT',
                        choices=['NONE', 'STRICT']
                    )
                )
                return tier1_ls_int_arg_spec

            @staticmethod
            def get_resource_base_url(parent_info):
                tier1_id = parent_info.get("tier1_id", 'default')
                locale_service_id = parent_info.get("ls_id", 'default')
                return TIER_1_LS_INTERFACE_URL.format(
                    tier1_id, locale_service_id)

            def update_resource_params(self, nsx_resource_params):
                # segment_id is a required attr
                segment_id = self.get_id_using_attr_name_else_fail(
                    "segment", nsx_resource_params, SEGMENT_URL, "Segment")
                nsx_resource_params["segment_path"] = (
                    SEGMENT_URL + "/" + segment_id)

                if self.do_resource_params_have_attr_with_id_or_display_name(
                        "ipv6_ndra_profile"):
                    ipv6_ndra_profile_id = (
                        self.get_id_using_attr_name_else_fail(
                            "ipv6_ndra_profile", nsx_resource_params,
                            IPV6_NDRA_PROFILE_URL, "Ipv6 NDRA Profile"))
                    nsx_resource_params["ipv6_profile_paths"] = [
                        IPV6_NDRA_PROFILE_URL + "/" + ipv6_ndra_profile_id]


if __name__ == '__main__':
    nsxt_tier1 = NSXTTier1()
    nsxt_tier1.realize()
