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
import os.path

import click

import cli.configuration
import cli.object_storage
import cli.pprint
import cli.util
import kamonohashi


@click.group()
@click.pass_context
def data_set(ctx):
    """Create/Update/Delete/Download your datasets."""
    api_client = cli.configuration.get_api_client()
    ctx.obj = kamonohashi.DataSetApi(api_client)


@data_set.command('list', help='List datasets in your tenant')
@click.option('--count', type=int, help='A number of dataset you want to retrieve')
@click.option('--id', help='id')
@click.option('--name', help='name')
@click.option('--memo', help='memo')
@click.option('--created-at', help='created at')
@click.pass_obj
def list_datasets(api, count, id, name, memo, created_at):
    """
    :param kamonohashi.DataSetApi api:
    """
    command_args = {
        'id': id,
        'name': name,
        'memo': memo,
        'created_at': created_at,
        'per_page': count,
    }
    args = dict((key, value) for key, value in command_args.items() if value is not None)
    result = api.list_datasets(**args)
    cli.pprint.pp_table(['id', 'name', 'created_at', 'memo'],
                        [[x.id, x.name, x.created_at, x.memo] for x in result])


@data_set.command(short_help='Get a detaset detail using dataset ID',
                  help='Get a dataset detail as a json or printing to console using a dataset ID. \
                  If you only specify the file name e.g. dataset.json, the command writes a json file to your current directory.')
@click.argument('id', type=int)
@click.option('-j', '--json', 'is_json', is_flag=True, help='Download a json file or print the content to console')
@click.option('-d', '--destination', type=click.Path(dir_okay=False), help='A file path of the output json file')
@click.pass_obj
def get(api, id, is_json, destination):
    """
    :param kamonohashi.DataSetApi api:
    """
    if is_json:
        with cli.util.release_conn(api.get_dataset(id, _preload_content=False)) as result:
            logging.info('open %s', destination)
            with io.open(destination, 'w', encoding='utf-8') as f:
                logging.info('begin io %s', destination)
                f.write(result.data.decode('utf-8'))
                logging.info('end io %s', destination)
        print('save', id, 'as', destination)
    else:
        result = api.get_dataset(id)
        cli.pprint.pp_dict(cli.util.to_dict(result))


@data_set.command(help='Create a new dataset')
@click.option('-f', '--file', required=True, type=click.Path(exists=True, dir_okay=False),
              help="""{
  "name": @name,
  "memo": @memo,
  "entries": {
    "additionalProp1": [
      {
        "id": @dataId
      }
    ],
    "additionalProp2": [
      {
        "id": @dataId
      }
    ],
    "additionalProp3": [
      {
        "id": @dataId
      }
    ]
  }
}""")
@click.pass_obj
def create(api, file):
    """
    :param kamonohashi.DataSetApi api:
    """
    logging.info('open %s', file)
    with io.open(file, 'r', encoding='utf-8') as f:
        logging.info('begin io %s', file)
        json_dict = json.load(f)
        logging.info('end io %s', file)
    result = api.create_dataset(model=json_dict)
    print('created', result.id)


@data_set.command(help='Update a dataset using dataset ID')
@click.argument('id', type=int)
@click.option('-f', '--file', required=True, type=click.Path(exists=True, dir_okay=False),
              help="""{
  "name": @name,
  "memo": @memo,
  "entries": {
    "additionalProp1": [
      {
        "id": @dataId
      }
    ],
    "additionalProp2": [
      {
        "id": @dataId
      }
    ],
    "additionalProp3": [
      {
        "id": @dataId
      }
    ]
  }
}""")
@click.pass_obj
def update(api, id, file):
    """
    :param kamonohashi.DataSetApi api:
    """
    logging.info('open %s', file)
    with io.open(file, 'r', encoding='utf-8') as f:
        logging.info('begin io %s', file)
        json_dict = json.load(f)
        logging.info('end io %s', file)
    result = api.update_dataset(id, model=json_dict)
    print('updated', result.id)


@data_set.command('update-meta-info', help="Update dataset's metadata (name and memo)")
@click.argument('id', type=int)
@click.option('-n', '--name', help='A name you want to update')
@click.option('-m', '--memo', help='A memo you want to update')
@click.pass_obj
def update_meta_info(api, id, name, memo):
    """
    :param kamonohashi.DataSetApi api:
    """
    model = kamonohashi.DataSetApiModelsEditInputModel(name=name, memo=memo)
    result = api.patch_dataset(id, model=model)
    print('meta-info updated', result.id)


@data_set.command(help='Delete a dataset using dataset ID')
@click.argument('id', type=int)
@click.pass_obj
def delete(api, id):
    """
    :param kamonohashi.DataSetApi api:
    """
    api.delete_dataset(id)
    print('deleted', id)


@data_set.command('download-files', help="Download dataset's content data using dataset ID")
@click.argument('id', type=int)
@click.option('-d', '--destination', type=click.Path(exists=True, file_okay=False), required=True, help='A file path of the output data')
@click.pass_obj
def download_files(api, id, destination):
    """
    :param kamonohashi.DataSetApi api:
    """
    result = api.list_dataset_files(id, with_url=True)
    pool_manager = api.api_client.rest_client.pool_manager
    for entry in result.entries:
        for file in entry.files:
            destination_dir_path = os.path.join(destination, entry.type, file.key, str(file.id))
            cli.object_storage.download_file(pool_manager, file.url, destination_dir_path, file.file_name)


@data_set.command('list-data-types',
    help='List data types of the dataset. Data type is a concept of dataset group like training, testing and validation.'
    'You can define any name of dataset type in the future release. Currently we only support training, testing '
    'and validation')
@click.pass_obj
def list_data_types(api):
    """
    :param kamonohashi.DataSetApi api:
    """
    result = api.list_dataset_datatypes()
    for x in result:
        print(x.name)
