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
module: nsxt_policy_security_policy
short_description: Create or Delete a Policy Security Policy
description:
    Creates or deletes a Policy Security Policy.
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
        description: The id of the Policy Security Policy.
        required: false
        type: str
    description:
        description: Security Policy description.
        type: str
    domain_id:
        description: The domain id where the Security Policy is realized.
        type: str
        required: true
    category:
        description:
            - A way to classify a security policy, if needed.
            - Distributed Firewall
                - Policy framework provides five pre-defined categories for
                classifying a security policy. They are "Ethernet",Emergency",
                "Infrastructure", "Environment" and "Application". There is a
                pre-determined order in which the policy framework manages the
                priority of these security policies. Ethernet category is for
                supporting layer 2 firewall rules. The other four categories
                are applicable for layer 3 rules. Amongst them, the Emergency
                category has the highest priority followed by Infrastructure,
                Environment and then Application rules. Administrator can
                choose to categorize a security policy into the above
                categories or can choose to leave it empty. If empty it will
                have the least precedence w.r.t the above four categories.
            - Edge Firewall
                - Policy Framework for Edge Firewall provides six pre-defined
                categories "Emergency", "SystemRules", "SharedPreRules",
                "LocalGatewayRules", "AutoServiceRules" and
                "Default", in order of priority of rules.
                All categories are allowed for Gatetway Policies
                that belong to 'default' Domain. However, for
                user created domains, category is restricted to
                "SharedPreRules" or "LocalGatewayRules" only.
                Also, the users can add/modify/delete rules from
                only the "SharedPreRules" and "LocalGatewayRules"
                categories. If user doesn't specify the category
                then defaulted to "Rules". System generated
                category is used by NSX created rules, for
                example BFD rules. Autoplumbed category used by
                NSX verticals to autoplumb data path rules.
                Finally, "Default" category is the placeholder
                default rules with lowest in the order of priority.
        type: str
    comments:
        type: str
        description: SecurityPolicy lock/unlock comments
    connectivity_strategy:
        type: str
        description:
            - Connectivity strategy applicable for this SecurityPolicy
            - This field indicates the default connectivity policy for the
              security policy. Based on the connectivitiy strategy, a default
              rule for this security policy will be created. An appropriate
              action will be set on the rule based on the value of the
              connectivity strategy. If NONE is selected or no connectivity
              strategy is specified, then no default rule for the security
              policy gets created. The default rule that gets created will be a
              any-any rule and applied to entities specified in the scope of
              the security policy. Specifying the connectivity_strategy without
              specifying the scope is not allowed. The scope has to be a
              Group and one cannot specify IPAddress directly in the group that
              is used as scope. This default rule is only applicable for the
              Layer3 security policies
            - WHITELIST - Adds a default drop rule. Administrator can then use
              "allow" rules (aka whitelist) to allow traffic between groups
            - BLACKLIST - Adds a default allow rule. Admin can then use "drop"
              rules (aka blacklist) to block traffic between groups
            - WHITELIST_ENABLE_LOGGING - Whitelising with logging enabled
            - BLACKLIST_ENABLE_LOGGING - Blacklisting with logging enabled
            - NONE - No default rule is created
    locked:
        type: bool
        description:
            - Lock a security policy
            - Indicates whether a security policy should be locked. If the
              security policy is locked by a user, then no other user would
              be able to modify this security policy. Once the user releases
              the lock, other users can update this security policy.
    scheduler_path:
        type: str
        description:
            - Path to the scheduler for time based scheduling
            - Provides a mechanism to apply the rules in this policy for a
              specified time duration.
    scope:
        description: The list of group paths where the rules in this
                     policy will get applied. This scope will take
                     precedence over rule level scope. Supported only
                     for security policies.
        type: list
    sequence_number:
        description: Sequence number to resolve conflicts across Domains
        type: int
    stateful:
        type: bool
        description:
            - Stateful nature of the entries within this security policy.
            - Stateful or Stateless nature of security policy is enforced
              on all rules in this security policy. When it is stateful, the
              state of the network connects are tracked and a stateful packet
              inspection is performed.
            - Layer3 security policies can be stateful or stateless.
              By default, they are stateful.
            - Layer2 security policies can only be stateless.
    rules:
        description: Rules that are a part of this SecurityPolicy
        type: list
        suboptions:
            action:
                description: The action to be applied to all the
                             services
                type: str
                choices:
                    - "ALLOW"
                    - "DROP"
                    - "REJECT"
            description:
                description: Description of this resource
                type: str
            destination_groups:
                description: Destination group paths
                type: list
                required: true
            destinations_excluded:
                description: Negation of destination groups

                             If set to true, the rule gets applied on
                             all the groups that are NOT part of the
                             destination groups. If false, the rule
                             applies to the destination groups.
                type: bool
                default: false
            direction:
                description: Define direction of traffic.
                type: str
                choices:
                    - IN
                    - OUT
                    - IN_OUT
            disabled:
                description: Flag to disable the rule
                type: bool
                default: false
            display_name:
                description: Identifier to use when displaying entity
                             in logs or GUI.

                             Defaults to ID if not set
                type: str
            id:
                description: Unique identifier of this resource
                type: str
                required: true
            ip_protocol:
                description:
                    - IPv4 vs IPv6 packet type
                    - Type of IP packet that should be matched while enforcing
                      the rule. The value is set to IPV4_IPV6 for Layer3 rule
                      if not specified. For Layer2/Ether rule the value must be
                      null.
                type: str
                choices:
                    - IPV4
                    - IPV6
                    - IPV4_IPV6
            logged:
                description: Flag to enable packet logging.
                             Default is disabled.
                type: bool
                default: false
            notes:
                description: Text for additional notes on changes
                type: str
            profiles:
                description:
                    - Layer 7 service profiles
                    - Holds the list of layer 7 service profile paths. These
                      profiles accept attributes and sub-attributes of various
                      network services (e.g. L4 AppId, encryption algorithm,
                      domain name, etc) as key value pairs
                type: list
            scope:
                description: The list of policy paths where the rule is applied
                             LR/Edge/T0/T1/LRP etc. Note that a given rule can
                             be applied on multiple LRs/LRPs
                type: list
            sequence_number:
                description: Sequence number of the this Rule
                type: int
            service_entries:
                description:
                    - Raw services
                    - In order to specify raw services this can be used,
                      along with services which contains path to services.
                      This can be empty or null
                type: list
                elements: dict
            services:
                description: Paths of services
                             In order to specify all services, use the
                             constant "ANY". This is case insensitive.
                             If "ANY" is used, it should be the ONLY
                             element in the services array. Error will
                             be thrown if ANY is used in conjunction
                             with other values.
                type: list
                required: true
            source_groups:
                description: Source group paths
                type: list
                required: true
            sources_excluded:
                description: Negation of source groups

                             If set to true, the rule gets applied on
                             all the groups that are NOT part of the
                             source groups. If false, the rule applies
                             to the source groups
                type: bool
                default: false
            tag:
                description:
                    - Tag applied on the rule
                    - User level field which will be printed in CLI and packet
                      logs.
                type: str
            tags:
                description: Opaque identifiers meaningful to the API user
                type: list
                elements: dict
                suboptions:
                    scope:
                        description: Tag scope
                        type: str
                    tag:
                        description: Tag value
                        type: str
    tcp_strict:
        type: bool
        description:
            - Enforce strict tcp handshake before allowing data packets
            - Ensures that a 3 way TCP handshake is done before the data
              packets are sent.
            - tcp_strict=true is supported only for stateful security policies
