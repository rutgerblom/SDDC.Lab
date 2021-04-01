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
module: nsxt_vm_tags
short_description: Update tags on NSXT VM
description:
    Update tags on NSXT VM
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
    validate_certs:
        description: Enable server certificate verification.
        type: bool
        default: False
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
    add_tags:
        type: list
        element: dict
        description: List of tags to be applied to the virtual machine
        suboptions:
            scope:
                description: Tag scope.
                required: true
                type: str
            tag:
                description: Tag value.
                required: true
                type: str
    remove_tags_with_scope:
        type: list
        element: str
        description:
            - Specify the scope of the tags that should be removed
            - If remove_other_tags is True, this becomes do not care
    virtual_machine_id:
        description: The identifier that is used in the enforcement point that
                     uniquely identifies the virtual machine. In case of NSXT
                     it would be the value of the external_id of the virtual
                     machine.
        type: str
    virtual_machine_display_name:
        description: Display name of the VM whose tags are to be updated.
                     Either this or virtual_machine_id must be specified. If
                     both are specified, virtual_machine_id is used
        type: str
    remove_other_tags:
        description:
            - Remove the tags that are not specified in the add_tags
            - Caution; If this is True, all tags that are not in add_tags will
              be removed
        default: false
'''

EXAMPLES = '''
- name: Update Tags on VMs
  nsxt_vm_tags:
    hostname: "10.10.10.10"
    nsx_cert_path: /root/com.vmware.nsx.ncp/nsx.crt
    nsx_key_path: /root/com.vmware.nsx.ncp/nsx.key
    validate_certs: False
    virtual_machine_display_name: App-VM-1
    remove_other_tags: False
    add_tags:
      - scope: my-scope
        tag: my-tag
    remove_tags_with_scope:
      - my-scope1
'''

RETURN = '''# '''


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.policy_communicator import PolicyCommunicator
from ansible.module_utils.nsxt_resource_urls import VM_URL
from ansible.module_utils._text import to_native


def get_resource_spec():
    vm_tag_spec = PolicyCommunicator.get_vmware_argument_spec()
    vm_tag_spec.update(dict(
        virtual_machine_id=dict(type='str'),
        virtual_machine_display_name=dict(type='str'),
        add_tags=dict(type='list', elements='dict', default=[],
                      options=dict(
                          scope=dict(required=True, type='str'),
                          tag=dict(required=True, type='str'))),
        remove_other_tags=dict(
            required=False, default=False, type='bool')),
        remove_tags_with_scope=dict(type='list', elements='str', default=[],
                                    options=dict(
                                        scope=dict(required=True, type='str'),
                                        tag=dict(required=False, type='str'))))
    return vm_tag_spec


class TagElement(object):
    def __init__(self, tag):
        self.scope, self.tag = tag['scope'], tag.get('tag')
        self.element = (self.scope, self.tag)

    def __eq__(self, other):
        if self.tag is None:
            return self.scope == other.scope
        return self.element == other.element

    def __hash__(self):
        return hash(self.scope)


def _fetch_all_tags_on_vm_and_infer_id(
        vm_id, policy_communicator, vm_display_name, module):
    _, resp = policy_communicator.request(
            VM_URL)
    vms = resp['results']
    target_vm = None
    if vm_id:
        for vm in vms:
            if vm['external_id'] == vm_id:
                return vm.get('tags', []), vm_id
        module.fail_json(msg="No VM found with the provided "
                         "virtual_machine_id")
    else:
        for vm in vms:
            if vm['display_name'] == vm_display_name:
                if target_vm is not None:
                    # Multiple VMs with same display name. Ask user
                    # to provide VM ID instead
                    module.fail_json(msg="Multiple VMs with same display "
                                     "name. Please provide "
                                     "virtual_machine_id to identify the "
                                     "target VM")
                target_vm = vm
        if target_vm:
            return target_vm.get('tags', []), target_vm['external_id']
        module.fail_json(msg="No VM found with the provided "
                         "virtual_machine_display_name")


def _get_tags_as_set(tags=[], scope_list=[]):
    tag_set = set()
    if tags:
        for tag in tags:
            tag_set.add(TagElement(tag))
    if scope_list:
        for scope in scope_list:
            tag_set.add(TagElement({'scope': scope}))
    return tag_set


def _read_tags_from_module_params(module_params, tag_identifier):
    return module_params[tag_identifier] or []


def realize():
    module = AnsibleModule(
        argument_spec=get_resource_spec(),
        supports_check_mode=False)

    virtual_machine_id = module.params['virtual_machine_id']
    virtual_machine_display_name = None
    if not virtual_machine_id:
        virtual_machine_display_name = module.params[
            'virtual_machine_display_name']
        if not virtual_machine_display_name:
            module.fail_json(msg="Please specify either virtual_machine_id or "
                                 "virtual_machine_display_name in the "
                                 "playbook")

    mgr_hostname = module.params.pop('hostname')
    mgr_username = module.params.pop('username')
    mgr_password = module.params.pop('password')

    nsx_cert_path = module.params['nsx_cert_path']
    nsx_key_path = module.params['nsx_key_path']

    request_headers = module.params['request_headers']
    ca_path = module.params['ca_path']

    validate_certs = module.params.pop('validate_certs')

    try:
        # Each manager has an associated PolicyCommunicator
        policy_communicator = PolicyCommunicator.get_instance(
            mgr_hostname, mgr_username, mgr_password, nsx_cert_path,
            nsx_key_path, request_headers, ca_path, validate_certs)

        all_tags, virtual_machine_id = _fetch_all_tags_on_vm_and_infer_id(
            virtual_machine_id, policy_communicator,
            virtual_machine_display_name, module)
        init_tags_set = _get_tags_as_set(tags=all_tags)
        if module.params.get('remove_other_tags'):
            tags_to_add = _get_tags_as_set(tags=_read_tags_from_module_params(
                module.params, 'add_tags'))
            for i, tag in enumerate(all_tags):
                if TagElement(tag) not in tags_to_add:
                    all_tags[i] = None
        elif _read_tags_from_module_params(
                module.params, 'remove_tags_with_scope'):
            tags_to_remove = _get_tags_as_set(
                scope_list=_read_tags_from_module_params(
                    module.params, 'remove_tags_with_scope'))
            for i, tag in enumerate(all_tags):
                if TagElement(tag) in tags_to_remove:
                    all_tags[i] = None
        persistent_tags = []
        for tag in all_tags:
            if tag:
                persistent_tags += tag,

        final_tags = persistent_tags
        final_tags_set = _get_tags_as_set(tags=final_tags)
        for tag in _read_tags_from_module_params(module.params, 'add_tags'):
            if TagElement(tag) in final_tags_set:
                for final_tag in final_tags:
                    if final_tag['scope'] == tag['scope']:
                        final_tag['tag'] = tag['tag']
                        break
            else:
                final_tags += tag,
        final_tags_set = _get_tags_as_set(tags=final_tags)

        if init_tags_set == final_tags_set:
            module.exit_json(msg="No tags detected to update")

        post_body = {
            "virtual_machine_id": virtual_machine_id,
            "tags": final_tags
        }
        _, resp = policy_communicator.request(
            VM_URL + '?action=update_tags', data=post_body,
            method="POST")
        module.exit_json(msg="Successfully updated tags on VM {}".format(
            virtual_machine_id), changed=True)
    except Exception as err:
        module.fail_json(msg="Failed to update tags on VM {} as API "
                         "returned error: {}. Please try "
                         "again".format(virtual_machine_id, err))


if __name__ == '__main__':
    realize()
