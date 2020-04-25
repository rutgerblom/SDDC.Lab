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
module: nsxt_edge_clusters
short_description: 'Create Edge Cluster'
description: "Creates a new edge cluster.
              It only supports homogeneous members.
              The TransportNodes backed by EdgeNode are only allowed in cluster members.
              DeploymentType (VIRTUAL_MACHINE|PHYSICAL_MACHINE) of these EdgeNodes is
              recommended to be the same. EdgeCluster supports members of different
              deployment types."
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
    cluster_profile_bindings:
        description: 'Edge cluster profile bindings'
        required: false
        type: 'array of ClusterProfileTypeIdEntry'
    display_name:
        description: 'Display name'
        required: true
        type: str
    description:
        description: Description of the resource
        required: false
        type: str
    members:
        description: "EdgeCluster only supports homogeneous members.
        These member should be backed by either EdgeNode or PublicCloudGatewayNode.
        TransportNode type of these nodes should be the same.
        DeploymentType (VIRTUAL_MACHINE|PHYSICAL_MACHINE) of these EdgeNodes is
        recommended to be the same. EdgeCluster supports members of different
        deployment types."
        required: false
        type: 'array of EdgeClusterMember'
    allocation_rules:
        description: Allocation rules for auto placement
        required: false
        type: list
    enable_inter_site_forwarding:
        description: Flag to enable inter site forwarding
        required: false
        type: bool
    node_rtep_ips:
        description: Remote tunnel endpoint ip address
        required: false
        type: list
    member_node_type:
        description: Node type of the cluster members
        required: false
        type: dict
        EdgeDeploymentType:
            description: Supported edge deployment type.
            required: false
            type: str
    deployment_type:
        description: Deplloyment type of the cluster members
        required: false
        type: dict
        EdgeDeploymentType:
            description: Supported edge deployment type.
            required: false
            type: str
    state:
        choices:
            - present
            - absent
        description: "State can be either 'present' or 'absent'.
                      'present' is used to create or update resource.
                      'absent' is used to delete resource."
        required: true

    
