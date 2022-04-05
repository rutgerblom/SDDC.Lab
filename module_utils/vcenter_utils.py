#!/usr/bin/env python

# Copyright 2019 VMware, Inc.
# SPDX-License-Identifier: BSD-2-Clause OR GPL-3.0-only
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
import ssl
import requests
import atexit

from pyVim import connect
from pyVmomi import vmodl
from pyVmomi import vim

def establish_vcenter_connection(module, vCenter_host, username, password):
    '''
    params:
    - vCenter_host: vCenter host IP
    - username: vCenter username
    - password: vCenter password
    result:
    Retrieves vCenter information from service instance and returns as content object. 
    '''
    try:
        service_instance = connect.SmartConnect(host=vCenter_host,
                                                user=username,
                                                pwd=password,
                                                port=443)
        if not service_instance:
            module.fail_json(msg="Could not connect to the specified vCenter "
                  "host using specified username and password")

        atexit.register(connect.Disconnect, service_instance)
    except (requests.ConnectionError, ssl.SSLError):
        try:
            sslContext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            sslContext.verify_mode = ssl.CERT_NONE
            service_instance = connect.SmartConnect(host=vCenter_host,
                                                user=username,
                                                pwd=password,
                                                port=443,
                                                sslContext=sslContext)
            if not service_instance:
                module.fail_json(msg="Could not connect to the specified vCenter "
                      "host using specified username and password")

            atexit.register(connect.Disconnect, service_instance)
        except vmodl.MethodFault as error:
            module.fail_json(msg="Caught vmodl fault while connecting to vCenter: " + error.msg)
    return service_instance.RetrieveContent()

def get_resource_id_from_name(module, vCenter_host, username, password, 
                              resource_type, resource_name):
    '''
    params:
    - resource_type: Type of vCenter resource. Accepted values 'host', 'cluster', 'storage' and 'network'. 
    - resouce_name: Name of the resource.
    result:
    - moref id of the resource name and type given.
    '''
    try:
        content = establish_vcenter_connection(module, vCenter_host, username, password)
        if resource_type == 'host':
            objview = content.viewManager.CreateContainerView(content.rootFolder,
                                  [vim.HostSystem], True)
        elif resource_type == 'cluster':
            objview = content.viewManager.CreateContainerView(content.rootFolder, 
                                  [vim.ClusterComputeResource], True)
        elif resource_type == 'storage':
            objview = content.viewManager.CreateContainerView(content.rootFolder,
                                  [vim.Datastore], True)
        elif resource_type == 'network':
            objview = content.viewManager.CreateContainerView(content.rootFolder,
                                  [vim.Network], True)
        else:
            module.fail_json(msg='Resource type provided by user either doesn\'t' 
                                 ' exist or is not supported')
        all_resources = objview.view
        objview.Destroy()
        for resource in all_resources:
            if resource.name == resource_name:
                return resource._moId
        module.fail_json(msg='%s doesnt exist in %s' % (resource_name, 
                                                        resource_type))
    except vmodl.MethodFault as error:
        print("Caught vmodl fault while fetching info from vCenter: " + error.msg)
        return -1

def get_data_network_id_from_name(module, vCenter_host, username, password, 
                                 data_network_name_list):
    '''
    params:
    - data_network_name_list: List of data network names
    result:
    list of data network ids. 
    '''
    try:
        content = establish_vcenter_connection(module, vCenter_host, username, password)
        objview = content.viewManager.CreateContainerView(content.rootFolder,
                                   [vim.Network], True)
        all_networks = objview.view
        objview.Destroy()
        network_dict = {}
        for network in all_networks:
            network_dict[network.name] = network._moId
        data_network_id_list = []
        for data_network_name in data_network_name_list:
            if data_network_name in network_dict:
                data_network_id_list.append(str(network_dict[data_network_name]))
            else:
                module.fail_json(msg='data network %s doesnt exist in the available'
                                     'list of networks' % data_network_name)
        return data_network_id_list
    except vmodl.MethodFault as error:
        print("Caught vmodl fault while fetching info from vCenter: " + error.msg)
