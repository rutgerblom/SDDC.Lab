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
module: nsxt_fabric_nodes
short_description: Register and Install NSX Components on a Node
description: Creates a host node (hypervisor) or edge node (router) in the transport
             network.

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
    action:
        description: 'PROTECT - Protect rules are defined per policy based
                      IPSec VPN session.
                      BYPASS - Bypass rules are defined per IPSec VPN
                      service and affects all policy based IPSec VPN sessions.
                      Bypass rules are prioritized over protect rules.'
        required: false
        type: str
    deployment_config:
        description: 'When this configuration is specified, edge fabric node of deployment_type
                      VIRTUAL_MACHINE will be deployed and registered with MP.'
        form_factor:
            description: Supported edge form factor.
            required: false
            type: str
        node_user_settings:
            audit_password:
                description: "Password for the node audit user. For deployment,
                              this property is required. After deployment, this property is 
                              ignored, and the node cli must be used to change the password.
                              The password specified must be at least 12 characters in length 
                              and must contain at least one lowercase, one uppercase, one 
                              numeric character and one special character (except quotes)."
                required: false
                type: str
            audit_username:
                description: "The default username is \"audit\". To configure username, you must 
                              provide this property together with <b>audit_password</b>."
                required: false
                type: str
            cli_password:
                description: "Password for the node cli user. For deployment,
                      this property is required. After deployment, this property is ignored, 
                      and the node cli must be used to change the password.
                      The password specified must be at least 12 characters in length and must
                      contain at least one lowercase, one uppercase, one numeric character and 
                      one special character (except quotes)."
                no_log: 'true'
                required: false
                type: str
            cli_username:
                description: "To configure username, you must provide this property together 
                              with <b>cli_password</b>."
                required: false
                type: str
            description: "Username and password settings for the node.
                          Note - these settings will be honored only during node deployment.
                          Post deployment, CLI must be used for changing the user settings, 
                          changes to these parameters will not have any effect."
            required: true
            root_password:
                description: "Password for the node root user. For deployment,
                      this property is required. After deployment, this property is ignored, 
                      and the node cli must be used to change the password.
                      The password specified must be at least 12 characters in length and must
                      contain at least one lowercase, one uppercase, one numeric character and 
                      one special character (except quotes)."
                no_log: 'true'
                required: false
                type: str
            type: dict
        required: false
        type: dict
        vm_deployment_config:
            allow_ssh_root_login:
                description: 'If true, the root user will be allowed to log into the VM.
                              Allowing root SSH logins is not recommended for security reasons.'
                required: false
                type: boolean
            compute_id:
                description: 'The cluster node VM will be deployed on the specified cluster or
                              resourcepool for specified VC server.'
                required: true
                type: str
            data_network_ids:
                description: "List of distributed portgroup or VLAN logical identifiers to which
                              the datapath serving vnics of edge node vm will be connected."
                required: true
                type: list
            default_gateway_addresses:
                description: 'The default gateway for the VM to be deployed must be specified
                              if all the other VMs it communicates with are not in the same 
                              subnet. Do not specify this field and management_port_subnets to 
                              use DHCP.
                              Note: only single IPv4 default gateway address is supported and it
                              must belong to management network.
                              IMPORTANT: VMs deployed using DHCP are currently not supported,
                              so this parameter should be specified.'
                required: false
                type: list
            description: 
            dns_servers:
                description: 'List of DNS servers.
                              If DHCP is used, the default DNS servers associated with
                              the DHCP server will be used instead.
                              Required if using static IP.'
                required: false
                type: list
            enable_ssh:
                description: 'If true, the SSH service will automatically be started on the VM.
                              Enabling SSH service is not recommended for security reasons.'
                required: false
                type: boolean
            host_id:
                description: "The service VM will be deployed on the specified host in the 
                              specified server within the cluster if host_id is specified.
                              Note: You must ensure that storage and specified networks are 
                              accessible by this host."
                required: false
                type: str
            hostname:
                description: Desired host name/FQDN for the VM to be deployed
                required: true
                type: str
            management_network_id:
                description: 'Distributed portgroup identifier to which the management vnic of
                              cluster node VM will be connected.'
                required: true
                type: str
            management_port_subnets:
                description: 'IP Address and subnet configuration for the management port.
                              Do not specify this field and default_gateway_addresses to use 
                              DHCP.
                              Note: only one IPv4 address is supported for the management port.
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
                description: "Specifies the config for the platform through which to deploy the VM"
                required: true
                type: str
            required: true
            search_domains:
                description: 'List of domain names that are used to complete unqualified host
                              names.'
                required: false
                type: list
            storage_id:
                description: Moref of the datastore in VC. If it is to be taken from 'Agent VM
                             Settings', then it should be empty.
                required: true
                type: str
            type: dict
            vc_name:
                description: Name of VC
                required: true
                type: str
    display_name:
        description: Display name
        required: true
        type: str
    external_id:
        description: ID of the Node maintained on the Node and used to recognize the Node
        required: false
        type: str
    host_credential:
        description: Login credentials for the host
        password:
            description: Password for the user (optionally specified on PUT, unspecified on
                         GET)
            no_log: 'true'
            required: false
            type: str
        required: false
        thumbprint:
            description: Hexadecimal SHA256 hash of the vIDM server's X.509 certificate
            no_log: 'true'
            required: false
            type: str
        type: dict
        username:
            description: Username value of the log
            required: false
            type: str
    ip_addresses:
        description: 'IP Addresses of the Node, version 4 or 6. This property is mandatory
                      for all nodes except for automatic deployment of edge virtual machine 
                      node. For automatic deployment, the ip address from
                      management_port_subnets property will be considered.'
        required: false
        type: array of IPAddress
    os_type:
        description: Hypervisor type, for example ESXi or RHEL KVM
        required: true
        type: str
    os_version:
        description: Version of the hypervisor operating system
        required: false
        type: str
    resource_type:
        choices:
        - HostNode
        - EdgeNode
        description: Fabric node type, for example 'HostNode', 'EdgeNode' or 
                     'PublicCloudGatewayNode'
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
    unprepare_host:
        description: Delete a host without uninstalling NSX components
        required: false
        type: str
