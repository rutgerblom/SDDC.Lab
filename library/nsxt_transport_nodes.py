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
module: nsxt_transport_nodes
short_description: Create a Transport Node
description: Transport nodes are hypervisor hosts and NSX Edges that will participate
              in an NSX-T overlay. For a hypervisor host, this means that it hosts
              VMs that will communicate over NSX-T logical switches. For NSX Edges,
              this means that it will have logical router uplinks and downlinks.

              This API creates transport node for a host node (hypervisor) or edge node
              (router) in the transport network.

              When you run this command for a host, NSX Manager attempts to install the
              NSX kernel modules, which are packaged as VIB, RPM, or DEB files. For the
              installation to succeed, you must provide the host login credentials and the
              host thumbprint.

              To get the ESXi host thumbprint, SSH to the host and run the
              <b>openssl x509 -in /etc/vmware/ssl/rui.crt -fingerprint -sha256 -noout</b>
              command.

              To generate host key thumbprint using SHA-256 algorithm please follow the
              steps below.

              Log into the host, making sure that the connection is not vulnerable to a
              man in the middle attack. Check whether a public key already exists.
              Host public key is generally located at '/etc/ssh/ssh_host_rsa_key.pub'.
              If the key is not present then generate a new key by running the following
              command and follow the instructions.

              <b>ssh-keygen -t rsa</b>

              Now generate a SHA256 hash of the key using the following command. Please
              make sure to pass the appropriate file name if the public key is stored with
              a different file name other than the default 'id_rsa.pub'.

              <b>awk '{print $2}' id_rsa.pub | base64 -d | sha256sum -b | sed 's/ .*$//' | xxd -r -p | base64</b>
              This api is deprecated as part of FN+TN unification. Please use Transport Node API
              to install NSX components on a node.

              Additional documentation on creating a transport node can be found
              in the NSX-T Installation Guide.

              In order for the transport node to forward packets,
              the host_switch_spec property must be specified.

              Host switches (called bridges in OVS on KVM hypervisors) are the
              individual switches within the host virtual switch. Virtual machines
              are connected to the host switches.

              When creating a transport node, you need to specify if the host switches
              are already manually preconfigured on the node, or if NSX should create
              and manage the host switches. You specify this choice by the type
              of host switches you pass in the host_switch_spec property of the
              TransportNode request payload.

              For a KVM host, you can preconfigure the host switch, or you can have
              NSX Manager perform the configuration. For an ESXi host or NSX Edge
              node, NSX Manager always configures the host switch.

              To preconfigure the host switches on a KVM host, pass an array
              of PreconfiguredHostSwitchSpec objects that describes those host
              switches. In the current NSX-T release, only one prefonfigured host
              switch can be specified.  See the PreconfiguredHostSwitchSpec schema
              definition for documentation on the properties that must be provided.
              Preconfigured host switches are only supported on KVM hosts, not on
              ESXi hosts or NSX Edge nodes.

              To allow NSX to manage the host switch configuration on KVM hosts,
              ESXi hosts, or NSX Edge nodes, pass an array of StandardHostSwitchSpec
              objects in the host_switch_spec property, and NSX will automatically
              create host switches with the properties you provide. In the current
              NSX-T release, up to 5 host switches can be automatically managed.
              See the StandardHostSwitchSpec schema definition for documentation on
              the properties that must be provided.

              Note: previous versions of NSX-T used a property named host_switches
              to specify the host switch configuration on the transport node. That
              property is deprecated, but still functions. You should configure new
              host switches using the host_switch_spec property.

              The request should either provide node_deployement_info or node_id.

              If the host node (hypervisor) or edge node (router) is already added in
              system then it can be converted to transport node by providing node_id in
              request.

              If host node (hypervisor) or edge node (router) is not already present in
              system then information should be provided under node_deployment_info.

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
        description: Description of this resource
        required: False
        type: str
    resource_type:
        description: Must be set to the value TransportNode
        required: False
        type: str
    host_switch_spec:
        description: 'This property is used to either create standard host switches
                      or to inform NSX about preconfigured host switches that already
                      exist on the transport node.
                      Pass an array of either StandardHostSwitchSpec objects or
                      PreconfiguredHostSwitchSpec objects. It is an error to pass
                      an array containing different types of HostSwitchSpec objects.'
        host_switches:
            description: This property is deprecated in favor of 'host_switch_spec'. Property
                          'host_switches' can only be used for NSX managed transport nodes. 
                          'host_switch_spec' can be used for both NSX managed or manually 
                          preconfigured host switches.
            required: true
            type: array of PreconfiguredHostSwitch
        required: false
        resource_type:
            description: Selects the type of the transport zone profile
            required: true
            type: str
        type: dict
    maintenance_mode:
        description: The property is read-only, used for querying result. User could update
                      transport node maintenance mode by UpdateTransportNodeMaintenanceMode call.
        required: false
        type: str
    node_deployment_info:
        allocation_list:
            description: List of logical router ids to which this edge node is allocated.
            required: false
            type: list
        deployment_config:
            description: 'When this configuration is specified, edge fabric node of deployment_type
                          VIRTUAL_MACHINE will be deployed and registered with MP.'
            form_factor:
                description: Supported edge form factor.
                required: false
                type: str
            node_user_settings:
                audit_password:
                    description: "Password for the node audit user. For deployment, this property
                                  is required. After deployment, this property is ignored, and
                                  the node cli must be used to change the password. The password 
                                  specified must be at least 12 characters in length and must 
                                  contain at least one lowercase, one uppercase, one numeric 
                                  character and one special character (except quotes)."
                    required: false
                    type: str
                audit_username:
                    description: "The default username is \"audit\". To configure username, you
                                  must provide this property together with <b>audit_password</b>."
                    required: false
                    type: str
                cli_password:
                    description: "Password for the node cli user. For deployment, this property
                                  is required. After deployment, this property is ignored, and 
                                  the node cli must be used to change the password. The password 
                                  specified must be at least 12 characters in length and must 
                                  contain at least one lowercase, one uppercase, one numeric 
                                  character and one special character (except quotes)."
                    required: false
                    type: str
                cli_username:
                    description: "To configure username, you must provide this property together 
                                  with <b>cli_password</b>."
                    required: false
                    type: str
                description: "Username and password settings for the node. Note - these settings
                             will be honored only during node deployment. Post deployment, CLI 
                             must be used for changing the user settings, changes to these 
                             parameters will not have any effect."
                required: true
                root_password:
                    description: "Password for the node root user. For deployment, this property
                                 is required. After deployment, this property is ignored, and the
                                 node cli must be used to change the password. The password 
                                 specified must be at least 12 characters in length and must 
                                 contain at least one lowercase, one uppercase, one numeric 
                                 character and one special character (except quotes)."
                    required: false
                    type: str
                type: dict
            required: false
            type: dict
            vm_deployment_config:
                allow_ssh_root_login:
                    description: 'If true, the root user will be allowed to log into the VM.
                                  Allowing root SSH logins is not recommended for security 
                                  reasons.'
                    required: false
                    type: boolean
                compute:
                    description: 'The cluster node VM will be deployed on the specified cluster
                                  or resourcepool for specified VC server. If vc_username and 
                                  vc_password are present then this field takes name else id.'
                    required: true
                    type: str
                data_networks:
                    description: "List of distributed portgroup or VLAN logical identifiers or names to
                       which the datapath serving vnics of edge node vm will be connected. If vc_username 
                      and vc_password are present then this field takes names else id."
                    required: true
                    type: list
                default_gateway_addresses:
                    description: 'The default gateway for the VM to be deployed must be specified
                                  if all the other VMs it communicates with are not in the same subnet.
                                  Do not specify this field and management_port_subnets to use DHCP.
                        
                                  Note: only single IPv4 default gateway address is supported and it
                                  must belong to management network.
                        
                                  IMPORTANT: VMs deployed using DHCP are currently not supported,
                                  so this parameter should be specified.'
                    required: false
                    type: list
                description: VM Deployment Configuration
                dns_servers:
                    description: 'List of DNS servers.
                                  If DHCP is used, the default DNS servers associated with
                                  the DHCP server will be used instead.
                                  Required if using static IP.'
                    required: false
                    type: list
                enable_ssh:
                    description: 'If true, the SSH service will automatically be started on the
                                  VM. Enabling SSH service is not recommended for security 
                                  reasons.'
                    required: false
                    type: boolean
                host:
                    description: "Name of the host where edge VM is to be deployed
                                  if vc_username and vc_password are present then
                                  this field takes host name else host id."
                    required: false
                    type: str
                hostname:
                    description: Desired host name/FQDN for the VM to be deployed
                    required: true
                    type: str
                management_network:
                    description: 'Distributed portgroup identifier to which the management vnic
                                  of cluster node VM will be connected. If vc_username and vc_password 
                                  are present then this field takes name else id.'
                    required: true
                    type: str
                management_port_subnets:
                    description: 'IP Address and subnet configuration for the management port.
                                  Do not specify this field and default_gateway_addresses to
                                  use DHCP.
                        
                                  Note: only one IPv4 address is supported for the management 
                                  port.
                        
                                  IMPORTANT: VMs deployed using DHCP are currently not supported,
                                  so this parameter should be specified.'
                    required: false
                    type: array of IPSubnet
                ntp_servers:
                    description: 'List of NTP servers.
                      To use hostnames, a DNS server must be defined. If not using DHCP,
                      a DNS server should be specified under dns_servers.'
                    required: false
                    type: list
                placement_type:
                    description: "Specifies the config for the platform through which to deploy
                       the VM"
                    required: true
                    type: str
                required: true
                search_domains:
                    description: 'List of domain names that are used to complete unqualified host
                                  names.'
                    required: false
                    type: list
                storage:
                    description: Moref or name of the datastore in VC. If it is to be taken from 'Agent
                                 VM Settings', then it should be empty If vc_username and vc_password are present then
                                  this field takes name else id.
                    required: true
                    type: str
                type: dict
                vc_name:
                    description: 'The VC-specific names will be resolved on this VC, so all
                                  other identifiers specified in the config must belong to this vCenter 
                                  server.'
                    required: true
                    type: str
                vc_username:
                    description: 'Username of VC'
                    required: false
                    type: str
                vc_password:
                    description: 'VC Password'
                    required: false
                    type: str
                reservation_info:
                    description: 'Resource reservation for memory and CPU resources'
                    required: false
                    type: dict
                    cpu_reservation:
                        description: 'Guaranteed minimum allocation of CPU resources'
                        required: false
                        type: dict
                        reservation_in_mhz:
                            description: 'GCPU resevation in mhz'
                            required: false
                            type: int
                        reservation_in_shares:
                            description: 'CPU reservation in shares'
                            required: false
                            type: str
                    memory_reservation:
                        description: 'Guaranteed minimum allocation of memory resources'
                        required: false
                        type: dict
                        reservation_percentage:
                            description: 'Memory reservation percentage'
                            required: false
                            type: int
                resource_allocation:
                    description: 'Resource reservation settings'
                    required: false
                    type: dict'
                    cpu_count:
                        description: 'CPU count'
                        required: false
                        type: int
                    memory_allocation_in_mb:
                        description: 'Memory allocation in MB'
                        required: false
                        type: int

        deployment_type:
            description: Specifies whether the service VM should be deployed on each host such
                          that it provides partner service locally on the host, or whether the 
                          service VMs can be deployed as a cluster. If deployment_type is 
                          CLUSTERED, then the clustered_deployment_count should be provided.
            required: false
            type: str
        description: None
        discovered_ip_addresses:
            description: Discovered IP Addresses of the fabric node, version 4 or 6
            required: false
            type: list
        discovered_node_id:
            description: Id of discovered node which was converted to create this node
            required: false
            type: str
        external_id:
            description: Current external id of this virtual machine in the system.
            required: false
            type: str
        fqdn:
            description: Domain name the entity binds to
            required: false
            type: str
        host_credential:
            description: Login credentials for the host
            password:
                description: Password for the user (optionally specified on PUT, unspecified
                  on GET)
                required: false
                type: str
            required: false
            thumbprint:
                description: Hexadecimal SHA256 hash of the vIDM server's X.509 certificate
                required: false
                type: str
            type: dict
            username:
                description: Username value of the log
                required: false
                type: str
        ip_addresses:
            description: Interface IP addresses
            required: false
            type: array of IPv4Address
        managed_by_server:
            description: The id of the vCenter server managing the ESXi type HostNode
            required: false
            type: str
        os_type:
            description: OS type of the discovered node
            required: true
            type: str
        os_version:
            description: OS version of the discovered node
            required: false
            type: str
        required: false
        resource_type:
            description: Selects the type of the transport zone profile
            required: true
            type: str
        type: dict
    remote_tunnel_endpoint:
        description: Configuration for a remote tunnel endpoin
        required: False 
        type: 'dict'
        host_switch_name:
            description: The host switch name to be used for the remote tunnel endpoint
            required: True
            type: 'str'
        named_teaming_policy:
            description: The named teaming policy to be used by the remote tunnel endpoint
            required: False
            type:'str'
        rtep_vlan:
            description: VLAN id for remote tunnel endpoint
            required:True
            type:'dict'
            VlanID:
                description: Virtual Local Area Network Identifier
                required:False
                type:'int'
        ip_assignment_spec:
            description: Specification for IPs to be used with host switch remote tunnel endpoints
            required:True
            type:'dict'
            resource_type:
                description: Resource type
                required:True
                type:'str'
            ip_pool_id:
                description: IP pool id
                required:False
                type:'str'
            ip_list:
                description: List of IPs for transport node host switch virtual tunnel endpoints
                required:False
                type:'list'
            ip_mac_list:
                description: List of IPs and MACs for transport node host switch virtual tunnel endpoints 
                required:False
                type:'list'
            default_gateway:
                description: Default gateway
                required:False
                type:'dict'
                IPAddress:
                    description: IPv4 or IPv6 address
                    required:False
                    type:'str'
            subnet_mask:
                description: Subnet mask
                required:False
                type:'dict'
                IPAddress:
                    description: IPv4 IPv6 address
                    required:False
                    type:'str'
    tags: 
        description: Opaque identifiers meaningful to the API user
        required: False
        type: array of Tag
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
        required: false
        type: array of TransportZoneEndPoint
    
