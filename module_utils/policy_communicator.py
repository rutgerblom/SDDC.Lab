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


import json
import hashlib

from ansible.module_utils.urls import open_url
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.vmware_nsxt import get_certificate_file_path
from ansible.module_utils.vmware_nsxt import is_json


class PolicyCommunicator:

    __instances = dict()

    @staticmethod
    def check_for_authorization_header(request_headers):
        if 'Authorization' in request_headers:
            return True
        return False

    @staticmethod
    def get_instance(mgr_hostname, mgr_username=None, mgr_password=None,
                     nsx_cert_path=None, nsx_key_path=None, request_headers={},
                     ca_path=None, validate_certs=True):
        """
            Returns an instance of PolicyCommunicator associated with
            (mgr_hostname, mgr_username, mgr_password) or
            (mgr_hostname, nsx_cert_path, nsx_key_path)
        """
        if mgr_username is not None:
            if mgr_password is None:
                raise InvalidInstanceRequest("mgr_password ")
            key = tuple([mgr_hostname, mgr_username, mgr_password])
        elif nsx_cert_path is not None:
            if not nsx_cert_path.endswith('.p12') and nsx_key_path is None:
                raise InvalidInstanceRequest("nsx_key_path")
            key = tuple([mgr_hostname, nsx_cert_path, nsx_key_path])
        elif get_certificate_file_path('NSX_MANAGER_CERT_PATH') is not None:
            nsx_cert_path = get_certificate_file_path('NSX_MANAGER_CERT_PATH')
            key = tuple([mgr_hostname, nsx_cert_path])
        elif PolicyCommunicator.check_for_authorization_header(
                request_headers):
            key = tuple([request_headers['Authorization']])
        else:
            raise InvalidInstanceRequest("(mgr_username, mgr_password) or"
                                         "(nsx_cert_path, nsx_key_path), or "
                                         "environment variable "
                                         "'NSX_MANAGER_CERT_PATH'")
        if key not in PolicyCommunicator.__instances:
            PolicyCommunicator(key, mgr_hostname, mgr_username, mgr_password,
                               nsx_cert_path, nsx_key_path, request_headers,
                               ca_path, validate_certs)
        return PolicyCommunicator.__instances.get(key)

    def __init__(self, key, mgr_hostname, mgr_username, mgr_password,
                 nsx_cert_path, nsx_key_path, request_headers,
                 ca_path, validate_certs):
        if key in PolicyCommunicator.__instances:
            raise Exception("The associated PolicyCommunicator is"
                            " already present! Please use getInstance to"
                            " retrieve it.")
        else:
            self.use_basic_auth = False
            if mgr_username is not None:
                self.use_basic_auth = True
            self.mgr_username = mgr_username
            self.mgr_password = mgr_password
            self.nsx_cert_path = nsx_cert_path
            self.nsx_key_path = nsx_key_path

            self.request_headers = request_headers or {}
            self.request_headers.update({
                'Accept': 'application/json',
                'Content-Type': 'application/json'})

            self.ca_path = ca_path
            self.validate_certs = validate_certs

            self.policy_url = 'https://{}/policy/api/v1'.format(mgr_hostname)
            self.active_requests = set()

            PolicyCommunicator.__instances[key] = self

    @staticmethod
    def get_vmware_argument_spec():
        return dict(
            hostname=dict(type='str', required=True),
            username=dict(type='str', required=False),
            password=dict(type='str', required=False, no_log=True),
            port=dict(type='int', default=443),
            validate_certs=dict(type='bool', requried=False, default=True),
            nsx_cert_path=dict(type='str', requried=False),
            nsx_key_path=dict(type='str', requried=False),
            request_headers=dict(type='dict'),
            ca_path=dict(type='str')
        )

    def request(self, url, data=None, method='GET',
                use_proxy=True, force=False, last_mod_time=None,
                timeout=300, http_agent=None, ignore_errors=False):
        # prepend the policy url
        url = self.policy_url + url
        # create a request ID associated with this request
        request_id = self._get_request_id(url, data, method)
        if self.register_request(request_id):
            # new request
            try:
                # connect to the API server
                if data is not None:
                    data = json.dumps(data)
                response = open_url(url=url, data=data,
                                    headers=self.request_headers,
                                    method=method,
                                    use_proxy=use_proxy, force=force,
                                    last_mod_time=last_mod_time,
                                    timeout=timeout,
                                    validate_certs=self.validate_certs,
                                    url_username=self.mgr_username,
                                    url_password=self.mgr_password,
                                    http_agent=http_agent,
                                    force_basic_auth=self.use_basic_auth,
                                    client_cert=self.nsx_cert_path,
                                    client_key=self.nsx_key_path,
                                    ca_path=self.ca_path)
            except HTTPError as err:
                response = err
            resp_code = response.getcode()
            resp_raw_data = response.read().decode('utf-8')

            # request completed by the server
            self.active_requests.remove(request_id)

            try:
                resp_data = resp_raw_data
                # infer the response
                if resp_raw_data and is_json(resp_raw_data):
                    resp_data = json.loads(resp_raw_data)
            except Exception as e:
                if not ignore_errors:
                    raise Exception(resp_code, resp_raw_data)

            # return the approprate response code and data
            if resp_code >= 400 and not ignore_errors:
                raise Exception(resp_code, resp_data)
            if resp_data is not None and 'error_code' in resp_data:
                raise Exception(resp_data['error_code'], resp_data)
            else:
                return resp_code, resp_data
        else:
            raise DuplicateRequestError

    def _get_request_id(self, url, data=None, method='GET'):
        """
            Creates a hash from url, data, and method that can be used
            as a request ID.
        """
        request = dict()
        request["data"] = data
        request['request_url'] = url
        request['request_method'] = method

        return hashlib.md5(json.dumps(request, sort_keys=True).
                           encode('utf-8')).hexdigest()

    def register_request(self, request_id):
        """
            This creates a hash from URL and data and stores it in a cache.
            If a same hash is created, the request is identified as a duplicate
            and it returns False. Otherwise, returns True.
        """
        if request_id in self.active_requests:
            return False
        self.active_requests.add(request_id)
        return True


class DuplicateRequestError(Exception):
    pass


class InvalidInstanceRequest(Exception):

    message = "Invalid instance Request, missing {}"

    def __init__(self, missing_fields):
        super(Exception, self).__init__(self.message.format(missing_fields))
