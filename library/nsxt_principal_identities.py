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
module: nsxt_principal_identities
short_description: 'Register a name-certificate combination.'
description: "Associates a principal's name with a certificate that is used to authenticate. "
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
        description: 'Identifier to use when displaying entity in logs or GUI'
        required: true
        type: str
    name:
        description: 'Name of the principal'
        required: true
        type: str
    node_id:
        description: 'Unique node-id'
        required: true
        type: str
    certificate_name:
        description: 'Display name of the certificate attached'
        required: true
        type: str
    role:
        description: 'Role'
        required: true
        type: str
    description:
        description: 'Description of this resource'
        required: false
        type: str
    resource_type:
        description: 'Must be set to the value PrincipalIdentity'
        required: false
        type: str
    id:
        description: 'Unique identifier of this resource'
        required: false
        type: str
    is_protected:
        description: 'Description of this resource'
        required: false
        type: bool
    tags:
        description: Opaque identifier meaninful to API user
        required: false
        type: Array of Tag
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
- hosts: 127.0.0.1
  connection: local
  become: yes
  vars_files:
    - answerfile.yml
  tasks:
    - name: Register a name-certificate combination
      nsxt_principal_identities:
        hostname: "{{hostname}}"
        username: "{{username}}"
        password: "{{password}}"
        validate_certs: False
        display_name: "Akhilesh_principal_display_name"
        name: "Akhilesh_principal_name"
        node_id: "node-1"
        role: "enterprise_admin"
        certificate_name: "Akhilesh_cert"
        state: "present"
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request, get_certificate_string
from ansible.module_utils._text import to_native

def get_principal_identity_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_principal_identity_update_params(args=None):
    args_to_remove = ['name', 'node_id', 'certificate_pem', 'role', 'is_protected']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def update_params_with_pem_encoding(principal_id_params):
    '''
    params: Parameters passed to the certificate
    result: Updated parameters. Files are replaced with the public and private strings. 
    '''
    principal_id_params['certificate_pem'] = get_certificate_string (principal_id_params.pop('certificate_pem_file', None))
    return principal_id_params

def update_params_with_id (module, manager_url, mgr_username, mgr_password, validate_certs, principal_id_params ):
    principal_id_params['certificate_id'] = get_id_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs,
                                            '/trust-management/certificates', principal_id_params.pop('certificate_name', None))
    return principal_id_params

