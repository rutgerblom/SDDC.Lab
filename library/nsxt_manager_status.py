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
module: nsxt_manager_status
short_description: Shows status of nsxt manager
description: Shows status of nsxt manager

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

'''

EXAMPLES = '''
- name: Shows status of nsxt manager
  nsxt_manager_status:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      wait_time: 50
'''

RETURN = '''# '''
import json, time
from datetime import datetime
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils._text import to_native

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(wait_time=dict(required=False, type='int'))
  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  changed = False
  wait_time = 10 # wait till 30 min
  while wait_time < (module.params['wait_time'] *60):
      try:
        current_time = datetime.now()
        (rc, resp) = request(manager_url+ '/cluster-manager/status', headers=dict(Accept='application/json'),
                        url_username=mgr_username, url_password=mgr_password, validate_certs=validate_certs, ignore_errors=True)
        if "overall_status" in resp and resp["overall_status"] == "STABLE":
            module.exit_json(changed=changed, msg= " NSX manager is UP")
        else:
            time_diff = datetime.now() - current_time
            time.sleep(10)
            wait_time = time_diff.seconds + wait_time + 10
      except Exception as err:
        time_diff = datetime.now() - current_time
        time.sleep(10)
        wait_time = time_diff.seconds + wait_time + 10
  module.fail_json(changed=changed, msg= " Error accessing nsx manager. Timed out")

if __name__ == '__main__':
	main()
