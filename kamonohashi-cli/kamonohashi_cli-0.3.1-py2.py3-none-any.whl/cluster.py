# -*- coding: utf-8 -*-
# Copyright 2018 NS Solutions Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import print_function, absolute_import, with_statement

import click

import cli.configuration
import kamonohashi


@click.group()
@click.pass_context
def cluster(ctx):
    """Handling various types of information related to cluster """
    api_client = cli.configuration.get_api_client()
    ctx.obj = kamonohashi.ClusterApi(api_client)


@cluster.command('list-partitions', help='List partitions of the tenant')
@click.pass_obj
def list_partitions(api):
    """
    :param kamonohashi.ClusterApi api:
    """
    result = api.list_partitions()
    for x in result:
        print(x)
