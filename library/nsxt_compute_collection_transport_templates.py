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
module: nsxt_compute_collection_transport_templates
short_description: 'Create transport node template for compute collection.'
description: 'If automated transport node creation is configured on compute collection,
              this template will serve as the default setting for transport node creation.'
version_added: '2.7'
author: 'Rahul Raghuvanshi'
options:
    hostname:
        description: 'Deployed NSX manager hostname.'
        required: true
        type: str
    username:
        description: 'The username to authenticate with the NSX manager.'
        required: true
        type: str
    password:
        description: 'The password to authenticate with the NSX manager.'
        required: true
        type: str
    compute_collections:
        description: 'Associated compute collections'
        required: false
        type: list
    display_name:
        description: 'Display name'
        required: false
        type: str
    host_switch_spec:
        description: "Property 'host_switch_spec' can be used to create either standard host
                      switch or preconfigured host switch."
        host_switches:
            description: 'Transport Node host switches'
            required: true
            type: 'array of HostSwitch'
        required: false
        resource_type:
            description: 'Selects the type of the transport zone profile'
            required: true
            type: str
        type: dict
    network_migration_spec_ids:
        description: "Property 'network_migration_spec_ids' should only be used for compute
                      collections which are clusters in VMware vCenter. Currently only 
                      HostProfileNetworkMigrationSpec type is supported. This specification 
                      will only apply to Stateless ESX hosts which are under this vCenter cluster."
        required: false
        type: 'array of NetworkMigrationSpecTypeIdEntry'
    state:
        choices:
            - present
            - absent
        description: "State can be either 'present' or 'absent'.
                      'present' is used to create or update resource.
                      'absent' is used to delete resource."
        required: true
    transport_zone_endpoints:
        description: 'Transport zone endpoints'
        required: false
        type: 'array of TransportZoneEndPoint'    
'''

EXAMPLES = '''
  - name: Create compute collection transport template
    nsxt_compute_collection_transport_templates:
      hostname: "{{hostname}}"
      username: "{{username}}"
      password: "{{password}}"
      validate_certs: False
      display_name: CCTT2
      compute_collections:
      - compute_manager_name: VC2
        cluster_name: "ControlCluster1-$$"
      host_switch_spec:
          resource_type: StandardHostSwitchSpec
          host_switches:
          - host_switch_profiles:
            - name: uplinkProfile1
              type: UplinkHostSwitchProfile
            host_switch_name: hostswitch1
            pnics:
            - device_name: vmnic1
              uplink_name: "uplink-1"
            ip_assignment_spec:
              resource_type: StaticIpPoolSpec
              ip_pool_name: "IPPool-IPV4-1"
      transport_zone_endpoints:
      - transport_zone_name: "TZ1"
      state: present
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native
import ssl
import socket
import hashlib

def get_compute_collection_transport_templates_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

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

def get_compute_collection_transport_templates(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/compute-collection-transport-node-templates', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing transport compute collection transport template. Error [%s]' % (to_native(err)))
    return resp

def get_compute_collection_transport_templates_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    compute_collection_transport_templates = get_compute_collection_transport_templates(module, manager_url, mgr_username, mgr_password, validate_certs)
    for compute_collection_transport_templates in compute_collection_transport_templates['results']:
        if compute_collection_transport_templates.__contains__('display_name') and compute_collection_transport_templates['display_name'] == display_name:
            return compute_collection_transport_templates
    return None

def wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      while True:
          (rc, resp) = request(manager_url+ '/compute-collection-transport-node-templates/%s'% id, headers=dict(Accept='application/json'),
                        url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
          time.sleep(10)
    except Exception as err:
      time.sleep(5)
      return
def get_compute_collecting_id (module, manager_url, mgr_username, mgr_password, validate_certs, manager_name, cluster_name):
    try:
      (rc, resp) = request(manager_url+ '/fabric/compute-collections', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      compute_manager_id = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                                                        "/fabric/compute-managers", manager_name)
    except Exception as err:
      module.fail_json(msg='Error accessing compute collection id for manager %s, cluster %s. Error [%s]' % (manager_name, cluster_name, to_native(err)))

    for result in resp['results']:
        if result.__contains__('display_name') and result['display_name'] == cluster_name and \
            result['origin_id'] == compute_manager_id:
            return result['external_id']
    module.fail_json(msg='No compute collection id exist with cluster name %s for compute manager %s' % (cluster_name, manager_name))

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, transport_template_params ):
    for host_switch in transport_template_params['host_switch_spec']['host_switches']:
        host_switch_profiles = host_switch.pop('host_switch_profiles', None)

        host_switch_profile_ids = []
        for host_switch_profile in host_switch_profiles:
            profile_obj = {}
            profile_obj['value'] = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                                                    "/host-switch-profiles", host_switch_profile['name'])
            profile_obj['key'] = host_switch_profile['type']
            host_switch_profile_ids.append(profile_obj)
        host_switch['host_switch_profile_ids'] = host_switch_profile_ids
        if host_switch.__contains__('ip_assignment_spec'):
            ip_pool_name = host_switch['ip_assignment_spec'].pop('ip_pool_name', None)
            host_switch['ip_assignment_spec']['ip_pool_id'] = get_id_from_display_name (module, manager_url,
                                                                                        mgr_username, mgr_password, validate_certs,
                                                                                        "/pools/ip-pools", ip_pool_name)
    if transport_template_params.__contains__('transport_zone_endpoints'):
        for transport_zone_endpoint in transport_template_params['transport_zone_endpoints']:
            transport_zone_name = transport_zone_endpoint.pop('transport_zone_name', None)
            transport_zone_endpoint['transport_zone_id'] = get_id_from_display_name (module, manager_url,
                                                                                    mgr_username, mgr_password, validate_certs,
                                                                                    "/transport-zones", transport_zone_name)
    compute_collections = transport_template_params.pop('compute_collections', None)
    if compute_collections:
        compute_collection_ids = []
        for compute_collection in compute_collections:
            compute_manager_name = compute_collection.pop('compute_manager_name', None)
            compute_cluster_name = compute_collection.pop('cluster_name', None)
            compute_collection_id = get_compute_collecting_id (module, manager_url, mgr_username, mgr_password, validate_certs,
                                                                compute_manager_name, compute_cluster_name)
            compute_collection_ids.append(compute_collection_id)
        transport_template_params['compute_collection_ids'] = compute_collection_ids
    return transport_template_params

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, compute_collection_transport_templates_ids):
    existing_transport_node = get_compute_collection_transport_templates_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, compute_collection_transport_templates_ids['display_name'])
    if existing_transport_node is None:
        return False
    if existing_transport_node.__contains__('transport_zone_endpoints') and compute_collection_transport_templates_ids.__contains__('transport_zone_endpoints'):
        return not id_exist_in_list_dict_obj('transport_zone_id', existing_transport_node['transport_zone_endpoints'], compute_collection_transport_templates_ids['transport_zone_endpoints'])
    if existing_transport_node.__contains__('host_switch_spec') and existing_transport_node['host_switch_spec'].__contains__('host_switches') and \
        compute_collection_transport_templates_ids.__contains__('host_switch_spec') and compute_collection_transport_templates_ids['host_switch_spec'].__contains__('host_switches') and \
        existing_transport_node['host_switch_spec']['host_switches'] != compute_collection_transport_templates_ids['host_switch_spec']['host_switches']:
        return True
    return False

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=False, type='str'),
                    host_switch_spec=dict(required=False, type='dict',
                    host_switches=dict(required=True, type='list'),
                    resource_type=dict(required=True, type='str')),
                    transport_zone_endpoints=dict(required=False, type='list'),
                    network_migration_spec_ids=dict(required=False, type='list'),
                    compute_collections=dict(required=False, type='list'),
                    state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True,
                         required_if=[['state', 'present', ['compute_collections']]])
  compute_collection_transport_templates_params = get_compute_collection_transport_templates_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  compute_collection_transport_templates_dict = get_compute_collection_transport_templates_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  compute_collection_transport_templates_id, revision = None, None
  if compute_collection_transport_templates_dict:
    compute_collection_transport_templates_id = compute_collection_transport_templates_dict['id']
    revision = compute_collection_transport_templates_dict['_revision']

  if state == 'present':
    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, compute_collection_transport_templates_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    if not updated:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(request_data), id='12345')
      request_data = json.dumps(body)
      try:
          if compute_collection_transport_templates_id:
              module.exit_json(changed=False, id=compute_collection_transport_templates_id, message="Compute collection transport template with display_name %s already exist."% module.params['display_name'])
          (rc, resp) = request(manager_url+ '/compute-collection-transport-node-templates', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
                module.fail_json(msg="Failed to add compute_collection_transport_templates. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Compute collection transport template with display name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(compute_collection_transport_templates_params)), id=compute_collection_transport_templates_id)
      compute_collection_transport_templates_params['_revision'] = revision # update current revision
      request_data = json.dumps(compute_collection_transport_templates_params)
      id = compute_collection_transport_templates_id
      try:
          (rc, resp) = request(manager_url+ '/compute-collection-transport-node-templates/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update compute_collection_transport_templates with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Compute collection transport template with Compute collection transport template id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = compute_collection_transport_templates_id
    if id is None:
        module.exit_json(changed=False, msg='No Compute collection transport template exist with display_name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(compute_collection_transport_templates_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/compute-collection-transport-node-templates/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete transport compute collection transport template with id %s. Error[%s]." % (id, to_native(err)))

    wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs)

    module.exit_json(changed=True, id=id, message="Compute collection transport template id %s deleted." % id)


if __name__ == '__main__':
    main()
