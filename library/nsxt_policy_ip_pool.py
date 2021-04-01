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
module: nsxt_policy_ip_pool
short_description: Create or Delete a Policy IP Pool
description:
    Creates or deletes a Policy IP Pool.
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
    create_or_update_subresource_first:
        type: bool
        default: false
        description:
            - Can be used to create subresources first.
            - Can be specified for each subresource.
    delete_subresource_first:
        type: bool
        default: true
        description:
            - Can be used to delete subresources first.
            - Can be specified for each subresource.
    achieve_subresource_state_if_del_parent:
        type: bool
        default: false
        description:
            - Can be used to achieve the state of subresources even if
              the parent(base) resource's state is absent.
            - Can be specified for each subresource.
    do_wait_till_create:
        type: bool
        default: false
        description:
            - Can be used to wait for the realization of subresource before the
              request to create the next resource is sent to the Manager.
            - Can be specified for each subresource.
    id:
        description: The id of the Policy IP Pool.
        required: false
        type: str
    description:
        description: Resource description.
        type: str
    pool_block_subnets:
        type: list
        element: dict
        description: Specify the IP Pool Block Subnets that need to be created,
                     updated, or deleted as a list of dict in this section
        suboptions:
            auto_assign_gateway:
                description:
                    - Indicate whether default gateway is to be reserved from
                      the range
                    - If this property is set to true, the first IP in the
                      range will be reserved for gateway.
                type: bool
                default: true
            description:
                description: Resource description.
                type: str
            display_name:
                description:
                    - Display name.
                    - If resource ID is not specified, display_name will be
                      used as ID.
                required: false
                type: str
            do_wait_till_create:
                type: bool
                default: false
                description: Can be used to wait for the realization of
                             subresource before the request to create the next
                             resource is sent to the Manager
            id:
                description: The id of the Policy IP Pool Block Subnet.
                required: false
                type: str
            ip_block_display_name:
                description: Same as ip_block_id. Either one must be specified.
                             If both are specified, ip_block_id takes
                             precedence.
                required: false
                type: str
            ip_block_id:
                description: The ID of the IpAddressBlock from which the subnet
                             is to be created
                type: str
            size:
                description:
                    - Represents the size or number of IP addresses in the
                      subnet
                    - The size parameter is required for subnet creation. It
                      must be specified during creation but cannot be changed
                      later.
                type: int
            state:
                choices:
                - present
                - absent
                description: "State can be either 'present' or 'absent'.
                            'present' is used to create or update resource.
                            'absent' is used to delete resource."
                required: true
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
    pool_static_subnets:
        type: list
        element: dict
        description: Specify the IP Pool Static Subnets that need to be
                     created, updated, or deleted as a list of dict in
                     this section
        suboptions:
            allocation_ranges:
                description: A collection of IPv4 or IPv6 IP Pool Ranges.
                type: list
                element: dict
                suboptions:
                    start:
                        description: The start IP Address of the IP Range.
                        type: str
                        required: true
                    end:
                        description: The end IP Address of the IP Range.
                        type: str
                        required: true
            cidr:
                description: Subnet representation is a network address
                             and prefix length
                type: str
                required: true
            description:
                description: Resource description.
                type: str
            display_name:
                description:
                    - Display name.
                    - If resource ID is not specified, display_name will be
                      used as ID.
                required: false
                type: str
            dns_nameservers:
                description: The collection of upto 3 DNS servers
                             for the subnet.
                type: list
                element: str
            dns_suffix:
                description: The DNS suffix for the DNS server.
                type: str
            do_wait_till_create:
                type: bool
                default: false
                description: Can be used to wait for the realization of
                             subresource before the request to create the next
                             resource is sent to the Manager
            gateway_ip:
                description: The default gateway address on a
                             layer-3 router.
                type: str
            id:
                description: The id of the Policy IP Pool Block Subnet.
                required: false
                type: str
            state:
                choices:
                - present
                - absent
                description: "State can be either 'present' or 'absent'.
                            'present' is used to create or update resource.
                            'absent' is used to delete resource."
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
'''

EXAMPLES = '''
- name: create IP Pool
  nsxt_policy_ip_pool:
    hostname: "10.10.10.10"
    nsx_cert_path: /root/com.vmware.nsx.ncp/nsx.crt
    nsx_key_path: /root/com.vmware.nsx.ncp/nsx.key
    validate_certs: False
    id: test-ip-pool
    display_name: test-ip-pool
    state: "absent"
    tags:
    - tag: "a"
      scope: "b"
    pool_block_subnets:
      - id: test-ip-subnet-1
        state: present
        ip_block_id: "test-ip-blk-1"
        size: 16
      - display_name: test-ip-subnet-2
        state: present
        ip_block_id: "test-ip-blk-1"
        size: 16
      - display_name: test-ip-subnet-3
        state: present
        ip_block_id: "test-ip-blk-1"
        size: 8
    pool_static_subnets:
      - id: test-ip-static-subnet-1
        state: present
        allocation_ranges:
          - start: '192.116.0.10'
            end: '192.116.0.20'
          - start: '192.116.0.30'
            end: '192.116.0.40'
        cidr: '192.116.0.0/26'
      - display_name: test-ip-static-subnet-2
        state: present
        allocation_ranges:
          - start: '192.116.1.10'
            end: '192.116.1.20'
          - start: '192.116.1.30'
            end: '192.116.1.40'
        cidr: '192.116.1.0/26'