'''

EXAMPLES = '''
- name: create Security Policy
  nsxt_policy_security_policy:
    hostname: "10.10.10.10"
    username: "username"
    password: "password"
    validate_certs: False
    id: test-sec-pol
    display_name: test-sec-pol
    state: "present"
    domain_id: "default"
    locked: True
    rules:
      - action: "ALLOW"
        description: "example-rule"
        sequence_number: 1
        display_name: "test-example-rule"
        id: "test-example-rule"
        source_groups: ["/infra/domains/vmc/groups/dbgroup"]
        destination_groups: ["/infra/domains/vmc/groups/appgroup"]
        services: ["/infra/services/HTTP", "/infra/services/CIM-HTTP"]
        tag: my-tag
        tags:
          - scope: scope-1
            tag: tag-1
        logged: True
        notes: dummy-notes
        ip_protocol: IPV4_IPV6
        scope: my-scope
        profiles: "encryption algorithm"
'''

RETURN = '''# '''

import json
import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.nsxt_base_resource import NSXTBaseRealizableResource
from ansible.module_utils.nsxt_resource_urls import SECURITY_POLICY_URL
from ansible.module_utils._text import to_native


class NSXTSecurityPolicy(NSXTBaseRealizableResource):
    @staticmethod
    def get_resource_spec():
        security_policy_arg_spec = {}
        security_policy_arg_spec.update(
            category=dict(
                required=False,
                type='str'
            ),
            comments=dict(
                required=False,
                type='str'
            ),
            connectivity_strategy=dict(
                required=False,
                type='str',
                choices=['WHITELIST', 'BLACKLIST', 'WHITELIST_ENABLE_LOGGING',
                         'BLACKLIST_ENABLE_LOGGING', 'NONE']
            ),
            domain_id=dict(
                required=True,
                type='str'
            ),
            locked=dict(
                required=False,
                type='bool'
            ),
            scheduler_path=dict(
                required=False,
                type='str'
            ),
            scope=dict(
                required=False,
                type='list'
            ),
            sequence_number=dict(
                required=False,
                type='int'
            ),
            stateful=dict(
                required=False,
                type='bool'
            ),
            rules=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    action=dict(
                        required=True,
                        type='str',
                        choices=["ALLOW", "DROP", "REJECT"]
                    ),
                    description=dict(
                        required=False,
                        type='str'
                    ),
                    destination_groups=dict(
                        required=True,
                        type='list'
                    ),
                    destinations_excluded=dict(
                        required=False,
                        type='bool',
                        default=False
                    ),
                    direction=dict(
                        required=False,
                        default="IN_OUT",
                        type='str',
                        choices=["IN_OUT", "IN", "OUT"]
                    ),
                    disabled=dict(
                        required=False,
                        type='bool',
                        default=False
                    ),
                    display_name=dict(
                        type='str'
                    ),
                    id=dict(
                        type='str'
                    ),
                    ip_protocol=dict(
                        type='str',
                        choices=['IPV4', 'IPV6', 'IPV4_IPV6']
                    ),
                    logged=dict(
                        type='bool',
                        default=False
                    ),
                    notes=dict(
                        type='str'
                    ),
                    profiles=dict(
                        type='list',
                        elements='str'
                    ),
                    scope=dict(
                        type='list',
                        elements='str'
                    ),
                    sequence_number=dict(
                        required=False,
                        type='int'
                    ),
                    service_entries=dict(
                        type='list',
                        elements='dict'
                    ),
                    services=dict(
                        required=True,
                        type='list'
                    ),
                    source_groups=dict(
                        required=True,
                        type='list'
                    ),
                    sources_excluded=dict(
                        required=False,
                        type='bool',
                        default=False
                    ),
                    tag=dict(
                        type='str'
                    ),
                    tags=dict(
                        type='list',
                        elements='dict',
                        options=dict(
                            scope=dict(
                                type='str'
                            ),
                            tag=dict(
                                type='str'
                            )
                        )
                    ),
                )
            ),
            tcp_strict=dict(
                required=False,
                type='bool'
            )
        )
        return security_policy_arg_spec

    @staticmethod
    def get_resource_base_url(baseline_args):
        return SECURITY_POLICY_URL.format(
            baseline_args["domain_id"])

    def update_resource_params(self, nsx_resource_params):
        nsx_resource_params.pop('domain_id')


if __name__ == '__main__':
    segment = NSXTSecurityPolicy()
    segment.realize(baseline_arg_names=["domain_id"])
