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
def registry(ctx):
    """Retrieve docker images information"""
    api_client = cli.configuration.get_api_client()
    ctx.obj = kamonohashi.RegistryApi(api_client)


@registry.command('list-container-images', help='List all docker images in the registry')
@click.pass_obj
def list_container_images(api):
    """
    :param kamonohashi.RegistryApi api:
    """
    result = api.list_container_images()
    for x in result:
        print(x)


@registry.command('list-container-image-tags', help='List all tags of the docker image')
@click.option('-i', '--image', required=True, help='A name of the image you want to list all tags')
@click.pass_obj
def list_container_image_tags(api, image):
    """
    :param kamonohashi.RegistryApi api:
    """
    result = api.list_container_image_tags(image)
    for x in result:
        print(x)
