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

SPEC = dict(
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
        required=False,
        type='str',
        default="default"
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
