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
module: nsxt_upgrade_postchecks
short_description: 'Execute post-upgrade checks'
description: "Run pre-defined checks to identify potential issues which can be 
              encountered after an upgrade. The results
              of the checks are added to the respective upgrade units aggregate-info. The 
              progress and status of operation is part of upgrade status summary of 
              individual components."
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
        choices:
            - host
            - mp
            - edge
        description: "Component type on which post upgrade is to be run.
        required: true   
'''

EXAMPLES = '''
- name: Runs post-upgrade checks
  nsxt_upgrade_postchecks:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      component_type: 'mp'
'''

RETURN = '''# '''

import json, time
from csv import reader
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils.common_utils import get_attribute_from_endpoint, clean_and_get_params, get_upgrade_orchestrator_node
from ansible.module_utils._text import to_native

def wait_for_post_upgrade_checks_to_execute(module, manager_url, endpoint, mgr_username,
                                  mgr_password, validate_certs, component_type, 
                                  time_out=10800):
  '''
    params:
    - endpoint: API endpoint.
    - attribute_list: The attribute whose value should become the desired attribute value
    - desired_attribute_value: The desired attribute value
    
    Function will wait till the attribute value derived from going deep to attribute list
    becomes equal to desired_attribute_value.
   '''
  operation_time = 0
  while True:
    try:
      (rc, resp) = request(manager_url + endpoint, headers=dict(Accept='application/json'),
                           url_username=mgr_username, url_password=mgr_password, 
                           validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
       module.fail_json(msg="Failed while polling for post upgrade checks to complete. Error[%s]." % to_native(err))
    if resp.__contains__('results'):
      flag = True
      results = resp['results']
      for result in results:
        if result['post_upgrade_status']['status'] != 'COMPLETED' and \
           result['type'] == component_type.upper() and \
           result['upgrade_unit_count'] > 0 and \
           result['status'] != 'NOT_STARTED':
          flag = False
      if flag:
        return None
    time.sleep(15)
    operation_time = operation_time + 15
    if operation_time > time_out:
      raise Exception('Operation timed out.')

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(timeout=dict(type='int', required=False),
                      component_type=dict(required=True, choices=['mp', 'host', 'edge']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  timeout = module.params['timeout']
  component_type= module.params['component_type']

  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'

  mgr_hostname = get_upgrade_orchestrator_node(module, mgr_hostname, mgr_username, 
                                            mgr_password, headers, validate_certs)

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  #if state == 'present':
  # Runs post upgrade checks
  if module.check_mode:
    module.exit_json(changed=False, debug_out='Post upgrade checks will be executed.', 
                     id='Post upgrade checks')
  try:
    (rc, resp) = request(manager_url + '/upgrade/%s?action=execute_post_upgrade_'
                        'checks' % component_type.upper(), data='', headers=headers,
                        method='POST', url_username=mgr_username, 
                        url_password=mgr_password, validate_certs=validate_certs, 
                        ignore_errors=True)
  except Exception as err:
    module.fail_json(msg="Failed to execute post upgrade checks. Error[%s]." % to_native(err))

  try:
    if timeout is None:
      wait_for_post_upgrade_checks_to_execute(module, manager_url, '/upgrade/upgrade-unit-groups'
                                             '/aggregate-info', mgr_username, mgr_password, 
                                             validate_certs, component_type)
    else:
      wait_for_post_upgrade_checks_to_execute(module, manager_url, '/upgrade/upgrade-unit-groups'
                                             '/aggregate-info', mgr_username, mgr_password,
                                             validate_certs, component_type, timeout)
  except Exception as err:
      module.fail_json(msg='Error while polling for execution of post upgrade'
                             ' checks. Error [%s]' % to_native(err))
  time.sleep(5)
  changed = True
  try:
    (rc, resp) = request(manager_url+ '/upgrade/upgrade-unit-groups/aggregate-info', 
                         url_username=mgr_username, url_password=mgr_password, 
                         validate_certs=validate_certs)
  except Exception as err:
    module.fail_json(msg='Post upgrade checks were executed successfully but error'
                  ' occured while retrieving the results. Error [%s]' % (to_native(err)))
  module.exit_json(changed=changed, message='Post upgrade checks are performed successfully:\n'
                     '----------------------------\n' + str(resp))

if __name__ == '__main__':
    main()
