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
import cli.object_storage
import cli.pprint
import cli.util
import kamonohashi


@click.group(short_help='Handling data related information')
@click.pass_context
def data(ctx):
    """Handling various types of information related to data e.g. Create, Upload, Download, Delete, List. """
    api_client = cli.configuration.get_api_client()
    ctx.obj = kamonohashi.DataApi(api_client)


@data.command('list',
              help='List data of your tenant by query conditions')
@click.option('--count', type=int, help='A number of data you want to retrieve')
@click.option('--id', help='id')
@click.option('--name', help='name')
@click.option('--memo', help='memo')
@click.option('--created-at', help='created at')
@click.option('--created-by', help='created by')
@click.option('--tag', multiple=True, help='tag')
@click.pass_obj
def list_data(api, count, id, name, memo, created_at, created_by, tag):
    """
    :param kamonohashi.DataApi api:
    """
    command_args = {
        'id': id,
        'name': name,
        'memo': memo,
        'created_at': created_at,
        'created_by': created_by,
        'per_page': count,
        'tag': tag,
    }
    args = dict((key, value) for key, value in command_args.items() if value is not None)
    result = api.list_data(**args)
    cli.pprint.pp_table(['id', 'name', 'created_at', 'created_by', 'memo', 'tags'],
                        [[x.id, x.name, x.created_at, x.created_by, x.memo, x.tags] for x in result])


@data.command(help='Get the detail of the data specified by ID')
@click.argument('id', type=int)
@click.pass_obj
def get(api, id):
    """
    :param kamonohashi.DataApi api:
    """
    result = api.get_data(id)
    cli.pprint.pp_dict(cli.util.to_dict(result))


@data.command(help='Create a data with name and data file. You can also upload an annotation file.')
@click.option('-n', '--name', required=True, help='The name of this data. Name must be unique in a tenant.')
@click.option('-d', '--data-file', type=click.Path(exists=True, dir_okay=False),
              help="The path string to the data file you want to upload", required=True)
@click.option('-a', '--annotation-file', type=click.Path(exists=True, dir_okay=False),
              help="The path string to the annotation file you want to upload")
@click.option('-m', '--memo', help='Free text that can helpful to explain the data')
@click.option('-t', '--tags', multiple=True,
              help='Attributes to the data. You can specify multiples tags using -t option several times. e.g. -t tag1 -t tag2')
@click.pass_obj
def create(api, name, data_file, annotation_file, memo, tags):
    """
    :param kamonohashi.DataApi api:
    """
    data_info = cli.object_storage.upload_file(api.api_client, data_file, 'Data')
    model = kamonohashi.DataApiModelsCreateInputModel(
        image_file_name=data_info.file_name,
        image_file_stored_path=data_info.stored_path,
        memo=memo,
        name=name,
        tags=list(tags)
    )
    if annotation_file:
        annotation_info = cli.object_storage.upload_file(api.api_client, annotation_file, 'Data')
        model.annotation_file_name = annotation_info.file_name
        model.annotation_file_stored_path = annotation_info.stored_path
    result = api.create_data(model=model)
    print('created', result.id)


@data.command(help='Update the date properties using data ID')
@click.argument('id', type=int)
@click.option('-m', '--memo', help='Free text that can helpful to explain the data')
@click.option('-t', '--tags', multiple=True, help='Free text that can helpful to explain the data')
@click.pass_obj
def update(api, id, memo, tags):
    """
    :param kamonohashi.DataApi api:
    """
    model = kamonohashi.DataApiModelsEditInputModel(memo=memo, tags=list(tags))
    result = api.update_data(id, model=model)
    print('updated', result.id)


@data.command(help='Delete the data using data ID')
@click.argument('id', type=int)
@click.pass_obj
def delete(api, id):
    """
    :param kamonohashi.DataApi api:
    """
    api.delete_data(id)
    print('deleted', id)


@data.command('list-files', help='List file information using data ID')
@click.argument('id', type=int)
@click.pass_obj
def list_files(api, id):
    """
    :param kamonohashi.DataApi api:
    """
    result = api.list_data_files(id)
    cli.pprint.pp_table(['file_id', 'key', 'file_name'],
                        [[x.file_id, x.key, x.file_name] for x in result])


@data.command('download-file', help='Download a file attached to data')
@click.argument('id', type=int)
@click.option('-d', '--destination', type=click.Path(exists=True, file_okay=False), required=True,
              help='A path to the output files')
@click.option('-k', '--key', type=click.Choice(['Image', 'Annotation']), required=True,
              help='File Key')
@click.pass_obj
def download_file(api, id, destination, key):
    """
    :param kamonohashi.DataApi api:
    """
    result = api.list_data_files(id, with_url=True)
    pool_manager = api.api_client.rest_client.pool_manager
    for x in result:
        if x.key == key:
            cli.object_storage.download_file(pool_manager, x.url, destination, x.file_name)


@data.command('upload-file', short_help='Upload an annotation file to specified data ID',
              help='Upload an annotation file to specified data ID. '
                   'This command only works when the annotation data is not uploaded yet.')
@click.argument('id', type=int)
@click.option('-f', '--file', type=click.Path(exists=True, dir_okay=False), required=True, help='A file path you want to upload')
@click.pass_obj
def upload_file(api, id, file):
    """
    :param kamonohashi.DataApi api:
    """
    annotation_info = cli.object_storage.upload_file(api.api_client, file, 'Data')
    model = kamonohashi.ComponentsAddFileInputModel(file_name=annotation_info.file_name, stored_path=annotation_info.stored_path)
    api.add_data_file(id, model=model)
