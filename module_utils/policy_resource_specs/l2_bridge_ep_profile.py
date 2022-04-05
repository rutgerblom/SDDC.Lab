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
    edge_nodes_info=dict(
        required=True,
        type='list',
        elements='dict',
        options=dict(
            # Note that only default site_id and
            # enforcementpoint_id are used
            site_id=dict(
                type='str',
                default="default"
            ),
            enforcementpoint_id=dict(
                type='str',
                default="default"
            ),
            edge_cluster_id=dict(
                type='str'
            ),
            edge_cluster_display_name=dict(
                type='str'
            ),
            edge_node_id=dict(
                type='str'
            ),
            edge_node_display_name=dict(
                type='str'
            )
        )
    ),
    enforcementpoint_id=dict(
        type='str',
        default="default"
    ),
    failover_mode=dict(
        required=False,
        default="PREEMPTIVE",
        choices=["PREEMPTIVE", "NON_PREEMPTIVE"],
        type='str'
    ),
    ha_mode=dict(
        required=False,
        type='str',
        default="ACTIVE_STANDBY",
        choices=["ACTIVE_STANDBY"]
    ),
    site_id=dict(
        type='str',
        default="default"
    ),
)
