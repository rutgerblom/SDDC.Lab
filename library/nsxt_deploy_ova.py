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
module: nsxt_deploy_ova
short_description: Deploys NSXT Manager
description: Deploys NSXT Manager
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
    ovftool_path:
        description: Path of ovf tool
        type: 'str',
    folder:
        description:  vCenter folder
        required: false
        type: 'str'
    datacenter:
        description: Datacenter name
        required: true 
        type: 'str'
    datastore:
        description: Data Store
        required: true
        type: 'str'
    portgroup:
        description: Port group
        required: true
        type: 'str'
    portgroup_ext:
        description: External Portgroup
        type: 'str'
    portgroup_transport:
        description: Transport Port Group
        type: 'str'
    cluster:
        description: vCenter Cluster
        required: true
        type: 'str'
    vmname:
        description: Name of VM
        required: true
        type: 'str'
    hostname:
        description: Name of host
        required: true 
        type: 'str'
    dns_server:
        description: DNS server address
        required: true
        type: 'str'
    ntp_server:
        description: NTP Server Address
        required: true
        type: 'str'
    dns_domain:
        description: DNS Domain name
        required: true
        type: 'str'
    gateway:
        description: Gateway Address
        required: true
        type: 'str'
    ip_address:
        description: IP Address
        required: true
        type: 'str'
    netmask:
        description: Netmask
        required: true
        type: 'str'
    admin_password:
        description: Admin Password
        required: true
        type: 'str'
        no_log: true
    cli_password:
        description: CLI Password
        required: true
        type: 'str'
        no_log: true
    ssh_enabled:
        description: If ssh is enabled
        default: false
    allow_ssh_root_login:
        description: If SSH root login is allowed
        default: false
    deployment_size:
        description: Size of the deployment
        default: 'medium'
        type: 'str'
    path_to_ova:
        description: Path to OVA file
        required: true
        type: 'str'
    ova_file:
        description: OVA File name
        required: true
        type: 'str'
    disk_mode:
        description: Disk mode to used. Thin or thick.
        default: 'thin'
    vcenter:
        description: vCenter name
        required: true
        type: 'str'
    vcenter_user:
        description: vCenter username
        required: true
        type: 'str'
    vcenter_passwd:
        description: vCenter password
        required: true
        type: 'str'
        no_log: true
    extra_para:
        description: Extra Parameters
        required: false
        type: 'str'
    role:
        description: Roles
        required: true
        type: 'str'
requirements:
    - PyVmOmi - Python library for vCenter api.
    - OVF Tools - Ovftool is used for ovf deployment.
'''

EXAMPLES = '''
- name: Deploy NSX Manager OVA
  deploy_ova:
    ovftool_path: "{{ ovfToolPath }}"
    datacenter: "private_dc"
    datastore: "data store"
    portgroup: "VM Network"
    cluster: "nsxt_cluster"
    vmname: "nsxt-manager"
    hostname: "nsxt-manager-10"
    dns_server: "10.161.244.213"
    dns_domain: "eng.vmware.com"
    ntp_server: "123.108.200.124"
    gateway: "10.112.203.253"
    ip_address: "10.112.201.24"
    netmask: "255.255.224.0"
    admin_password: "Admin!23Admin"
    cli_password: "Admin!23Admin"
    path_to_ova: "http://build-squid.eng.vmware.com/build/mts/release/bora-8411846/publish/nsx-unified-appliance/exports/ovf"
    ova_file: "nsx-unified-appliance-2.2.0.0.0.8411854.ovf"
    vcenter: "10.161.244.213"
    vcenter_user: "administrator@vsphere.local"
    vcenter_passwd: "Admin!23"
    deployment_size: "small"
    role: "nsx-manager nsx-controller"
'''

RETURN = '''# '''
import requests
import ssl

from pyVim.connect import SmartConnect
from pyVmomi import vim, vmodl


def find_virtual_machine(content, searched_vm_name):
    virtual_machines = get_all_objs(content, [vim.VirtualMachine])
    for vm in virtual_machines:
        if vm.name == searched_vm_name:
            return vm
    return None


def get_all_objs(content, vimtype):
    obj = {}
    container = content.viewManager.CreateContainerView(content.rootFolder, vimtype, True)
    for managed_object_ref in container.view:
        obj.update({managed_object_ref: managed_object_ref.name})
    return obj