'''

EXAMPLES = '''
- name: Create transport node
  nsxt_transport_nodes:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    resource_type: "TransportNode"
    display_name: "NSX Configured TN"
    description: "NSX configured Test Transport Node"
    host_switch_spec:
      resource_type: "StandardHostSwitchSpec"
      host_switches:
      - host_switch_profiles:
        - name: "uplinkProfile1"
          type: "UplinkHostSwitchProfile"
        host_switch_name: "hostswitch1"
        pnics:
        - device_name: "vmnic1"
          uplink_name: "uplink-1"
        ip_assignment_spec:
          resource_type: "StaticIpPoolSpec"
          ip_pool_name: "IPPool-IPV4-1"
        transport_zone_endpoints:
        - transport_zone_name: "TZ1"
    node_deployment_info:
      resource_type: "HostNode"
      display_name: "Host_1"
      ip_addresses: ["10.149.55.21"]
      os_type: "ESXI"
      os_version: "6.5.0"
      host_credential:
        username: "root"
        password: "ca$hc0w"
        thumbprint: "e7fd7dd84267da10f991812ca62b2bedea3a4a62965396a04728da1e7f8e1cb9"
    state: "present"

'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request, get_vc_ip_from_display_name
from ansible.module_utils.vcenter_utils import get_resource_id_from_name, get_data_network_id_from_name
from ansible.module_utils._text import to_native
import socket
import hashlib
import ssl

