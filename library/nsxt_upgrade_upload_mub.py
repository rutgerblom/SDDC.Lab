#!/usr/bin/env python
#
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

from __future__ import absolute_import, division, print_function
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: nsxt_upgrade_upload_mub
short_description: 'Uploads upgrade mub'
description: "Uploads upgrade mub"
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
    file:
        description: 'The path of the mub file'
        required: false
        type: str
    url:
        description: 'URL of MUB file'
        required: false
        type: str
'''

EXAMPLES = '''
- name: Upload MUB
  upload_mub:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      url: "https://file-server.com/file.mub"
'''

RETURN = '''# '''
import atexit
import mmap
import os

import json
import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils.common_utils import wait_for_operation_to_execute
from ansible.module_utils._text import to_native


def get_upload_mub_params(args=None):
    args_to_remove = ['username', 'password', 'port', 'hostname', 'validate_certs', 'timeout']
    for key in args_to_remove:
        args.pop(key, None)
    for key, value in args.copy().items():
        if value is None:
            args.pop(key, None)
    return args

def get_mgr_ip_upgrade_enabled(module, mgr_url, mgr_username, mgr_password,
                               headers, validate_certs):
    try:
        (rc, resp) = request(mgr_url + '/node/services/install-upgrade',
               headers=headers, url_username=mgr_username, url_password=mgr_password, 
                             validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
        module.fail_json(changed=True, msg='Error getting ip address where '
                        'upgrade is enabled. Error: {}'.format(err))
    return resp['service_properties']['enabled_on'];

def wait_till_upload_done(module, bundle_id, mgr_url, mgr_username, mgr_password, 
                          headers, validate_certs):
    try:
       while True:
         (rc, resp) = request(mgr_url + '/upgrade/bundles/%s/upload-status'% bundle_id,
                             headers=headers, url_username=mgr_username, 
                             url_password=mgr_password, validate_certs=validate_certs, 
                             ignore_errors=True)
         if resp['status'] == 'FAILED':
             module.fail_json(msg='Failed to upload upgrade bunlde. Error: %s' % 
                              resp['detailed_status'])
         if resp['status'] == 'SUCCESS':
             time.sleep(5)
             return
    except Exception as err:
          module.fail_json(changed=True, msg="Error: %s" % err)

def upload_mub(module, mgr_url, mgr_username, mgr_password, validate_certs, request_data, 
               headers, ip_address, timeout=10800):
    endpoint = '/upgrade/bundles'
    mub_type = 'url'
    #headers = {}
    if module.params['file'] is not None:
        mub_type = 'file'
        endpoint = endpoint +'?action=upload'
    if mub_type == 'file':
        file_path = module.params['file']
        try:
            file_data = open(file_path, 'rb')
            atexit.register(file_data.close)
        except Exception as e:
            module.fail_json(msg='failed to open mub file %s Error: %s' %
                             (file_path, to_native(e)))

        if os.stat(file_path).st_size == 0:
            request_data = ''
        else:
            request_data = mmap.mmap(file_data.fileno(), 0, access=mmap.ACCESS_READ)
            atexit.register(request_data.close)


        from urllib3 import encode_multipart_formdata
        from urllib3.fields import RequestField

        with open(file_path, 'rb') as src_file:
             rf = RequestField('file', src_file.read(), os.path.basename(src_file.name))
             rf.make_multipart()
             body, content_type = encode_multipart_formdata([rf])
  
        headers['Content-Type'] = content_type
        headers['Content-length'] = len(body)

    if mub_type == 'url':
      body = request_data

    try:
        (rc, resp) = request(mgr_url + endpoint, data=body, headers=headers, 
                             method='POST', url_username=mgr_username, 
                             url_password=mgr_password, validate_certs=validate_certs, 
                             ignore_errors=True)
        if rc == 200:
            bundle_id = 'latest'#resp['bundle_id']
            headers = dict(Accept="application/json")
            headers['Content-Type'] = 'application/json'
            try:
                wait_for_operation_to_execute(mgr_url, 
                    '/upgrade/bundles/%s/upload-status'% bundle_id, 
                    mgr_username, mgr_password, validate_certs, 
                    ['status'], ['SUCCESS'], ['FAILED'])
            except Exception as err:
                module.fail_json(msg='Error while uploading upgrade bundle. Error [%s]' % to_native(err))
            module.exit_json(changed=True, ip_address=ip_address, response=resp, 
            message='The upgrade bundle %s got uploaded successfully.' % module.params[mub_type])
        else:
            module.fail_json(msg='Failed to run upload mub. response code: {}'
                                 ' response: {}'.format(rc, resp))
    except Exception as err:
        module.fail_json(changed=True, msg="Error: {}".format(err))


def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(url=dict(type='str'),
                         file=dict(type='str'),
                         timeout=dict(type='int', required=False))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, 
                           required_one_of=[('url', 'file')])
    upgrade_params = get_upload_mub_params(module.params.copy())

    mgr_hostname = module.params['hostname']
    mgr_username = module.params['username']
    mgr_password = module.params['password']
    validate_certs = module.params['validate_certs']
    timeout = module.params['timeout']
    manager_url = 'https://{}/api/v1'.format(mgr_hostname)
    headers = dict(Accept="application/json")
    headers['Content-Type'] = 'application/json'
    request_data = json.dumps(upgrade_params)
    node_ip_address = get_mgr_ip_upgrade_enabled(module, manager_url, mgr_username, mgr_password,
                                                 headers, validate_certs)
    update_node_url = 'https://{}/api/v1'.format(node_ip_address)
    if timeout is not None:
        upload_mub(module, update_node_url, mgr_username, mgr_password, validate_certs, request_data, 
               headers, node_ip_address, timeout)
    else:
        upload_mub(module, update_node_url, mgr_username, mgr_password, validate_certs, request_data, 
               headers, node_ip_address)

if __name__ == '__main__':
    main()