'''

EXAMPLES = '''
  - name: Create Edge Cluster
    nsxt_edge_clusters:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      display_name: edge-cluster-1  `
      cluster_profile_bindings:
        - profile_name: "nsx-edge-profile"
          resource_type: EdgeHighAvailabilityProfile
      members:
        - transport_node_name: "TN_1"
      state: present
'''

RETURN = '''# '''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native


def get_edge_cluster_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_edge_clusters(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/edge-clusters', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing edge clusters. Error [%s]' % (to_native(err)))
    return resp

def get_id_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, endpoint, display_name):
    try:
      (rc, resp) = request(manager_url+ endpoint, headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing id for display name %s. Error [%s]' % (display_name, to_native(err)))

    for result in resp['results']:
        if result.__contains__('display_name') and result['display_name'] == display_name:
            return result['id']
    module.fail_json(msg='No id exist with display name %s' % display_name)

def get_edge_clusters_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    edge_clusters = get_edge_clusters(module, manager_url, mgr_username, mgr_password, validate_certs)
    for edge_cluster in edge_clusters['results']:
        if edge_cluster.__contains__('display_name') and edge_cluster['display_name'] == display_name:
            return edge_cluster
    return None

# def ordered(obj):
#     if isinstance(obj, dict):
#         return sorted((k, ordered(v)) for k, v in obj.items())
#     if isinstance(obj, list):
#         return sorted(ordered(x) for x in obj)
#     else:
#         return obj

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, edge_cluster_with_id):
    existing_edge_cluster = get_edge_clusters_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, edge_cluster_with_id['display_name'])
    if existing_edge_cluster is None:
        return False
    if existing_edge_cluster.__contains__('description') and not edge_cluster_with_id.__contains__('description'):
        return True
    if not existing_edge_cluster.__contains__('description') and edge_cluster_with_id.__contains__('description'):
        return True
    if existing_edge_cluster.__contains__('description') and edge_cluster_with_id.__contains__('description') and \
        existing_edge_cluster['description'] != edge_cluster_with_id['description']:
        return True
    if existing_edge_cluster.__contains__('members') and not edge_cluster_with_id.__contains__('members'):
        return True
    if not existing_edge_cluster.__contains__('members') and edge_cluster_with_id.__contains__('members'):
        return True
    if existing_edge_cluster.__contains__('members') and edge_cluster_with_id.__contains__('members') and \
        existing_edge_cluster['members'] != edge_cluster_with_id['members']:
        return True
    return False

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, edge_cluster_params):
    if edge_cluster_params.__contains__('members'):
        for transport_node in edge_cluster_params['members']:
            transport_node_name = transport_node.pop('transport_node_name', None)
            transport_node['transport_node_id'] = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                                                    "/transport-nodes", transport_node_name)
    return edge_cluster_params

def get_cluster_profiles(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/cluster-profiles', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing edge clusters. Error [%s]' % (to_native(err)))
    return resp

def get_profile_id_from_profile_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    cluster_profiles = get_cluster_profiles(module, manager_url, mgr_username, mgr_password, validate_certs)
    for cluster_profile in cluster_profiles['results']:
        if cluster_profile.__contains__('display_name') and cluster_profile['display_name'] == display_name:
            return cluster_profile['id']
    module.fail_json(msg='No id exist with display name %s' % display_name)

def update_params_with_profile_id(module, manager_url, mgr_username, mgr_password, validate_certs, edge_cluster_params):
    if edge_cluster_params.__contains__('cluster_profile_bindings'):
        for cluster_profile in edge_cluster_params['cluster_profile_bindings']:
            cluster_profile_name = cluster_profile.pop('profile_name', None)
            cluster_profile['profile_id'] = get_profile_id_from_profile_name(module, manager_url, mgr_username, mgr_password, validate_certs, cluster_profile_name)
    return edge_cluster_params

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                        description=dict(required=False, type='str'),
                        cluster_profile_bindings=dict(required=False, type='list'),
                        members=dict(required=False, type='list'), # tranpost_node_name
                        allocation_rules=dict(required=False, type='list'),
                        deployment_type=dict(required=False, type='dict',
                        EdgeDeploymentType=dict(required=False, type='str')),
                        enable_inter_site_forwarding=dict(required=False, type='bool'),
                        member_node_type=dict(required=False, type='dict',
                        EdgeClusterNodeType=dict(required=False, type='str')),
                        node_rtep_ips=dict(required=False, type='str'),
                        tags=dict(required=False, type='list'),
                        state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  edge_cluster_params = get_edge_cluster_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  edge_cluster_dict = get_edge_clusters_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  edge_cluster_id, revision = None, None
  if edge_cluster_dict:
    edge_cluster_id = edge_cluster_dict['id']
    revision = edge_cluster_dict['_revision']

  if state == 'present':
    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, edge_cluster_params)
    body = update_params_with_profile_id(module, manager_url, mgr_username, mgr_password, validate_certs, edge_cluster_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'

    if not updated:
      # add the edge_cluster
      request_data = json.dumps(body)
      if module.check_mode:
        module.exit_json(changed=True, debug_out=str(request_data), id='12345')
      try:
          if edge_cluster_id:
            module.exit_json(changed=False, id=edge_cluster_id, message="Edge cluster with display_name %s already exist."% module.params['display_name'])
          (rc, resp) = request(manager_url+ '/edge-clusters', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
                module.fail_json(msg="Failed to add edge cluster. Request body [%s]. Error[%s]." % (request_data, to_native(err)))
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="edge cluster with display name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(edge_cluster_params)), id=edge_cluster_id)
      body['_revision'] = revision # update current revision
      request_data = json.dumps(body)
      id = edge_cluster_id
      try:
          (rc, resp) = request(manager_url+ '/edge-clusters/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update edge cluster with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Edge cluster with edge cluster id %s updated." % id)

  elif state == 'absent':
    # delete the edge cluster
    id = edge_cluster_id
    if id is None:
        module.exit_json(changed=False, msg='No edge cluster exist with display name %s' % display_name)

    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(edge_cluster_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/edge-clusters/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete edge cluster with id %s. Error[%s]." % (id, to_native(err)))

    module.exit_json(changed=True, id=id, message="edge cluster with edge cluster id %s deleted." % id)


if __name__ == '__main__':
    main()