FAILED_STATES = ["failed"]
IN_PROGRESS_STATES = ["pending", "in_progress"]
SUCCESS_STATES = ["partial_success", "success", "NODE_READY"]

def get_transport_node_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_transport_nodes(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/transport-nodes', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing transport nodes. Error [%s]' % (to_native(err)))
    return resp

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

def get_tn_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    transport_nodes = get_transport_nodes(module, manager_url, mgr_username, mgr_password, validate_certs)
    for transport_node in transport_nodes['results']:
        if transport_node.__contains__('display_name') and transport_node['display_name'] == display_name:
            return transport_node
    return None

def wait_till_create(node_id, module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      count = 0;
      while True:
          (rc, resp) = request(manager_url+ '/transport-nodes/%s/state'% node_id, headers=dict(Accept='application/json'),
                        url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
          if any(resp['state'] in progress_status for progress_status in IN_PROGRESS_STATES) and \
          any(resp['node_deployment_state']['state'] in progress_status for progress_status in IN_PROGRESS_STATES):
              time.sleep(10)
              count = count + 1
              if count == 90:
                  #Wait for max 15 minutes for host to realize
                  module.fail_json(msg= 'Error creating transport node: creation state %s, node_deployment_state %s, Failure message: %s'%(str(resp['state']), str(resp['node_deployment_state']['state']), str(resp['failure_message'])))
          elif any(resp['state'] in progress_status for progress_status in SUCCESS_STATES) and\
          any(resp['node_deployment_state']['state'] in progress_status for progress_status in SUCCESS_STATES):
              time.sleep(5)
              return
          elif any(resp['state'] in progress_status for progress_status in FAILED_STATES) or\
          any(resp['node_deployment_state']['state'] in progress_status for progress_status in FAILED_STATES):
              module.fail_json(msg= 'Error creating transport node: creation state %s, node_deployment_state %s'%(str(resp['state']), str(resp['node_deployment_state']['state'])))
          else:
              time.sleep(10)
              count = count + 1
              if count == 90:
                   module.fail_json(msg= 'Error creating transport node: creation state %s, node_deployment_state %s'%(str(resp['state']), str(resp['node_deployment_state']['state'])))
    except Exception as err:
      module.fail_json(msg='Error accessing transport node. Error [%s]' % (to_native(err)))

def wait_till_delete(vm_id, module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      while True:
          (rc, resp) = request(manager_url+ '/transport-nodes/%s/state'% vm_id, headers=dict(Accept='application/json'),
                        url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
          time.sleep(10)
    except Exception as err:
      time.sleep(5)
      return

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

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_params ):
    if transport_node_params.__contains__('host_switch_spec'):
        for host_switch in transport_node_params['host_switch_spec']['host_switches']:
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
            if host_switch.__contains__('ip_assignment_spec') and host_switch['ip_assignment_spec']['resource_type'] == 'StaticIpPoolSpec':
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
                for network in host_switch['vmk_install_migration']:
                    if network.__contains__('destination_network'):
                        network['destination_network'] = get_id_from_display_name (module, manager_url, mgr_username,
                                                                                   mgr_password, validate_certs,
                                                                                   "/logical-switches", network['destination_network'])

    if transport_node_params.__contains__('transport_zone_endpoints'):
        for transport_zone_endpoint in transport_node_params['transport_zone_endpoints']:
            transport_zone_name = transport_zone_endpoint.pop('transport_zone_name', None)
            transport_zone_endpoint['transport_zone_id'] = get_id_from_display_name (module, manager_url,
                                                                                    mgr_username, mgr_password, validate_certs,
                                                                                    "/transport-zones", transport_zone_name)
    if transport_node_params.__contains__('node_deployment_info') and transport_node_params['node_deployment_info'].__contains__('resource_type') and transport_node_params['node_deployment_info']['resource_type'] == 'EdgeNode':
        vc_name = transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('vc_name', None)
        transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['vc_id'] = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                    "/fabric/compute-managers", vc_name)

    transport_node_params['display_name'] = transport_node_params.pop('display_name', None)
    return transport_node_params

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

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_with_ids):
    existing_transport_node = get_tn_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_with_ids['display_name'])
    
    if existing_transport_node is None:
        return False
    if not existing_transport_node.__contains__('description') and transport_node_with_ids.__contains__('description'):
        return True
    if existing_transport_node.__contains__('description') and transport_node_with_ids.__contains__('description') and existing_transport_node['description'] != transport_node_with_ids['description']:
        return True
    if existing_transport_node.__contains__('description') and not transport_node_with_ids.__contains__('description'):
        return True
    if transport_node_with_ids.__contains__('host_switch_spec') and transport_node_with_ids['host_switch_spec'].__contains__('host_switches'):
        existing_host_switches = existing_transport_node['host_switch_spec']['host_switches']
        sorted_existing_host_switches = sorted(existing_host_switches, key = lambda i: i['host_switch_name'])
        sorted_new_host_switches = sorted(transport_node_with_ids['host_switch_spec']['host_switches'], key = lambda i: i['host_switch_name'])
        if len(sorted_existing_host_switches) != len(sorted_new_host_switches):
           return True
        for i in range(len(sorted_existing_host_switches)):
           diff_obj = {k: sorted_existing_host_switches[i][k] for k in sorted_existing_host_switches[i] if k in sorted_new_host_switches[i] and sorted_existing_host_switches[i][k] != sorted_new_host_switches[i][k]}
           if not cmp_dict(diff_obj, sorted_new_host_switches[i]):
              return True
    return False

