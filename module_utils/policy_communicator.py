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


class PolicyCommunicator:

    __instances = dict()

    @staticmethod
    def get_instance(mgr_username, mgr_hostname, mgr_password):
        """
            Returns an instance of PolicyCommunicator associated with
            mgr_username, mgr_hostname, mgr_password
        """
        key = tuple([mgr_username, mgr_hostname, mgr_password])
        if key not in PolicyCommunicator.__instances:
            PolicyCommunicator(mgr_username, mgr_hostname,
                               mgr_password)
        return PolicyCommunicator.__instances.get(key)

    def __init__(self, mgr_username, mgr_hostname, mgr_password):
        key = tuple([mgr_username, mgr_hostname, mgr_password])
        if key in PolicyCommunicator.__instances:
            raise Exception("The associated PolicyCommunicator is"
                            " already present! Please use getInstance to"
                            " retrieve it.")
        else:
            self.mgr_username = mgr_username
            self.policy_url = 'https://{}/policy/api/v1'.format(mgr_hostname)
            self.mgr_password = mgr_password
            self.active_requests = set()

            PolicyCommunicator.__instances[key] = self

    @staticmethod
    def get_vmware_argument_spec():
        return dict(
            hostname=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            port=dict(type='int', default=443),
            validate_certs=dict(type='bool', requried=False, default=True)
        )

    def request(self, url, data=None, headers={'Accept': 'application/json',
                'Content-Type': 'application/json'}, method='GET',
                use_proxy=True, force=False, last_mod_time=None,
                timeout=300, validate_certs=True, http_agent=None,
                force_basic_auth=True, ignore_errors=False):
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
                response = open_url(url=url, data=data, headers=headers,
                                    method=method,
                                    use_proxy=use_proxy, force=force,
                                    last_mod_time=last_mod_time,
                                    timeout=timeout,
                                    validate_certs=validate_certs,
                                    url_username=self.mgr_username,
                                    url_password=self.mgr_password,
                                    http_agent=http_agent,
                                    force_basic_auth=force_basic_auth)
                resp_code = response.getcode()
                resp_raw_data = response.read().decode('utf-8') or None
            except HTTPError as err:
                response = err.fp
                resp_code = response.getcode()
                resp_raw_data = err.fp.read().decode('utf-8')

            # request completed by the server
            self.active_requests.remove(request_id)

            try:
                # infer the response
                if resp_raw_data:
                    resp_data = json.loads(resp_raw_data)
                elif data is not None:
                    resp_data = json.loads(data)
                else:
                    resp_data = None
            except Exception as e:
                if ignore_errors:
                    pass
                else:
                    raise Exception(resp_raw_data)

            # return the approprate response code and data
            if resp_code >= 400 and not ignore_errors:
                raise Exception(resp_code, None)
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