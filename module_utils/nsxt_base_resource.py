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


from ansible.module_utils.policy_communicator import PolicyCommunicator
from ansible.module_utils.policy_communicator import DuplicateRequestError

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

from abc import ABC, abstractmethod

import time
import json

import inspect
# Add all the base resources that can be configured in the
# Policy API here. Required to infer base resource params.
BASE_RESOURCES = {"NSXTSegment", "NSXTTier0", "NSXTTier1",
                  "NSXTSecurityPolicy", "NSXTPolicyGroup",
                  "NSXTIpBlock", "NSXTIpPool", "NSXTBFDProfile",
                  "NSXTGatewayPolicy", "NSXTL2BridgeEpProfile"}


class NSXTBaseRealizableResource(ABC):

    INCORRECT_ARGUMENT_NAME_VALUE = "error_invalid_parameter"

    def realize(self, supports_check_mode=True,
                successful_resource_exec_logs=[],
                baseline_arg_names=[], resource_params=None):
        # must call this method to realize the creation, update, or deletion of
        # resource

        self.resource_class = self.__class__

        if not hasattr(self, "_arg_spec"):
            # Base resource
            self._make_ansible_arg_spec(
                supports_check_mode=supports_check_mode)

        if not hasattr(self, 'module'):
            self.module = AnsibleModule(
                argument_spec=self._arg_spec,
                supports_check_mode=supports_check_mode)

            self.set_baseline_args(baseline_arg_names)

        # Infer manager credentials
        mgr_hostname = self.module.params['hostname']
        mgr_username = self.module.params['username']
        mgr_password = self.module.params['password']
        nsx_cert_path = self.module.params['nsx_cert_path']
        nsx_key_path = self.module.params['nsx_key_path']

        request_headers = self.module.params['request_headers']
        ca_path = self.module.params['ca_path']
        validate_certs = self.module.params['validate_certs']

        # Each manager has an associated PolicyCommunicator
        self.policy_communicator = PolicyCommunicator.get_instance(
            mgr_hostname, mgr_username, mgr_password, nsx_cert_path,
            nsx_key_path, request_headers, ca_path, validate_certs)

        if resource_params is None:
            resource_params = self.module.params

        self.resource_params = resource_params

        self._state = self.get_attribute('state', resource_params)
        if not (hasattr(self, 'id') and self.id):
            if self.get_resource_name() in BASE_RESOURCES:
                self.id = self._get_id_using_attr_name(
                    None, resource_params,
                    self.get_resource_base_url(self.baseline_args),
                    self.get_spec_identifier(),
                    fail_if_not_found=False)
            else:
                self.id = self._get_id_using_attr_name(
                    None, resource_params,
                    self.get_resource_base_url(self._parent_info),
                    self.get_spec_identifier(),
                    fail_if_not_found=False)
                if self.id is None:
                    self.id = self.infer_resource_id(self._parent_info)
                if self.id is None:
                    self.module.fail_json(
                        msg="Please specify either id or display_name for "
                            "resource {}".format(str(
                                self.get_spec_identifier())))

        # Extract the resource params from module
        self.nsx_resource_params = self._extract_nsx_resource_params(
            resource_params)

        # parent_info is passed to subresources of a resource automatically
        if not hasattr(self, "_parent_info"):
            self._parent_info = {}
        self.update_parent_info(self._parent_info)

        try:
            # get existing resource schema
            _, self.existing_resource = self._send_request_to_API(
                "/" + self.id, ignore_error=False,
                accepted_error_codes=set([404]))
            self.existing_resource_revision = self.existing_resource[
                '_revision']
            # As Policy API's PATCH requires all attributes to be filled,
            # we fill the missing resource params (the params not specified)
            # by user using the existing params
            self._fill_missing_resource_params(
                self.existing_resource, self.nsx_resource_params)
        except Exception as err:
            # the resource does not exist currently on the manager
            self.existing_resource = None
            self.existing_resource_revision = None
        finally:
            self._clean_none_resource_params(
                self.existing_resource, self.nsx_resource_params)
        self._achieve_state(resource_params, successful_resource_exec_logs)

    @classmethod
    def get_spec_identifier(cls):
        # Can be overriden in the subclass to provide different
        # unique_arg_identifier. It is used to infer which args belong to which
        # subresource.
        # By default, class name is used for subresources.
        return cls.get_resource_name()

    def get_state(self):
        return self._state

    def get_parent_info(self):
        return self._parent_info

    def infer_resource_id(self, parent_info):
        # This is called when the user has not specified the ID or
        # display_name of any child resource or its sub-resources
        pass

    @staticmethod
    @abstractmethod
    def get_resource_base_url(parent_info):
        # Must be overridden by the subclass
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def get_resource_spec():
        # Must be overridden by the subclass
        raise NotImplementedError

    @classmethod
    def get_resource_name(cls):
        return cls.__name__

    def create_or_update_subresource_first(self):
        # return True if subresource should be created/updated before parent
        # resource
        return self.resource_params.get(
            "create_or_update_subresource_first", False)

    def delete_subresource_first(self):
        # return True if subresource should be deleted before parent resource
        return self.resource_params.get("delete_subresource_first", True)

    def achieve_subresource_state_if_del_parent(self):
        # return True if this resource is to be realized with its own specified
        # state irrespective of the state of its parent resource.
        return self.resource_params.get(
            "achieve_subresource_state_if_del_parent", False)

    def do_wait_till_create(self):
        # By default, we do not wait for the parent resource to be created or
        # updated before its subresource is to be realized.
        return self.resource_params.get("do_wait_till_create", False)

    @staticmethod
    def get_resource_update_priority():
        # this priority can be used to create/delete subresources
        # at the same level in a particular order.
        # by default, it returns 1 so the resources are created/updated/
        # deleted in a fixed but random order.
        # should be overloaded in subclass to specify its priority.
        # for creation or update, we iterate in descending order.
        # for deletion, we iterate in ascending order.
        return 1

    def set_arg_spec(self, arg_spec):
        self._arg_spec = arg_spec

    def set_ansible_module(self, ansible_module):
        self.module = ansible_module

    def set_parent_info(self, parent_info):
        self._parent_info = parent_info

    def achieve_subresource_state(
            self, resource_params, successful_resource_exec_logs):
        """
            Achieve the state of each sub-resource.
        """
        for sub_resource_class in self._get_sub_resources_class_of(
                self.resource_class):
            if sub_resource_class.allows_multiple_resource_spec():
                children_resource_spec = (resource_params.get(
                    sub_resource_class.get_spec_identifier()) or [])
            else:
                children_resource_spec = ([resource_params.get(
                    sub_resource_class.get_spec_identifier())] or [])

            # Update the parent pointer
            my_parent = self._parent_info.get('_parent', '')
            self._update_parent_info()

            for resource_param_spec in children_resource_spec:
                if resource_param_spec is not None:
                    sub_resource = sub_resource_class()

                    sub_resource.set_arg_spec(self._arg_spec)
                    sub_resource.set_ansible_module(self.module)

                    sub_resource.set_parent_info(self._parent_info)

                    sub_resource.realize(
                        successful_resource_exec_logs=(
                            successful_resource_exec_logs),
                        resource_params=resource_param_spec)

            # Restore the parent pointer
            self._parent_info['_parent'] = my_parent

    def update_resource_params(self, nsx_resource_params):
        # Can be used to updates the params of resource before making
        # the API call.
        # Should be overridden in the subclass if needed
        pass

    def check_for_update(self, existing_params, resource_params):
        """
            resource_params: dict
            existing_params: dict

            Compares the existing_params with resource_params and returns
            True if they are different. At a base level, it traverses the
            params and matches one-to-one. If the value to be matched is a
            - dict, it traverses that also.
            - list, it merely compares the order.
            Can be overriden in the subclass for specific custom checking.

            Returns true if the params differ
        """
        if not existing_params:
            return False
        for k, v in resource_params.items():
            if k not in existing_params:
                return True
            elif type(v).__name__ == 'dict':
                if self.check_for_update(existing_params[k], v):
                    return True
            elif v != existing_params[k]:
                def compare_lists(list1, list2):
                    # Returns True if list1 and list2 differ
                    try:
                        # If the lists can be converted into sets, do so and
                        # compare lists as sets.
                        set1 = set(list1)
                        set2 = set(list2)
                        return set1 != set2
                    except Exception:
                        return True
                if type(v).__name__ == 'list':
                    if compare_lists(v, existing_params[k]):
                        return True
                    continue
                return True
        return False

    def update_parent_info(self, parent_info):
        # Override this and fill in self._parent_info if that is to be passed
        # to the sub-resource
        # By default, parent's id is passed
        parent_info[self.get_spec_identifier() + "_id"] = self.id

    def get_attribute(self, attribute, resource_params):
        """
            attribute: String
            resource_params: Parameters of the resource
        """
        if (attribute == "state" and
                self.get_resource_name() not in BASE_RESOURCES):
            # if parent has absent state, subresources should have absent
            # state if . So, irrespective of what user specifies, if parent
            # is to be deleted, the child resources will be deleted.
            # override achieve_subresource_state_if_del_parent
            # in resource class to change this behavior
            if (self._parent_info["_parent"].get_state() == "absent" and
                    not self.achieve_subresource_state_if_del_parent()):
                return "absent"
        return resource_params.get(
            attribute, self.INCORRECT_ARGUMENT_NAME_VALUE)

    def set_baseline_args(self, baseline_arg_names):
        # Can be overriden in subclass
        self.baseline_args = {}
        for baseline_arg_name in baseline_arg_names:
            self.baseline_args[baseline_arg_name] = self.module.params[
                baseline_arg_name]

    def do_resource_params_have_attr_with_id_or_display_name(self, attr):
        if (attr + "_id" in self.nsx_resource_params or
                attr + "_display_name" in self.nsx_resource_params):
            return True
        return False

    def get_id_using_attr_name_else_fail(self, attr_name, params,
                                         resource_base_url, resource_type):
        return self._get_id_using_attr_name(
            attr_name, params, resource_base_url, resource_type,
            fail_if_not_found=True)

    def exit_with_failure(self, msg, **kwargs):
        self.module.fail_json(msg=msg, **kwargs)

    def skip_delete(self):
        """
        Override in subclass if this resource is skipped to be deleted.
        Note that the children of this resource will still be deleted unless
        they override this method as well.
        """
        return False

    @classmethod
    def is_required_in_spec(cls):
        """
        Override in subclass if this resource is optional to be specified
        in the ansible playbook.
        """
        return False

    @classmethod
    def allows_multiple_resource_spec(cls):
        """
        Override in the resource class definition with False if only one
        resource can be associated with the parent. By default, we accept
        multiple
        """
        return True

    def _get_id_using_attr_name(self, attr_name, params,
                                resource_base_url, resource_type,
                                fail_if_not_found=True):
        # Pass attr_name '' or None to infer base resource's ID
        id_identifier = 'id'
        display_name_identifier = 'display_name'
        if attr_name:
            id_identifier = attr_name + "_id"
            display_name_identifier = attr_name + "_display_name"
        if id_identifier in params and params[id_identifier]:
            return params.pop(id_identifier)
        if (display_name_identifier in params and
                params[display_name_identifier]):
            resource_display_name = params.pop(display_name_identifier)
            # Use display_name as ID if ID is not specified.
            return (self.get_id_from_display_name(
                resource_base_url, resource_display_name, resource_type,
                not fail_if_not_found) or resource_display_name)
        if fail_if_not_found:
            # Incorrect usage of Ansible Module
            self.module.fail_json(
                msg="Please specify either {} id or display_name for the "
                    "resource {}".format(attr_name, str(resource_type)))

    def get_id_from_display_name(self, resource_base_url,
                                 resource_display_name,
                                 resource_type, ignore_not_found_error=True):
        try:
            # Get the id from the Manager
            (_, resp) = self._send_request_to_API(
                resource_base_url=resource_base_url)
            matched_resource = None
            for resource in resp['results']:
                if (resource.__contains__('display_name') and
                        resource['display_name'] == resource_display_name):
                    if matched_resource is None:
                        matched_resource = resource
                    else:
                        # Multiple resources with same display_name!
                        # Ask the user to specify ID instead.
                        self.module.fail_json(
                            msg="Multiple {} found with display_name {}. "
                                "Please specify the resource using id in "
                                "the playbook.".format(resource_type,
                                                       resource_display_name))
            if matched_resource is not None:
                return matched_resource['id']
            else:
                if ignore_not_found_error:
                    return None
                else:
                    # No resource found with this display_name
                    self.module.fail_json(
                        msg="No {} found with display_name {} for the "
                            "specified configuration.".format(
                                resource_type, resource_display_name))
        except Exception as e:
            # Manager replied with invalid URL. It means that the resource
            # does not exist on the Manager. So, return the display_name
            return resource_display_name

    def _update_parent_info(self):
        # This update is always performed and should not be overriden by the
        # subresource's class
        self._parent_info["_parent"] = self

    def _make_ansible_arg_spec(self, supports_check_mode=True):
        """
            We read the arg_spec of all the resources associated that
            are associated with this resource and create one complete
            arg_spec.
        """
        if self.get_resource_name() in BASE_RESOURCES:
            self._arg_spec = {}
            # Update it with VMware arg spec
            self._arg_spec.update(
                PolicyCommunicator.get_vmware_argument_spec())

            # ... then update it with top most resource spec ...
            self._update_arg_spec_with_resource(
                self.resource_class, self._arg_spec)
            # Update with all sub-resources arg spec
            for sub_resources_class in self._get_sub_resources_class_of(
                    self.resource_class):
                self._update_arg_spec_with_all_resources(
                    sub_resources_class, self._arg_spec)

    def _update_arg_spec_with_resource(self, resource_class, arg_spec):
        # updates _arg_spec with resource_class's arg_spec
        resource_arg_spec = self._get_base_arg_spec_of_resource()
        resource_arg_spec.update(self._get_base_arg_spec_of_nsx_resource())
        resource_arg_spec.update(resource_class.get_resource_spec())
        if resource_class.__name__ not in BASE_RESOURCES:
            arg_spec.update(
                {
                    resource_class.get_spec_identifier(): dict(
                        options=resource_arg_spec,
                        required=resource_class.is_required_in_spec(),
                        type='dict',
                    )
                })
            if resource_class.allows_multiple_resource_spec():
                arg_spec[resource_class.get_spec_identifier()]['type'] = 'list'
                arg_spec[resource_class.get_spec_identifier()]['elements'] = (
                    'dict')
        else:
            arg_spec.update(resource_arg_spec)
        return resource_arg_spec

    def _update_arg_spec_with_all_resources(self, resource_class, arg_spec):
        # updates _arg_spec with resource_class's arg_spec and all it's
        # sub-resources
        resource_arg_spec = self._update_arg_spec_with_resource(
            resource_class, arg_spec)
        # go to each child of resource_class and update it
        for sub_resources_class in self._get_sub_resources_class_of(
                resource_class):
            self._update_arg_spec_with_all_resources(
                sub_resources_class, resource_arg_spec)

    def _get_base_arg_spec_of_nsx_resource(self):
        resource_base_arg_spec = {}
        resource_base_arg_spec.update(
            # these are the base args for any NSXT Resource
            display_name=dict(
                required=False,
                type='str'
            ),
            description=dict(
                required=False,
                type='str'
            ),
            tags=dict(
                required=False,
                type='list',
                elements='dict',
                options=dict(
                    scope=dict(
                        required=True,
                        type='str'
                    ),
                    tag=dict(
                        required=True,
                        type='str'
                    )
                )
            )
        )
        return resource_base_arg_spec

    def _get_base_arg_spec_of_resource(self):
        resource_base_arg_spec = {}
        resource_base_arg_spec.update(
            id=dict(
                type='str'
            ),
            state=dict(
                required=True,
                type='str',
                choices=['present', 'absent']
            ),
            create_or_update_subresource_first=dict(
                default=False,
                type='bool'
            ),
            delete_subresource_first=dict(
                default=True,
                type='bool'
            ),
            achieve_subresource_state_if_del_parent=dict(
                default=False,
                type='bool'
            ),
            do_wait_till_create=dict(
                default=False,
                type='bool'
            )
        )
        return resource_base_arg_spec

    def _extract_nsx_resource_params(self, resource_params):
        # extract the params belonging to this resource only.
        filtered_params = {}

        def filter_with_spec(spec):
            for key in spec.keys():
                if (key in resource_params and
                        resource_params[key] is not None):
                    filtered_params[key] = resource_params[key]

        filter_with_spec(self.get_resource_spec())
        filter_with_spec(self._get_base_arg_spec_of_nsx_resource())
        return filtered_params

    def _achieve_present_state(self, successful_resource_exec_logs):
        self.update_resource_params(self.nsx_resource_params)
        is_resource_updated = self.check_for_update(
            self.existing_resource, self.nsx_resource_params)
        if not is_resource_updated:
            # Either the resource does not exist or it exists but was not
            # updated in the YAML.
            if self.module.check_mode:
                successful_resource_exec_logs.append({
                    "changed": True,
                    "debug_out": self.resource_params,
                    "id": '12345',
                    "resource_type": self.get_resource_name()
                })
                return
            try:
                if self.existing_resource:
                    # Resource already exists
                    successful_resource_exec_logs.append({
                        "changed": False,
                        "id": self.id,
                        "message": "%s with id %s already exists." %
                        (self.get_resource_name(), self.id),
                        "resource_type": self.get_resource_name()
                    })
                    return
                # Create a new resource
                _, resp = self._send_request_to_API(
                    suffix="/" + self.id, method='PATCH',
                    data=self.nsx_resource_params)
                if self.do_wait_till_create() and not self._wait_till_create():
                    raise Exception

                successful_resource_exec_logs.append({
                    "changed": True,
                    "id": self.id,
                    "body": str(resp),
                    "message": "%s with id %s created." %
                    (self.get_resource_name(), self.id),
                    "resource_type": self.get_resource_name()
                })
            except Exception as err:
                srel = successful_resource_exec_logs
                self.module.fail_json(msg="Failed to add %s with id %s."
                                          "Request body [%s]. Error[%s]."
                                          % (self.get_resource_name(),
                                             self.id, self.nsx_resource_params,
                                             to_native(err)
                                             ),
                                      successfully_updated_resources=srel)
        else:
            # The resource exists and was updated in the YAML.
            if self.module.check_mode:
                successful_resource_exec_logs.append({
                    "changed": True,
                    "debug_out": self.resource_params,
                    "id": self.id,
                    "resource_type": self.get_resource_name()
                })
                return
            self.nsx_resource_params['_revision'] = \
                self.existing_resource['_revision']
            try:
                _, patch_resp = self._send_request_to_API(
                    suffix="/"+self.id, method="PATCH",
                    data=self.nsx_resource_params)
                # Get the resource again and compare version numbers
                _, updated_resource_spec = self._send_request_to_API(
                    suffix="/"+self.id, method="GET")
                if updated_resource_spec[
                        '_revision'] != self.existing_resource_revision:
                    successful_resource_exec_logs.append({
                        "changed": True,
                        "id": self.id,
                        "body": str(patch_resp),
                        "message": "%s with id %s updated." %
                        (self.get_resource_name(), self.id),
                        "resource_type": self.get_resource_name()
                    })
                else:
                    successful_resource_exec_logs.append({
                        "changed": False,
                        "id": self.id,
                        "message": "%s with id %s already exists." %
                        (self.get_resource_name(), self.id),
                        "resource_type": self.get_resource_name()
                    })
            except Exception as err:
                srel = successful_resource_exec_logs
                self.module.fail_json(msg="Failed to update %s with id %s."
                                          "Request body [%s]. Error[%s]." %
                                          (self.get_resource_name(), self.id,
                                           self.nsx_resource_params, to_native(
                                               err)
                                           ),
                                      successfully_updated_resources=srel)

    def _achieve_absent_state(self, successful_resource_exec_logs):
        if self.skip_delete():
            return

        if self.existing_resource is None:
            successful_resource_exec_logs.append({
                "changed": False,
                "msg": 'No %s exist with id %s' %
                (self.get_resource_name(), self.id),
                "resource_type": self.get_resource_name()
            })
            return
        if self.module.check_mode:
            successful_resource_exec_logs.append({
                "changed": True,
                "debug_out": self.resource_params,
                "id": self.id,
                "resource_type": self.get_resource_name()
            })
            return
        try:
            self._send_request_to_API("/" + self.id, method='DELETE')
            self._wait_till_delete()
            successful_resource_exec_logs.append({
                "changed": True,
                "id": self.id,
                "message": "%s with id %s deleted." %
                (self.get_resource_name(), self.id)
            })
        except Exception as err:
            srel = successful_resource_exec_logs
            self.module.fail_json(msg="Failed to delete %s with id %s. "
                                      "Error[%s]." % (self.get_resource_name(),
                                                      self.id, to_native(err)),
                                  successfully_updated_resources=srel)

    def _send_request_to_API(self, suffix="", ignore_error=False,
                             method='GET', data=None,
                             resource_base_url=None,
                             accepted_error_codes=set()):
        try:
            if not resource_base_url:
                if self.get_resource_name() not in BASE_RESOURCES:
                    resource_base_url = (self.resource_class.
                                         get_resource_base_url(
                                             parent_info=self._parent_info))
                else:
                    resource_base_url = (self.resource_class.
                                         get_resource_base_url(
                                             baseline_args=self.baseline_args))
            (rc, resp) = self.policy_communicator.request(
                resource_base_url + suffix,
                ignore_errors=ignore_error, method=method, data=data)
            return (rc, resp)
        except DuplicateRequestError:
            self.module.fail_json(msg='Duplicate request')
        except Exception as e:
            if (e.args[0] not in accepted_error_codes and
                    self.get_resource_name() in BASE_RESOURCES):
                msg = ('Received {} from NSX Manager. Please try '
                       'again. '.format(e.args[0]))
                if len(e.args) == 2 and e.args[1] and (
                        'error_message' in e.args[1]):
                    msg += e.args[1]['error_message']
                self.module.fail_json(msg=msg)
            raise e

    def get_all_resources_from_nsx(self):
        rc, resp = self._send_request_to_API()
        if rc != 200:
            self.module.fail_json(
                "Invalid URL to retrieve all configured {} NSX "
                "resources".format(self.get_spec_identifier()))
        return resp['results']

    def _achieve_state(self, resource_params,
                       successful_resource_exec_logs=[]):
        """
            Achieves `present` or `absent` state as specified in the YAML.
        """
        if self.id == self.INCORRECT_ARGUMENT_NAME_VALUE:
            # The resource was not specified in the YAML.
            # So, no need to realize it.
            return
        if (self._state == "present" and
                self.create_or_update_subresource_first()):
            self.achieve_subresource_state(
                resource_params, successful_resource_exec_logs)
        if self._state == "absent" and self.delete_subresource_first():
            self.achieve_subresource_state(
                resource_params, successful_resource_exec_logs)

        if self._state == 'present':
            self._achieve_present_state(
                successful_resource_exec_logs)
        else:
            self._achieve_absent_state(successful_resource_exec_logs)

        if self._state == "present" and not (
                self.create_or_update_subresource_first()):
            self.achieve_subresource_state(
                resource_params,
                successful_resource_exec_logs=successful_resource_exec_logs)

        if self._state == "absent" and not self.delete_subresource_first():
            self.achieve_subresource_state(
                resource_params, successful_resource_exec_logs)

        if self.get_resource_name() in BASE_RESOURCES:
            changed = False
            for successful_resource_exec_log in successful_resource_exec_logs:
                if successful_resource_exec_log["changed"]:
                    changed = True
                    break
            srel = successful_resource_exec_logs
            self.module.exit_json(changed=changed,
                                  successfully_updated_resources=srel)

    def _get_sub_resources_class_of(self, resource_class):
        subresources = []
        for attr in resource_class.__dict__.values():
            if (inspect.isclass(attr) and
                    issubclass(attr, NSXTBaseRealizableResource)):
                subresources.append(attr)
        if hasattr(self, "_state") and self._state == "present":
            subresources.sort(key=lambda subresource:
                              subresource().get_resource_update_priority(),
                              reverse=True)
        else:
            subresources.sort(key=lambda subresource:
                              subresource().get_resource_update_priority(),
                              reverse=False)
        for subresource in subresources:
            yield subresource

    def _wait_till_delete(self):
        """
            Periodically checks if the resource still exists on the API server
            every 10 seconds. Returns after it has been deleted.
        """
        while True:
            try:
                self._send_request_to_API(
                    "/" + self.id, accepted_error_codes=set([404]))
                time.sleep(10)
            except DuplicateRequestError:
                self.module.fail_json(msg='Duplicate request')
            except Exception:
                return

    def _wait_till_create(self):
        FAILED_STATES = ["failed"]
        IN_PROGRESS_STATES = ["pending", "in_progress"]
        SUCCESS_STATES = ["partial_success", "success"]
        try:
            count = 0
            while True:
                rc, resp = self._send_request_to_API(
                    "/" + self.id, accepted_error_codes=set([404]))
                if 'state' in resp:
                    if any(resp['state'] in progress_status for progress_status
                            in IN_PROGRESS_STATES):
                        time.sleep(10)
                        count = count + 1
                        if count == 90:
                            # Wait for max 15 minutes for host to realize
                            return False
                    elif any(resp['state'] in progress_status for
                             progress_status in SUCCESS_STATES):
                        return True
                    else:
                        # Failed State
                        return False
                else:
                    if rc != 200:
                        time.sleep(1)
                        count = count + 1
                        if count == 90:
                            # Wait for max 15 minutes for host to realize
                            return False
                    else:
                        return True
        except Exception as err:
            return False

    def _fill_missing_resource_params(self, existing_params, resource_params):
        """
            resource_params: dict
            existing_params: dict

            Fills resource_params with the key:value from existing_params if
            missing in the former.
        """
        if not existing_params:
            return
        for k, v in existing_params.items():
            if k not in resource_params:
                resource_params[k] = v
            elif type(v).__name__ == 'dict':
                self._fill_missing_resource_params(v, resource_params[k])

    def _clean_none_resource_params(self, existing_params, resource_params):
        keys_to_remove = []
        for k, v in resource_params.items():
            if v is None and (
                    existing_params is None or k not in existing_params):
                keys_to_remove.append(k)
        for key in keys_to_remove:
            resource_params.pop(key)
        for k, v in resource_params.items():
            if type(v).__name__ == 'dict':
                self._clean_none_resource_params(existing_params, v)
