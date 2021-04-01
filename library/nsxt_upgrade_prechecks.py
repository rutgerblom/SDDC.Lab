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
module: nsxt_upgrade_prechecks
short_description: 'Execute pre-upgrade checks'
description: "Run pre-defined checks to identify potential issues which can be 
              encountered during an upgrade or can cause an upgrade to fail. The results 
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
    timeout:
        description: 'Timeout while polling for prechecks to complete'
        required: false
        type: int
    state:
        choices:
            - present
            - absent
        description: "State can be either 'present' or 'absent'.
                      'present' is used to run pre upgrade checks.
                      'absent' is used to abort preupgrade checks."
        required: true   
'''

EXAMPLES = '''
- name: Runs and aborts pre-upgrade checks
  nsxt_upgrade_prechecks:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      state: 'present'
'''

RETURN = '''# '''

import json, time
from csv import reader
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils.common_utils import get_attribute_from_endpoint, clean_and_get_params, get_upgrade_orchestrator_node
from ansible.module_utils._text import to_native

def wait_for_pre_upgrade_checks_to_execute(module, manager_url, endpoint, mgr_username,
                                  mgr_password, validate_certs, time_out=10800):
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
       pass
    if resp.__contains__('component_status'):
      flag = True
      component_statuses = resp['component_status']
      for component_status in component_statuses:
        if component_status['pre_upgrade_status']['status'] == 'ABORTED':
          module.exit_json(changed= False, message='Pre upgrade checks started to run,'
                                                   ' but aborted before they could finish.')
        if component_status['pre_upgrade_status']['status'] != 'COMPLETED':
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
                      state=dict(required=True, choices=['present', 'absent']))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  upgrade_prechecks_params = clean_and_get_params(module.params.copy(), ['timeout'])
  state = module.params['state']
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  timeout = module.params['timeout']

  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'
  
  mgr_hostname = get_upgrade_orchestrator_node(module, mgr_hostname, mgr_username, 
                                            mgr_password, headers, validate_certs)

  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  if state == 'present':
    # Runs pre upgrade checks
    if module.check_mode:
      module.exit_json(changed=False, debug_out='Pre upgrade checks will be executed.', 
                       id='Pre upgrade checks')
    request_data = json.dumps(upgrade_prechecks_params)
    try:
      (rc, resp) = request(manager_url + '/upgrade?action=execute_pre_upgrade_checks', 
                           data='', headers=headers, method='POST', 
                           url_username=mgr_username, url_password=mgr_password, 
                           validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg="Failed to execute pre upgrade checks. Error[%s]." % to_native(err))

    try:
      if timeout is None:
        wait_for_pre_upgrade_checks_to_execute(module, manager_url, '/upgrade/status-summary',
                          mgr_username, mgr_password, validate_certs)
      else:
        wait_for_pre_upgrade_checks_to_execute(module, manager_url, '/upgrade/status-summary',
                          mgr_username, mgr_password, validate_certs, timeout)
    except Exception as err:
        module.fail_json(msg='Error while polling for execution of pre upgrade'
                             ' checks. Error [%s]' % to_native(err))
    time.sleep(5)
    changed = False
    try:
      (rc, resp) = request(manager_url+ '/upgrade/pre-upgrade-checks/failures',
                           url_username=mgr_username, url_password=mgr_password, 
                           validate_certs=validate_certs)
    except Exception as err:
      module.fail_json(msg='Pre upgrade checks were executed successfully but error'
                  ' occured while retrieving the results. Error [%s]' % (to_native(err)))
    # Fail module in case any pre upgrade check fails
    prechecks_failure = False
    if  'results' in resp:
      for result in resp['results']:
        if  'type' in result and result['type'] == 'FAILURE':
          prechecks_failure = True
    if prechecks_failure:
      module.fail_json(msg='Pre upgrade checks are performed successsfully. Found errors. '
                            'Thus, you cannot proceed. To get full report run upgrade groups '
                            'facts module. Precheck results: %s' % str(resp))
    module.exit_json(changed=changed, message='Pre upgrade checks are performed successfully:'
                     ' Failures are listed. To get full report run upgrade groups '
                     'facts module.' + str(resp))
  elif state == 'absent':
    # Aborts pre upgrade checks
    try:
       (rc, resp) = request(manager_url + '/upgrade?action=abort_pre_upgrade_checks', 
                            data='', headers=headers, method='POST',
                            url_username=mgr_username, url_password=mgr_password, 
                            validate_certs=validate_certs, ignore_errors=True)
    except Exception as err:
      module.fail_json(msg="Failed to abort running pre upgrade checks. Error[%s]." % to_native(err))

    time.sleep(5)
    module.exit_json(changed=True, message="Upgrade prechecks are aborted.")


if __name__ == '__main__':
    main()
