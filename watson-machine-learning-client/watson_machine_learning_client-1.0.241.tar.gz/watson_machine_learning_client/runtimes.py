################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
import requests
import json
from watson_machine_learning_client.utils import INSTANCE_DETAILS_TYPE, RUNTIME_SPEC_DETAILS_TYPE, STR_TYPE, STR_TYPE_NAME, docstring_parameter, str_type_conv, print_text_header_h2
from watson_machine_learning_client.wml_client_error import WMLClientError
from watson_machine_learning_client.href_definitions import is_uid
from watson_machine_learning_client.wml_resource import WMLResource
from watson_machine_learning_client.metanames import RuntimeMetaNames
from repository_v3.mlrepositoryartifact import MLRepositoryArtifact
from repository_v3.mlrepository import MetaProps, MetaNames


class Runtimes(WMLResource):
    """
        Creates Runtime Specs and associated Custom Libraries.
    """
    def __init__(self, client):
        WMLResource.__init__(self, __name__, client)
        Runtimes._validate_type(client.service_instance.details, u'instance_details', dict, True)
        Runtimes._validate_type_of_details(client.service_instance.details, INSTANCE_DETAILS_TYPE)
        self.ConfigurationMetaNames = RuntimeMetaNames()

    def _create_custom_library(self, definition):
        self._validate_meta_prop(definition, 'name', STR_TYPE, True)
        self._validate_meta_prop(definition, 'version', STR_TYPE, True)
        self._validate_meta_prop(definition, 'platform', dict, True)
        self._validate_meta_prop(definition, 'description', STR_TYPE, False)

        lib_metadata = {
            MetaNames.LIBRARIES.NAME: definition['name'],
            MetaNames.LIBRARIES.VERSION: definition['version'],
            MetaNames.LIBRARIES.PLATFORM: json.dumps(definition['platform'])
        }

        if 'description' in definition:
            lib_metadata[MetaNames.LIBRARIES.DESCRIPTION] = definition['description']

        try:
            libArtifact = MLRepositoryArtifact(definition['filepath'], meta_props=MetaProps(lib_metadata.copy()))
            lib_artifact = self._client.repository._ml_repository_client.libraries.save(libArtifact)
            return lib_artifact.uid
        except Exception as e:
            raise WMLClientError('Failure during creation of custom library.', e)

    def _create_runtime_spec(self, custom_libs_list, meta_props):
        metadata = {
            MetaNames.RUNTIMES.NAME: meta_props[self.ConfigurationMetaNames.NAME],
            MetaNames.RUNTIMES.PLATFORM: json.dumps(meta_props[self.ConfigurationMetaNames.PLATFORM]),
        }

        if self.ConfigurationMetaNames.DESCRIPTION in meta_props:
            metadata[MetaNames.DESCRIPTION] = meta_props[self.ConfigurationMetaNames.DESCRIPTION]

        if custom_libs_list is not None:
            metadata[MetaNames.RUNTIMES.CUSTOM_LIBRARIES_URLS] = json.dumps({
                "urls": [self._href_definitions.get_custom_library_href(uid) for uid in custom_libs_list]
            })

        if self.ConfigurationMetaNames.CONFIGURATION_FILEPATH in meta_props:
            metadata[MetaNames.CONTENT_LOCATION] = meta_props[self.ConfigurationMetaNames.CONFIGURATION_FILEPATH]

        try:
            runtimeArtifact = MLRepositoryArtifact(meta_props=MetaProps(metadata.copy()))
            if self.ConfigurationMetaNames.CONFIGURATION_FILEPATH in meta_props:
                runtime_artifact = self._client.repository._ml_repository_client.runtimes.save(
                    runtimeArtifact,
                    meta_props[self.ConfigurationMetaNames.CONFIGURATION_FILEPATH]
                )
            else:
                runtime_artifact = self._client.repository._ml_repository_client.runtimes.save(runtimeArtifact)
            return runtime_artifact.uid
        except Exception as e:
            raise WMLClientError('Failure during creation of runtime.', e)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def create(self, meta_props):
        """
            Create runtime.

            :param meta_props: dictionary with parameters describing runtime spec
            :type meta_props: dict

            :returns: details of created runtime
            :rtype: dict

            A way you might use me is:

             >>> runtime_details = client.runtimes.create({
                    client.runtimes.ConfigurationMetaNames.NAME: "test",
                    client.runtimes.ConfigurationMetaNames.PLATFORM: {"name": "python", "version": "3.5"}
                 })
         """
        self.ConfigurationMetaNames._validate(meta_props)

        custom_libs_list = []

        if self.ConfigurationMetaNames.CUSTOM_LIBRARIES_DEFINITIONS in meta_props:
            custom_libs_list.extend(
                [self._create_custom_library(definition) for definition in
                 meta_props[self.ConfigurationMetaNames.CUSTOM_LIBRARIES_DEFINITIONS]]
            )

        if self.ConfigurationMetaNames.CUSTOM_LIBRARIES_UIDS in meta_props:
            custom_libs_list.extend(meta_props[self.ConfigurationMetaNames.CUSTOM_LIBRARIES_UIDS])

        runtime_uid = self._create_runtime_spec(custom_libs_list, meta_props)

        return self.get_details(runtime_uid)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_details(self, runtime_uid=None, limit=None):
        """
           Get information about your runtime(s).

           :param runtime_uid:  Runtime UID (optional)
           :type runtime_uid: {str_type}

           :param limit: limit number of fetched records (optional)
           :type limit: int

           :returns: metadata of runtime(s)
           :rtype: dict

           A way you might use me is:

            >>> runtime_details = client.runtimes.get_details(runtime_uid)
            >>> runtime_details = client.runtimes.get_details(runtime_uid=runtime_uid)
            >>> runtime_details = client.runtimes.get_details()
        """
        runtime_uid = str_type_conv(runtime_uid)
        Runtimes._validate_type(runtime_uid, u'runtime_uid', STR_TYPE, False)

        if runtime_uid is not None and not is_uid(runtime_uid):
            raise WMLClientError(u'\'runtime_uid\' is not an uid: \'{}\''.format(runtime_uid))

        url = self._href_definitions.get_runtime_specs_href()

        return self._get_artifact_details(url, runtime_uid, limit, 'runtimes')

    def _get_custom_libraries_details(self, library_uid=None, limit=None):
        library_uid = str_type_conv(library_uid)
        Runtimes._validate_type(library_uid, u'library_uid', STR_TYPE, False)

        if library_uid is not None and not is_uid(library_uid):
            raise WMLClientError(u'\'library_uid\' is not an uid: \'{}\''.format(library_uid))

        url = self._href_definitions.get_custom_libraries_href()

        return self._get_artifact_details(url, library_uid, limit, 'custom libraries')

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_url(runtime_details):
        """
            Get runtime url from runtime details.

            :param runtime_details: Created runtime details
            :type runtime_details: dict

            :returns: runtime url
            :rtype: {str_type}

            A way you might use me is:

             >>> runtime_url = client.runtimes.get_url(runtime_details)
        """
        Runtimes._validate_type(runtime_details, u'runtime_details', dict, True)
        Runtimes._validate_type_of_details(runtime_details, RUNTIME_SPEC_DETAILS_TYPE)

        return Runtimes._get_required_element_from_dict(runtime_details, 'runtime_details', ['metadata', 'url'])

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_uid(runtime_details):
        """
            Get runtime uid from runtime details.

            :param runtime_details: Created runtime details
            :type runtime_details: dict

            :returns: runtime uid
            :rtype: {str_type}

            A way you might use me is:

            >>> runtime_uid = client.runtimes.get_uid(runtime_details)
        """
        Runtimes._validate_type(runtime_details, u'runtime_details', dict, True)
        Runtimes._validate_type_of_details(runtime_details, RUNTIME_SPEC_DETAILS_TYPE)

        # TODO error handling
        return Runtimes._get_required_element_from_dict(runtime_details, 'runtime_details', ['metadata', 'guid'])

    def _get_runtimes_uids_for_lib(self, library_uid, runtime_details=None):
        if runtime_details is None:
            runtime_details = self.get_details()

        return list(map(
            lambda x: x['metadata']['guid'],
            filter(
                lambda x: any(
                    filter(
                        lambda y: library_uid in y['url'],
                        x['entity']['custom_libraries'] if 'custom_libraries' in x['entity'] else [])
                ),
                runtime_details['resources']
            )
        ))

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete(self, runtime_uid, cascade=False):
        """
            Delete runtime.

            :param runtime_uid: Runtime UID
            :type runtime_uid: {str_type}

            :param cascade: if set to False, only runtime will be removed, if set to True, all custom_libraries belonging only to it will be removed
            :type cascade: bool

            A way you might use me is:

            >>> client.runtimes.delete(runtime_uid)
        """
        runtime_uid = str_type_conv(runtime_uid)
        Runtimes._validate_type(runtime_uid, u'runtime_uid', STR_TYPE, True)
        Runtimes._validate_type(cascade, u'cascade', bool, True)

        if runtime_uid is not None and not is_uid(runtime_uid):
            raise WMLClientError(u'\'runtime_uid\' is not an uid: \'{}\''.format(runtime_uid))

        if cascade:
            runtime_details = self.get_details(runtime_uid)

        url = self._href_definitions.get_runtime_spec_href(runtime_uid)

        response_delete = requests.delete(
            url,
            headers=self._client._get_headers())

        self._handle_response(204, u'runtime deletion', response_delete, False)

        if cascade:
            if 'custom_libraries' in runtime_details['entity']:
                details = self.get_details()
                custom_libs_uids = map(lambda x: x['url'].split('/')[-1], runtime_details['entity']['custom_libraries'])
                custom_libs_to_remove = filter(
                    lambda x: len(self._get_runtimes_uids_for_lib(x, details)) == 0,
                    custom_libs_uids
                )

                for uid in custom_libs_to_remove:
                    print('Deleting orphaned custom library \'{}\' during cascade delete.'.format(uid))
                    self.delete_custom_library(uid)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete_orphaned_custom_libraries(self):
        """
            Delete all custom libraries without runtime.

            A way you might use me is:
            >>> client.repository.delete_orphaned_custom_libraries()
        """
        lib_details = self._get_custom_libraries_details()
        for lib in lib_details['resources']:
            print('Deleting orphaned \'{}\' custom library... '.format(lib['metadata']['guid']), end="")
            library_endpoint = self._href_definitions.get_custom_library_href(lib['metadata']['guid'])
            response_delete = requests.delete(library_endpoint, headers=self._client._get_headers())

            try:
                self._handle_response(204, u'custom library deletion', response_delete, False)
                print('SUCCESS')
            except:
                pass


    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete_custom_library(self, custom_library_uid):
        """
            Delete custom library from repository.

            :param custom_library_uid: stored custom library UID
            :type custom_library_uid: {str_type}

            A way you might use me is:
            >>> client.repository.delete_custom_library(custom_library_uid)
        """
        Runtimes._validate_type(custom_library_uid, u'custom_library_uid', STR_TYPE,True)
        library_endpoint = self._href_definitions.get_custom_library_href(custom_library_uid)
        response_delete = requests.delete(library_endpoint, headers=self._client._get_headers())

        self._handle_response(204, u'custom library deletion', response_delete, False)

    def list(self, limit=None):
        """
           List runtimes. If limit is set to None there will be only first 50 records shown.

           :param limit: limit number of fetched records (optional)
           :type limit: int

           A way you might use me is:

           >>> client.runtimes.list()
        """
        details = self.get_details()
        resources = details[u'resources']
        values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'], m[u'entity'][u'platform']['name'] + '-' + m[u'entity'][u'platform']['version']) for m in resources]

        self._list(values, [u'GUID', u'NAME', u'CREATED', u'PLATFORM'], limit, 50)

    def list_runtimes_for_libraries(self):
        """
           List runtimes uids for libraries.

           A way you might use me is:

           >>> client.runtimes.list_runtimes_for_libraries()
           >>> client.runtimes.list_runtimes_for_libraries(library_uid)
        """
        details = self._get_custom_libraries_details()
        runtime_details = self.get_details()

        values = [
            (m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'entity'][u'version'],
             ', '.join(self._get_runtimes_uids_for_lib(m[u'metadata'][u'guid'], runtime_details))) for m in
            details['resources']]

        values = sorted(sorted(values, key=lambda x: x[2], reverse=True), key=lambda x: x[1])

        from tabulate import tabulate

        header = [u'GUID', u'NAME', u'VERSION', u'RUNTIMES']
        table = tabulate([header] + values)

        print(table)

    def list_custom_libraries(self, runtime_uid=None, limit=None):
        """
           List custom libraries. If limit is set to None there will be only first 50 records shown.

           :param runtime_uid: Runtime UID
           :type runtime_uid: {str_type}

           :param limit: limit number of fetched records (optional)
           :type limit: int

           A way you might use me is:

           >>> client.runtimes.list_custom_libraries()
           >>> client.runtimes.list_custom_libraries(runtime_uid)
        """
        runtime_uid = str_type_conv(runtime_uid)
        Runtimes._validate_type(runtime_uid, u'runtime_uid', STR_TYPE, False)

        if runtime_uid is None:
            details = self._get_custom_libraries_details()

            resources = details[u'resources']
            values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'entity'][u'version'], m[u'metadata'][u'created_at'],
                       m[u'entity'][u'platform']['name'], m[u'entity'][u'platform'][u'versions']) for m in
                      resources]

            self._list(values, [u'GUID', u'NAME', u'VERSION', u'CREATED', u'PLATFORM NAME', u'PLATFORM VERSIONS'], limit, 50)
        else:
            details = self.get_details(runtime_uid)

            if 'custom_libraries' not in details['entity'] or len(details['entity']['custom_libraries']) == 0:
                print('No custom libraries found for this runtime.')
                return

            values = [(m[u'url'].split('/')[-1], m[u'name'], m['version']) for m in details['entity']['custom_libraries']]

            values = sorted(sorted(values, key=lambda x: x[2], reverse=True), key=lambda x: x[1])

            from tabulate import tabulate

            header = [u'GUID', u'NAME', u'VERSION']
            table = tabulate([header] + values)

            print(table)

    def download_configuration_file(self, runtime_uid, filename=None):
        """
            Downloads configuration file for runtime with specified UID.

            :param runtime_uid:  UID of runtime
            :type runtime_uid: {str_type}
            :param filename: filename of downloaded archive (optional)
            :type filename: {str_type}

            :returns: path to downloaded file
            :rtype: {str_type}
        """

        runtime_uid = str_type_conv(runtime_uid)
        Runtimes._validate_type(runtime_uid, u'runtime_uid', STR_TYPE, True)

        if not is_uid(runtime_uid):
            raise WMLClientError(u'\'runtime_uid\' is not an uid: \'{}\''.format(runtime_uid))

        download_url = self._href_definitions.get_runtime_spec_href(runtime_uid) + '/content'

        response_get = requests.get(
            download_url,
            headers=self._client._get_headers())

        if filename is None:
            filename = 'runtime_configuration.yaml'

        if response_get.status_code == 200:
            with open(filename, "wb") as new_file:
                new_file.write(response_get.content)
                new_file.close()

                print_text_header_h2(
                    u'Successfully downloaded configuration file: ' + str(filename))

                return filename
        else:
            raise WMLClientError(u'Unable to download configuration content: ' + response_get.text)