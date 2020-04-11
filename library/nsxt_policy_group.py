#!/usr/bin/env python
#
# Copyright 2018 VMware, Inc.
# SPDX-License-Identifier: BSD-2-Clause OR GPL-3.0-only
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
# OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: nsxt_policy_group
short_description: Create or Delete a Policy Policy Group
description:
    Creates or deletes a Policy Policy Group.
    Required attributes include id and display_name.
version_added: "2.8"
author: Gautam Verma
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
        description: The password to authenticate with the NSX manager
        required: true
        type: str
    display_name:
        description:
            - Display name.
            - If resource ID is not specified, display_name will be used as ID.
        required: false
        type: str
    state:
        choices:
        - present
        - absent
        description: "State can be either 'present' or 'absent'.
                    'present' is used to create or update resource.
                    'absent' is used to delete resource."
        required: true
    validate_certs:
        description: Enable server certificate verification.
        type: bool
        default: False
    tags:
        description: Opaque identifiers meaningful to the API user.
        type: dict
        suboptions:
            scope:
                description: Tag scope.
                required: true
                type: str
            tag:
                description: Tag value.
                required: true
                type: str
    do_wait_till_create:
        type: bool
        default: false
        description:
            - Can be used to wait for the realization of subresource before the
              request to create the next resource is sent to the Manager.
            - Can be specified for each subresource.
    id:
        description: The id of the Policy Policy Group.
        required: false
        type: str
    description:
        description: Policy Group description.
        type: str
    domain_id:
        description: Domain ID.
        type: str
    expression:
        description:
            - The expression list must follow below criteria
                - 1. A non-empty expression list, must be of odd size.
                  In a list, with indices starting from 0, all
                  non-conjunction expressions must be at
                  even indices, separated by a conjunction expression
                  at odd indices.
                - 2. The total of ConditionExpression and
                  NestedExpression in a list should not exceed 5.
                - 3. The total of IPAddressExpression,
                  MACAddressExpression, external IDs in an
                  ExternalIDExpression and paths in a PathExpression
                  must not exceed 500.
                - 4. Each expression must be a valid Expression. See
                  the definition of the Expression type for more
                  information.
        type: list
    extended_expression:
        description:
            - Extended Expression allows additional higher level context to be
              specified for grouping criteria (e.g. user AD group). This field
              allow users to specified user context as the source of a firewall
              rule for IDFW feature.  Current version only support a single
              IdentityGroupExpression. In the future, this might expand to
              support other conjunction and non-conjunction expression.
            - The extended expression list must follow below criteria
                - 1. Contains a single IdentityGroupExpression. No conjunction
                  expression is supported
                - 2. No other non-conjunction expression is supported, except
                  for IdentityGroupExpression
                - 3. Each expression must be a valid Expression. See the
                  definition of the Expression type for more information
                - 4. Extended expression are implicitly AND with expression
                - 5. No nesting can be supported if this value is used
                - 6. If a Group is using extended expression, this group must
                  be the only member in the source field of an communication
                  map
        type: list
    group_state:
        description: Realization state of this group
        type: str
        choices:
            - IN_PROGRESS
            - SUCCESS
            - FAILURE
'''

EXAMPLES = '''
- name: create Policy Group
  nsxt_policy_group:
    hostname: "10.10.10.10"
    username: "username"
    password: "password"
    validate_certs: False
    id: test-lb-service
    display_name: test-lb-service
    state: "present"
    domain_id: "default"
    expression:
      - member_type: "VirtualMachine"
        value: "webvm"
        key: "Tag"
        operator: "EQUALS"
        resource_type: "Condition"
'''

RETURN = '''# '''

import json
import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.nsxt_base_resource import NSXTBaseRealizableResource
from ansible.module_utils.nsxt_resource_urls import POLICY_GROUP_URL
from ansible.module_utils._text import to_native


class NSXTPolicyGroup(NSXTBaseRealizableResource):
    @staticmethod
    def get_resource_spec():
        policy_group_arg_spec = {}
        policy_group_arg_spec.update(
            domain_id=dict(
                required=True,
                type='str'
            ),
            expression=dict(
                required=True,
                type='list'
            ),
            extended_expression=dict(
                required=False,
                type='list'
            ),
            group_state=dict(
                required=False,
                type='str'
            ),
        )
        return policy_group_arg_spec

    @staticmethod
    def get_resource_base_url(baseline_args):
        return POLICY_GROUP_URL.format(
            baseline_args["domain_id"]
        )

    def update_resource_params(self, nsx_resource_params):
        nsx_resource_params.pop('domain_id')


if __name__ == '__main__':
    policy_group = NSXTPolicyGroup()
    policy_group.realize(baseline_arg_names=["domain_id"])
