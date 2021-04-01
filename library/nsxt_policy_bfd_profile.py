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
module: nsxt_policy_bfd_profile
short_description: Create or Delete a Policy BFD Profile
description:
    Creates or deletes a Policy BFD Profile.
    Required attributes include id and display_name.
version_added: "2.8"
author: Gautam Verma
extends_documentation_fragment: vmware_nsxt
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
    do_wait_till_create:
        type: bool
        default: false
        description:
            - Can be used to wait for the realization of subresource before the
              request to create the next resource is sent to the Manager.
            - Can be specified for each subresource.
    id:
        description: The id of the BFD Profile.
        required: true
        type: str
    description:
        description: BFD Profile description.
        type: str
    interval:
        description:
            - Time interval between heartbeat packets in milliseconds
            - Should be in the range [50-60000]
        type: int
        default: 500
    multiple:
        description:
            - Declare dead multiple.
            - Number of times heartbeat packet is missed before BFD declares
              the neighbor is down.
            - Should be in the range [2-16]
        type: int
        default: 3
'''

EXAMPLES = '''
- name: Update BFD Profile
  nsxt_policy_bfd_profile:
    hostname: "10.10.10.10"
    nsx_cert_path: /root/com.vmware.nsx.ncp/nsx.crt
    nsx_key_path: /root/com.vmware.nsx.ncp/nsx.key
    validate_certs: False
    display_name: test-bfd-profile
    state: present
    interval: 200
    multiple: 10
'''

RETURN = '''# '''

import json
import time
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.nsxt_base_resource import NSXTBaseRealizableResource
from ansible.module_utils.nsxt_resource_urls import BFD_PROFILE_URL
from ansible.module_utils._text import to_native


class NSXTBFDProfile(NSXTBaseRealizableResource):
    @staticmethod
    def get_resource_spec():
        bfd_profile_arg_spec = {}
        bfd_profile_arg_spec.update(
            interval=dict(
                default=500,
                type='int'
            ),
            multiple=dict(
                default=3,
                type='int'
            )
        )
        return bfd_profile_arg_spec

    @staticmethod
    def get_resource_base_url(baseline_args=None):
        return BFD_PROFILE_URL


if __name__ == '__main__':
    bfd_profile = NSXTBFDProfile()
    bfd_profile.realize()
