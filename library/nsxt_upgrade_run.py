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
module: nsxt_upgrade_run
short_description: 'Start the upgrade'
description: 'Upgrade will start as per the upgrade plan.'
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
    paused_upgrade:
        description: 'Mode of upgrade'
        required: true
        type: bool
'''

EXAMPLES = '''
- name: Runs the upgrade
  nsxt_upgrade_run:
      hostname: "10.192.167.137"
      username: "admin"
      password: "Admin!23Admin"
      validate_certs: False
      paused_upgrade: True
'''

RETURN = '''# '''

import json, time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.vmware_nsxt import vmware_argument_spec, request
from ansible.module_utils.common_utils import get_attribute_from_endpoint, clean_and_get_params, get_upgrade_orchestrator_node
from ansible.module_utils._text import to_native

def get_upgrade_status(module, manager_url, mgr_username, mgr_password, validate_certs):
  '''
  Get the current status of upgrade at the start.
  Doesn't upgrade if any component is in progress 
  or system is already upgraded.
  '''
  no_of_checks = 0
  while True:
    upgrade_status = get_attribute_from_endpoint(module, manager_url, '/upgrade/status-summary',
                     mgr_username, mgr_password, validate_certs, 'overall_upgrade_status', 
                     False)
    no_of_checks = no_of_checks + 1
    if upgrade_status == 'IN_PROGRESS' or upgrade_status == 'PAUSING':
      if no_of_checks > 2:
        module.fail_json(msg='Upgrade is in state: %s, can\'t continue' % upgrade_status)
    elif upgrade_status == 'SUCCESS':
      module.exit_json(changed=False, message='Upgrade state is SUCCESS. No need to'
                    ' continue.')
    else:
      return upgrade_status
    time.sleep(20)

def decide_next_step(module, manager_url, mgr_username, mgr_password, 
                     validate_certs, can_continue, is_failed):
  '''
  params:
  - can_continue: if upgrade can be continued 
  - is_failed: Is there any component Failure
  return:
  - Decides the next operation to be done based on 
    can_continue and is_failed values 
  '''
  if can_continue and is_failed:
    return
  elif can_continue and not is_failed:
    return
  elif not can_continue and is_failed:
    raise Exception('Upgrade failed. Please run upgrade status summary'
                    ' to see the reason of upgrade failure.')
  else:
    time.sleep(15)
    try:
      upgrade_status = get_attribute_from_endpoint(module, manager_url, '/upgrade/summary',
                        mgr_username, mgr_password, validate_certs, 'upgrade_status',
                        False)
    except Exception as err:
      return
    if upgrade_status == 'SUCCESS':
      module.exit_json(changed=True, message='System has been upgraded successfully!!!')
    elif upgrade_status == 'IN_PROGRESS' or upgrade_status == 'PAUSING' or upgrade_status == 'PAUSED':
      return
    else:
      module.fail_json(msg='All components till last one are upgraded. Still upgrade status'
        ' is %s. Please run upgrade status summary to see the reason.' % upgrade_status)


def check_continuity(module, manager_url, mgr_username, mgr_password, validate_certs):
  '''
  Returns:
  Based on the output of upgrade status summary API, gets the
  checks and returns if upgrade can be continued and
  if there is any component fail in the upgrade
  '''
  try:
    component_status_list = get_attribute_from_endpoint(module, manager_url, 
                          '/upgrade/status-summary', mgr_username, mgr_password,
                          validate_certs, 'component_status', False)
  except Exception as err:
    can_continue = True
    is_failed = True
    return can_continue, is_failed
  try:
    can_continue = True
    for component_status in component_status_list:
      if component_status['status'] == 'IN_PROGRESS' or \
         component_status['status'] == 'PAUSING':
        can_continue = False
        break
    if not can_continue:
      return can_continue, False
    else:
      is_failed = False
      found_not_started = False
      for component_status in component_status_list[::-1]:
        if component_status['status'] == 'NOT_STARTED':
          found_not_started = True
        elif component_status['status'] == 'PAUSED':
          can_continue = True
          is_failed = False
          return can_continue, is_failed
        elif component_status['status'] == 'SUCCESS':
          if not found_not_started:
            can_continue = False
            is_failed = False
            return can_continue, is_failed
          else:
            can_continue = True
            is_failed = False
            return can_continue, is_failed
        elif component_status['status'] == 'FAILED':
          can_continue = False
          is_failed = True
          return can_continue, is_failed
        elif component_status['status'] == 'IN_PROGRESS' or \
        component_status['status'] == 'PAUSING':
          can_continue = False
          is_failed = False
          return can_continue, is_failed
        else:
          return True, True
  except Exception as err:
    can_continue = True
    is_failed = True
    return can_continue, is_failed

