#!/usr/bin/python

import requests
import ssl, time
from pyVim import connect
from pyVim.connect import SmartConnect
from pyVmomi import vim, vmodl
import vsanapiutils

def connect_to_api(vchost, vc_user, vc_pwd):
    global service_instance
    try:
        service_instance = SmartConnect(host=vchost, user=vc_user, pwd=vc_pwd)
    except (requests.ConnectionError, ssl.SSLError):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.verify_mode = ssl.CERT_NONE
            service_instance = SmartConnect(host=vchost, user=vc_user, pwd=vc_pwd, sslContext=context)
        except Exception as e:
            raise Exception(e)
    return service_instance.RetrieveContent()

def get_obj(content, vimtype, name):
    obj = None
    container = content.viewManager.CreateContainerView( content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break
    return obj

  
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



def configure_vsan():
    vsan_config = vim.vsan.cluster.ConfigInfo()
    vsan_config.enabled = True
    vsan_config.defaultConfig = vim.vsan.cluster.ConfigInfo.HostDefaultInfo()
    vsan_config.defaultConfig.autoClaimStorage = False
    return vsan_config

def main():

    module = AnsibleModule(
        argument_spec=dict(
            vcenter=dict(required=True, type='str'),
            user=dict(required=True, type='str'),
            passwd=dict(required=True, type='str', no_log=True),
	        cluster=dict(required=True, type='str'),
            datastorename=dict(required=True, type='str'),
        ),
        supports_check_mode=False,
    )

    try:
        content = connect_to_api(module.params['vcenter'], module.params['user'],
                                 module.params['passwd'])
    except vim.fault.InvalidLogin:
        module.fail_json(msg='exception while connecting to vCenter, login failure, check username and password')
    except requests.exceptions.ConnectionError:
        module.fail_json(msg='exception while connecting to vCenter, check hostname, FQDN or IP')

    content = service_instance.RetrieveContent()
    cluster = get_obj(content, [vim.ClusterComputeResource], module.params['cluster'])
    cluster_config_spec = vim.cluster.ConfigSpecEx()
    cluster_config_spec.vsanConfig = configure_vsan()
    task = cluster.ReconfigureComputeResource_Task(cluster_config_spec, True)
    wait_for_tasks([task])
 
    for host in cluster.host:
        diskmap = {host: {'cache': [], 'capacity': []}}
        cacheDisks = []
        capacityDisks = []
        result = host.configManager.vsanSystem.QueryDisksForVsan()
        ssds = []
        for ssd in result:
            if ssd.state == 'eligible' and (ssd.disk.capacity.block) / 2 / 1024 / 1024 > 19:
                ssds.append(ssd.disk)
        if ssds:
            smallerSize = min([disk.capacity.block * disk.capacity.blockSize for disk in ssds])
            for ssd in ssds:
                size = ssd.capacity.block * ssd.capacity.blockSize
                if size == smallerSize:
                    diskmap[host]['cache'].append(ssd)
                    cacheDisks.append((ssd.displayName, size, host.name))
                else:
                    diskmap[host]['capacity'].append(ssd)
                    capacityDisks.append((ssd.displayName, size, host.name))
            for host, disks in diskmap.items():
                if disks['cache'] and disks['capacity']:
                    dm = vim.VimVsanHostDiskMappingCreationSpec(
                        cacheDisks=disks['cache'], capacityDisks=disks['capacity'],
                        creationType='allFlash',
                        host=host)
            tasks = []
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            vcMos = vsanapiutils.GetVsanVcMos(service_instance._stub, context=context)
            vsanVcDiskManagementSystem = vcMos['vsan-disk-management-system']
            task = vsanVcDiskManagementSystem.InitializeDiskMappings(dm)
            tasks.append(task)
            vsanapiutils.WaitForTasks(tasks, service_instance)

    cl = get_obj(content, [vim.ClusterComputeResource], module.params['cluster'])
    for ds in cl.datastore:
        if ds.summary.name.startswith("vsanDatastore"):
            ds.RenameDatastore(module.params['datastorename'])

    module.exit_json(changed=True, result="vSAN Disks claimed !!!!")

    return 0

from ansible.module_utils.basic import *

# Start program
if __name__ == "__main__":
    main()

