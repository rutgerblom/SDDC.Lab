#!/usr/bin/python

import requests
import ssl, time
from pyVim import connect
from pyVim.connect import SmartConnect
from pyVmomi import vim, vmodl

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
#    print cluster.name +", id: "+str(cluster)  
    for host in cluster.host:
#        print host.name +", id: "+str(host) 
        disk_list = []
        disks = host.configManager.vsanSystem.QueryDisksForVsan()
        for diskResult in disks:
            if diskResult.state == "eligible":
#                print ( diskResult.disk.displayName + ", SSD: " + str(diskResult.disk.ssd))
                disk_list.append(diskResult.disk)
        host.configManager.vsanSystem.AddDisks(disk=disk_list)
    time.sleep(60)

    cl = get_obj(content, [vim.ClusterComputeResource], module.params['cluster'])
    for ds in cl.datastore:
        if ds.summary.name.startswith("vsanDatastore"):
            ds.RenameDatastore("vsanDatastore" + module.params['cluster'])

#        print str(host.config.vsanHostConfig.storageInfo.diskMapping) 
    module.exit_json(changed=True, result="vSAN Disks claimed !!!!")

    return 0

from ansible.module_utils.basic import *

# Start program
if __name__ == "__main__":
    main()

