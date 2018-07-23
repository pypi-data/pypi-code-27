################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################


import logging
import re
import json

from .function_adapter import FunctionAdapter
from repository_v3.swagger_client.rest import ApiException
from repository_v3.mlrepository import MetaNames
from repository_v3.mlrepositoryartifact.function_artifact import FunctionArtifact
from repository_v3.swagger_client.models.ml_assets_create_function_input import MlAssetsCreateFunctionInput
from repository_v3.swagger_client.models import TagRepository

logger = logging.getLogger('FunctionCollection')


class FunctionCollection:
    """
    Client operating on functions in repository service.

    :param str base_path: base url to Watson Machine Learning instance
    :param MLRepositoryApi repository_api: client connecting to repository rest api
    :param MLRepositoryClient client: high level client used for simplification and argument for constructors
    """
    def __init__(self, base_path, repository_api, client):

        from repository_v3.mlrepositoryclient import MLRepositoryClient, MLRepositoryApi

        if not isinstance(base_path, str) and not isinstance(base_path, unicode):
            raise ValueError('Invalid type for base_path: {}'.format(base_path.__class__.__name__))

        if not isinstance(repository_api, MLRepositoryApi):
            raise ValueError('Invalid type for repository_api: {}'.format(repository_api.__class__.__name__))

        if not isinstance(client, MLRepositoryClient):
            raise ValueError('Invalid type for client: {}'.format(client.__class__.__name__))

        self.base_path = base_path
        self.repository_api = repository_api
        self.client = client

    def all(self, queryMap=None):
        """
        Gets info about all functions which belong to this user.

        Not complete information is provided by all(). To get detailed information about function use get().

        :return: info about functions
        :rtype: list[FunctionArtifact]
        """
        all_functions = self.repository_api.repository_functions_list(queryMap)
        list_functions_artifact = []
        if all_functions is not None:
            resr = all_functions.resources
            for iter1 in resr:
                list_functions_artifact.append(FunctionAdapter(iter1, self.client).artifact())
            return list_functions_artifact
        else:
            return []

    def get(self, artifact_id):
        """
        Gets detailed information about function.

        :param str artifact_id: uid used to identify function
        :return: returned object has all attributes of FunctionArtifact
        :rtype: FunctionArtifact
        """
        logger.debug('Fetching information about function: {}'.format(artifact_id))

        if not isinstance(artifact_id, str) and not isinstance(artifact_id, unicode):
            raise ValueError('Invalid type for artifact_id: {}'.format(artifact_id.__class__.__name__))

        function_output = self.repository_api.repository_function_get(artifact_id)

        if function_output is not None:

            return FunctionAdapter(function_output, self.client).artifact()
        else:
            logger.debug('Function with guid={} not found'.format(artifact_id))
            raise ApiException('Function with guid={} not found'.format(artifact_id))

    def revisions(self, artifact_id):
        """
        Gets all available revisions.

        :param str artifact_id: uid used to identify function
        :return: ???
        :rtype: list[str]
        """

        if not isinstance(artifact_id, str) and not isinstance(artifact_id, unicode):
            raise ValueError('Invalid type for artifact_id: {}'.format(artifact_id.__class__.__name__))

        logger.debug('Fetching information about function: {}'.format(artifact_id))

        function_output = self.repository_api.repository_list_function_revisions(artifact_id)

        list_function_revision_artifact = [FunctionArtifact]
        if function_output is not None:
            resr = function_output.resources
            for iter1 in resr:
                list_function_revision_artifact.append(FunctionAdapter(iter1, self.client).artifact())
            return list_function_revision_artifact
        else:
            logger.debug('Function with guid={} not found'.format(artifact_id))
            raise ApiException('Function with guid={} not found'.format(artifact_id))

    def revision(self, artifact_id, rev):
        """
        Gets Function revision with given artifact_id and ver
        :param str artifact_id: uid used to identify function
        :param str rev: uid used to identify revision of function
        :return: FunctionArtifact(FunctionLoader) -- returned object has all attributes of FunctionArtifact
        """
        logger.debug('Fetching information about function revision: {}, {}'.format(artifact_id, rev))

        if not isinstance(artifact_id, str) and not isinstance(artifact_id, unicode):
            raise ValueError('Invalid type for artifact_id: {}'.format(artifact_id.__class__.__name__))

        if not isinstance(rev, str) and not isinstance(rev, unicode):
            raise ValueError('Invalid type for rev: {}'.format(rev.__class__.__name__))

        function_revision_output = self.repository_api.repository_get_function_revision(artifact_id, rev)
        if function_revision_output is not None:
            if function_revision_output is not None:
                return FunctionAdapter(function_revision_output[0], self.client).artifact()
            else:
                raise Exception('Function with guid={} not found'.format(artifact_id))
        else:
            raise Exception('Function with guid={} not found'.format(artifact_id))

    def revision_from_href(self, artifact_revision_href):
        """
        Gets function revision from given href

        :param str artifact_revision_href: href identifying artifact and revision
        :return: returned object has all attributes of FunctionArtifact
        :rtype: FunctionArtifact(FunctionLoader)
        """

        if not isinstance(artifact_revision_href, str) and not isinstance(artifact_revision_href, unicode):
            raise ValueError('Invalid type for artifact_revision_href: {}'.format(artifact_revision_href.__class__.__name__))

        matched = re.search('.*/v4/functions/([A-Za-z0-9\-]+)/revisions/([A-Za-z0-9\-]+)',
                            artifact_revision_href)
        if matched is not None:
            artifact_id = matched.group(1)
            revision_id = matched.group(2)
            return self.revision(artifact_id, revision_id)
        else:
            raise ValueError('Unexpected artifact revision href: {} format'.format(artifact_revision_href))

    def save(self, artifact):
        """
        Saves function in repository service.

        :param FunctionArtifact artifact: artifact to be saved in the repository service
        :return: saved artifact with changed MetaProps
        :rtype: FunctionArtifact
        """

        logger.debug('Creating a new function: {}'.format(artifact.name))

        if not issubclass(type(artifact), FunctionArtifact) :
            raise ValueError('Invalid type for artifact: {}'.format(artifact.__class__.__name__))

        if artifact.meta.prop(MetaNames.FUNCTIONS.REVISION_URL) is not None:
            raise ApiException(400, 'Invalid operation: save the same function artifact twice')

        try:
            function_id = artifact.uid
            if function_id is None:
                function_input = self._prepare_function_input(artifact)
                r = self.repository_api.repository_new_function(function_input)
                statuscode = r[1]
                if statuscode is not 201:
                    logger.info('Error while creating function: no location header')
                    raise ApiException(404, 'No artifact location')

                function_artifact = self._extract_function_from_output(r)
                location = r[2].get('Location')
                location_match = re.search('.*/v4/functions/([A-Za-z0-9\\-]+)', location)

                if location_match is not None:
                    function_id = location_match.group(1)
                else:
                    logger.info('Error while creating function: no location header')
                    raise ApiException(404, 'No artifact location')
                artifact_with_guid = artifact._copy(function_id)
                revision_location = function_artifact.meta.prop(MetaNames.FUNCTIONS.REVISION_URL)
                revision_id = function_artifact.meta.prop(MetaNames.FUNCTIONS.REVISION)

                if revision_location is not None:
                    content_stream = artifact_with_guid.reader().read()
                    self.repository_api.upload_function_revision(function_id, revision_id, content_stream)
                    content_stream.close()
                    artifact_with_guid.reader().close()
                    return function_artifact
                else:
                    logger.info('Error while creating function revision: no location header')
                    raise ApiException(404, 'No artifact location')
            else:
                raise ApiException(404, 'Function not found')

        except Exception as e:
            logger.info('Error in function creation')
            import traceback
            print(traceback.format_exc())
            raise e

    def _extract_function_from_output(self, service_output):
        return FunctionAdapter(service_output[0], self.client).artifact()

    @staticmethod
    def _prepare_function_input(artifact):
        function_input = MlAssetsCreateFunctionInput()
        function_input.name = artifact.name
        function_input.description = artifact.meta.prop(MetaNames.FUNCTIONS.DESCRIPTION)
        function_input.type = artifact.meta.prop(MetaNames.FUNCTIONS.TYPE)
        function_input.runtime_url = artifact.meta.prop(MetaNames.RUNTIMES.URL)

        input_data_schema = artifact.meta.prop(MetaNames.FUNCTIONS.INPUT_DATA_SCHEMA)
        output_data_schema = artifact.meta.prop(MetaNames.FUNCTIONS.OUTPUT_DATA_SCHEMA)


        function_input.input_data_schema = input_data_schema
        function_input.output_data_schema = output_data_schema
        if artifact.meta.prop(MetaNames.FUNCTIONS.TAGS) is not None:
            tags=artifact.meta.prop(MetaNames.FUNCTIONS.TAGS)
            tags_data_list = []
            if isinstance(tags, str):
                tags_list = json.loads(artifact.meta.prop(MetaNames.FUNCTIONS.TAGS))
                if isinstance(tags_list, list):
                    for iter1 in tags_list:
                        tags_data = TagRepository()
                        for key in iter1:
                            if key == 'value':
                                tags_data.value= iter1['value']
                            if key == 'description':
                                tags_data.description = iter1['description']
                        tags_data_list.append(tags_data)
                else:
                    raise ValueError("Invalid tag Input")
                function_input.tags =  tags_data_list

        return function_input
