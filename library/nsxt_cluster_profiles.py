#!/usr/bin/env python
#
# Copyright 2020 VMware, Inc.
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
module: nsxt_cluster_profiles
short_description: 'Create a Cluster Profile'
description: "Create a cluster profile. The resource_type is required."
version_added: '2.7'
author: 'Kommireddy Akhilesh'
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
    display_name:
        description: 'Display name'
        required: true
        type: str
    description:
        description: Description of the resource
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
  - name: Create Cluster Profiles
    nsxt_cluster_profiles:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False `
      resource_type: EdgeHighAvailabilityProfile
      display_name: edge-cluster-profile-East
      bfd_probe_interval: 1000
      bfd_declare_dead_multiple: 3
      bfd_allowed_hops: 1
      state: present
'''

RETURN = '''# '''

import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native


def get_cluster_profiles_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_cluster_profiles(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/cluster-profiles', headers=dict(Accept='application/json'),
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

def cmp_dict(dict1, dict2):
    for k2, v2 in dict2.items():
        found = False
        if k2 not in dict1:
            continue
        if type(v2) != list and dict1[k2] != dict2[k2]:
            return False
        for obj2 in v2:
            for obj1 in dict1[k2]:
                if all(item in obj1.items() for item in obj2.items()):
                           found = True
        if not found:
            return False
    return True

def get_cluster_profiles_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    cluster_profiles = get_cluster_profiles(module, manager_url, mgr_username, mgr_password, validate_certs)
    for cluster_profile in cluster_profiles['results']:
        if cluster_profile.__contains__('display_name') and cluster_profile['display_name'] == display_name:
            return cluster_profile
    return None

# def ordered(obj):
#     if isinstance(obj, dict):
#         return sorted((k, ordered(v)) for k, v in obj.items())
#     if isinstance(obj, list):
#         return sorted(ordered(x) for x in obj)
#     else:
#         return obj

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, cluster_profiles_body):
    existing_edge_cluster = get_cluster_profiles_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, cluster_profiles_body['display_name'])
    if existing_edge_cluster is None:
        return False
    if existing_edge_cluster.__contains__('description') and not cluster_profiles_body.__contains__('description'):
        return True
    if not existing_edge_cluster.__contains__('description') and cluster_profiles_body.__contains__('description'):
        return True
    if existing_edge_cluster.__contains__('description') and cluster_profiles_body.__contains__('description') and \
        existing_edge_cluster['description'] != cluster_profiles_body['description']:
        return True
    if existing_edge_cluster.__contains__('bfd_allowed_hops') and not cluster_profiles_body.__contains__('bfd_allowed_hops'):
        return True
    if not existing_edge_cluster.__contains__('bfd_allowed_hops') and cluster_profiles_body.__contains__('bfd_allowed_hops'):
        return True
    if existing_edge_cluster.__contains__('bfd_allowed_hops') and cluster_profiles_body.__contains__('bfd_allowed_hops') and \
        existing_edge_cluster['bfd_allowed_hops'] != cluster_profiles_body['bfd_allowed_hops']:
        return True
    if existing_edge_cluster.__contains__('bfd_declare_dead_multiple') and not cluster_profiles_body.__contains__('bfd_declare_dead_multiple'):
        return True
    if not existing_edge_cluster.__contains__('bfd_declare_dead_multiple') and cluster_profiles_body.__contains__('bfd_declare_dead_multiple'):
        return True
    if existing_edge_cluster.__contains__('bfd_declare_dead_multiple') and cluster_profiles_body.__contains__('bfd_declare_dead_multiple') and \
        existing_edge_cluster['bfd_declare_dead_multiple'] != cluster_profiles_body['bfd_declare_dead_multiple']:
        return True
    if existing_edge_cluster.__contains__('standby_relocation_config') and not cluster_profiles_body.__contains__('standby_relocation_config'):
        return True
    if not existing_edge_cluster.__contains__('standby_relocation_config') and cluster_profiles_body.__contains__('standby_relocation_config'):
        return True
    if existing_edge_cluster.__contains__('standby_relocation_config') and cluster_profiles_body.__contains__('standby_relocation_config') and \
        not cmp_dict(existing_edge_cluster['standby_relocation_config'], cluster_profiles_body['standby_relocation_config']):
        return True
    return False

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, cluster_profile_params):
    return cluster_profile_params

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
                        resource_type=dict(required=True, type='str'),
                        bfd_allowed_hops=dict(required=False, type='int'),
                        bfd_declare_dead_multiple=dict(required=False, type='int'),
                        bfd_probe_interval=dict(required=False, type='int'),
                        standby_relocation_config=dict(required=False, type=dict,
                        standby_relocation_threshold=dict(required=False, type='int')),
                        tags=dict(required=False, type='list'),
                        state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  cluster_profile_params = get_cluster_profiles_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  cluster_profiles_dict = get_cluster_profiles_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  cluster_profile_id, revision = None, None
  if cluster_profiles_dict:
    cluster_profile_id = cluster_profiles_dict['id']
    revision = cluster_profiles_dict['_revision']

  if state == 'present':
    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, cluster_profile_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'

    if not updated:
      # add the edge_cluster
      request_data = json.dumps(body)
      if module.check_mode:
        module.exit_json(changed=True, debug_out=str(request_data), id='12345')
      try:
          if cluster_profile_id:
            module.exit_json(changed=False, id=cluster_profile_id, message="Cluster profile with display_name %s already exist."% module.params['display_name'])
          (rc, resp) = request(manager_url+ '/cluster-profiles', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
                module.fail_json(msg="Failed to add cluster profile. Request body [%s]. Error[%s]." % (request_data, to_native(err)))
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Cluster profile with display name %s created." % module.params['display_name'])
    else:
      if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(edge_cluster_params)), id=cluster_profile_id)
      body['_revision'] = revision # update current revision
      request_data = json.dumps(body)
      id = cluster_profile_id
      try:
          (rc, resp) = request(manager_url+ '/cluster-profiles/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update cluster profile with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Cluster profile with id %s updated." % id)

  elif state == 'absent':
    # delete the edge cluster
    id = cluster_profile_id
    if id is None:
        module.exit_json(changed=False, msg='No cluster profile exist with display name %s' % display_name)

    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(edge_cluster_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/cluster-profiles/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete cluster profile with id %s. Error[%s]." % (id, to_native(err)))

    module.exit_json(changed=True, id=id, message="Cluster profile with id %s deleted." % id)


if __name__ == '__main__':
    main()
