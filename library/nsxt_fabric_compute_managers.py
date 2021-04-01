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
module: nsxt_fabric_compute_managers
short_description: 'Register compute manager with NSX'
description: "Registers compute manager with NSX. Inventory service will collect
              data from the registered compute manager"
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
    credential:
        asymmetric_credential:
            description: 'Asymmetric login credential'
            required: false
            type: str
        credential_key:
            description: 'Credential key'
            no_log: 'True'
            required: false
            type: str
        credential_type:
            description: 'Possible values are UsernamePasswordLoginCredential, VerifiableAsymmetricLoginCredential.'
            required: true
            type: str
        credential_verifier:
            description: 'Credential verifier'
            required: false
            type: str
        description: 'Login credentials for the compute manager'
        password:
            description: "Password for the user (optionally specified on PUT, unspecified on
                          GET)"
            no_log: 'True'
            required: false
            type: str
        required: false
        thumbprint:
            description: 'Hexadecimal SHA256 hash of the vIDM server''s X.509 certificate'
            no_log: 'True'
            required: false
            type: str
        type: dict
        username:
            description: 'Username value of the log'
            required: false
            type: str
    display_name:
        description: 'Display name'
        required: true
        type: str
    origin_type:
        description: 'Compute manager type like vCenter'
        required: true
        type: str
    description:
        description: 'Description of the resource'
        required: false
        type: str
    server:
        description: 'IP address or hostname of compute manager'
        required: true
        type: str
    set_as_oidc_provider:
        description: "Specifies whether compute manager has been set as OIDC provider
                        If the compute manager is VC and need to set set as OIDC provider for NSX then
                        this flag should be set as true. This is specific to TKGS. NSX-T 3.0 only"
        required: false
        type: bool
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
- name: Register compute manager with NSX
  nsxt_fabric_compute_managers:
    hostname: "10.192.167.137"
    username: "admin"
    password: "Admin!23Admin"
    validate_certs: False
    display_name: "vCenter"
    server: "10.161.244.213"
    description: "Description of the resource"
    origin_type: vCenter
    credential:
      credential_type: "UsernamePasswordLoginCredential"
      username: "administrator@vsphere.local"
      password: "Admin!23"
      thumbprint: "36:43:34:D9:C2:06:27:4B:EE:C3:4A:AE:23:BF:76:A0:0C:4D:D6:8A:D3:16:55:97:62:07:C2:84:0C:D8:BA:66"
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

def get_fabric_compute_manager_params(args=None):
    args_to_remove = ['state', 'username', 'password', 'port', 'hostname', 'validate_certs']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value == None:
            args.pop(key, None)
    return args

def get_thumb(module):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    wrappedSocket = ssl.wrap_socket(sock)
    try:
      wrappedSocket.connect((module.params['server'], 443))
    except:
      module.fail_json(msg='Connection error while fatching thumbprint for server [%s].' % module.params['server'])
    else:
      der_cert_bin = wrappedSocket.getpeercert(True)
      pem_cert = ssl.DER_cert_to_PEM_cert(wrappedSocket.getpeercert(True))
      print(pem_cert)

      #Thumbprint
      thumb_sha256 = hashlib.sha256(der_cert_bin).hexdigest()
      wrappedSocket.close()
      # The API call expects the Thumbprint in Uppercase. While the API call is fixed,
      # below is a quick fix
      thumbprint = ""
      thumbprint = ':'.join(a+b for a,b in zip(thumb_sha256[::2], thumb_sha256[1::2]))
      return thumbprint.upper()

