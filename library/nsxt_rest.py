#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, sky-joker
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

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: nsxt_rest
short_description: Direct access to the NSX REST API
description:
    - Provides direct access to the NSX REST API to execute the API.
author:
    - sky-joker (@sky-joker)
requirements:
    - "python >= 2.7"
options:
    hostname:
        description: "Deployed NSX manager hostname."
        required: true
        type: str
    username:
        description: "The username to authenticate with the NSX manager."
        required: true
        type: str
    password:
        description: "The password to authenticate with the NSX manager."
        required: true
        type: str
    path:
        description: "URI being used to execute API calls."
        required: true
        type: str
    method:
        description:
            - "The HTTP method of the request."
        required: false
        choices:
            - get
            - post
            - put
            - patch
            - delete
        default: get
        type: str
    src:
        description:
            - "The absolute path to the file containing the request body(payload) to be sent to the NSX REST API."
            - "If this option isn't used, use the C(content) option instead."
            - "If this option is used, the C(content) option is ignored."
        required: false
        type: str
    content:
        description:
            - "The request body(payload) to be sent to the NSX REST API."
            - "If this option isn't used, use the C(src) option instead."
        required: false
        type: raw
'''

EXAMPLES = '''
- name: create a new segment
  nsxt_rest:
    hostname: "{{ nsxt_hostname }}"
    username: "{{ nsxt_username }}"
    password: "{{ nsxt_password }}"
    validate_certs: false
    method: patch
    path: /policy/api/v1/infra/segments/segment
    content:
      {
        "display_name": "segment",
        "subnets": [
          {
            "gateway_address": "192.168.0.1/24"
          }
        ],
      }

- name: get segment information
  nsxt_rest:
    hostname: "{{ nsxt_hostname }}"
    username: "{{ nsxt_username }}"
    password: "{{ nsxt_password }}"
    validate_certs: false
    method: get
    path: /policy/api/v1/infra/segments/segment
  register: get_segment_information_result

- name: delete a segment
  nsxt_rest:
    hostname: "{{ nsxt_hostname }}"
    username: "{{ nsxt_username }}"
    password: "{{ nsxt_password }}"
    validate_certs: false
    method: delete
    path: /policy/api/v1/infra/segments/segment
'''

RETURN = '''
body:
    description: dictionary of requested result information
    returned: always
    type: dict
    sample:
      {
          "_create_time": 1588405512111,
          "_create_user": "admin",
          "_last_modified_time": 1588405613884,
          "_last_modified_user": "admin",
          "_protection": "NOT_PROTECTED",
          "_revision": 1,
          "_system_owned": false,
          "admin_state": "UP",
          "display_name": "segment",
          "id": "segment",
          "marked_for_delete": false,
          "overridden": false,
          "parent_path": "/infra",
          "path": "/infra/segments/segment",
          "relative_path": "segment",
          "replication_mode": "MTEP",
          "resource_type": "Segment",
          "subnets": [
              {
                  "gateway_address": "192.168.0.1/24",
                  "network": "192.168.0.0/24"
              }
          ],
          "type": "DISCONNECTED",
          "unique_id": "0361313c-20f0-42ba-aa77-e090277a50ac"
      }
'''


import os
import json
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec
from ansible.module_utils.urls import basic_auth_header, fetch_url


class VMwareNSXTRest():
    def __init__(self, module):
        self.module = module
        self.mgr_hostname = module.params["hostname"]
        self.mgr_username = module.params["username"]
        self.mgr_password = module.params["password"]
        self.path = module.params["path"]
        self.method = module.params["method"]
        self.src = module.params["src"]
        self.content = module.params["content"]

        self.manager_url = "https://{}".format(self.mgr_hostname)
        self.headers = {
            "authorization": basic_auth_header(self.mgr_username, self.mgr_password),
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        if self.src:
            if os.path.isfile(self.src):
                try:
                    with open(self.src, "r") as f:
                        self.content = json.loads(f.read())
                except Exception as err:
                    self.module.fail_json(msg="src read error: %s" % err)
            else:
                self.module.fail_json(msg="cannot find/access src '%s'" % self.src)

    def error_code_check(self, info):
        status = info.get('status')
        if status >= 400:
            self.module.fail_json(msg="error_code: %s, error_message: %s"
                                      % (status, json.loads(info.get('body'))['error_message']))

        if status == -1:
            self.module.fail_json(msg="error_code: %s, error_message: %s" % (status, info.get('msg')))

    def operate_nsxt(self, method, ignore_errors=False):
        try:
            (resp, info) = fetch_url(self.module, self.manager_url + self.path, method=method.upper(), headers=self.headers,
                                     data=json.dumps(self.content))
        except Exception as err:
            self.module.fail_json(msg="nsxt rest api request error: %s, error url: %s"
                                      % (err, self.manager_url + self.path))

        if ignore_errors is False:
            self.error_code_check(info)

        resp_body = resp.read() if 'read' in dir(resp) else False
        if resp_body:
            return json.loads(resp_body)
        else:
            return ""

    def execute(self):
        if self.method == "get":
            resp = self.operate_nsxt(method=self.method)
            self.module.exit_json(changed=False, body=resp)

        if self.method == "post" or self.method == "put" or self.method == "patch":
            before_resp = self.operate_nsxt(method="get", ignore_errors=True)
            if before_resp:
                before_revision = before_resp["_revision"]
            else:
                before_revision = ""

            _ = self.operate_nsxt(method=self.method)

            after_resp = self.operate_nsxt(method="get")
            after_revision = after_resp["_revision"]

            if before_revision == after_revision:
                self.module.exit_json(changed=False, body=after_resp)
            else:
                self.module.exit_json(changed=True, body=after_resp)

        if self.method == "delete":
            resp = self.operate_nsxt(method="get", ignore_errors=True)
            if resp:
                resp = self.operate_nsxt(method=self.method)
                self.module.exit_json(changed=True, body=resp)
            else:
                self.module.exit_json(changed=False, body=resp)


def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(path=dict(type='str', required=True),
                         method=dict(type='str', choices=['get', 'post', 'put', 'patch', 'delete'], default='get'),
                         src=dict(type='str'),
                         content=dict(type='raw'),)

    module = AnsibleModule(argument_spec, supports_check_mode=True)

    vmware_nsx_rest = VMwareNSXTRest(module)
    vmware_nsx_rest.execute()


if __name__ == '__main__':
    main()