'''

RETURN = '''# '''

import json
import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.nsxt_base_resource import NSXTBaseRealizableResource
from ansible.module_utils.nsxt_resource_urls import (
    IP_ADDRESS_POOL_SUBNET_URL, IP_BLOCK_URL, IP_POOL_URL)
from ansible.module_utils._text import to_native


class NSXTIpPool(NSXTBaseRealizableResource):
    @staticmethod
    def get_resource_spec():
        ip_pool_arg_spec = {}
        return ip_pool_arg_spec

    @staticmethod
    def get_resource_base_url(baseline_args=None):
        return IP_POOL_URL

    def update_parent_info(self, parent_info):
        parent_info["ip_pool_id"] = self.id

    class NSXTIpAddressPoolBlockSubnet(NSXTBaseRealizableResource):
        def get_spec_identifier(self):
            return (NSXTIpPool.NSXTIpAddressPoolBlockSubnet.
                    get_spec_identifier())

        @classmethod
        def get_spec_identifier(cls):
            return "pool_block_subnets"

        @staticmethod
        def get_resource_spec():
            ip_addr_pool_blk_subnet_arg_spec = {}
            ip_addr_pool_blk_subnet_arg_spec.update(
                ip_block_id=dict(
                    required=False,
                    type='str'
                ),
                ip_block_display_name=dict(
                    required=False,
                    type='str'
                ),
                auto_assign_gateway=dict(
                    required=False,
                    type='bool'
                ),
                size=dict(
                    required=True,
                    type='int'
                ),
                start_ip=dict(
                    required=False,
                    type='str'
                ),
            )
            return ip_addr_pool_blk_subnet_arg_spec

        @staticmethod
        def get_resource_base_url(parent_info):
            return IP_ADDRESS_POOL_SUBNET_URL.format(
                parent_info["ip_pool_id"]
            )

        def update_resource_params(self, nsx_resource_params):
            # ip_block is a required attr
            ip_block_id = self.get_id_using_attr_name_else_fail(
                "ip_block", nsx_resource_params,
                IP_BLOCK_URL, "IP Block")
            nsx_resource_params["ip_block_path"] = (
                IP_BLOCK_URL + "/" + ip_block_id)

            nsx_resource_params["resource_type"] = "IpAddressPoolBlockSubnet"

    class NSXTIpAddressPoolStaticSubnet(NSXTBaseRealizableResource):
        def get_spec_identifier(self):
            return (NSXTIpPool.NSXTIpAddressPoolStaticSubnet.
                    get_spec_identifier())

        @classmethod
        def get_spec_identifier(cls):
            return "pool_static_subnets"

        @staticmethod
        def get_resource_spec():
            ip_addr_pool_static_subnet_arg_spec = {}
            ip_addr_pool_static_subnet_arg_spec.update(
                auto_assign_gateway=dict(
                    required=False,
                    type='bool'
                ),
                allocation_ranges=dict(
                    required=True,
                    elements='dict',
                    type='list',
                    options=dict(
                        start=dict(
                            required=True,
                            type='str'
                        ),
                        end=dict(
                            required=True,
                            type='str'
                        ),
                    )
                ),
                cidr=dict(
                    required=True,
                    type='str'
                ),
                dns_nameservers=dict(
                    required=False,
                    elements='str',
                    type='list'
                ),
                dns_suffix=dict(
                    required=False,
                    type='str'
                ),
                gateway_ip=dict(
                    required=False,
                    type='str'
                ),
            )
            return ip_addr_pool_static_subnet_arg_spec

        @staticmethod
        def get_resource_base_url(parent_info):
            return IP_ADDRESS_POOL_SUBNET_URL.format(
                parent_info["ip_pool_id"]
            )

        def update_resource_params(self, nsx_resource_params):
            nsx_resource_params["resource_type"] = "IpAddressPoolStaticSubnet"


if __name__ == '__main__':
    ip_pool = NSXTIpPool()
    ip_pool.realize()