def get_api_cert_thumbprint(ip_address, module):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    wrappedSocket = ssl.wrap_socket(sock)
    try:
        wrappedSocket.connect((ip_address, 443))
    except Exception as err:
        module.fail_json(msg='Failed to get node ID from ESXi host with IP {}. Error: {}'.format(ip_address, err))
    else:
        der_cert_bin = wrappedSocket.getpeercert(True)
        thumb_sha256 = hashlib.sha256(der_cert_bin).hexdigest()
        return thumb_sha256
    finally:
        wrappedSocket.close()


def inject_vcenter_info(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_params):
  '''
  params:
  - transport_node_params: These are the transport node parameters passed from playbook file
  result:
  - takes the vecenter parameters accepted by playbook and converts it into the form accepted
    by transport node api using pyvmomi functions.
  '''
  vm_deployment_config = transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']
      
  if vm_deployment_config.__contains__('vc_username') and vm_deployment_config.__contains__('vc_password'):
    vc_name = vm_deployment_config['vc_name']
    vc_ip = get_vc_ip_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                                         "/fabric/compute-managers", vc_name)
    
        
    vc_username = transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('vc_username', None)
        
    vc_password = transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('vc_password', None)

    if vm_deployment_config.__contains__('host'):
      host = vm_deployment_config.pop('host', None)
      host_id = get_resource_id_from_name(module, vc_ip, vc_username, vc_password, 
                                    'host', host)
      transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['host_id'] = str(host_id)
        
    storage = vm_deployment_config.pop('storage')
    storage_id = get_resource_id_from_name(module, vc_ip, vc_username, vc_password, 
                                           'storage', storage)
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['storage_id'] = str(storage_id)

    cluster = vm_deployment_config.pop('compute')
    cluster_id = get_resource_id_from_name(module, vc_ip, vc_username, vc_password, 
                                           'cluster', cluster)
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['compute_id'] = str(cluster_id)

    management_network = vm_deployment_config.pop('management_network')
    management_network_id = get_resource_id_from_name(module, vc_ip, vc_username, vc_password, 
                                               'network', management_network)
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['management_network_id'] = str(management_network_id)

    data_networks = vm_deployment_config.pop('data_networks')
    data_network_ids = get_data_network_id_from_name(module, vc_ip, vc_username, vc_password, 
                                                data_networks)
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['data_network_ids'] = data_network_ids
        
    if vm_deployment_config.__contains__('host'):
      transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('host', None)
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('cluster', None)
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('storage', None)
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('management_network', None)
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('data_networks', None)
  else:
    if vm_deployment_config.__contains__('host'):
      host_id = transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('host', None)
      transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['host_id'] = host_id
        
    cluster_id = transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('compute', None)
    storage_id = transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('storage', None)
    management_network_id = transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('management_network', None)
    data_network_ids = transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config'].pop('data_networks', None)
        
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['compute_id'] = cluster_id
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['storage_id'] = storage_id
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['management_network_id'] = management_network_id
    transport_node_params['node_deployment_info']['deployment_config']['vm_deployment_config']['data_network_ids'] = data_network_ids