'''

EXAMPLES = '''
- name: Add fabric node
  nsxt_fabric_nodes:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    resource_type: "HostNode"
    #node_id: "fefc3fed-84d9-4170-bf7c-5d7438ba91e9"
    display_name: "Host_10"
    ip_addresses: ["10.160.183.166"]
    os_type: "ESXI"
    os_version: "6.5.0"
    host_credential:
        username: "root"
        password: "ca$hc0w"
        thumbprint: "60:0A:68:4B:3F:B5:6C:FE:31:B0:2A:BC:CA:F8:61:CA:7B:B2:70:D5:D5:04:58:DB:59:E0:2A:22:64:35:35:C9"
    state: "present"

- name: Add Edge VM
  nsxt_fabric_nodes:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    resource_type: "EdgeNode"
    display_name: "EdegeNode1"
    #node_id: "eaaadf98-0f1a-4eb3-b8e7-2cc62ca8877b"
    ip_addresses:
      - 10.112.201.26
    deployment_config:
      form_factor: "SMALL"
      node_user_settings:
        cli_password: "Admin!23Admin"
        root_password: "Admin!23Admin"
      vm_deployment_config:
        placement_type: VsphereDeploymentConfig
        vc_name: "VC1"
        data_network_ids:
        - network-44
        - network-44
        - network-44
        management_network_id: "network-44"
        hostname: "EdgeVM1"
        compute_id: "domain-c49"
        storage_id: "datastore-43"
        default_gateway_addresses:
        - 10.112.203.253
        management_port_subnets:
        - ip_addresses:
          - 10.112.201.26
          prefix_length: "19"
    state: "present"

'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def get_fabric_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_fabric_nodes(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/fabric/nodes', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing fabric node. Error [%s]' % (to_native(err)))
    return resp

def get_fabric_node_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    fabric_nodes = get_fabric_nodes(module, manager_url, mgr_username, mgr_password, validate_certs)
    for fabric_node in fabric_nodes['results']:
        if fabric_node.__contains__('display_name') and fabric_node['display_name'] == display_name:
            return fabric_node
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

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, fabric_params ):
    if fabric_params['resource_type'] == 'EdgeNode':
        vc_name = fabric_params['deployment_config']['vm_deployment_config'].pop('vc_name', None)
        fabric_params['deployment_config']['vm_deployment_config']['vc_id'] = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                    "/fabric/compute-managers", vc_name)
    return fabric_params

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, fabric_params):
    if fabric_params['resource_type'] != 'HostNode': # only host node update is allowed
        return False
    existing_fabric_node = get_fabric_node_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, fabric_params['display_name'])
    if existing_fabric_node is None:
        return False
    if existing_fabric_node.__contains__('ip_addresses') and fabric_params.__contains__('ip_addresses') and \
        existing_fabric_node['ip_addresses'] != fabric_params['ip_addresses']:
        return True
    return False

