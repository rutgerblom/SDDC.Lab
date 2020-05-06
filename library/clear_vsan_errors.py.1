#!/usr/bin/env python

from __future__ import print_function
import logging
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import tostring

import atexit
import requests
import ssl
from pyVim import connect
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl




def reset_alarm(**kwargs):
 
    service_instance = kwargs.get("service_instance")
    payload = _build_payload(**kwargs)
    logging.debug(payload)
    session = service_instance._stub
    if not _send_request(payload, session):
        return False
    return True


def _build_payload(**kwargs):
   
    entity_moref = kwargs.get("entity_moref")
    entity_type = kwargs.get("entity_type")
    alarm_moref = kwargs.get("alarm_moref")
    if not entity_moref or not entity_type or not alarm_moref:
        raise ValueError("entity_moref, entity_type, and alarm_moref "
                         "must be set")

    attribs = {
        'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema',
        'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
        'xmlns:soap': 'http://schemas.xmlsoap.org/soap/envelope/'
    }
    root = Element('soap:Envelope', attribs)
    body = SubElement(root, 'soap:Body')
    alarm_status = SubElement(body, 'SetAlarmStatus', {'xmlns': 'urn:vim25'})
    this = SubElement(alarm_status, '_this', {
        'xsi:type': 'ManagedObjectReference',
        'type': 'AlarmManager'
    })
    this.text = 'AlarmManager'
    alarm = SubElement(alarm_status, 'alarm', {'type': 'Alarm'})
    alarm.text = alarm_moref
    entity = SubElement(alarm_status, 'entity', {
        'xsi:type': 'ManagedObjectReference',
        'type': entity_type
    })
    entity.text = entity_moref
    status = SubElement(alarm_status, 'status')
    status.text = 'green'
 
    return '<?xml version="1.0" encoding="UTF-8"?>{0}'.format(tostring(root))


def _send_request(payload=None, session=None):
  
    stub = session
    host_port = stub.host
    # Ive seen some code in pyvmomi where it seems like we check for http vs
    # https but since the default is https do people really run it on http?
    url = 'https://{0}/sdk'.format(host_port)
    logging.debug("Sending {0} to {1}".format(payload, url))
    # I opted to ignore invalid ssl here because that happens in pyvmomi.
    # Once pyvmomi validates ssl it wont take much to make it happen here.
    res = requests.post(url=url, data=payload, headers={
        'Cookie': stub.cookie,
        'SOAPAction': 'urn:vim25',
        'Content-Type': 'application/xml'
    }, verify=False)
    if res.status_code != 200:
        logging.debug("Failed to reset alarm. HTTP Status: {0}".format(
            res.status_code))
        return False
    return True


def print_triggered_alarms(entity=None):
  
    alarms = entity.triggeredAlarmState
    for alarm in alarms:
  #       print("#"*40)
        # The alarm key looks like alarm-101.host-95
        return alarm.key.split('.')[0]
        

def get_alarm_refs(entity=None):
  
    alarm_states = entity.triggeredAlarmState
    ret = []
    for alarm_state in alarm_states:
        tdict = {
            "alarm": alarm_state.key.split('.')[0],
            "status": alarm_state.overallStatus
        }
        ret.append(tdict)
    return ret
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

def printAlarms(content, type, name):
    obj = get_obj(content, type, name)
    alarmMoref =  print_triggered_alarms(entity=obj)
    print (alarmMoref)

def clearAlarmsCycle(SI, content):
    check = 0
    container = content.viewManager.CreateContainerView( content.rootFolder, [vim.ClusterComputeResource], True)
    for ent in container.view:
        if print_triggered_alarms(entity=ent) is not None:
            print (ent.name +", id: "+str(ent) )
            printAlarms(content, [vim.ClusterComputeResource], ent.name)
            check = 1
            reset_alarm(
                    entity_moref=ent._moId, 
                    entity_type='ClusterComputeResource', 
                    alarm_moref=print_triggered_alarms(entity=ent).strip(), 
                    service_instance=SI
                    )
            for host in ent.host:
                if print_triggered_alarms(entity=host) is not None:
                    print (host.name)
                    printAlarms(content, [vim.HostSystem], host.name)
                    reset_alarm(
                                entity_moref=host._moId, 
                                entity_type='HostSystem', 
                                alarm_moref=print_triggered_alarms(entity=host).strip(), 
                                service_instance=SI
                    )
    
    container = content.viewManager.CreateContainerView( content.rootFolder, [vim.Datacenter], True)
    for ent in container.view:
        if print_triggered_alarms(entity=ent) is not None:
            print (ent.name +", id: "+str(ent) )
            check = 1
            printAlarms(content, [vim.Datacenter], ent.name) 
            reset_alarm(
                    entity_moref=ent._moId, 
                    entity_type='Datacenter', 
                    alarm_moref=print_triggered_alarms(entity=ent).strip(), 
                    service_instance=SI
                    ) 
    return check
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

def main():
    module = AnsibleModule(
        argument_spec=dict(
            vcenter=dict(required=True, type='str'),
            user=dict(required=True, type='str'),
            passwd=dict(required=True, type='str', no_log=True),
        ),
        supports_check_mode=False,
    )

    requests.packages.urllib3.disable_warnings()
    try:
	SI = connect.SmartConnect(host=module.params['vcenter'],
                                            user=module.params['user'],
                                            pwd=module.params['passwd'])

    except (requests.ConnectionError, ssl.SSLError):
        try:
            context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            context.verify_mode = ssl.CERT_NONE
	    SI = connect.SmartConnect(host=module.params['vcenter'],
                                            user=module.params['user'],
                                            pwd=module.params['passwd'],
                                            sslContext=context)

        except Exception as e:
            raise Exception(e)
    except vim.fault.InvalidLogin:
        module.fail_json(msg='exception while connecting to vCenter, login failure, check username and password')

    if not SI:
        module.fail_json(msg='exception while connecting to vCenter, no Service Instance')

    atexit.register(connect.Disconnect, SI)

    content = SI.RetrieveContent()
    check = 1
    while check == 1:
        check = clearAlarmsCycle(SI, content)

    module.exit_json(changed=True, result="vSAN Errors are cleared!!!!")

from ansible.module_utils.basic import *

# Start program
if __name__ == "__main__":
    main()
