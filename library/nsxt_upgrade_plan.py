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
module: nsxt_upgrade_plan
short_description: 'Upgrade plan settings for the component'
description: 'Upgrade plan settings for the component'
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
    component_type:
        description: 'Component whose upgrade plan is to be changed'
        choices:
            - host
            - edge
            - mp
        required: true
        type: str
    parallel:
        description: 'Upgrade Method to specify whether the upgrade is 
                      to be performed serially or in parallel'
        required: true
        type: boolean
    pause_after_each_group:
        description: 'Flag to indicate whether to pause the upgrade after
                      upgrade of each group is completed'
        required: true
        type: boolean
    pause_on_error:
        description: 'Flag to indicate whether to pause the upgrade plan 
                      execution when an error occurs'
        required: true
        type: boolean
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
- name: Modifies default upgrade plan
  nsxt_upgrade_plan:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      component_type: 'host'
      parallel: True
      pause_after_each_group: True
      pause_on_error: True
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils.common_utils import get_attribute_from_endpoint, clean_and_get_params, get_upgrade_orchestrator_node
from ansible.module_utils._text import to_native


def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(component_type=dict(type='str', required=True, choices=['host', 'edge', 'mp']),
                       parallel=dict(type='bool', required=False),
                       pause_after_each_group=dict(type='bool', required=False),
                       pause_on_error=dict(type='bool', required=False),
                    state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  upgrade_plan_params = clean_and_get_params(module.params.copy(), ['component_type'])
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  component_type = module.params['component_type']

  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'

  mgr_hostname = get_upgrade_orchestrator_node(module, mgr_hostname, mgr_username, 
                                            mgr_password, headers, validate_certs)

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  if state == 'present':
    # update the default upgrade plan
    if module.check_mode:
      module.exit_json(changed=False, debug_out='Upgrade Plan will be modified.'
        ' parallel: %s, pause_after_each_group: %s, pause_on_error: %s' % 
        (module.params['parallel'], module.params['pause_after_each_group'], 
        module.params['pause_on_error']), id=module.params['component_type'])
    request_data = json.dumps(upgrade_plan_params)
    try:
      (rc, resp) = request(manager_url+ '/upgrade/plan/%s/settings' % component_type.upper(), 
                           data=request_data, headers=headers, method='PUT', 
                           url_username=mgr_username, url_password=mgr_password, 
                           validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg="Failed to update upgrade plan. Error[%s]." % to_native(err))

    time.sleep(5)
    module.exit_json(changed=True, message="Upgrade plan is updated.")

  elif state == 'absent':
    # reset to default upgrade plan
    try:
       (rc, resp) = request(manager_url+ '/upgrade/plan?action=reset&'
                            'component_type=%s' % component_type.upper(), 
                            data='', headers=headers, method='POST',
                            url_username=mgr_username, url_password=mgr_password, 
                            validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg="Failed while reseting the upgrade plan. Error[%s]." % to_native(err))

    time.sleep(5)
    module.exit_json(changed=True, message="Upgrade plan is reset.")


if __name__ == '__main__':
    main()