def wait_till_create(id, module, manager_url, mgr_username, mgr_password, validate_certs):
    DEPLOYMENT_PROGRESS = ['INSTALL_IN_PROGRESS', 'VM_DEPLOYMENT_IN_PROGRESS', 'VM_DEPLOYMENT_QUEUED', 'VM_POWER_ON_IN_PROGRESS', 'NODE_NOT_READY', 'REGISTRATION_PENDING']
    DEPLOYMENT_SUCCESS = ['NODE_READY', 'INSTALL_SUCCESSFUL']
    try:
      while True:
          (rc, resp) = request(manager_url+ '/fabric/nodes/%s/status'% id, headers=dict(Accept='application/json'),
                        url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
          if resp['host_node_deployment_status'] in DEPLOYMENT_PROGRESS:
              time.sleep(10)
          elif resp['host_node_deployment_status'] in DEPLOYMENT_SUCCESS:
              time.sleep(5)
              return
          else:
              module.fail_json(msg= 'Error in fabric node status: %s'%(str(resp['host_node_deployment_status'])))
    except Exception as err:
      module.fail_json(msg='Error accessing fabric node status. Error [%s]' % (to_native(err)))

def wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      while True:
          (rc, resp) = request(manager_url+ '/fabric/nodes/%s/status'% id, headers=dict(Accept='application/json'),
                        url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
          time.sleep(10)
    except Exception as err:
      time.sleep(5)
      return

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                    action=dict(required=False, type= 'str'),
                    unprepare_host=dict(required=False, type= 'str'),
                    os_version=dict(required=False, type='str'),
                    os_type=dict(required=False, type='str'),
                    host_credential=dict(required=False, type='dict',
                        username=dict(required=False, type='str'),
                        password=dict(required=False, type='str', no_log=True),
                        thumbprint=dict(required=False, type='str', no_log=True)),
                    deployment_config=dict(required=False, type='dict',
                        node_user_settings=dict(required=True, type='dict',
                            cli_username=dict(required=False, type='str'),
                            audit_username=dict(required=False, type='str'),
                            root_password=dict(required=False, type='str', no_log=True),
                            cli_password=dict(required=False, type='str', no_log=True),
                            audit_password=dict(required=False, type='str')),
                        vm_deployment_config=dict(required=True, type='dict',
                            data_network_ids=dict(required=True, type='list'),
                            dns_servers=dict(required=False, type='list'),
                            ntp_servers=dict(required=False, type='list'),
                            management_network_id=dict(required=True, type='str'),
                            enable_ssh=dict(required=False, type='boolean'),
                            allow_ssh_root_login=dict(required=False, type='boolean'),
                            compute_id=dict(required=True, type='str'),
                            search_domains=dict(required=False, type='list'),
                            vc_name=dict(required=True, type='str'),
                            storage_id=dict(required=True, type='str'),
                            default_gateway_addresses=dict(required=False, type='list'),
                            management_port_subnets=dict(required=False, type='list'),
                            host_id=dict(required=False, type='str'),
                            hostname=dict(required=True, type='str'),
                            placement_type=dict(required=True, type='str')),
                        form_factor=dict(required=False, type='str')),
                    ip_addresses=dict(required=False, type='list'),
                    external_id=dict(required=False, type='str'),
                    resource_type=dict(required=True, type='str', choices=['HostNode', 'EdgeNode']),
                    state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True,
                         required_if=[['resource_type', 'HostNode', ['os_type']],
                                      ['resource_type', 'EdgeNode', ['deployment_config']]])
  fabric_params = get_fabric_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  node_dict = get_fabric_node_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  node_id, revision = None, None
  if node_dict:
    node_id = node_dict['id']
    revision = node_dict['_revision']

  if state == 'present':
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    body = update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, fabric_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)

    if not updated:
      # add the node
      request_data = json.dumps(fabric_params)
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(request_data), id='12345')
      try:
          if node_id:
              module.exit_json(changed=False, id=node_id, message="Fabric node with display_name %s already exist."% module.params['display_name'])
          (rc, resp) = request(manager_url+ '/fabric/nodes', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
                module.fail_json(msg="Failed to add node. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      wait_till_create(resp['id'], module, manager_url, mgr_username, mgr_password, validate_certs)

      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Fabric node with display name %s created succcessfully." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(fabric_params)), id=id)

      fabric_params['_revision'] = revision # update current revision
      request_data = json.dumps(fabric_params)
      id = node_id
      try:
          (rc, resp) = request(manager_url+ '/fabric/nodes/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update node wit id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Fabric node with node id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = node_id
    if id is None:
        module.exit_json(changed=False, msg='No fabric node exist with display name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(fabric_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/fabric/nodes/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete fabric node with id %s. Error[%s]." % (id, to_native(err)))

    wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs)

    module.exit_json(changed=True, id=id, message="Fabric node with node id %s deleted." % id)


if __name__ == '__main__':
    main()