def get_id_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, endpoint, display_name):
  try:
    (rc, resp) = request(manager_url+ endpoint, headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
  except Exception as err:
    module.fail_json(msg='Error accessing id for display name %s. Error [%s]' % (display_name, to_native(err)))

  for result in resp['results']:
    if result.__contains__('display_name') and result['display_name'] == display_name:
      return result['id']
  module.fail_json(msg='No id exists with display name %s' % display_name)

def get_principal_ids(module, manager_url, mgr_username, mgr_password, validate_certs):
  try:
    (rc, resp) = request(manager_url+ '/trust-management/principal-identities', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
  except Exception as err:
    module.fail_json(msg='Error accessing principal identities. Error [%s]' % (to_native(err)))
  return resp

def get_principal_id_with_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
  '''
  result: returns the principal id of the display name provided
  '''
  principal_ids = get_principal_ids(module, manager_url, mgr_username, mgr_password, validate_certs)
  if principal_ids and len(principal_ids['results'])>0:
    for principal_id in principal_ids['results']:
      if principal_id.__contains__('display_name') and principal_id['display_name'] == display_name:
        return principal_id
  return None

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, display_name, principal_id_params):
  '''
      Checks if principal identity exists, if exists it means we need to update already existing
      principal identity after checking if there are any differences with respect to existing
      display name
  '''
  existing_principal_id = get_principal_id_with_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  if existing_principal_id is None:
    return False
  if not existing_principal_id.__contains__('description') and principal_id_params.__contains__('description'):
    return True
  if existing_principal_id.__contains__('description') and not principal_id_params.__contains__('description'):
    return True
  if existing_principal_id.__contains__('description') and principal_id_params.__contains__('description') and\
  existing_principal_id['description'] != principal_id_params['description']:
    return True
  if existing_principal_id.__contains__('certificate_id') and principal_id_params.__contains__('certificate_id') and\
  existing_principal_id['certificate_id'] != principal_id_params['certificate_id']:
    return True
  return False

def get_certificate_id_with_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
  '''
  result: returns the certificate object with the display name provided
  '''
  certificates = get_certificates(module, manager_url, mgr_username, mgr_password, validate_certs)
  if certificates and certificates['result_count']>0:
    for certificate in certificates['results']:
      if certificate.__contains__('display_name') and certificate['display_name'] == display_name:
        return certificate['id']
  return None

def main():
  argument_spec = dict()
  argument_spec.update(hostname=dict(type='str', required=True),
                       username=dict(type='str', required=True),
                       password=dict(type='str', required=True, no_log=True),
                       port=dict(type='int', default=443),
                       validate_certs=dict(type='bool', requried=False, default=True),
                       display_name=dict(required=True, type='str'),
                       name=dict(required=True, type='str'), 
                       node_id=dict(required=True, type='str'),
                       certificate_name=dict(required=False, type='str'),
                       certificate_pem_file=dict(required=True, type='str', no_log=True),
                       role=dict(required=False, type='str'),
                       description=dict(required=False, type='str'),
                       resource_type=dict(required=False, type='str'),
                       id=dict(required=False, type='str'),
                       is_protected=dict(required=False, type='bool'),
                       tags=dict(required=False, type='list'),
                    state=dict(required=True, choices=['present', 'absent']))
  '''
  Core function of the module reponsible for adding and deleting the certififcate.
  '''
  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  principal_id_params = get_principal_identity_params(module.params.copy())
  principal_id_params = update_params_with_pem_encoding(principal_id_params)
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'
  if principal_id_params.__contains__('certificate_name'):
    principal_id_params = update_params_with_id(module, manager_url, mgr_username, mgr_password, validate_certs, principal_id_params)
  principal_id_with_display_name = get_principal_id_with_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name)

  if state == 'present':
    # update the principal identity
    if check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, display_name, principal_id_params):
      if principal_id_with_display_name:
        principal_id_params['principal_identity_id'] = principal_id_with_display_name['id']
        principal_id_params = get_principal_identity_update_params(principal_id_params.copy())
        request_data = json.dumps(principal_id_params)
        try:
          (rc, resp) = request(manager_url+ '/trust-management/principal-identities?action=update_certificate', data=request_data, headers=headers, method='POST',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
        except Exception as err:
          module.fail_json(msg="Failed to update principal identity. Error[%s]. Request body [%s]." % (request_data, to_native(err)))
        time.sleep(5)
        module.exit_json(changed=True, result=resp, message="Principal identity updated.")
    # add the principal identity
    if principal_id_with_display_name:
      module.exit_json(changed=False, msg="Principal id with display name \'%s\' already exists." % display_name) 
    request_data = json.dumps(principal_id_params)
    try:
        (rc, resp) = request(manager_url+ '/trust-management/principal-identities/with-certificate', data=request_data, headers=headers, method='POST',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
        module.fail_json(msg="Failed to add principal identity. Error[%s]. Request body [%s]." % (request_data, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, result=resp, message="Principal identity created.")

  elif state == 'absent':
    # delete the principal identity
    if not principal_id_with_display_name:
      module.fail_json(msg="Principal identity with display name \'%s\' doesn't exists." % display_name)
    principal_id = principal_id_with_display_name['id']
    try:
       (rc, resp) = request(manager_url+ '/trust-management/principal-identities/' + principal_id, method='DELETE',
                            url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg="Failed to delete principal identity with display name \'%s\'. Error[%s]." % (display_name, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=principal_id, message="Principal identity with display name \'%s\' and principal id \'%s\' deleted." %(display_name, principal_id))


if __name__ == '__main__':
    main()
