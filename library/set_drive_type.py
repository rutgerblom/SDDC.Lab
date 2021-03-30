#!/usr/bin/env python
#
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

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: set_drive_type

short_description: Manage the drive type of a vSAN eligible 'disk' storage devices on an ESXi servers which are members of a vCenter Server

description:
    Manage the drive type of vSAN eligible 'disk' type storage devices on an ESXi server to be either a 'Flash' or 'HDD' type device.
    The module is idempotent, and only makes changes to the drive type if they are not already properly set.  If only a vSphere Data
    Center is specified, then changes apply to all hosts within that data center that match the filtering criteria.  If 'drive_capacity'
    is specified, it will act as a filter, and only matching drives will be considered.  If 'esxi_hostname' is included, it must be a
    member of a vCenter Server.  To run against a stand-alone ESXi host directly, do not include 'datacenter', 'cluster_name', or
    'esxi_hostname' variables, and reference the ESXi host directory (see example).

version_added: "1.0.0"

options:
    hostname:
        description: The hostname or IP address of the vSphere vCenter or ESXi server.
        required: true
        type: str
    username:
        description: The username to authenticate with vSphere vCenter or ESXi server.
        required: true
        type: str
    password:
        description: The password to authenticate with vSphere vCenter or ESXi server.
        required: true
        type: str
    datacenter:
        description: The name of the vSphere vCenter datacenter.
        required: false
        type: str
    cluster_name:
        description:
            The name of the vSphere vCenter cluster.  If specified, 'datacenter' is required.  All hosts within vSphere vCenter cluster will be updated.
        required: false
        type: str
    esxi_hostname:
        description:
            The name of the ESXi host that is managed by vCenter Server to modify.
            If specified, 'datacenter' and 'cluster_name' are not used even if they are included.
        required: false
        type: str
    set_drivetype_to_flash:
        description: Specify 'true' if the disk type should be set to 'Flash', or 'false' if the disk type should be set to 'HDD'.
        required: false
        default: true
        type: boolean
    drive_capacity:
        description: Speicify disk size to match in MB.  Only disks with matching sizes are modified.  Size of '0' will match all disks.
        required: false
        default: 0
        type: integer

author:
    - Luis Chanu (@LuisChanu)

requirements:
    - PyVmomi - Python library for vCenter api.
'''

EXAMPLES = '''
- name: Modify all disks on all hosts in the 'Pod-200-DataCenter' datacenter (i.e. All clusters) to be 'Flash' type devices
  set_drive_type:
    hostname: "Pod-200-vCenter.SDDC.Lab"
    username: "administrator@vsphere.local"
    password: "VMware1!"
    datacenter: "Pod-200-DataCenter"
    set_drivetype_to_flash: true
  delegate_to: localhost

- name: Modify all disks in 'Compute-A' cluster to be 'Flash' type devices
  set_drive_type:
    hostname: "Pod-200-vCenter.SDDC.Lab"
    username: "administrator@vsphere.local"
    password: "VMware1!"
    datacenter: "Pod-200-DataCenter"
    cluster_name: "Compute-A"
    set_drivetype_to_flash: true
  delegate_to: localhost

- name: Modify all 10GB disks on ESXi host 'Pod-200-ComputeA-1' to be 'HDD' type devices
  set_drive_type:
    hostname: "Pod-200-vCenter.SDDC.Lab"
    username: "administrator@vsphere.local"
    password: "VMware1!"
    esxi_hostname: "Pod-200-ComputeA-1"
    drive_capacity: 10240
    set_drivetype_to_flash: false
  delegate_to: localhost

- name: Modify all drives on a stand-alone ESXi host to be 'HDD' type devices
  set_drive_type:
    hostname: "Pod-200-Edge-1.SDDC.Lab"
    username: "root"
    password: "VMware1!"
    drive_capacity: 0
    set_drivetype_to_flash: false
  delegate_to: localhost

'''

RETURN = '''# '''


import requests
import ssl
from pyVim import connect
from pyVmomi import vim, vmodl
from ansible.module_utils.basic import AnsibleModule


