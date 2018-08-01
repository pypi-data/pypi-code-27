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

import io
import json
import logging

import click

import cli.configuration
import cli.pprint
import cli.util
import kamonohashi


@click.group()
@click.pass_context
def preprocessing(ctx):
    """Create/Update/Delete preprocessing"""
    api_client = cli.configuration.get_api_client()
    ctx.obj = kamonohashi.PreprocessingApi(api_client)


@preprocessing.command('list', help='List all preprocesssings by query conditions')
@click.option('--count', type=int, help='A number of preprocessing you want to retrieve')
@click.option('--id', help='id')
@click.option('--name', help='name')
@click.option('--created-at', help='created at')
@click.option('--memo', help='memo')
@click.pass_obj
def list_preprocessings(api, count, id, name, created_at, memo):
    """
    :param kamonohashi.PreprocessingApi api:
    """
    command_args = {
        'id': id,
        'name': name,
        'memo': memo,
        'created_at': created_at,
        'per_page': count,
    }
    args = dict((key, value) for key, value in command_args.items() if value is not None)
    result = api.list_preprocessings(**args)
    cli.pprint.pp_table(['id', 'name', 'created_at', 'memo'],
                        [[x.id, x.name, x.created_at, x.memo] for x in result])


@preprocessing.command(help='Get a preprocessing detail as a json or printing to console using a preprocessing ID')
@click.argument('id', type=int)
@click.option('-j', '--json', 'is_json', is_flag=True, help='Download a json file or print the content to console')
@click.option('-d', '--destination', type=click.Path(dir_okay=False), help='A file path of the output json file')
@click.pass_obj
def get(api, id, is_json, destination):
    """
    :param kamonohashi.PreprocessingApi api:
    """
    if is_json:
        with cli.util.release_conn(api.get_preprocessing(id, _preload_content=False)) as result:
            logging.info('open %s', destination)
            with io.open(destination, 'w', encoding='utf-8') as f:
                logging.info('begin io %s', destination)
                f.write(result.data.decode('utf-8'))
                logging.info('end io %s', destination)
        print('save', id, 'as', destination)
    else:
        result = api.get_preprocessing(id)
        cli.pprint.pp_dict(cli.util.to_dict(result))


@preprocessing.command(help='Create a new preprocessing')
@click.option('-f', '--file', required=True, type=click.Path(exists=True, dir_okay=False),
              help="""{
  "name": @name,
  "entryPoint": @entryPoint,
  "containerImage": {
    "image": @image,
    "tag": "@tag,
  },
  "gitModel": {
    "repository": @repository,
    "owner": @owner,
    "branch": @branch,
    "commitId": @commitId,
  },
  "memo": @memo
}""")
@click.pass_obj
def create(api, file):
    """
    :param kamonohashi.PreprocessingApi api:
    """
    logging.info('open %s', file)
    with io.open(file, 'r', encoding='utf-8') as f:
        logging.info('begin io %s', file)
        json_dict = json.load(f)
        logging.info('end io %s', file)
    result = api.create_preprocessing(model=json_dict)
    print('created', result.id)


@preprocessing.command(help='Update a preprocessing using preprocess ID')
@click.argument('id', type=int)
@click.option('-f', '--file', required=True, type=click.Path(exists=True, dir_okay=False),
              help="""{
  "name": @name,
  "entryPoint": @entryPoint,
  "containerImage": {
    "image": @image,
    "tag": "@tag,
  },
  "gitModel": {
    "repository": @repository,
    "owner": @owner,
    "branch": @branch,
    "commitId": @commitId,
  },
  "memo": @memo
}""")
@click.pass_obj
def update(api, id, file):
    """
    :param kamonohashi.PreprocessingApi api:
    """
    logging.info('open %s', file)
    with io.open(file, 'r', encoding='utf-8') as f:
        logging.info('begin io %s', file)
        json_dict = json.load(f)
        logging.info('end io %s', file)
    result = api.update_preprocessing(id, model=json_dict)
    print('updated', result.id)


@preprocessing.command('update-meta-info', help="Update preprocessing's metadata (name and memo)")
@click.argument('id', type=int)
@click.option('-n', '--name', help='A name you want to update')
@click.option('-m', '--memo', help='A memo you want to update')
@click.pass_obj
def patch(api, id, name, memo):
    """
    :param kamonohashi.PreprocessingApi api:
    """
    model = kamonohashi.PreprocessingApiModelsEditInputModel(name=name, memo=memo)
    result = api.patch_preprocessing(id, model=model)
    print('meta-info updated', result.id)


@preprocessing.command(help='Delete a preprocesssing using preprocessing ID')
@click.argument('id', type=int)
@click.pass_obj
def delete(api, id):
    """
    :param kamonohashi.PreprocessingApi api:
    """
    api.delete_preprocessing(id)
    print('deleted', id)