def get_fabric_compute_managers(module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      (rc, resp) = request(manager_url+ '/fabric/compute-managers', headers=dict(Accept='application/json'),
                      url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Error accessing fabric compute manager. Error [%s]' % (to_native(err)))
    return resp

def get_compute_manager_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, display_name):
    compute_managers = get_fabric_compute_managers(module, manager_url, mgr_username, mgr_password, validate_certs)
    for compute_manager in compute_managers['results']:
        if compute_manager.__contains__('display_name') and compute_manager['display_name'] == display_name:
            return compute_manager
    return None

def wait_till_create(id, module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      down_counter = 0
      while True:
          (rc, resp) = request(manager_url+ '/fabric/compute-managers/%s/status'% id, headers=dict(Accept='application/json'),
                        url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
          if resp['registration_status'] == "REGISTERING":
              time.sleep(10)
          elif resp['registration_status'] == "REGISTERED":
            if resp["connection_status"] == "CONNECTING":
                time.sleep(10)
            elif resp["connection_status"] == "DOWN" and down_counter < 3:
              time.sleep(10)
              down_counter = down_counter + 1
            elif resp["connection_status"] == "UP":
              time.sleep(5)
              return
            else:
              module.fail_json(msg= 'Error connecting to compute manager. Connection status : %s'%(str(resp["connection_status"])))
          else:
              module.fail_json(msg= 'Error in compute manager status: %s'%(str(resp['registration_status'])))
    except Exception as err:
      module.fail_json(msg='Error accessing compute manager status. Error [%s]' % (to_native(err)))

def wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs):
    try:
      while True:
          (rc, resp) = request(manager_url+ '/fabric/compute-managers/%s/status'% id, headers=dict(Accept='application/json'),
                        url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
          time.sleep(10)
    except Exception as err:
      time.sleep(5)
      return

def check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, compute_manager_with_ids):
    existing_compute_manager = get_compute_manager_from_display_name(module, manager_url, mgr_username, mgr_password, validate_certs, compute_manager_with_ids['display_name'])
    if existing_compute_manager is None:
        return False
    if not existing_compute_manager.__contains__('description') and compute_manager_with_ids.__contains__('description'):
        return True
    if existing_compute_manager.__contains__('description') and compute_manager_with_ids.__contains__('description') and \
        existing_compute_manager['description'] != compute_manager_with_ids['description']:
        return True
    if existing_compute_manager['server'] != compute_manager_with_ids['server'] or \
        existing_compute_manager['credential']['thumbprint'] != compute_manager_with_ids['credential']['thumbprint'] or \
        existing_compute_manager['origin_type'] != compute_manager_with_ids['origin_type']:
        return True
    if existing_compute_manager.__contains__('set_as_oidc_provider') and compute_manager_with_ids.__contains__('set_as_oidc_provider') and \
        existing_compute_manager['set_as_oidc_provider'] != compute_manager_with_ids['set_as_oidc_provider']:
        return True
    return False

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(display_name=dict(required=True, type='str'),
                    credential=dict(required=False, type='dict', no_log=True,
                    username=dict(required=False, type='str'),
                    password=dict(required=False, type='str'),
                    thumbprint=dict(required=False, type='str'),
                    asymmetric_credential=dict(required=False, type='str'),
                    credential_verifier=dict(required=False, type='str'),
                    credential_key=dict(required=False, type='str', no_log=True),
                    credential_type=dict(required=True, type='str')),
                    origin_type=dict(required=True, type='str'),
                    description=dict(required=False, type='str'),
                    server=dict(required=True, type='str'),
                    set_as_oidc_provider=dict(required=False, type='bool'),
                    state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  fabric_compute_manager_params = get_fabric_compute_manager_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  display_name = module.params['display_name']
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)
  if not fabric_compute_manager_params['credential'].__contains__('thumbprint'):
      fabric_compute_manager_params['credential']['thumbprint'] = get_thumb(module)

  compute_manager_dict = get_compute_manager_from_display_name (module, manager_url, mgr_username, mgr_password, validate_certs, display_name)
  compute_manager_id, revision = None, None
  if compute_manager_dict:
    compute_manager_id = compute_manager_dict['id']
    revision = compute_manager_dict['_revision']

  if state == 'present':
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    updated = check_for_update(module, manager_url, mgr_username, mgr_password, validate_certs, fabric_compute_manager_params)
    if not updated:
      # add the compute_manager
      request_data = json.dumps(fabric_compute_manager_params)
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(request_data), id='12345')
      try:
          if compute_manager_id:
              module.exit_json(changed=False, id=compute_manager_id, message="Compute manager with display_name %s already exist."% module.params['display_name'])
          (rc, resp) = request(manager_url+ '/fabric/compute-managers', data=request_data, headers=headers, method='POST',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
                module.fail_json(msg="Failed to add compute_manager. Request body [%s]. Error[%s]." % (request_data, to_native(err)))

      wait_till_create(resp['id'], module, manager_url, mgr_username, mgr_password, validate_certs)

      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="fabric compute manager with ip %s created." % module.params['server'])
    else:
      if module.check_mode:
          module.exit_json(changed=True, debug_out=str(json.dumps(fabric_compute_manager_params)), id=compute_manager_id)
      fabric_compute_manager_params['_revision'] = revision # update current revision
      request_data = json.dumps(fabric_compute_manager_params)
      id = compute_manager_id
      try:
          (rc, resp) = request(manager_url+ '/fabric/compute-managers/%s' % id, data=request_data, headers=headers, method='PUT',
                                url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
          module.fail_json(msg="Failed to update compute_manager with id %s. Request body [%s]. Error[%s]." % (id, request_data, to_native(err)))
      module.exit_json(changed=True, id=resp["id"], body= str(resp), message="fabric compute manager with compute manager id %s updated." % id)

  elif state == 'absent':
    # delete the array
    id = compute_manager_id
    if id is None:
        module.exit_json(changed=False, msg='No compute manager exist with display_name %s' % display_name)
    if module.check_mode:
        module.exit_json(changed=True, debug_out=str(json.dumps(fabric_compute_manager_params)), id=id)
    try:
        (rc, resp) = request(manager_url + "/fabric/compute-managers/%s" % id, method='DELETE',
                              url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs)
    except Exception as err:
        module.fail_json(msg="Failed to delete fabric compute manager with id %s. Error[%s]." % (id, to_native(err)))

    wait_till_delete(id, module, manager_url, mgr_username, mgr_password, validate_certs)

    module.exit_json(changed=True, id=id, message="fabric compute manager with compute manager id %s deleted." % id)


if __name__ == '__main__':
    main()
