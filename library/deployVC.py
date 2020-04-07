#!/usr/bin/env python
# coding=utf-8
#
# Copyright © 2015 VMware, Inc. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions
# of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

__author__ = 'yasensim'

import requests
import ssl
import os
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
def deployVC(templ, is65):
    os.chdir("/mnt/VCSA/vcsa-cli-installer/lin64/")
    if is65:
	return os.system("./vcsa-deploy install --accept-eula --no-esx-ssl-verify /tmp/"+templ+" 2> /dev/null")
    else:
	return os.system("./vcsa-deploy --accept-eula --no-esx-ssl-verify /tmp/"+templ)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            vmname=dict(required=True, type='str'),
            pESX=dict(required=True, type='str'),
            pESX_user=dict(required=True, type='str'),
            pESX_passwd=dict(required=True, type='str', no_log=True),
	    templ=dict(required=True, type='str'),
	    is65=dict(required=True, type='bool'),
        ),
        supports_check_mode=True,
    )
    try:
        content = connect_to_api(module.params['pESX'], module.params['pESX_user'],
                                 module.params['pESX_passwd'])
    except vim.fault.InvalidLogin:
        module.fail_json(msg='exception while connecting to vCenter, login failure, check username and password')
    except requests.exceptions.ConnectionError:
        module.fail_json(msg='exception while connecting to vCenter, check hostname, FQDN or IP')
    vm = find_virtual_machine(content, module.params['vmname'])
    if vm:
        module.exit_json(changed=False, msg='A VM with the name {} was already present'.format(module.params['vmname']))
    if module.check_mode:
        module.exit_json(changed=True, debug_out="Test Debug out, Yasen !!!")

    result = deployVC(module.params['templ'], module.params['is65'])
    if result != 0:
        module.fail_json(msg='Failed to deploy vCenter with name {}'.format(module.params['vmname']))
    module.exit_json(changed=True, result=module.params['vmname'] + " created")

from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
