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
module: nsxt_certificates
short_description: 'Add a New Certificate'
description: "Adds a new private-public certificate or a chain of certificates (CAs) and, 
              optionally, a private key that can be applied to one of the user-facing 
              components (appliance management or edge). The certificate and the key 
              should be stored in PEM format. If no private key is provided, the 
              certificate is used as a client certificate in the trust store."
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
        description:'Identifier to use when displaying entity in logs or GUI'
        required: true
        type: str
    pem_encoded_file:
        description: 'File containing pem encoded certificate data'
        required: true
        type='str' 
    private_key_file:
        description: 'File containing private key data'
        required: false
        type: str
    passphrase:
        description: 'Password for private key encryption'
        required: false
        type: str
    description:
        description: 'Description of this resource'
        required: false
        type: str
    id:
        description: 'Unique identifier of this resource'
        required: false
        type: str
    key_algo:
        description: 'Key algorithm contained in this certificate'
        required: false
        type: str
    resource_type:
        description: 'Must be set to the value TrustObjectData'
        required: false
        type: str
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
    - name: Add a new certificate
      nsxt_certificates:
        hostname: "{{hostname}}"
        username: "{{username}}"
        password: "{{password}}"
        validate_certs: False
        display_name: "Certificate_file"
        pem_encoded_file: "/Path/to/crt/file"
        passphrase: "paraphrase"
        state: "present"
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request, get_certificate_string, get_private_key_string
from ansible.module_utils._text import to_native

def update_params_with_pem_encoding(certificate_params):
    '''
    params: Parameters passed to the certificate
    result: Updated parameters. Files are replaced with the public and private strings. 
    '''
    certificate_params['pem_encoded'] = get_certificate_string (certificate_params.pop('pem_encoded_file', None))
    if certificate_params.get('private_key_file') is not None:
        certificate_params['private_key'] = get_private_key_string (certificate_params.pop('private_key_file', None))
    return certificate_params

def get_certificate_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_certificates(module, manager_url, mgr_username, mgr_password, validate_certs):
  try:
    (rc, resp) = request(manager_url+ '/trust-management/certificates', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
  except Exception as err:
    module.fail_json(msg='Error accessing trust management certificates. Error [%s]' % (to_native(err)))
  return resp

def get_certificate_with_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
  '''
  result: returns the certificate object with the display name provided
  '''
  certificates = get_certificates(module, manager_url, mgr_username, mgr_password, validate_certs)
  if certificates and certificates['result_count']>0:
    for certificate in certificates['results']:
      if certificate.__contains__('display_name') and certificate['display_name'] == display_name:
        return certificate
  return None

def main():
  argument_spec = dict()
  argument_spec.update(hostname=dict(type='str', required=True),
                       username=dict(type='str', required=True),
                       password=dict(type='str', required=True, no_log=True),
                       port=dict(type='int', default=443),
                       validate_certs=dict(type='bool', requried=False, default=True),
                       display_name=dict(required=True, type='str'),
                       pem_encoded_file=dict(required=True, type='str', no_log=True), 
                       private_key_file=dict(required=False, type='str', no_log=True),
                       passphrase=dict(required=False, type='str', no_log=True),
                       description=dict(required=False, type='str'),
                       id=dict(required=False, type='str'),
                       key_algo=dict(required=False, type='str'),
                       resource_type=dict(required=False, type='str'),
                       tags=dict(required=False, type='list'),
                    state=dict(required=True, choices=['present', 'absent']))
  '''
  Core function of the module reponsible for adding and deleting the certififcate.
  '''

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  certificate_params = get_certificate_params(module.params.copy())
  certificate_params = update_params_with_pem_encoding(certificate_params)
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'
  request_data = json.dumps(certificate_params)
  certificate_with_display_name = get_certificate_with_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name)


  if state == 'present':
    # add the certificate
    if certificate_with_display_name:
      module.fail_json(msg="Certificate with display name \'%s\' already exists." % display_name)  
    try:
      (rc, resp) = request(manager_url+ '/trust-management/certificates?action=import', data=request_data, headers=headers, method='POST',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg="Failed to add certificate.\n Error: [%s].\n Request_body[%s]." % (to_native(err), request_data))

    time.sleep(5)
    module.exit_json(changed=True, result=resp, message="certificate created. Response: [%s]" % str(resp))

  elif state == 'absent': 
    #Delete the certificate   
    if not certificate_with_display_name:
      module.fail_json(msg="Certificate with display name \'%s\' doesn't exists." % display_name)
    certificate_id = certificate_with_display_name['id']
    try:
       (rc, resp) = request(manager_url+ '/trust-management/certificates/' + certificate_id, method='DELETE',
                            url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg="Failed to delete certificate with display name \'%s\'. Error[%s]." % (display_name, to_native(err)))

    time.sleep(5)
    module.exit_json(changed=True, object_name=certificate_id, message="Certificate with certificate id: %s deleted." % certificate_id)


if __name__ == '__main__':
    main()
