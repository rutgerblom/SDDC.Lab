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
module: nsxt_compute_collection_fabric_templates
short_description: 'Create a compute collection fabric template'
description: 'Fabric templates are fabric configurations applied at the compute collection 
              level. This configurations is used to decide what automated operations should 
              be a run when a host membership changes.'
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
    auto_install_nsx:
        description: "Indicates whether NSX components should be automcatically installed.
                      When 'true' NSX components will be automatically installed on the new 
                      host added to compute collection."
        required: false
        type: bool
    cluster_name:
        description: 'Cluster Name'
        required: false
        type: str
    compute_manager_name:
        description: 'Cluster Manager's Name'
        required: false
        type: str
    display_name:
        description: 'Display name'
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

'''

EXAMPLES = '''
  - name: Create compute collection fabric template
      nsxt_compute_collection_fabric_templates:
        hostname: "{{hostname}}"
        username: "{{username}}"
        password: "{{password}}"
        validate_certs: False
        display_name: CC_fabric_template
        cluster_name: "cl1"
        compute_manager_name: VC1
        auto_install_nsx: True
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

def get_compute_collection_templates_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_compute_collection_templates(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/fabric/compute-collection-fabric-templates', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing fabric compute collection fabric template. Error [%s]' % (to_native(err)))
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

def get_compute_collection_templates_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    compute_collection_templates = get_compute_collection_templates(module, manager_url, mgr_username, mgr_password, validate_certs)
    for compute_collection_templates in compute_collection_templates['results']:
        if compute_collection_templates.__contains__('display_name') and compute_collection_templates['display_name'] == display_name:
            return compute_collection_templates
    return None

def wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      while True:
          (rc, resp) = request(manager_url+ '/fabric/compute-collection-fabric-templates/%s'% id, headers=dict(Accept='application/json'),
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

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, fabric_template ):
    compute_manager_name = fabric_template.pop('compute_manager_name', None)
    compute_cluster_name = fabric_template.pop('cluster_name', None)
    compute_collection_id = get_compute_collecting_id (module, manager_url, mgr_username, mgr_password, validate_certs,
                                                        compute_manager_name, compute_cluster_name)
    fabric_template['compute_collection_id'] = compute_collection_id
    return fabric_template

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, compute_collection_templates_with_ids):
    existing_compute_collection_templates = get_compute_collection_templates_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, compute_collection_templates_with_ids['display_name'])
    if existing_compute_collection_templates is None:
        return False
    if existing_compute_collection_templates['compute_collection_id'] != compute_collection_templates_with_ids['compute_collection_id']:
        return True
    return False

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                    compute_manager_name=dict(required=False, type='str'),
                    cluster_name=dict(required=False, type='str'),
                    auto_install_nsx=dict(required=False, type='bool'),
                    state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True,
                         required_if=[['state', 'present', ['compute_manager_name', 'cluster_name', 'auto_install_nsx']]])
  compute_collection_templates_params = get_compute_collection_templates_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  compute_collection_templates_dict = get_compute_collection_templates_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  compute_collection_templates_id, revision = None, None
  if compute_collection_templates_dict:
    compute_collection_templates_id = compute_collection_templates_dict['id']
    revision = compute_collection_templates_dict['_revision']

  if state == 'present':
    body = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, compute_collection_templates_params)
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, body)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    if not updated:
      # add the compute_collection_templates
      request_data = json.dumps(compute_collection_templates_params)
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(request_data), id='12345')
      try:
          if compute_collection_templates_id:
              module.exit_json(changed=False, id=compute_collection_templates_id, message="Compute collection fabric template with display_name %s already exist."% module.params['display_name'])
          (rc, resp) = request(manager_url+ '/fabric/compute-collection-fabric-templates', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
                module.fail_json(msg="Failed to add compute_collection_templates. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="Compute collection fabric template created for cluster %s." % module.params['cluster_name'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(compute_collection_templates_params)), id=compute_collection_templates_id)
      compute_collection_templates_params['_revision'] = revision # update current revision
      request_data = json.dumps(compute_collection_templates_params)
      id = compute_collection_templates_id
      try:
          (rc, resp) = request(manager_url+ '/fabric/compute-collection-fabric-templates/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update compute_collection_templates with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="fabric compute collection fabric template with Compute collection fabric template id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = compute_collection_templates_id
    if id is None:
        module.exit_json(changed=False, msg='No Compute collection fabric template exist with display_name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(compute_collection_templates_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/fabric/compute-collection-fabric-templates/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete fabric compute collection fabric template with id %s. Error[%s]." % (id, to_native(err)))

    wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs)

    module.exit_json(changed=True, id=id, message="Compute collection fabric template id %s deleted." % id)


if __name__ == '__main__':
    main()