def connect_to_api(hostname, username, password):
    global service_instance
    try:
        service_instance = connect.SmartConnect(host=hostname, user=username, pwd=password)
    except (requests.ConnectionError, ssl.SSLError):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.verify_mode = ssl.CERT_NONE
            service_instance = connect.SmartConnect(host=hostname, user=username, pwd=password, sslContext=context)
        except Exception as e:
            raise Exception(e) from e
    return service_instance.RetrieveContent()


# Modified 'get_obj' that includes base "search_root" argument
def get_obj(content, search_root, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView(search_root, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break
    return obj


# Calculate disk size in MB
def capacity(disk):
    capacity = int((disk.capacity.block * disk.capacity.blockSize) / 1024 / 1024)
    return capacity


def wait_for_tasks(tasks):
    property_collector = service_instance.content.propertyCollector
    task_list = [str(task) for task in tasks]
    obj_specs = [vmodl.query.PropertyCollector.ObjectSpec(obj=task)
                 for task in tasks]
    property_spec = vmodl.query.PropertyCollector.PropertySpec(type=vim.Task,
                                                               pathSet=[],
                                                               all=True)
    filter_spec = vmodl.query.PropertyCollector.FilterSpec()
    filter_spec.objectSet = obj_specs
    filter_spec.propSet = [property_spec]
    pcfilter = property_collector.CreateFilter(filter_spec, True)
    try:
        version, state = None, None
        while len(task_list):
            update = property_collector.WaitForUpdates(version)
            for filter_set in update.filterSet:
                for obj_set in filter_set.objectSet:
                    task = obj_set.obj
                    for change in obj_set.changeSet:
                        if change.name == 'info':
                            state = change.val.state
                        elif change.name == 'info.state':
                            state = change.val
                        else:
                            continue

                        if not str(task) in task_list:
                            continue

                        if state == vim.TaskInfo.State.success:
                            task_list.remove(str(task))
                        elif state == vim.TaskInfo.State.error:
                            raise task.info.error
            version = update.version
    finally:
        if pcfilter:
            pcfilter.Destroy()


def main():

    module = AnsibleModule(
        argument_spec=dict(
            hostname=dict(required=True, type='str'),
            username=dict(required=True, type='str'),
            password=dict(required=True, type='str', no_log=True),
            datacenter=dict(required=False, type='str', default=None),
            cluster_name=dict(required=False, type='str', default=None, aliases=['cluster']),
            esxi_hostname=dict(required=False, type='str', default=None, aliases=['esxi']),
            set_drivetype_to_flash=dict(required=False, type='bool', default=True),
            drive_capacity=dict(required=False, type='int', default=0)
        ),
        supports_check_mode=True,
        required_together=[
            ('hostname', 'username', 'password'),
        ],
        required_by={
            'cluster_name': 'datacenter',
        }
    )

    try:
        content = connect_to_api(module.params['hostname'], module.params['username'],
                                 module.params['password'])
    except vim.fault.InvalidLogin:
        module.fail_json(msg='exception while connecting to vCenter or ESXi host.  Login failure, check username and password')
    except requests.exceptions.ConnectionError:
        module.fail_json(msg='exception while connecting to vCenter or ESXi host.  Please check hostname, FQDN or IP')

    content = service_instance.RetrieveContent()

    # Retrieve objects from vCenter/Host Inventory.  NoneType returned if empty not found.
    datacenter = get_obj(content, content.rootFolder, [vim.Datacenter], module.params['datacenter'])
    cluster = get_obj(content, datacenter, [vim.ClusterComputeResource], module.params['cluster_name'])
    esxi = get_obj(content, content.rootFolder, [vim.HostSystem], module.params['esxi_hostname'])

    # Initialize list of hosts to process
    hosts = []

    # Check if we are targeting an stand-alone ESXi host directly (datacenter=cluster=esxi=None) or a specific ESXi host within vCenter
    if (datacenter is None and cluster is None and esxi is None) or module.params['esxi_hostname'] is not None:
        hosts = [esxi]

    # Check if cluster was specified
    elif module.params['cluster_name'] is not None:
        hosts = cluster.host

    # Else we are processing all the hosts of a DataCenter
    else:
        # Create a custom view of all the hosts in the datacenter
        container = content.viewManager.CreateContainerView(datacenter, [vim.HostSystem], True)
        hosts = container.view

    # ############################################################################################################################
    # # Data structure being used is nested dicts containing host and list of disks on that host, which looks like the following #
    # ############################################################################################################################
    #
    #   hosts_with_disks = {
    #       "host1":{
    #            "host": host_object,
    #           "disks": [disk_object1, disk_object2, ...]
    #       },
    #       "host2":{
    #            "host": host_object,
    #           "disks": [disk_object1, disk_object2, ...]
    #       },
    #       ...
    #   }
    #

    # Initialize variables
    hosts_with_disks = {}
    disks = []

    # Iterate through each of the hosts to get the storage devices on that host which need to be modified
    for host in hosts:

        # Iterate through each vSAN eligible storage device on the host.  We only allow vSAN storage devices
        # because they exclude boot devices and non-disk devices (i.e. CDROMs)
        for vsan_disk in host.configManager.vsanSystem.QueryDisksForVsan():

            # If vsan_disk is NOT available for vSAN use
            if vsan_disk.state != "eligible":
                # Go check next vSAN disk
                continue

            # Obtain the disk object
            disk = vsan_disk.disk

            # Calculate drive capacity in MB
            drive_capacity = capacity(disk)

            # Check if drive_capacity matches
            if drive_capacity == module.params['drive_capacity'] or module.params['drive_capacity'] == 0:

                # See if host already exists in the disks dict, add disk to list of disks
                if host.name in hosts_with_disks:
                    nested_host = hosts_with_disks.pop(host.name)
                    disks = nested_host['disks']
                    disks.append(disk)
                # This is the first entry, so we add that disk by itself
                else:
                    disks = [disk]

                # Build updated nested host data structure
                nested_host = {
                    "host": host,
                    "disks": disks
                }

                # Add the nested host with the key being the human readable name of the ESXi host
                hosts_with_disks[host.name] = nested_host

    #
    # At this point, 'hosts_with_disks' should have all the ESXi hosts, along with the disk objects that matched the size condition.
    # So, now we just need to iterate through them, and set the ssd flag accordingly
    #

    # If module was run with "--check", keep track of change that would have been made
    checkmode_changes = []
    actual_changes = []

    # Iterate through the hosts with disks
    for hostname in hosts_with_disks:

        # Get host
        nested_host = hosts_with_disks[hostname]

        # Iterate through the disks of the host
        for disk in nested_host['disks']:
            # Make "Flash", but only if not already a ssd (idempotency check)
            if module.params['set_drivetype_to_flash'] and not disk.ssd:
                # If we are running in "--check" mode
                if module.check_mode:
                    # Return description of what would have been done
                    checkmode_changes.append('CHECK MODE: Host: {0}, CTL: {1}, Capacity: {2:7d}MB, Would be set to Flash (Set SSD flag)'
                                             .format(hostname, disk.canonicalName, capacity(disk)))
                else:
                    # Set SSD flag (Flash)
                    task = nested_host['host'].configManager.storageSystem.MarkAsSsd_Task(disk.uuid)
                    wait_for_tasks([task])
                    actual_changes.append('Host: {0}, CTL: {1}, Capacity: {2:7d}MB, Set to Flash (Set SSD flag)'
                                          .format(hostname, disk.canonicalName, capacity(disk)))

            # Make "HDD", but only if already a SSD, which is NOT a HDD (idempotency check)
            elif not module.params['set_drivetype_to_flash'] and disk.ssd:
                # If we are running in "--check" mode
                if module.check_mode:
                    # Return description of what would have been done
                    checkmode_changes.append('CHECK MODE: Host: {0}, CTL: {1}, Capacity: {2:7d}MB, Would be set to HDD (Clear SSD flag)'
                                             .format(hostname, disk.canonicalName, capacity(disk)))
                else:
                    # Clear SSD flag (HDD)
                    task = nested_host['host'].configManager.storageSystem.MarkAsNonSsd_Task(disk.uuid)
                    wait_for_tasks([task])
                    actual_changes.append('Host: {0}, CTL: {1}, Capacity: {2:7d}MB, Set to HDD (Clear SSD flag)'
                                          .format(hostname, disk.canonicalName, capacity(disk)))

    # If running in Check-Mode
    if module.check_mode:
        # Return changes that would have been made to the user
        module.exit_json(changed=False, msg=checkmode_changes)
    else:
        module.exit_json(changed=True, msg=actual_changes)


if __name__ == '__main__':
    main()
