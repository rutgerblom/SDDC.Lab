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
module: nsxt_upgrade_groups
short_description: 'Create a group of upgrade units.'
description: 'Create a group of upgrade units.'
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
    type:
        description: 'Component type'
        required: true
        type: str
    parallel:
        description: 'Upgrade Method to specify whether the upgrade is 
                      to be performed serially or in parallel'
        required: false
        type: boolean
    upgrade_unit_count:
        description: 'Count of upgrade units in the group'
        required: false
        type: int
    upgrade_units:
        description: 'List of upgrade units in the group'
        required: false
        type: list
    enabled:
        description: 'Flag to indicate whether upgrade of this group is enabled or not'
        required: false
        type: boolean
    extended_configuration:
        description: 'Extended configuration for the group'
        required: false
        type: list
    resource_type:
        description: 'Resource type'
        required: false
        type: str
    tags:
        description: 'Opaque identifiers meaningful to the API user'
        required: false
        type: list
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
- name: Modifies default upgrade Group
  nsxt_upgrade_groups:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      display_name: "MyUpgradeGroup"
      type: 'MP'
      parallel: True
      enabled: True
      state: Present
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils.common_utils import clean_and_get_params, get_id_from_display_name_results, get_upgrade_orchestrator_node
from ansible.module_utils._text import to_native

def update_group_parameters(module, manager_url, 
                            mgr_username, mgr_password, 
                            validate_certs,
                            upgrade_group_parameters):
  if upgrade_group_parameters.__contains__('upgrade_units'):
    for upgrade_unit in upgrade_group_parameters['upgrade_units']:
      host_name = upgrade_unit.pop('host_name', None)
      upgrade_unit_id = get_id_from_display_name_results(module, manager_url, 
                                     '/upgrade/upgrade-units', mgr_username,
                                     mgr_password, validate_certs, 
                                     ['display_name'], ['id'],
                                     host_name)
      upgrade_unit['id']= upgrade_unit_id
  return upgrade_group_parameters

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(description=dict(type='str', required=False),
                       display_name=dict(type='str', required=True),
                       enabled=dict(type='bool', required=False, default=True),
                       extended_configuration=dict(type='list', required=False),
                       parallel=dict(type='bool', required=False, default=True),
                       resource_type=dict(type='str', required=False),
                       tags=dict(type='list', required=False),
                       type=dict(type='str', required=True),
                       upgrade_unit_count=dict(type='int', required=False),
                       upgrade_units=dict(type='list', required=False),
                    state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  upgrade_group_params = clean_and_get_params(module.params.copy())
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']

  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'

  mgr_hostname = get_upgrade_orchestrator_node(module, mgr_hostname, mgr_username, 
                                            mgr_password, headers, validate_certs)

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)


  upgrade_group_params = update_group_parameters(module, manager_url, mgr_username, 
                                                 mgr_password, validate_certs, 
                                                 upgrade_group_params)

  upgrade_unit_group_id = get_id_from_display_name_results(module, manager_url, 
                                        '/upgrade/upgrade-unit-groups', mgr_username, 
                                        mgr_password, validate_certs, ['display_name'], 
                                        ['id'], upgrade_group_params['display_name'], 
                                        False)
  if state == 'present':
    # create a new upgrade group or modify the existing one 
    if module.check_mode:
      module.exit_json(changed=False, debug_out='A new upgrade unit will be created with'
                                                ' name: %s' % module.params['display_name'])
    request_data = json.dumps(upgrade_group_params)
    if upgrade_unit_group_id is None:
      try:
        (rc, resp) = request(manager_url + '/upgrade/upgrade-unit-groups', 
                            data=request_data, headers=headers, method='POST', 
                            url_username=mgr_username, url_password=mgr_password, 
                            validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
        module.fail_json(msg="Failed to add upgrade group. Error[%s]." % to_native(err))

      time.sleep(5)
      module.exit_json(changed=True, message="Upgrade group is added successfully.")
    else:
      try:
        (rc, resp) = request(manager_url + '/upgrade/upgrade-unit-'
                            'groups/%s' % upgrade_unit_group_id,
                            data=request_data, headers=headers, method='PUT', 
                            url_username=mgr_username, url_password=mgr_password, 
                            validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
        module.fail_json(msg="Failed to modify upgrade group. Error[%s]." % to_native(err))

      time.sleep(5)
      module.exit_json(changed=True, message='Upgrade group with group id '
                       '%s is updated.' % upgrade_unit_group_id)
  elif state == 'absent':
    # remove an existing upgrade group
    try:
       (rc, resp) = request(manager_url+ '/upgrade/upgrade-unit-groups'
                            '/%s' % upgrade_unit_group_id, 
                            data='', headers=headers, method='DELETE',
                            url_username=mgr_username, url_password=mgr_password, 
                            validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg='Failed while deleting the upgrade'
                           ' group. Error[%s].' % to_native(err))

    time.sleep(5)
    module.exit_json(changed=True, message='Upgrade group with group id '
                     '%s is deleted.' % upgrade_unit_group_id)


if __name__ == '__main__':
    main()