def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                       description=dict(required=False, type='str'),
                       host_switch_spec=dict(required=False, type='dict',
                       host_switches=dict(required=True, type='list'),
                       resource_type=dict(required=True, type='str')),
                       node_deployment_info=dict(required=False, type='dict',
                       discovered_node_id=dict(required=False, type='str'),
                       deployment_config=dict(required=False, type='dict',
                       node_user_settings=dict(required=True, type='dict',
                       cli_username=dict(required=False, type='str'),
                       audit_username=dict(required=False, type='str'),
                       root_password=dict(required=False, type='str', no_log=True),
                       cli_password=dict(required=False, type='str', no_log=True),
                       audit_password=dict(required=False, type='str', no_log=True)),
                       vm_deployment_config=dict(required=True, type='dict',
                       data_networks=dict(required=True, type='list'),
                       dns_servers=dict(required=False, type='list'),
                       ntp_servers=dict(required=False, type='list'),
                       management_network=dict(required=True, type='str'),
                       vc_username=dict(required=False, type='str'),
                       vc_password=dict(required=False, type='str', no_log=True),
                       enable_ssh=dict(required=False, type='boolean'),
                       allow_ssh_root_login=dict(required=False, type='boolean'),
                       placement_type=dict(required=True, type='str'),
                       compute=dict(required=True, type='str'),
                       search_domains=dict(required=False, type='list'),
                       vc_name=dict(required=True, type='str'),
                       storage=dict(required=True, type='str'),
                       default_gateway_addresses=dict(required=False, type='list'),
                       management_port_subnets=dict(required=False, type='list'),
                       host=dict(required=False, type='str'),
                       hostname=dict(required=True, type='str'),
                       reservation_info=dict(required=False, type='dict',
                       cpu_reservation=dict(required=False, type='dict',
                       reservation_in_mhz=dict(required=False, type='int'),
                       reservation_in_shares=dict(required=False, type='str')),
                       memory_reservation=dict(required=False, type='dict',
                       reservation_percentage=dict(required=False, type='int'))),
                       resource_allocation=dict(required=False, type='dict',
                       cpu_count=dict(required=False, type='int'),
                       memory_allocation_in_mb=dict(required=False, type='int'))),
                       form_factor=dict(required=False, type='str')),
                       discovered_ip_addresses=dict(required=False, type='list'),
                       ip_addresses=dict(required=False, type='list'),
                       fqdn=dict(required=False, type='str'),
                       os_version=dict(required=False, type='str'),
                       managed_by_server=dict(required=False, type='str'),
                       host_credential=dict(required=False, type='dict',
                       username=dict(required=False, type='str'),
                       password=dict(required=False, type='str', no_log=True),
                       thumbprint=dict(required=False, type='str')),
                       allocation_list=dict(required=False, type='list'),
                       os_type=dict(required=True, type='str'),
                       external_id=dict(required=False, type='str'),
                       resource_type=dict(required=True, type='str'),
                       deployment_type=dict(required=False, type='str')),
                       maintenance_mode=dict(required=False, type='str'),
                       remote_tunnel_endpoint=dict(required=False, type='dict',
                       host_switch_name=dict(required=True, type='str'),
                       named_teaming_policy=dict(required=False, type='str'),
                       rtep_vlan=dict(required=True, type='dict',
                       VlanID=dict(required=False, type='int')),
                       ip_assignment_spec=dict(required=True, type='dict',
                       resource_type=dict(required=True, type='str'),
                       ip_pool_id=dict(required=False, type='str'),
                       ip_list=dict(required=False, type='list'),
                       ip_mac_list=dict(required=False, type='list'),
                       default_gateway=dict(required=False, type='dict',
                       IPAddress=dict(required=False, type='str')),
                       subnet_mask=dict(required=False, type='dict',
                       IPAddress=dict(required=False, type='str')))),
                       tags=dict(required=False, type='list'),
                       transport_zone_endpoints=dict(required=False, type='list'),
                       state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  transport_node_params = get_transport_node_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  transport_node_dict = get_tn_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  transport_node_id, revision, node_deployment_revision = None, None, None
  if transport_node_dict:
    transport_node_id = transport_node_dict['id']
    revision = transport_node_dict['_revision']
    if transport_node_dict.__contains__('node_deployment_info'):
      node_deployment_revision = transport_node_dict['node_deployment_info']['_revision']

  if state == 'present':
    if transport_node_params.__contains__('node_deployment_info') and transport_node_params['node_deployment_info']['resource_type'] == 'EdgeNode':
      inject_vcenter_info(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_params)

    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    if not updated:
      # add the node
      if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(logical_switch_params)), id='12345')

      if body["node_deployment_info"].__contains__('host_credential'):
        if body["node_deployment_info"]["host_credential"].__contains__("thumbprint"):
          thumbprint = body["node_deployment_info"]["host_credential"]["thumbprint"]
        else:
          if not body["node_deployment_info"].__contains__("ip_addresses"):
            module.fail_json(msg="ESXi ip adresses are not provided")
          esxi_ip_address = body["node_deployment_info"]["ip_addresses"][0]
          thumbprint = get_api_cert_thumbprint(esxi_ip_address, module)
          body["node_deployment_info"]["host_credential"]["thumbprint"] = thumbprint
      request_data = json.dumps(body)
      try:
          if not transport_node_id:
              transport_node_id = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, '/transport-nodes', display_name, exit_if_not_found=False)
          if transport_node_id:
              module.exit_json(changed=False, id=transport_node_id, message="Transport node with display_name %s already exist."% module.params['display_name'])
          (rc, resp) = request(manager_url+ '/transport-nodes', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
           module.fail_json(msg="Failed to add transport node. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      wait_till_create(resp['node_id'], module, manager_url, mgr_username, mgr_password, validate_certs)
      time.sleep(5)
      module.exit_json(changed=True, id=resp["node_id"], body= str(resp), message="Transport node with display name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(body)), id=transport_node_id)

      body['_revision'] = revision # update current revision
      # node deployment revision is also important - node id also has a revision
      if body.__contains__('node_deployment_info') and node_deployment_revision is not None:
          body['node_deployment_info']['_revision'] = node_deployment_revision
      else:
          module.fail_json(msg="Failed to update Transport Node. Either node deployment info is not provided or "
            "node deployement revision couldn't be retrieved.")
      #update node id with tn id - as result of FN TN unification
      body['node_id'] = transport_node_id

      request_data = json.dumps(body)
      id = transport_node_id
      try:
          (rc, resp) = request(manager_url+ '/transport-nodes/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update transport node with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))

      time.sleep(5)
      module.exit_json(changed=True, id=resp["node_id"], body= str(resp), message="Transport node with node id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = transport_node_id
    if id is None:
        module.exit_json(changed=False, msg='No transport node exist with display name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(transport_node_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/transport-nodes/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete transport node with id %s. Error[%s]." % (id, to_native(err)))

    wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs)
    time.sleep(5)
    module.exit_json(changed=True, object_name=id, message="Transport node with node id %s deleted." % id)



if __name__ == '__main__':
    main()
