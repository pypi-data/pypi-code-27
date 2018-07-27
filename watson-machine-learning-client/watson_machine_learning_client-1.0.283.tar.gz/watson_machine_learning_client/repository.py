################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
from repository_v3.mlrepositoryartifact import MLRepositoryArtifact
from repository_v3.mlrepository import MetaProps, MetaNames
import requests
from watson_machine_learning_client.utils import get_url, MODEL_DETAILS_TYPE, DEFINITION_DETAILS_TYPE, EXPERIMENT_DETAILS_TYPE, INSTANCE_DETAILS_TYPE, FUNCTION_DETAILS_TYPE, load_model_from_directory, STR_TYPE, STR_TYPE_NAME, docstring_parameter, meta_props_str_conv, str_type_conv, is_python_2, get_file_from_cos, is_of_python_basic_type
from watson_machine_learning_client.metanames import ModelDefinitionMetaNames, ModelMetaNames, ExperimentMetaNames, FunctionMetaNames
import os
import copy
import json
from watson_machine_learning_client.wml_client_error import WMLClientError, MissingMetaProp, UnexpectedType
from watson_machine_learning_client.wml_resource import WMLResource
from multiprocessing import Pool
from repository_v3.mlrepositoryclient import MLRepositoryClient

_DEFAULT_LIST_LENGTH = 50


