#!/usr/bin/env python
#
# Copyright 2020 VMware, Inc.
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
module: nsxt_policy_gateway_policy
short_description: Update a Gateway Policy
description:
    Updates a Gateway Policy
    Required attributes include id or display_name
version_added: "2.8"
author: Gautam Verma
options:
    hostname:
        description: Deployed NSX manager hostname.
        required: true
        type: str
    username:
        description: The username to authenticate with the NSX manager.
        type: str
    password:
        description:
            - The password to authenticate with the NSX manager.
            - Must be specified if username is specified
        type: str
    ca_path:
        description: Path to the CA bundle to be used to verify host's SSL
                     certificate
        type: str
    nsx_cert_path:
        description: Path to the certificate created for the Principal
                     Identity using which the CRUD operations should be
                     performed
        type: str
    nsx_key_path:
        description:
            - Path to the certificate key created for the Principal Identity
              using which the CRUD operations should be performed
            - Must be specified if nsx_cert_path is specified
        type: str
    request_headers:
        description: HTTP request headers to be sent to the host while making
                     any request
        type: dict
    display_name:
        description:
            - Display name.
            - If resource ID is not specified, display_name will be used as ID
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
    id:
        description: The id of the Gateway Policy
        required: false
        type: str
    description:
        description: Gateway Policy description.
        type: str
    category:
        description:
            Policy Framework for Edge Firewall provides six pre-defined
            categories - "Emergency", "SystemRules", "SharedPreRules",
            "LocalGatewayRules", "AutoServiceRules" and "Default", in order
            of priority of rules. All categories are allowed for Gatetway
            Policies that belong to 'default' Domain. However, for user
            created domains, category is restricted to "SharedPreRules" or
            "LocalGatewayRules" only. Also, the users can add/modify/delete
            rules from only the "SharedPreRules" and "LocalGatewayRules"
            categories. If user doesn't specify the category then defaulted
            to "Rules". System generated category is used by NSX created
            rules, for example BFD rules. Autoplumbed category used by NSX
            verticals to autoplumb data path rules. Finally, "Default"
            category is the placeholder default rules with lowest in the order
            of priority
        required: false
        type: str
        choices:
            - Emergency
            - SystemRules
            - SharedPreRules
            - LocalGatewayRules
            - AutoServiceRules
            - Default
        default: Default
    comments:
        description: Comments for security policy lock/unlock
        required: false
        type: str
    locked:
        description: Indicates whether a security policy should be locked.
                     If the security policy is locked by a user, then no other
                     user would be able to modify this security policy. Once
                     the user releases the lock, other users can update this
                     security policy
        required: false
        type: bool
        default: false
    rules:
        description: Rules that are a part of this GatewayPolicy
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
    scheduler_path:
        description:
            - Path to the scheduler for time based scheduling
            - Provides a mechanism to apply the rules in this policy for a
              specified time duration
        required: false
        type: str
    scope:
        description: The list of group paths where the rules in this policy
                     will get applied. This scope will take precedence over
                     rule level scope. Supported only for security and
                     redirection policies. In case of RedirectionPolicy, it is
                     expected only when the policy is NS and redirecting to
                     service chain.
        required: false
        type: list
        element: str
    sequence_number:
        description:
            - Sequence number to resolve conflicts across Domains
            - This field is used to resolve conflicts between security
              policies across domains. In order to change the sequence number
              of a policy one can fire a POST request on the policy entity
              with a query parameter action=revise The sequence number field
              will reflect the value of the computed sequence number upon
              execution of the above mentioned POST request. For scenarios
              where the administrator is using a template to update several
              security policies, the only way to set the sequence number is
              to explicitly specify the sequence number for each security
              policy. If no sequence number is specified in the payload, a
              value of 0 is assigned by default. If there are multiple
              policies with the same sequence number then their order is not
              deterministic. If a specific order of policies is desired, then
              one has to specify unique sequence numbers or use the POST
              request on the policy entity with a query parameter
              action=revise to let the framework assign a sequence number
        required: false
        type: int
    stateful:
        description:
            - Stateful nature of the entries within this security policy.
            - Stateful or Stateless nature of security policy is enforced on
              all rules in this security policy. When it is stateful, the state
              of the network connects are tracked and a stateful packet
              inspection is performed. Layer3 security policies can be stateful
              or stateless. By default, they are stateful. Layer2 security
              policies can only be stateless.
        required: false
        type: bool
    tcp_strict:
        description:
            - Enforce strict tcp handshake before allowing data packets
            - Ensures that a 3 way TCP handshake is done before the data
              packets are sent. tcp_strict=true is supported only for stateful
              security policies.
        required: false
        type: bool
'''

EXAMPLES = '''
- name: Update Gateway Policy
  nsxt_policy_gateway_policy:
    hostname: "10.10.10.10"
    nsx_cert_path: /root/com.vmware.nsx.ncp/nsx.crt
    nsx_key_path: /root/com.vmware.nsx.ncp/nsx.key
    validate_certs: False
    display_name: test-gateway-policy
    state: present
'''

RETURN = '''# '''

import json
import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.nsxt_base_resource import NSXTBaseRealizableResource
from ansible.module_utils.nsxt_resource_urls import GATEWAY_POLICY_URL
from ansible.module_utils.policy_resource_specs.security_policy import (
    SPEC as SecurityPolicySpec)
from ansible.module_utils._text import to_native


class NSXTGatewayPolicy(NSXTBaseRealizableResource):
    @staticmethod
    def get_resource_spec():
        gateway_policy_arg_spec = {}
        gateway_policy_arg_spec.update(
            SecurityPolicySpec
        )
        gateway_policy_arg_spec.pop('connectivity_strategy')
        return gateway_policy_arg_spec

    @staticmethod
    def get_resource_base_url(baseline_args):
        return GATEWAY_POLICY_URL.format(
            baseline_args["domain_id"])

    def update_resource_params(self, nsx_resource_params):
        nsx_resource_params.pop('domain_id')


if __name__ == '__main__':
    gw_policy = NSXTGatewayPolicy()
    gw_policy.realize(baseline_arg_names=["domain_id"])
