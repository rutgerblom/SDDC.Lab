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
module: nsxt_transport_node_collections
short_description: Create transport node collection by attaching Transport Node Profile to cluster.
description: When transport node collection is created the hosts which are part
of compute collection will be prepared automatically i.e. NSX Manager
attempts to install the NSX components on hosts. Transport nodes for these
hosts are created using the configuration specified in transport node
profile.

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
    cluster_name:
        description: CLuster Name
        required: false
        type: str
    compute_manager_name:
        description: Cluster Manager Name
        required: false
        type: str
    description:
        description: Description
        required: true
        type: str
    display_name:
        description: Display name
        required: true
        type: str
    resource_type:
        description: "A Policy Based VPN requires to define protect rules that match
                      local and peer subnets. IPSec security associations is
                      negotiated for each pair of local and peer subnet.
                      A Route Based VPN is more flexible, more powerful and recommended over
                      policy based VPN. IP Tunnel port is created and all traffic routed via
                      tunnel port is protected. Routes can be configured statically
                      or can be learned through BGP. A route based VPN is must for establishing
                      redundant VPN session to remote sites"
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
    transport_node_profile_name:
        description: Transport Node Profile Names
        required: true
        type: str
    
'''

EXAMPLES = '''
- name: Create transport node collection
    nsxt_transport_node_collections:
      hostname: "{{hostname}}"
      username: "{{username}}"
      password: "{{password}}"
      validate_certs: False
      display_name: "TNC1"
      resource_type: "TransportNodeCollection"
      description: "Transport Node Collections 1"
      compute_manager_name: "VC1"
      cluster_name: "cl1"
      transport_node_profile_name: "TNP1"
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

def get_transport_node_collections_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_transport_node_collections(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/transport-node-collections', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing transport-node-collections. Error [%s]' % (to_native(err)))
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

def get_transport_node_collection_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    transport_node_collections = get_transport_node_collections(module, manager_url, mgr_username, mgr_password, validate_certs)
    for transport_node_collection in transport_node_collections['results']:
        if transport_node_collection.__contains__('display_name') and transport_node_collection['display_name'] == display_name:
            return transport_node_collection
    return None

def wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      while True:
          (rc, resp) = request(manager_url+ '/transport-node-collections/%s'% id, headers=dict(Accept='application/json'),
                        url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
          time.sleep(10)
    except Exception as err:
      time.sleep(5)
      return

def get_transport_node_profile_id (module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_profile_name):
    try:
      return get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                                       "/transport-node-profiles", transport_node_profile_name)
    except Exception as err:
      module.fail_json(msg='Error accessing id for display name %s. Error [%s]' % (transport_node_profile_name, to_native(err)))

def get_compute_collection_id (module, manager_url, mgr_username, mgr_password, validate_certs, manager_name, cluster_name):
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

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_collection_params ):
    compute_manager_name = transport_node_collection_params.pop('compute_manager_name', None)
    compute_cluster_name = transport_node_collection_params.pop('cluster_name', None)
    compute_collection_id = get_compute_collection_id (module, manager_url, mgr_username, mgr_password, validate_certs,
                                                        compute_manager_name, compute_cluster_name)
    transport_node_collection_params['compute_collection_id'] = compute_collection_id

    transport_node_profile_name = transport_node_collection_params.pop('transport_node_profile_name', None)
    transport_node_profile_id = get_transport_node_profile_id (module, manager_url, mgr_username, mgr_password, validate_certs,
                                                        transport_node_profile_name)
    transport_node_collection_params['transport_node_profile_id'] = transport_node_profile_id
    return transport_node_collection_params

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_collection_with_ids):
    existing_tnc = get_transport_node_collection_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_collection_with_ids['display_name'])
    if existing_tnc is None:
        return False
    if existing_tnc['compute_collection_id'] == transport_node_collection_with_ids['compute_collection_id'] and \
        existing_tnc['transport_node_profile_id'] != transport_node_collection_with_ids['transport_node_profile_id']:
        return True
    return False

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                    description=dict(required=True, type='str'),
                    resource_type=dict(required=True, type='str'),
                    transport_node_profile_name=dict(required=True, type='str'),
                    compute_manager_name=dict(required=False, type='str'),
                    cluster_name=dict(required=False, type='str'),
                    state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  transport_node_collections_params = get_transport_node_collections_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  transport_node_collections_dict = get_transport_node_collection_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  transport_node_collection_id, revision = None, None
  if transport_node_collections_dict:
    transport_node_collection_id = transport_node_collections_dict['id']
    revision = transport_node_collections_dict['_revision']

  if state == 'present':
    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, transport_node_collections_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    if not updated:
      # add the transport_node_collections
      request_data = json.dumps(transport_node_collections_params)
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(request_data), id='12345')
      try:
          if transport_node_collection_id:
              module.exit_json(changed=False, id=transport_node_collection_id,
              message="transport-node-collection with display_name %s already exist on cluster %s." % (module.params['display_name'], module.params['cluster_name']))
          (rc, resp) = request(manager_url+ '/transport-node-collections', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
                module.fail_json(msg="Failed to add transport_node_collections. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="transport-node-collection created for cluster %s." % module.params['cluster_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(transport_node_collections_params)), id=transport_node_collection_id)
      transport_node_collections_params['_revision'] = revision # update current revision
      request_data = json.dumps(transport_node_collections_params)
      id = transport_node_collection_id
      try:
          (rc, resp) = request(manager_url+ '/transport-node-collections/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update transport_node_collections with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="transport-node-collection with Compute collection fabric template id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = transport_node_collection_id
    if id is None:
        module.exit_json(changed=False, msg='No transport-node-collection exist with display_name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(transport_node_collections_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/transport-node-collections/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete transport-node-collection with name %s. Error[%s]." % (display_name, to_native(err)))

    wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs)

    module.exit_json(changed=True, id=id, message="transport-node-collection with name %s deleted." % display_name)


if __name__ == '__main__':
    main()