class Repository(WMLResource):
    """
    Store and manage your models, definitions and experiments using Watson Machine Learning Repository.
    """
    DefinitionMetaNames = ModelDefinitionMetaNames()
    """MetaNames for definitions creation."""
    ModelMetaNames = ModelMetaNames()
    """MetaNames for models creation."""
    ExperimentMetaNames = ExperimentMetaNames()
    """MetaNames for experiments creation."""
    FunctionMetaNames = FunctionMetaNames()
    """MetaNames for python functions creation."""

    def __init__(self, client):
        WMLResource.__init__(self, __name__, client)
        Repository._validate_type(client.service_instance.details, u'instance_details', dict, True)
        Repository._validate_type_of_details(client.service_instance.details, INSTANCE_DETAILS_TYPE)
        self._ml_repository_client = None
        self._refresh_repo_client() # regular token is initialized in service_instance

    def _refresh_repo_client(self):
        self._ml_repository_client = MLRepositoryClient(self._wml_credentials[u'url'])
        self._ml_repository_client.authorize(self._wml_credentials[u'username'], self._wml_credentials[u'password'])
        self._ml_repository_client._add_header('X-WML-User-Client', 'PythonClient')
        if self._client.project_id is not None:
            self._ml_repository_client._add_header('X-Watson-Project-ID', self._client.project_id)

    def _validate_if_functions_are_available(self, op_name):
        self._validate_plan(op_name, ['enterpriseAIS', 'ais-enterprise'])

    def store_experiment(self, meta_props):
        """
           Store experiment into Watson Machine Learning repository on IBM Cloud.

            :param meta_props: meta data of the experiment configuration. To see available meta names use:

               >>> client.repository.ExperimentMetaNames.get()
            :type meta_props: dict

            :returns: stored experiment details
            :rtype: dict

           A way you might use me is:

           >>> metadata = {
           >>>  client.repository.ExperimentMetaNames.NAME: 'my_experiment',
           >>>  client.repository.ExperimentMetaNames.EVALUATION_METRICS: ['accuracy'],
           >>>  client.repository.ExperimentMetaNames.TRAINING_DATA_REFERENCE: {'connection': {'endpoint_url': 'https://s3-api.us-geo.objectstorage.softlayer.net', 'access_key_id': '***', 'secret_access_key': '***'}, 'source': {'bucket': 'train-data'}, 'type': 's3'},
           >>>  client.repository.ExperimentMetaNames.TRAINING_RESULTS_REFERENCE: {'connection': {'endpoint_url': 'https://s3-api.us-geo.objectstorage.softlayer.net', 'access_key_id': '***', 'secret_access_key': '***'}, 'target': {'bucket': 'result-data'}, 'type': 's3'},
           >>>  client.repository.ExperimentMetaNames.TRAINING_REFERENCES: [
           >>>      {
           >>>        'training_definition_url': definition_url_1
           >>>      },
           >>>      {
           >>>        'training_definition_url': definition_url_2
           >>>      },
           >>>   ],
           >>> }
           >>> experiment_details = client.repository.store_experiment(meta_props=metadata)
           >>> experiment_url = client.repository.get_experiment_url(experiment_details)
        """
        Repository._validate_type(meta_props, u'meta_props', dict, True)
        meta_props_str_conv(meta_props)
        self.ExperimentMetaNames._validate(meta_props)

        training_references = copy.deepcopy(meta_props[self.ExperimentMetaNames.TRAINING_REFERENCES])

        if any(u'training_definition_url' not in x for x in training_references):
            raise MissingMetaProp(u'training_references.training_definition_url')

        for ref in training_references:
            if u'name' not in ref or u'command' not in ref:

                training_definition_response = requests.get(ref[u'training_definition_url'].replace(u'/content', u''), headers=self._client._get_headers())
                result = self._handle_response(200, u'getting training definition', training_definition_response)

                if not u'name' in ref:
                    ref.update({u'name': result[u'entity'][u'name']})
                if not u'command' in ref:
                    ref.update({u'command': result[u'entity'][u'command']})

        experiment_metadata = {
            u'settings': {
                u'name': meta_props[self.ExperimentMetaNames.NAME],
                u'description': "",
                u'author': {
                },
            },
            u'training_references': training_references,
            u'training_data_reference': meta_props[self.ExperimentMetaNames.TRAINING_DATA_REFERENCE],
            u'training_results_reference': meta_props[self.ExperimentMetaNames.TRAINING_RESULTS_REFERENCE],
        }

        if (self.ExperimentMetaNames.EVALUATION_METRICS in meta_props) and (self.ExperimentMetaNames.EVALUATION_METHOD in meta_props):
            experiment_metadata['settings'].update({
                              u'evaluation_definition': {
                                 u'method': meta_props[self.ExperimentMetaNames.EVALUATION_METHOD],
                                 u'metrics': [{u'name': x} for x in meta_props[self.ExperimentMetaNames.EVALUATION_METRICS]]
                              }
                           }
            )

        if self.ExperimentMetaNames.DESCRIPTION in meta_props:
            experiment_metadata[u'settings'].update({u'description': meta_props[self.ExperimentMetaNames.DESCRIPTION]})

        if self.ExperimentMetaNames.AUTHOR_NAME in meta_props:
            experiment_metadata[u'settings'][u'author'].update({u'name': meta_props[self.ExperimentMetaNames.AUTHOR_NAME]})

        if self.ExperimentMetaNames.TAGS in meta_props:
            experiment_metadata[u'tags'] = meta_props[self.ExperimentMetaNames.TAGS]

        response_experiment_post = requests.post(self._href_definitions.get_experiments_href(), json=experiment_metadata, headers=self._client._get_headers())

        return self._handle_response(201, u'saving experiment', response_experiment_post)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def store_definition(self, training_definition, meta_props):
        """
            Store training definition into Watson Machine Learning repository on IBM Cloud.

            :param training_definition:  path to zipped model_definition
            :type training_definition: {str_type}

            :param meta_props: meta data of the training definition. To see available meta names use:

               >>> client.repository.DefinitionMetaNames.get()
            :type meta_props: dict


            :returns: stored training definition details
            :rtype: dict

            A way you might use me is:

            >>> metadata = {
            >>>  client.repository.DefinitionMetaNames.NAME: 'my_training_definition',
            >>>  client.repository.DefinitionMetaNames.FRAMEWORK_NAME: 'tensorflow',
            >>>  client.repository.DefinitionMetaNames.FRAMEWORK_VERSION: '1.5',
            >>>  client.repository.DefinitionMetaNames.RUNTIME_NAME: 'python',
            >>>  client.repository.DefinitionMetaNames.RUNTIME_VERSION: '3.5',
            >>>  client.repository.DefinitionMetaNames.EXECUTION_COMMAND: 'python3 tensorflow_mnist_softmax.py --trainingIters 20'
            >>> }
            >>> definition_details = client.repository.store_definition(training_definition_filepath, meta_props=metadata)
            >>> definition_url = client.repository.get_definition_url(definition_details)
        """

        # quick support for COS credentials instead of local path
        # TODO add error handling and cleaning (remove the file)
        if type(training_definition) is dict:
            training_definition = get_file_from_cos(training_definition)

        training_definition = str_type_conv(training_definition)
        Repository._validate_type(training_definition, u'training_definition', STR_TYPE, True)
        Repository._validate_type(meta_props, u'meta_props', dict, True)
        meta_props_str_conv(meta_props)
        self.DefinitionMetaNames._validate(meta_props)

        # TODO to be replaced with repository client

        training_definition_metadata = {
                               u'name': meta_props[self.DefinitionMetaNames.NAME],
                               u'framework': {
                                   u'name': meta_props[self.DefinitionMetaNames.FRAMEWORK_NAME],
                                   u'version': meta_props[self.DefinitionMetaNames.FRAMEWORK_VERSION],
                                   u'runtimes': [{
                                        u'name': meta_props[self.DefinitionMetaNames.RUNTIME_NAME],
                                        u'version': meta_props[self.DefinitionMetaNames.RUNTIME_VERSION]
                                    }]
                                },
                               u'command': meta_props[self.DefinitionMetaNames.EXECUTION_COMMAND]
        }

        if self.DefinitionMetaNames.DESCRIPTION in meta_props:
            training_definition_metadata.update({u'description': meta_props[self.DefinitionMetaNames.DESCRIPTION]})

        response_definition_post = requests.post(self._href_definitions.get_definitions_href(), json=training_definition_metadata, headers=self._client._get_headers())

        details = self._handle_response(201, u'saving model definition', response_definition_post)

        definition_version_content_url = details[u'entity'][u'training_definition_version'][u'content_url']

        # save model definition content
        put_header = self._client._get_headers(no_content_type=True)
        with open(training_definition, 'rb') as data:
            response_definition_put = requests.put(definition_version_content_url, data=data, headers=put_header)

        self._handle_response(200, u'saving model definition content', response_definition_put)

        return details

    @staticmethod
    def _meta_props_to_repository_v3_style(meta_props):
        if is_python_2():
            new_meta_props = meta_props.copy()

            for key in new_meta_props:
                if type(new_meta_props[key]) is unicode:
                    new_meta_props[key] = str(new_meta_props[key])

            return new_meta_props
        else:
            return meta_props

    def _publish_from_object(self, model, meta_props, training_data=None, training_target=None, pipeline=None):
        """
        Store model from object in memory into Watson Machine Learning repository on Cloud
        """
        self._validate_meta_prop(meta_props, self.ModelMetaNames.NAME, STR_TYPE, True)

        try:
            meta_data = MetaProps(Repository._meta_props_to_repository_v3_style(meta_props))

            if 'pyspark.ml.pipeline.PipelineModel' in str(type(model)):
                pipeline_artifact = MLRepositoryArtifact(pipeline, name=str(meta_props[self.ModelMetaNames.NAME]))
                model_artifact = MLRepositoryArtifact(model, name=str(meta_props[self.ModelMetaNames.NAME]), meta_props=meta_data, training_data=training_data, pipeline_artifact=pipeline_artifact)
            else:
                model_artifact = MLRepositoryArtifact(model, name=str(meta_props[self.ModelMetaNames.NAME]), meta_props=meta_data, training_data=training_data, training_target=training_target)

            saved_model = self._ml_repository_client.models.save(model_artifact)
        except Exception as e:
            raise WMLClientError(u'Publishing model failed.', e)
        else:
            return self.get_details(u'{}'.format(saved_model.uid))

    def _publish_from_training(self, model, meta_props, training_data=None, training_target=None):
        """
        Store trained model from object storage into Watson Machine Learning repository on IBM Cloud
        """
        self._validate_meta_prop(meta_props, self.ModelMetaNames.NAME, STR_TYPE, True)

        # TODO - check type etc
        #if not is_uid(model):
        #    raise WMLClientError('Invalid uid: \'{}\'.'.format(model))

        ml_asset_endpoint = u'{}/v3/models/{}/ml_asset'.format(self._wml_credentials[u'url'], model)
        details = self._client.training.get_details(model)

        if details is not None:
            base_payload = {self.DefinitionMetaNames.NAME: meta_props[self.ModelMetaNames.NAME]}

            if meta_props is None:
                payload = base_payload
            else:
                payload = dict(base_payload, **meta_props)

            response_model_put = requests.put(ml_asset_endpoint, json=payload, headers=self._client._get_headers())

            saved_model_details = self._handle_response(202, u'saving trained model', response_model_put)

            model_guid = WMLResource._get_required_element_from_dict(saved_model_details, u'saved_model_details', [u'entity', u'ml_asset_guid'])
            content_status_endpoint = self._wml_credentials[u'url'] + u'/v3/ml_assets/models/' + str(model_guid)
            response_content_status_get = requests.get(content_status_endpoint, headers=self._client._get_headers())

            state = self._handle_response(200, u'checking saved model content status', response_content_status_get)[u'entity'][u'model_version'][u'content_status'][u'state']

            while (u'persisted' not in state) and (u'persisting_failed' not in state) and (u'failure' not in state):
                response_content_status_get = requests.get(content_status_endpoint, headers=self._client._get_headers())

                state = self._handle_response(200, u'checking saved model content status', response_content_status_get)[u'entity'][u'model_version'][u'content_status'][u'state']

            if u'persisted' in state:
                return saved_model_details
            else:
                raise WMLClientError(u'Saving trained model in repository for url: \'{}\' failed.'.format(content_status_endpoint), response_content_status_get.text)

    def _publish_from_file(self, model, meta_props=None, training_data=None, training_target=None):
        """
        Store saved model into Watson Machine Learning repository on IBM Cloud
        """
        def is_xml(model_filepath):
            return os.path.splitext(os.path.basename(model_filepath))[-1] == '.xml'

        self._validate_meta_prop(meta_props, self.ModelMetaNames.NAME, STR_TYPE, True)
        self._validate_meta_prop(meta_props, self.ModelMetaNames.FRAMEWORK_NAME, STR_TYPE, True)

        import tarfile
        import zipfile

        model_filepath = model
        if os.path.isdir(model):
            # TODO this part is ugly, but will work. In final solution this will be removed
            if meta_props[self.ModelMetaNames.FRAMEWORK_NAME] == u'tensorflow':
                # TODO currently tar.gz is required for tensorflow - the same ext should be supported for all frameworks
                if os.path.basename(model) == '':
                    model = os.path.dirname(model)
                filename = os.path.basename(model) + '.tar.gz'
                current_dir = os.getcwd()
                os.chdir(model)
                target_path = os.path.dirname(model)

                with tarfile.open(os.path.join('..', filename), mode='w:gz') as tar:
                    tar.add('.')

                os.chdir(current_dir)
                model_filepath = os.path.join(target_path, filename)
                if tarfile.is_tarfile(model_filepath) or zipfile.is_zipfile(model_filepath) or is_xml(model_filepath):
                    try:
                        model_artifact = MLRepositoryArtifact(str(model_filepath), name=str(meta_props[self.ModelMetaNames.NAME]),
                                                              meta_props=MetaProps(Repository._meta_props_to_repository_v3_style(meta_props)))
                        saved_model = self._ml_repository_client.models.save(model_artifact)
                    except Exception as e:
                        raise WMLClientError(u'Publishing model failed.', e)
                    else:
                        return self.get_details(saved_model.uid)
            else:
                self._validate_meta_prop(meta_props, self.ModelMetaNames.FRAMEWORK_NAME, STR_TYPE, True)

                loaded_model = load_model_from_directory(meta_props[self.ModelMetaNames.FRAMEWORK_NAME], model)

                saved_model = self._publish_from_object(loaded_model, meta_props, training_data, training_target)

                return saved_model

        elif is_xml(model_filepath):
            try:
                model_artifact = MLRepositoryArtifact(str(model_filepath), name=str(meta_props[self.ModelMetaNames.NAME]), meta_props=MetaProps(Repository._meta_props_to_repository_v3_style(meta_props)))
                saved_model = self._ml_repository_client.models.save(model_artifact)
            except Exception as e:
                raise WMLClientError(u'Publishing model failed.', e)
            else:
                return self.get_details(saved_model.uid)
        elif tarfile.is_tarfile(model_filepath) or zipfile.is_zipfile(model_filepath):
            return self._publish_from_archive(model, meta_props)
        else:
            raise WMLClientError(u'Saving trained model in repository failed. \'{}\' file does not have valid format'.format(model_filepath))

    # TODO make this way when all frameworks will be supported
    # def _publish_from_archive(self, path_to_archive, meta_props=None):
    #     self._validate_meta_prop(meta_props, self.ModelMetaNames.FRAMEWORK_NAME, STR_TYPE, True)
    #     self._validate_meta_prop(meta_props, self.ModelMetaNames.FRAMEWORK_VERSION, STR_TYPE, True)
    #     self._validate_meta_prop(meta_props, self.ModelMetaNames.NAME, STR_TYPE, True)
    #
    #     try:
    #         meta_data = MetaProps(Repository._meta_props_to_repository_v3_style(meta_props))
    #
    #         model_artifact = MLRepositoryArtifact(path_to_archive, name=str(meta_props[self.ModelMetaNames.NAME]), meta_props=meta_data)
    #
    #         saved_model = self._ml_repository_client.models.save(model_artifact)
    #     except Exception as e:
    #         raise WMLClientError(u'Publishing model failed.', e)
    #     else:
    #         return self.get_details(u'{}'.format(saved_model.uid))

    def _publish_from_archive(self, path_to_archive, meta_props=None):
        self._validate_meta_prop(meta_props, self.ModelMetaNames.FRAMEWORK_NAME, STR_TYPE, True)
        self._validate_meta_prop(meta_props, self.ModelMetaNames.FRAMEWORK_VERSION, STR_TYPE, True)
        self._validate_meta_prop(meta_props, self.ModelMetaNames.NAME, STR_TYPE, True)

        url = self._client.wml_credentials['url'] + '/v3/ml_assets/models'

        payload = {
            "framework": {
                "name": meta_props[self.ModelMetaNames.FRAMEWORK_NAME],
                "version": meta_props[self.ModelMetaNames.FRAMEWORK_VERSION]
            },
            "name": meta_props[self.ModelMetaNames.NAME],
            "author": {
            }
        }

        if self.ModelMetaNames.RUNTIME_NAME in meta_props and self.ModelMetaNames.RUNTIME_VERSION in meta_props:
            payload['framework'].update({
                "runtimes": [
                    {
                        "name": meta_props[self.ModelMetaNames.RUNTIME_NAME],
                        "version": meta_props[self.ModelMetaNames.RUNTIME_VERSION]
                    }
                ]
            })

        if self.ModelMetaNames.FRAMEWORK_LIBRARIES in meta_props:
            payload['framework'].update({"libraries": meta_props[self.ModelMetaNames.FRAMEWORK_LIBRARIES]})

        if self.ModelMetaNames.DESCRIPTION in meta_props:
            payload.update({'description': meta_props[self.ModelMetaNames.DESCRIPTION]})

        if self.ModelMetaNames.AUTHOR_NAME in meta_props:
            payload['author'].update({'name': meta_props[self.ModelMetaNames.AUTHOR_NAME]})

        if self.ModelMetaNames.EVALUATION_METHOD in meta_props and self.ModelMetaNames.EVALUATION_METRICS in meta_props:
            payload.update({'evaluation': {
                    "method": meta_props[self.ModelMetaNames.EVALUATION_METHOD],
                    "metrics": meta_props[self.ModelMetaNames.EVALUATION_METRICS]
                }
            })

        if self.ModelMetaNames.RUNTIME_UID in meta_props:
            payload['runtime_url'] = self._href_definitions.get_runtime_href(meta_props[self.ModelMetaNames.RUNTIME_UID])

        response = requests.post(
            url,
            json=payload,
            headers=self._client._get_headers()
        )

        result = self._handle_response(201, u'creating model', response)
        model_uid = self._get_required_element_from_dict(result, 'model_details', ['metadata', 'guid'])

        url = self._get_required_element_from_dict(result, 'model_details', ['entity', 'model_version', 'content_url'])

        with open(path_to_archive, 'rb') as f:
            response = requests.put(
                url,
                data=f,
                headers=self._client._get_headers(content_type='application/octet-stream')
            )

            self._handle_response(200, u'uploading model content', response, False)

            return self.get_model_details(model_uid)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def store_model(self, model, meta_props=None, training_data=None, training_target=None, pipeline=None):
        """
        Store trained model into Watson Machine Learning repository on Cloud.

        :param model:  The train model object (e.g: spark PipelineModel), or path to saved model in format .tar.gz/.str/.xml or directory containing model file(s), or trained model guid
        :type model: object/{str_type}

        :param meta_props: meta data of the training definition. To see available meta names use:

            >>> client.repository.ModelMetaNames.get()

        :type meta_props: dict/{str_type}

        :param training_data:  Spark DataFrame supported for spark models. Pandas dataframe, numpy.ndarray or array supported for scikit-learn models
        :type training_data: spark dataframe, pandas dataframe, numpy.ndarray or array

        :param training_target: array with labels required for scikit-learn models
        :type training_target: array

        :param pipeline: pipeline required for spark mllib models
        :type training_target: object

        :returns: stored model details
        :rtype: dict

        The most simple use is:

        >>> stored_model_details = client.repository.store_model(model, name)

        In more complicated cases you should create proper metadata, similar to this one:

        >>> metadata = {
        >>>        client.repository.ModelMetaNames.NAME: 'customer satisfaction prediction model',
        >>>        client.repository.ModelMetaNames.FRAMEWORK_NAME: 'tensorflow',
        >>>        client.repository.ModelMetaNames.FRAMEWORK_VERSION: '1.5',
        >>>        client.repository.ModelMetaNames.RUNTIME_NAME: 'python',
        >>>        client.repository.ModelMetaNames.RUNTIME_VERSION: '3.5'
        >>>}

        where FRAMEWORK_NAME may be one of following: "spss-modeler", "tensorflow", "xgboost", "scikit-learn", "pmml".

        A way you might use me with local tar.gz containing model:

        >>> stored_model_details = client.repository.store_model(path_to_tar_gz, meta_props=metadata, training_data=None)

        A way you might use me with local directory containing model file(s):

        >>> stored_model_details = client.repository.store_model(path_to_model_directory, meta_props=metadata, training_data=None)

        A way you might use me with trained model guid:

        >>> stored_model_details = client.repository.store_model(trained_model_guid, meta_props=metadata, training_data=None)
        """
        model = str_type_conv(model)
        Repository._validate_type(model, u'model', object, True)
        meta_props = copy.deepcopy(meta_props)
        meta_props = str_type_conv(meta_props)  # meta_props may be str, in this situation for py2 it will be converted to unicode
        Repository._validate_type(meta_props, u'meta_props', [dict, STR_TYPE], True)
        # Repository._validate_type(training_data, 'training_data', object, False)
        # Repository._validate_type(training_target, 'training_target', list, False)
        meta_props_str_conv(meta_props)

        if type(meta_props) is STR_TYPE:
            meta_props = {
                self.ModelMetaNames.NAME: meta_props
            }

        self.ModelMetaNames._validate(meta_props)

        if self.ModelMetaNames.RUNTIME_NAME in meta_props and self.ModelMetaNames.RUNTIME_VERSION in meta_props:
            meta_props[MetaNames.FRAMEWORK_RUNTIMES] = json.dumps([{u'name': meta_props[self.ModelMetaNames.RUNTIME_NAME], u'version': meta_props[self.ModelMetaNames.RUNTIME_VERSION]}])

        if self.ModelMetaNames.TRAINING_DATA_REFERENCE in meta_props:
            meta_props[MetaNames.TRAINING_DATA_REFERENCE] = json.dumps(meta_props[self.ModelMetaNames.TRAINING_DATA_REFERENCE])

        if self.ModelMetaNames.EVALUATION_METRICS in meta_props:
            meta_props[MetaNames.EVALUATION_METRICS] = json.dumps(meta_props[self.ModelMetaNames.EVALUATION_METRICS])

        if self.ModelMetaNames.RUNTIME_UID in meta_props:
            # TODO workaround for Jihyoung MetaNames.RUNTIMES.URL
            meta_props["runtimesUrl"] = self._href_definitions.get_runtime_href(meta_props[self.ModelMetaNames.RUNTIME_UID])

        if not isinstance(model, STR_TYPE):
            saved_model = self._publish_from_object(model=model, meta_props=meta_props, training_data=training_data, training_target=training_target, pipeline=pipeline)
        else:
            if (os.path.sep in model) or os.path.isfile(model) or os.path.isdir(model):
                if not os.path.isfile(model) and not os.path.isdir(model):
                    raise WMLClientError(u'Invalid path: neither file nor directory exists under this path: \'{}\'.'.format(model))
                saved_model = self._publish_from_file(model=model, meta_props=meta_props, training_data=training_data, training_target=training_target)
            else:
                saved_model = self._publish_from_training(model=model, meta_props=meta_props, training_data=training_data, training_target=training_target)

        return saved_model

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def store_function(self, function, meta_props):
        """
            Store function into Watson Machine Learning repository on Cloud.

            As a 'function' may be used one of the following:
             - filepath to gz file
             - 'score' function reference, where the function is the function which will be deployed
             - generator function, which takes no argument or arguments which all have primitive python default values and as result return 'score' function

            :param meta_props: meta data or name of the function. To see available meta names use:

                >>> client.repository.FunctionMetaNames.get()

            :type meta_props: dict/{str_type}

            :param function: path to file with archived function content or function (as described above)
            :type function: {str_type} or function

            :returns: stored function details
            :rtype: dict

            The most simple use is (using `score` function):

                >>> def score(payload):
                        values = [[row[0]*row[1]] for row in payload['values']]
                        return {'fields': ['multiplication'], 'values': values}
                >>> stored_function_details = client.repository.store_function(score, name)

            Other, more interesting example is using generator function.
            In this situation it is possible to pass some variables:

                >>> wml_creds = {...}
                >>> def gen_function(wml_credentials=wml_creds, x=2):
                        def f(payload):
                            values = [[row[0]*row[1]*x] for row in payload['values']]
                            return {'fields': ['multiplication'], 'values': values}
                        return f
                >>> stored_function_details = client.repository.store_function(gen_function, name)

            In more complicated cases you should create proper metadata, similar to this one:

                >>> metadata = {
                >>>    client.repository.FunctionMetaNames.NAME: "function",
                >>>    client.repository.FunctionMetaNames.DESCRIPTION: "This is ai function",
                >>>    client.repository.FunctionMetaNames.RUNTIME_UID: "53dc4cf1-252f-424b-b52d-5cdd9814987f",
                >>>    client.repository.FunctionMetaNames.INPUT_DATA_SCHEMA: {"fields": [{"metadata": {}, "type": "string", "name": "GENDER", "nullable": True}]},
                >>>    client.repository.FunctionMetaNames.OUTPUT_DATA_SCHEMA: {"fields": [{"metadata": {}, "type": "string", "name": "GENDER", "nullable": True}]},
                >>>    client.repository.FunctionMetaNames.TAGS: [{"value": "ProjectA", "description": "Functions created for ProjectA"}]
                >>> }
                >>> stored_function_details = client.repository.store_function(score, metadata)
            """
        self._validate_if_functions_are_available('store function')
        function = str_type_conv(function)
        import types
        Repository._validate_type(function, u'function', [STR_TYPE, types.FunctionType], True)
        meta_props = str_type_conv(meta_props)  # meta_props may be str, in this situation for py2 it will be converted to unicode
        Repository._validate_type(meta_props, u'meta_props', [dict, STR_TYPE], True)

        if type(meta_props) is STR_TYPE:
            meta_props = {
                self.FunctionMetaNames.NAME: meta_props
            }

        self.FunctionMetaNames._validate(meta_props)

        if type(function) is STR_TYPE:
            content_path = function
        else:
            try:
                import inspect
                import gzip
                import uuid
                import re
                import shutil
                code = inspect.getsource(function).split('\n')
                r = re.compile(r"^ *")
                m = r.search(code[0])
                intend = m.group(0)

                code = [line.replace(intend, '', 1) for line in code]

                args_spec = inspect.getargspec(function)

                defaults = args_spec.defaults if args_spec.defaults is not None else []
                args = args_spec.args if args_spec.args is not None else []

                if function.__name__ is 'score':
                    code = '\n'.join(code)
                    file_content = code
                elif len(args) == len(defaults):
                    for i, d in enumerate(defaults):
                        if not is_of_python_basic_type(d):
                            raise UnexpectedType(args[i], 'primitive python type', type(d))

                    new_header = 'def {}({}):'.format(
                        function.__name__,
                        ', '.join(
                            ['{}={}'.format(arg_name, json.dumps(defaults[0])) for arg_name, default in zip(args, defaults)]
                        )
                    )

                    code[0] = new_header
                    code = '\n'.join(code)
                    file_content = """
{}

score = {}()
""".format(code, function.__name__)
                else:
                    raise WMLClientError("Function passed is not \'score\' function nor generator function. Generator function should have no arguments or all arguments with primitive python default values.")

                tmp_uid = 'tmp_python_function_code_{}'.format(str(uuid.uuid4()).replace('-', '_'))
                filename = '{}.py'.format(tmp_uid)

                with open(filename, 'w') as f:
                    f.write(file_content)

                archive_name = '{}.py.gz'.format(tmp_uid)

                with open(filename, 'rb') as f_in:
                    with gzip.open(archive_name, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)

                os.remove(filename)

                content_path = archive_name
            except Exception as e:
                try:
                    os.remove(filename)
                except:
                    pass
                try:
                    os.remove(archive_name)
                except:
                    pass
                raise WMLClientError('Exception during getting function code.', e)

        try:
            function_metadata = {
                u'name': meta_props[self.FunctionMetaNames.NAME],
            }

            if self.FunctionMetaNames.DESCRIPTION in meta_props:
                function_metadata.update({u'description': meta_props[self.FunctionMetaNames.DESCRIPTION]})

            if self.FunctionMetaNames.TAGS in meta_props:
                function_metadata.update({u'tags': meta_props[self.FunctionMetaNames.TAGS]})

            if self.FunctionMetaNames.RUNTIME_UID in meta_props:
                function_metadata.update({u'runtime_url': self._href_definitions.get_function_href(meta_props[self.FunctionMetaNames.RUNTIME_UID])})
            else:
                print('No RUNTIME_UID passed. Creating default runtime... ', end="")
                meta = {
                    self._client.runtimes.ConfigurationMetaNames.NAME: meta_props[self.FunctionMetaNames.NAME] + "_py_3.5",
                    self._client.runtimes.ConfigurationMetaNames.PLATFORM: {
                        "name": "python",
                        "version": "3.5"
                    }
                }
                runtime_details = self._client.runtimes.store(meta)
                runtime_url = self._client.runtimes.get_url(runtime_details)
                runtime_uid = self._client.runtimes.get_uid(runtime_details)
                print('SUCCESS\n\nSuccessfully created default runtime with uid: {}'.format(runtime_uid))
                function_metadata.update({u'runtime_url': runtime_url})

            if self.FunctionMetaNames.INPUT_DATA_SCHEMA in meta_props:
                function_metadata.update({u'input_data_schema': meta_props[self.FunctionMetaNames.INPUT_DATA_SCHEMA]})

            if self.FunctionMetaNames.OUTPUT_DATA_SCHEMA in meta_props:
                function_metadata.update({u'output_data_schema': meta_props[self.FunctionMetaNames.OUTPUT_DATA_SCHEMA]})

            response_post = requests.post(self._href_definitions.get_functions_href(), json=function_metadata, headers=self._client._get_headers())

            details = self._handle_response(201, u'saving function', response_post)

            function_content_url = details[u'entity'][u'function_revision'][u'url'] + '/content'

            put_header = self._client._get_headers(no_content_type=True)
            with open(content_path, 'rb') as data:
                response_definition_put = requests.put(function_content_url, data=data, headers=put_header)

        except Exception as e:
            raise e
        finally:
            try:
                os.remove(archive_name)
            except:
                pass


        self._handle_response(200, u'saving function content', response_definition_put)

        return details

    def update_model(self, model_uid, content_path=None, meta_props=None):
        """
            Update content of model with new one.

            :param model_uid:  Model UID
            :type model_uid: str
            :param content_path: path to tar.gz with new content of model
            :type content_path: str

            :returns: updated metadata of model
            :rtype: dict

            A way you might use me is:

            >>> model_details = client.repository.update_model_content(model_uid, content_path)
        """
        Repository._validate_type(model_uid, 'model_uid', STR_TYPE, True)
        Repository._validate_type(content_path, 'content_path', STR_TYPE, False)

        response = requests.get(
            self._href_definitions.get_model_last_version_href(model_uid),
            headers=self._client._get_headers(no_content_type=True),
        )
        model_details = self._handle_response(200, 'getting model details', response)

        if meta_props is not None: # TODO
            raise WMLClientError('Meta_props update unsupported.')
            # url = self._get_required_element_from_dict(model_details, 'model_details', ['entity', 'model_version', 'url'])
            #
            # if self.ModelMetaNames.AUTHOR_EMAIL in meta_props:
            #     self._logger.warning('\'AUTHOR_EMAIL\' meta prop is deprecated. It will be ignored.')
            #
            # self._update(url, model_details, meta_props, [
            #     {"name": self.ModelMetaNames.NAME, "type": STR_TYPE, "path": ['name']},
            #     {"name": self.ModelMetaNames.DESCRIPTION, "type": STR_TYPE, "path": ['description']},
            #     {"name": self.ModelMetaNames.AUTHOR_NAME, "type": STR_TYPE, "path": ['author', 'name']},
            #     {"name": self.ModelMetaNames.FRAMEWORK_NAME, "type": STR_TYPE, "path": ['framework', 'name']},
            #     {"name": self.ModelMetaNames.FRAMEWORK_VERSION, "type": STR_TYPE, "path": ['framework', 'version']},
            #     {"name": self.ModelMetaNames.FRAMEWORK_LIBRARIES, "type": list, "path": ['framework', 'libraries']},
            #     {"name": self.ModelMetaNames.RUNTIME_NAME, "type": STR_TYPE, "path": ['framework', 'runtimes', 0, 'name']},
            #     {"name": self.ModelMetaNames.RUNTIME_VERSION, "type": STR_TYPE, "path": ['framework', 'runtimes', 0, 'version']},
            #     {"name": self.ModelMetaNames.TRAINING_DATA_REFERENCE, "type": dict, "path": ['training_data_reference']},
            #     {"name": self.ModelMetaNames.EVALUATION_METHOD, "type": STR_TYPE, "path": ['evaluation', 'method']},
            #     {"name": self.ModelMetaNames.EVALUATION_METRICS, "type": list, "path": ['evaluation', 'metrics']},
            # ])

        if content_path is not None:
            response = requests.post(
                self._href_definitions.get_model_last_version_href(model_uid),
                headers=self._client._get_headers(),
                json = self._get_required_element_from_dict(model_details, 'model_details', ['entity'])
            )

            # TODO probably should be 202
            new_details = self._handle_response(201, 'creating new model version', response)

            version_url = self._get_required_element_from_dict(new_details, 'model_details', ['entity', 'model_version', 'url'])

            with open(content_path, 'rb') as data:
                response = requests.put(
                    version_url + '/content',
                    headers=self._client._get_headers(content_type='application/octet-stream'),
                    data=data
                )

            self._handle_response(200, 'uploading model content', response, False)

        return self.get_model_details()

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def update_experiment(self, experiment_uid, changes):
        """
        Updates existing experiment metadata.

        :param experiment_uid: UID of experiment which definition should be updated
        :type experiment_uid: {str_type}

        :param changes: elements which should be changed, where keys are ExperimentMetaNames
        :type changes: dict

        :return: metadata of updated experiment
        :rtype: dict
        """
        experiment_uid = str_type_conv(experiment_uid)
        self._validate_type(experiment_uid, u'experiment_uid', STR_TYPE, True)
        self._validate_type(changes, u'changes', dict, True)
        meta_props_str_conv(changes)
        self.ExperimentMetaNames._check_types_only(changes)

        details = self.get_experiment_details(experiment_uid)

        def _decide_op(details, path):
            try:
                if len(path) == 1:
                    x = details[path[0]]
                    if x is not None:
                        return u'replace'
                    else:
                        return u'add'
                else:
                    _decide_op(details[path[0]], path[1:])
            except:
                return u'add'

        def _update_patch_payload(patch_payload, changes, path, meta_name, value=None):
            if meta_name in changes:
                if value is None:
                    value = changes[meta_name]

                patch_payload.append(
                    {
                        u'op': _decide_op(details, path),
                        u'path': u'/' + u'/'.join(path),
                        u'value': value
                    }
                )

        patch_payload = []
        _update_patch_payload(patch_payload, changes, [u'settings', u'name'], self.ExperimentMetaNames.NAME)
        _update_patch_payload(patch_payload, changes, [u'settings', u'description'], self.ExperimentMetaNames.DESCRIPTION)
        _update_patch_payload(patch_payload, changes, [u'settings', u'author', u'name'], self.ExperimentMetaNames.AUTHOR_NAME)
        _update_patch_payload(patch_payload, changes, [u'settings', u'evaluation_definition', u'method'], self.ExperimentMetaNames.EVALUATION_METHOD)
        _update_patch_payload(patch_payload, changes, [u'training_data_reference'], self.ExperimentMetaNames.TRAINING_DATA_REFERENCE)
        _update_patch_payload(patch_payload, changes, [u'training_results_reference'], self.ExperimentMetaNames.TRAINING_RESULTS_REFERENCE)

        if self.ExperimentMetaNames.EVALUATION_METRICS in changes:
            prepared_metrics = [{u'name': x} for x in changes[self.ExperimentMetaNames.EVALUATION_METRICS]]
            _update_patch_payload(patch_payload, changes, [u'settings', u'evaluation_definition', u'metrics'], self.ExperimentMetaNames.EVALUATION_METRICS, prepared_metrics)

        if self.ExperimentMetaNames.TRAINING_REFERENCES in changes:
            prepared_references = copy.deepcopy(changes[self.ExperimentMetaNames.TRAINING_REFERENCES])
            for ref in prepared_references:
                if u'name' not in ref or u'command' not in ref:

                    training_definition_response = requests.get(ref[u'training_definition_url'].replace(u'/content', u''),
                                                                headers=self._client._get_headers())
                    result = self._handle_response(200, u'getting training definition', training_definition_response)

                    if not u'name' in ref:
                        ref.update({u'name': result[u'entity'][u'name']})
                    if not u'command' in ref:
                        ref.update({u'command': result[u'entity'][u'command']})
            _update_patch_payload(patch_payload, changes, [u'training_references'], self.ExperimentMetaNames.TRAINING_REFERENCES, prepared_references)

        url = self._href_definitions.get_experiment_href(experiment_uid)
        response = requests.patch(url, json=patch_payload, headers=self._client._get_headers())
        updated_details = self._handle_response(200, u'experiment patch', response)

        return updated_details

    # def update_function(self): not very important on the beginning, probably this part needs much more work and refactoring
    #     pass # TODO func

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def load(self, artifact_uid):
        """
        Load model from repository to object in local environment.

        :param artifact_uid:  stored model UID
        :type artifact_uid: {str_type}

        :returns: trained model
        :rtype: object

        A way you might use me is:

        >>> model = client.repository.load(model_uid)
        """
        artifact_uid = str_type_conv(artifact_uid)
        Repository._validate_type(artifact_uid, u'artifact_uid', STR_TYPE, True)

        try:
            loaded_model = self._ml_repository_client.models.get(artifact_uid)
            loaded_model = loaded_model.model_instance()
            self._logger.info(u'Successfully loaded artifact with artifact_uid: {}'.format(artifact_uid))
            return loaded_model
        except Exception as e:
            raise WMLClientError(u'Loading model with artifact_uid: \'{}\' failed.'.format(artifact_uid), e)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def download(self, artifact_uid, filename='downloaded_artifact.tar.gz'):
        """
        Download artifact (model or function content) from repository to local file.

        :param artifact_uid: stored artifact UID
        :type artifact_uid: {str_type}

        :param filename: name of local file to create (optional)
        :type filename: {str_type}

        Side effect:
            save artifact to file.

        A way you might use me is:

        >>> client.repository.download(model_uid, 'my_model.tar.gz')
        """
        self._validate_type(artifact_uid, 'artifact_uid', STR_TYPE, True)
        self._validate_type(filename, 'filename', STR_TYPE, True)

        res = self._check_artifact_type(artifact_uid)

        if res['model'] is True:
            return self._download_model(artifact_uid, filename)
        elif res['function'] is True:
            return self._download_function(artifact_uid, filename)
        elif res['library'] is True:
            return self._client.runtimes.download_library(artifact_uid, filename)
        elif res['runtime'] is True:
            return self._client.runtimes.download_configuration(artifact_uid, filename)
        else:
            raise WMLClientError('Unexpected type of artifact to download: {}'.format(res))

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def _download_model(self, artifact_uid, filename='downloaded_model.tar.gz'):
        """
            Download model from repository to local file.

            :param artifact_uid: stored model UID
            :type artifact_uid: {str_type}

            :param filename: name of local file to create (optional)
            :type filename: {str_type}

            Side effect:
                save model to file.

            A way you might use me is:

            >>> client.repository.download(model_uid, 'my_model.tar.gz')
        """
        if os.path.isfile(filename):
            raise WMLClientError(u'File with name: \'{}\' already exists.'.format(filename))

        artifact_uid = str_type_conv(artifact_uid)
        Repository._validate_type(artifact_uid, u'artifact_uid', STR_TYPE, True)
        filename = str_type_conv(filename)
        Repository._validate_type(filename, u'filename', STR_TYPE, True)

        artifact_url = self._href_definitions.get_model_last_version_href(artifact_uid)

        try:
            artifact_content_url = str(artifact_url + u'/content')
            r = requests.get(artifact_content_url, headers=self._client._get_headers(), stream=True)

            self._handle_response(200, 'downloading model', r, False)

            downloaded_model = r.content
            self._logger.info(u'Successfully downloaded artifact with artifact_url: {}'.format(artifact_url))
        except WMLClientError as e:
            raise e
        except Exception as e:
            raise WMLClientError(u'Downloading model with artifact_url: \'{}\' failed.'.format(artifact_url), e)

        try:
            with open(filename, 'wb') as f:
                f.write(downloaded_model)
            self._logger.info(u'Successfully saved artifact to file: \'{}\''.format(filename))
            return None
        except IOError as e:
            raise WMLClientError(u'Saving model with artifact_url: \'{}\' failed.'.format(filename), e)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def _download_function(self, artifact_uid, filename='downloaded_function.gz'):
        """
            Download function content from repository to local file.

            :param artifact_uid: stored function UID
            :type artifact_uid: {str_type}

            :param filename: name of local file to create (optional)
            :type filename: {str_type}

            Side effect:
                save function to file.

            A way you might use me is:

            >>> client.repository.download_function(function_uid, 'my_func.tar.gz')
        """
        if os.path.isfile(filename):
            raise WMLClientError(u'File with name: \'{}\' already exists.'.format(filename))

        artifact_uid = str_type_conv(artifact_uid)
        Repository._validate_type(artifact_uid, u'artifact_uid', STR_TYPE, True)
        filename = str_type_conv(filename)
        Repository._validate_type(filename, u'filename', STR_TYPE, True)

        artifact_url = self._href_definitions.get_function_href(artifact_uid)
        artifact_content_url = self._href_definitions.get_function_latest_revision_content_href(artifact_uid)

        try:
            r = requests.get(artifact_content_url, headers=self._client._get_headers(), stream=True)

            self._handle_response(200, 'downloading function content', r, False)

            downloaded_model = r.content
            self._logger.info(u'Successfully downloaded artifact with artifact_url: {}'.format(artifact_url))
        except WMLClientError as e:
            raise e
        except Exception as e:
            raise WMLClientError(u'Downloading function content with artifact_url: \'{}\' failed.'.format(artifact_url), e)

        try:
            with open(filename, 'wb') as f:
                f.write(downloaded_model)
            self._logger.info(u'Successfully saved artifact to file: \'{}\''.format(filename))
            return None
        except IOError as e:
            raise WMLClientError(u'Saving function content with artifact_url: \'{}\' failed.'.format(filename), e)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete(self, artifact_uid):
        """
            Delete model, definition, experiment or function from repository.

            :param artifact_uid: stored model, definition, experiment or function UID
            :type artifact_uid: {str_type}

            A way you might use me is:

            >>> client.repository.delete(artifact_uid)
        """
        artifact_uid = str_type_conv(artifact_uid)
        Repository._validate_type(artifact_uid, u'artifact_uid', STR_TYPE, True)

        artifact_type = self._check_artifact_type(artifact_uid)
        self._logger.debug(u'Attempting deletion of artifact with type: \'{}\''.format(str(artifact_type)))

        if artifact_type[u'model'] is True:
            try:
                deleted = self._ml_repository_client.models.remove(str(artifact_uid))
                self._logger.info(u'Successfully deleted model with artifact_uid: \'{}\''.format(artifact_uid))
                self._logger.debug(u'Return object: {}'.format(deleted))
                return
            except Exception as e:
                raise WMLClientError(u'Model deletion failed.', e)
        elif artifact_type[u'definition'] is True:
            definition_endpoint = self._href_definitions.get_definition_href(artifact_uid)
            self._logger.debug(u'Deletion artifact definition endpoint: {}'.format(definition_endpoint))
            response_delete = requests.delete(definition_endpoint, headers=self._client._get_headers())

            self._handle_response(204, u'model definition deletion', response_delete, False)
            return

        elif artifact_type[u'experiment'] is True:
            experiment_endpoint = self._href_definitions.get_experiment_href(artifact_uid)
            self._logger.debug(u'Deletion artifact experiment endpoint: {}'.format(experiment_endpoint))
            response_delete = requests.delete(experiment_endpoint, headers=self._client._get_headers())

            self._handle_response(204, u'experiment deletion', response_delete, False)
            return

        elif artifact_type[u'function'] is True:
            function_endpoint = self._href_definitions.get_function_href(artifact_uid)
            self._logger.debug(u'Deletion artifact function endpoint: {}'.format(function_endpoint))
            response_delete = requests.delete(function_endpoint, headers=self._client._get_headers())

            self._handle_response(204, u'function deletion', response_delete, False)
            return

        elif artifact_type[u'runtime'] is True:
            self._client.runtimes.delete(artifact_uid)
            return

        elif artifact_type[u'library'] is True:
            self._client.runtimes.delete_library(artifact_uid)
            return

        else:
            raise WMLClientError(u'Artifact with artifact_uid: \'{}\' does not exist.'.format(artifact_uid))

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete_model(self, artifact_uid):
        """
            Delete model from repository.

            :param artifact_uid: stored model UID
            :type artifact_uid: {str_type}

            A way you might use me is:

            >>> client.repository.delete_model(artifact_uid)
        """

        self.delete(artifact_uid)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete_definition(self, artifact_uid):
        """
            Delete definition from repository.

            :param artifact_uid: stored definition UID
            :type artifact_uid: {str_type}

            A way you might use me is:

            >>> client.repository.delete_definition(artifact_uid)
        """

        self.delete(artifact_uid)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete_experiment(self, artifact_uid):
        """
            Delete experiment definition from repository.

            :param artifact_uid: stored experiment UID
            :type artifact_uid: {str_type}

            A way you might use me is:

            >>> client.repository.delete_experiment(artifact_uid)
        """

        self.delete(artifact_uid)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def delete_function(self, artifact_uid):
        """
            Delete function from repository.

            :param artifact_uid: stored function UID
            :type artifact_uid: {str_type}

            A way you might use me is:

            >>> client.repository.delete_function(artifact_uid)
        """
        self._validate_if_functions_are_available('delete function')

        self.delete(artifact_uid)

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_details(self, artifact_uid=None):
        """
           Get metadata of stored artifacts. If uid is not specified returns all models, definitions, experiment, functions, libraries and runtimes metadata.

           :param artifact_uid:  stored model, definition, experiment, function, library or runtime UID (optional)
           :type artifact_uid: {str_type}

           :returns: stored artifacts metadata
           :rtype: dict

           A way you might use me is:

           >>> details = client.repository.get_details(artifact_uid)
           >>> details = client.repository.get_details()
        """
        artifact_uid = str_type_conv(artifact_uid)
        Repository._validate_type(artifact_uid, u'artifact_uid', STR_TYPE, False)

        if artifact_uid is None:
            model_details = self.get_model_details()
            definition_details = self.get_definition_details()
            experiment_details = self.get_experiment_details()
            function_details = None
            library_details = self._client.runtimes.get_library_details()
            runtime_details = self._client.runtimes.get_details()
            try: # TODO it is to not crash this function if not enterprise account
                import logging
                logging.getLogger('watson_machine_learning_client.wml_client_error').disabled = True
                function_details = self.get_function_details()
            except:
                pass
            finally:
                import logging
                logging.getLogger('watson_machine_learning_client.wml_client_error').disabled = False
            details = {
                u'models': model_details,
                u'definitions': definition_details,
                u'experiments': experiment_details,
                u'runtimes': runtime_details,
                u'libraries': library_details,
            }
            if function_details is not None:
                details[u'functions'] = function_details
        else:
            uid_type = self._check_artifact_type(artifact_uid)
            if uid_type[u'model'] is True:
                details = self.get_model_details(artifact_uid)
            elif uid_type[u'definition'] is True:
                details = self.get_definition_details(artifact_uid)
            elif uid_type[u'experiment'] is True:
                details = self.get_experiment_details(artifact_uid)
            elif uid_type[u'function'] is True:
                details = self.get_function_details(artifact_uid)
            elif uid_type[u'runtime'] is True:
                details = self._client.runtimes.get_details(artifact_uid)
            elif uid_type[u'library'] is True:
                details = self._client.runtimes.get_library_details(artifact_uid)
            else:
                raise WMLClientError(u'Getting artifact details failed. Artifact uid: \'{}\' not found.'.format(artifact_uid))

        return details

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_model_details(self, model_uid=None, limit=None):
        """
           Get metadata of stored models. If model uid is not specified returns all models metadata.

           :param model_uid: stored model, definition or pipeline UID (optional)
           :type model_uid: {str_type}

           :param limit: limit number of fetched records (optional)
           :type limit: int

           :returns: stored model(s) metadata
           :rtype: dict

           A way you might use me is:

           >>> model_details = client.repository.get_model_details(model_uid)
           >>> models_details = client.repository.get_model_details()
        """
        model_uid = str_type_conv(model_uid)
        Repository._validate_type(model_uid, u'model_uid', STR_TYPE, False)
        Repository._validate_type(limit, u'limit', int, False)

        url = self._client.service_instance.details.get(u'entity').get(u'published_models').get(u'url')
        return self._get_artifact_details(url, model_uid, limit, 'models')

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_definition_details(self, definition_uid=None, limit=None):
        """
            Get metadata of stored definitions. If definition uid is not specified returns all model definitions metadata.

            :param definition_uid:  stored model definition UID (optional)
            :type definition_uid: {str_type}

            :param limit: limit number of fetched records (optional)
            :type limit: int

            :returns: stored definition(s) metadata
            :rtype: dict

            A way you might use me is:

            >>> definition_details = client.repository.get_definition_details(definition_uid)
            >>> definition_details = client.repository.get_definition_details()
         """
        definition_uid = str_type_conv(definition_uid)
        Repository._validate_type(definition_uid, u'definition_uid', STR_TYPE, False)
        Repository._validate_type(limit, u'limit', int, False)

        url = self._href_definitions.get_definitions_href()

        return self._get_artifact_details(url, definition_uid, limit, 'definitions')

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_experiment_details(self, experiment_uid=None, limit=None):
        """
            Get metadata of stored experiments. If no experiment uid is specified all experiments metadata is returned.

            :param experiment_uid: stored experiment UID (optional)
            :type experiment_uid: {str_type}

            :param limit: limit number of fetched records (optional)
            :type limit: int

            :returns: stored experiment(s) metadata
            :rtype: dict

            A way you might use me is:

            >>> experiment_details = client.repository.get_experiment_details(experiment_uid)
            >>> experiment_details = client.repository.get_experiment_details()
         """
        experiment_uid = str_type_conv(experiment_uid)
        Repository._validate_type(experiment_uid, u'experiment_uid', STR_TYPE, False)
        Repository._validate_type(limit, u'limit', int, False)

        url = self._href_definitions.get_experiments_href()

        return self._get_artifact_details(url, experiment_uid, limit, 'experiments')

    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_function_details(self, function_uid=None, limit=None):
        """
            Get metadata of function. If no function uid is specified all functions metadata is returned.

            :param function_uid: stored function UID (optional)
            :type function_uid: {str_type}

            :param limit: limit number of fetched records (optional)
            :type limit: int

            :returns: stored function(s) metadata
            :rtype: dict

            A way you might use me is:

            >>> function_details = client.repository.get_function_details(function_uid)
            >>> function_details = client.repository.get_function_details()
         """
        self._validate_if_functions_are_available('get function details')
        function_uid = str_type_conv(function_uid)
        Repository._validate_type(function_uid, u'function_uid', STR_TYPE, False)
        Repository._validate_type(limit, u'limit', int, False)

        url = self._href_definitions.get_functions_href()

        return self._get_artifact_details(url, function_uid, limit, 'functions')

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_model_url(model_details):
        """
            Get url of stored model.

            :param model_details:  stored model details
            :type model_details: dict

            :returns: url to stored model
            :rtype: {str_type}

            A way you might use me is:

            >>> model_url = client.repository.get_model_url(model_details)
        """
        Repository._validate_type(model_details, u'model_details', object, True)
        Repository._validate_type_of_details(model_details, MODEL_DETAILS_TYPE)

        try:
            return model_details[u'entity'][u'ml_asset_url']
        except:
            return WMLResource._get_required_element_from_dict(model_details, u'model_details', [u'metadata', u'url'])

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_model_uid(model_details):
        """
            Get uid of stored model.

            :param model_details:  stored model details
            :type model_details: dict

            :returns: uid of stored model
            :rtype: {str_type}

            A way you might use me is:

            >>> model_uid = client.repository.get_model_uid(model_details)
        """
        Repository._validate_type(model_details, u'model_details', object, True)
        Repository._validate_type_of_details(model_details, MODEL_DETAILS_TYPE)

        try:
            return model_details[u'entity'][u'ml_asset_guid']
        except:
            return WMLResource._get_required_element_from_dict(model_details, u'model_details', [u'metadata', u'guid'])

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_definition_url(definition_details):
        """
            Get url of stored definition.

            :param definition_details:  stored definition details
            :type definition_details: dict

            :returns: url of stored definition
            :rtype: {str_type}

            A way you might use me is:

            >>> definition_url = client.repository.get_definition_url(definition_details)
        """
        Repository._validate_type(definition_details, u'definition_details', object, True)
        Repository._validate_type_of_details(definition_details, DEFINITION_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(definition_details, u'definition_details', [u'metadata', u'url'])

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def _get_definition_version_url(definition_details):
        """
            Get url of stored definition version.

            :param definition_details:  stored definition details
            :type definition_details: dict

            :returns: url of stored definition version
            :rtype: {str_type}

            A way you might use me is:

            >>> definition_version_url = client.repository.get_definition_version_url(definition_details)
        """
        Repository._validate_type(definition_details, u'definition_details', object, True)
        Repository._validate_type_of_details(definition_details, DEFINITION_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(definition_details, 'definition_details', ['entity', 'training_definition_version', 'url'])

    @staticmethod
    def get_definition_uid(definition_details):
        """
            Get uid of stored definition.

            :param definition_details: stored definition details
            :type definition_details: dict

            :returns: uid of stored model
            :rtype: str

            A way you might use me is:

            >>> definition_uid = client.repository.get_definition_uid(definition_details)
        """
        Repository._validate_type(definition_details, u'definition_details', object, True)
        Repository._validate_type_of_details(definition_details, DEFINITION_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(definition_details, u'definition_details', [u'metadata', u'guid'])

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_experiment_uid(experiment_details):
        """
            Get uid of stored experiment.

            :param experiment_details: stored experiment details
            :type experiment_details: dict

            :returns: uid of stored experiment
            :rtype: {str_type}

            A way you might use me is:

            >>> experiment_uid = client.repository.get_experiment_uid(experiment_details)
        """
        Repository._validate_type(experiment_details, u'experiment_details', object, True)
        Repository._validate_type_of_details(experiment_details, EXPERIMENT_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(experiment_details, u'experiment_details', [u'metadata', u'guid'])

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_experiment_url(experiment_details):
        """
            Get url of stored experiment.

            :param experiment_details:  stored experiment details
            :type experiment_details: dict

            :returns: url of stored experiment
            :rtype: {str_type}

            A way you might use me is:

            >>> experiment_url = client.repository.get_experiment_url(experiment_details)
        """
        Repository._validate_type(experiment_details, u'experiment_details', object, True)
        Repository._validate_type_of_details(experiment_details, EXPERIMENT_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(experiment_details, u'experiment_details', [u'metadata', u'url'])

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_function_uid(function_details):
        """
            Get uid of stored function.

            :param function_details:  stored function details
            :type function_details: dict

            :returns: uid of stored function
            :rtype: {str_type}

            A way you might use me is:

            >>> function_uid = client.repository.get_function_uid(function_details)
        """
        Repository._validate_type(function_details, u'function_details', object, True)
        Repository._validate_type_of_details(function_details, FUNCTION_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(function_details, u'function_details',
                                                           [u'metadata', u'guid'])

    @staticmethod
    @docstring_parameter({'str_type': STR_TYPE_NAME})
    def get_function_url(function_details):
        """
            Get url of stored function.

            :param function_details:  stored function details
            :type function_details: dict

            :returns: url of stored function
            :rtype: {str_type}

            A way you might use me is:

            >>> function_url = client.repository.get_function_url(function_details)
        """
        Repository._validate_type(function_details, u'function_details', object, True)
        Repository._validate_type_of_details(function_details, FUNCTION_DETAILS_TYPE)

        return WMLResource._get_required_element_from_dict(function_details, u'function_details', [u'metadata', u'url'])

    def list(self):
        """
           List stored models, definitions and experiments. Only first 50 records is shown. For more result use specific list functions.

           A way you might use me is:

           >>> client.repository.list()
        """
        from tabulate import tabulate

        headers = self._client._get_headers()
        params = {u'limit': 1000} # TODO - should be unlimited, if results not sorted

        pool = Pool(processes=4)
        endpoints = {
            u'model': self._client.service_instance.details.get(u'entity').get(u'published_models').get(u'url'),
            u'definition': self._href_definitions.get_definitions_href(),
            u'experiment': self._href_definitions.get_experiments_href(),
            u'function': self._href_definitions.get_functions_href(),
            u'runtime': self._href_definitions.get_runtimes_href(),
            u'library': self._href_definitions.get_custom_libraries_href()
        }
        artifact_get = {artifact: pool.apply_async(get_url, (endpoints[artifact], headers, params)) for artifact in endpoints}
        resources = {artifact: [] for artifact in endpoints}

        for artifact in endpoints:
            try:
                response = artifact_get[artifact].get()
                response_text = self._handle_response(200, u'getting all {}s'.format(artifact), response)
                resources[artifact] = response_text[u'resources']
            except Exception as e:
                self._logger.error(e)

        pool.close()

        model_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'], m[u'entity'][u'model_type'], u'model') for m in resources[u'model']]
        experiment_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'settings'][u'name'], m['metadata']['created_at'], u'-', u'experiment') for m in resources[u'experiment']]
        definition_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'], m[u'entity'][u'framework'][u'name'], u'definition') for m in resources[u'definition']]
        function_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'], u'-', m[u'entity'][u'type'] + u' function') for m in resources[u'function']]
        runtime_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'], u'-', m[u'entity'][u'platform'][u'name'] + u' runtime') for m in resources[u'runtime']]
        library_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'], u'-', m[u'entity'][u'platform'][u'name'] + u' library') for m in resources[u'library']]

        values = list(set(model_values + definition_values + experiment_values + function_values + runtime_values + library_values))
        values = sorted(sorted(values, key=lambda x: x[2], reverse=True), key=lambda x: x[4])
        # TODO add intelligent sorting
        table = tabulate([[u'GUID', u'NAME', u'CREATED', u'FRAMEWORK', u'TYPE']] + values[:_DEFAULT_LIST_LENGTH])
        print(table)
        if len(values) > _DEFAULT_LIST_LENGTH:
            print('Note: Only first {} records were displayed. To display more use more specific list functions.'.format(_DEFAULT_LIST_LENGTH))

    def list_models(self, limit=None):
        """
           List stored models. If limit is set to None there will be only first 50 records shown.

           :param limit: limit number of fetched records (optional)
           :type limit: int

           A way you might use me is

           >>> client.repository.list_models()
        """

        model_resources = self.get_model_details(limit=limit)[u'resources']
        model_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'], m[u'entity'][u'model_type']) for m in model_resources]

        self._list(model_values, [u'GUID', u'NAME', u'CREATED', u'FRAMEWORK'], limit, _DEFAULT_LIST_LENGTH)

    def list_experiments(self, limit=None):
        """
           List stored experiments. If limit is set to None there will be only first 50 records shown.

           :param limit: limit number of fetched records (optional)
           :type limit: int

           A way you might use me is

           >>> client.repository.list_experiments()
        """
        experiment_resources = self.get_experiment_details(limit=limit)[u'resources']
        experiment_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'settings'][u'name'], m[u'metadata'][u'created_at']) for m in experiment_resources]

        self._list(experiment_values, [u'GUID', u'NAME', u'CREATED'], limit, _DEFAULT_LIST_LENGTH)

    def list_definitions(self, limit=None):
        """
           List stored definitions. If limit is set to None there will be only first 50 records shown.

           :param limit: limit number of fetched records (optional)
           :type limit: int

           A way you might use me is

           >>> client.repository.list_definitions()
        """
        definition_resources = self.get_definition_details(limit=limit)[u'resources']
        definition_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'], m[u'entity'][u'framework'][u'name']) for m in definition_resources]

        self._list(definition_values, [u'GUID', u'NAME', u'CREATED', u'FRAMEWORK'], limit, _DEFAULT_LIST_LENGTH)

    def list_functions(self, limit=None):
        """
            List stored functions. If limit is set to None there will be only first 50 records shown.

            :param limit: limit number of fetched records (optional)
            :type limit: int

            A way you might use me is

            >>> client.repository.list_functions()
        """
        self._validate_if_functions_are_available('list functions')
        function_resources = self.get_function_details()[u'resources']
        function_values = [(m[u'metadata'][u'guid'], m[u'entity'][u'name'], m[u'metadata'][u'created_at'],
                              m[u'entity'][u'type']) for m in function_resources]

        self._list(function_values, [u'GUID', u'NAME', u'CREATED', u'TYPE'], limit, _DEFAULT_LIST_LENGTH)

    def _check_artifact_type(self, artifact_uid):
        artifact_uid = str_type_conv(artifact_uid)
        Repository._validate_type(artifact_uid, u'artifact_uid', STR_TYPE, True)

        def _artifact_exists(response):
            return (response is not None) and (u'status_code' in dir(response)) and (response.status_code == 200)

        pool = Pool(processes=4)
        headers = self._client._get_headers()
        endpoints = {
            u'definition': self._href_definitions.get_definition_href(artifact_uid),
            u'model': self._client.service_instance.details.get(u'entity').get(u'published_models').get(u'url') + u'/' + artifact_uid,
            u'experiment': self._href_definitions.get_experiment_href(artifact_uid),
            u'function': self._href_definitions.get_function_href(artifact_uid),
            u'runtime': self._href_definitions.get_runtime_href(artifact_uid),
            u'library': self._href_definitions.get_custom_library_href(artifact_uid)
        }
        future = {artifact: pool.apply_async(get_url, (endpoints[artifact], headers)) for artifact in endpoints}
        response_get = {artifact: None for artifact in endpoints}

        for artifact in endpoints:
            try:
                response_get[artifact] = future[artifact].get()
                self._logger.debug(u'Response({})[{}]: {}'.format(endpoints[artifact], response_get[artifact].status_code, response_get[artifact].text))
            except Exception as e:
                self._logger.debug(u'Error during checking artifact type: ' + str(e))

        pool.close()

        artifact_type = {artifact: _artifact_exists(response_get[artifact]) for artifact in response_get}

        return artifact_type