def connect_to_api(vchost, vc_user, vc_pwd):
    try:
        service_instance = SmartConnect(host=vchost, user=vc_user, pwd=vc_pwd)
    except (requests.ConnectionError, ssl.SSLError):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_default_certs()
            service_instance = SmartConnect(host=vchost, user=vc_user, pwd=vc_pwd, sslContext=context)
        except Exception as e:
            raise Exception(e)
    return service_instance.RetrieveContent()


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ovftool_path=dict(type='str'),
            folder=dict(required=False, type='str'),
            datacenter=dict(required=True, type='str'),
            datastore=dict(required=True, type='str'),
            portgroup=dict(required=True, type='str'),
            portgroup_ext=dict(type='str'),
            portgroup_transport=dict(type='str'),
            cluster=dict(required=True, type='str'),
            vmname=dict(required=True, type='str'),
            hostname=dict(required=True, type='str'),
            dns_server=dict(required=True, type='str'),
            ntp_server=dict(required=True, type='str'),
            dns_domain=dict(required=True, type='str'),
            gateway=dict(required=True, type='str'),
            ip_address=dict(required=True, type='str'),
            netmask=dict(required=True, type='str'),
            admin_password=dict(required=True, type='str', no_log=True),
            cli_password=dict(required=True, type='str', no_log=True),
            ssh_enabled=dict(default=False),
            allow_ssh_root_login=dict(default=False),
            deployment_size=dict(default='medium', type='str'),
            path_to_ova=dict(required=True, type='str'),
            ova_file=dict(required=True, type='str'),
            disk_mode=dict(default='thin'),
            vcenter=dict(required=True, type='str'),
            vcenter_user=dict(required=True, type='str'),
            vcenter_passwd=dict(required=True, type='str', no_log=True),
            extra_para=dict(type='str'),
            role=dict(required=True, type='str')
        ),
        supports_check_mode=True,
        required_together=[['portgroup_ext', 'portgroup_transport']]
    )

    try:
        content = connect_to_api(module.params['vcenter'], module.params['vcenter_user'],
                                 module.params['vcenter_passwd'])
    except vim.fault.InvalidLogin:
        module.fail_json(msg='exception while connecting to vCenter, login failure, check username and password')
    except requests.exceptions.ConnectionError:
        module.fail_json(msg='exception while connecting to vCenter, check hostname, FQDN or IP')

    nsx_manager_vm = find_virtual_machine(content, module.params['vmname'])

    if nsx_manager_vm:
        module.exit_json(changed=False, msg='A VM with the name {} was already present'.format(module.params['vmname']))

    ovftool_exec = '{}/ovftool'.format(module.params['ovftool_path'])
    ovf_command = [ovftool_exec]

    ovf_base_options = ['--acceptAllEulas', '--skipManifestCheck', '--X:injectOvfEnv', '--powerOn', '--noSSLVerify',
                        '--allowExtraConfig', '--diskMode={}'.format(module.params['disk_mode']),
                        '--datastore={}'.format(module.params['datastore']),
                        '--name={}'.format(module.params['vmname'])]
    if module.params['portgroup_ext']:
        ovf_base_options.extend(['--net:Network 0={}'.format(module.params['portgroup']),
                                 '--net:Network 1={}'.format(module.params['portgroup_ext']),
                                 '--net:Network 2={}'.format(module.params['portgroup_transport']),
                                 '--net:Network 3={}'.format(module.params['portgroup'])])
    else:
        ovf_base_options.extend(['--network={}'.format(module.params['portgroup'])])
    ovf_command.extend(ovf_base_options)

    ovf_deployement_size = ['--deploymentOption={}'.format(module.params['deployment_size'])]
    ovf_command.extend(ovf_deployement_size)

    ovf_ext_prop = ['--prop:nsx_hostname={}'.format(module.params['hostname']),
                   '--prop:nsx_dns1_0={}'.format(module.params['dns_server']),
                   '--prop:nsx_domain_0={}'.format(module.params['dns_domain']),
                   '--prop:nsx_ntp_0={}'.format(module.params['ntp_server']),
                   '--prop:nsx_gateway_0={}'.format(module.params['gateway']),
                   '--prop:nsx_ip_0={}'.format(module.params['ip_address']),
                   '--prop:nsx_netmask_0={}'.format(module.params['netmask']),
                   '--prop:nsx_passwd_0={}'.format(module.params['admin_password']),
                   '--prop:nsx_cli_passwd_0={}'.format(module.params['cli_password']),
                   '--prop:nsx_isSSHEnabled={}'.format(module.params['ssh_enabled']),
                   '--prop:nsx_allowSSHRootLogin={}'.format(module.params['allow_ssh_root_login']),
                   '--prop:nsx_role={}'.format(module.params['role'])]
    ovf_command.extend(ovf_ext_prop)

    if module.params['extra_para']:
        ovf_command.extend(['--prop:extraPara={}'.format(module.params['extra_para'])])

    ova_file = '{}/{}'.format(module.params['path_to_ova'], module.params['ova_file'])
    ovf_command.append(ova_file)

    vi_string = 'vi://{}:{}@{}/'.format(module.params['vcenter_user'],
                                                   module.params['vcenter_passwd'], module.params['vcenter'])
    if module.params.__contains__('folder') and module.params['folder']:
        vi_string = vi_string + module.params['folder']

    vi_string = vi_string + '/{}/host/{}/'.format(module.params['datacenter'], module.params['cluster'])

    ovf_command.append(vi_string)

    if module.check_mode:
        module.exit_json(changed=True, debug_out=ovf_command)

    ova_tool_result = module.run_command(ovf_command)

    if ova_tool_result[0] != 0:
        module.fail_json(msg='Failed to deploy OVA, error message from ovftool is: {}, the comand was {}'.format(ova_tool_result[1], ovf_command))

    module.exit_json(changed=True, ova_tool_result=ova_tool_result)

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