def main():
  argument_spec = vmware_argument_spec()
  argument_spec.update(paused_upgrade=dict(type='bool', required=True))

  module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
  mgr_hostname = module.params['hostname']
  mgr_username = module.params['username']
  mgr_password = module.params['password']
  validate_certs = module.params['validate_certs']
  paused_upgrade = module.params['paused_upgrade']
  
  headers = dict(Accept="application/json")
  headers['Content-Type'] = 'application/json'
  
  mgr_hostname = get_upgrade_orchestrator_node(module, mgr_hostname, mgr_username, 
                                            mgr_password, headers, validate_certs)
  
  manager_url = 'https://{}/api/v1'.format(mgr_hostname)

  if module.check_mode:
    if paused_upgrade:
      module.exit_json(changed=False, debug_out='NSX-T will upgrade with pauses.')
    else:
      module.exit_json(changed=False, debug_out='NSX-T will upgrade without pauses.')

  # If paused_upgrade is not true i.e auto mode
  if not paused_upgrade:
    while True:
      upgrade_status = get_upgrade_status(module, manager_url, mgr_username,
                                          mgr_password, validate_certs)
      if upgrade_status == 'NOT_STARTED':
        try:
          (rc, resp) = request(manager_url+ '/upgrade/plan?action=start', 
                         data='', headers=headers, method='POST', 
                         url_username=mgr_username, url_password=mgr_password, 
                         validate_certs=validate_certs, ignore_errors=True)
        except Exception as err:
          module.fail_json(msg="Failed while upgrading. Error[%s]." % to_native(err))
      else:
        try:
          (rc, resp) = request(manager_url+ '/upgrade/plan?action=continue', 
                         data='', headers=headers, method='POST', 
                         url_username=mgr_username, url_password=mgr_password, 
                         validate_certs=validate_certs, ignore_errors=True)
        except Exception as err:
          module.fail_json(msg="Failed while upgrading. Error[%s]." % to_native(err))

      time.sleep(10)
      while True:
        try:
          can_continue, is_failed = check_continuity(module, manager_url, mgr_username,
                                                     mgr_password, validate_certs)
          decide_next_step(module, manager_url, mgr_username, mgr_password, 
                           validate_certs, can_continue, is_failed)
          if can_continue and not is_failed:
            break
          time.sleep(10)
        except Exception as err:
          module.fail_json(msg='Upgrade failed. Error: [%s]' % to_native(err))
  else:
    # Paused upgrade i.e manual mode
    upgrade_status = get_upgrade_status(module, manager_url, mgr_username,
                                          mgr_password, validate_certs)
    if upgrade_status == 'NOT_STARTED':
      try:
        (rc, resp) = request(manager_url+ '/upgrade/plan?action=start', 
                     data='', headers=headers, method='POST', 
                     url_username=mgr_username, url_password=mgr_password, 
                     validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
        module.fail_json(msg="Failed while upgrading. Error[%s]." % to_native(err))
    else:
      try:
        (rc, resp) = request(manager_url+ '/upgrade/plan?action=continue', 
                     data='', headers=headers, method='POST', 
                     url_username=mgr_username, url_password=mgr_password, 
                     validate_certs=validate_certs, ignore_errors=True)
      except Exception as err:
        module.fail_json(msg="Failed while upgrading. Error[%s]." % to_native(err))
    time.sleep(10)
    while True:
      try:
        can_continue, is_failed = check_continuity(module, manager_url, mgr_username,
                                                   mgr_password, validate_certs)
        decide_next_step(module, manager_url, mgr_username, mgr_password, 
                         validate_certs, can_continue, is_failed)
        if can_continue and not is_failed:
          break
        time.sleep(10)
      except Exception as err:
        module.fail_json(msg='Upgrade failed. Error: [%s]' % to_native(err))
    module.exit_json(changed=True, message='A component has been upgraded successfully.'
                                           ' Whole system is not. Please run the module'
                                           ' again till the time whole system is'
                                           ' not upgraded.')

if __name__ == '__main__':
    main()
