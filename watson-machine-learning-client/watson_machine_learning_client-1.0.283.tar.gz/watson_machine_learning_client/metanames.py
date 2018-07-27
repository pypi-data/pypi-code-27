################################################################################
#
# Licensed Materials - Property of IBM
# (C) Copyright IBM Corp. 2017
# US Government Users Restricted Rights - Use, duplication disclosure restricted
# by GSA ADP Schedule Contract with IBM Corp.
#
################################################################################

from __future__ import print_function
from repository_v3.mlrepository import MetaNames
from tabulate import tabulate
import json
from watson_machine_learning_client.wml_resource import WMLResource
from watson_machine_learning_client.utils import STR_TYPE, STR_TYPE_NAME
from watson_machine_learning_client.log_util import get_logger

logger = get_logger('watson_machine_learning_client.metanames')


class MetaProp:
    def __init__(self, name, key, prop_type, required, example_value, ignored=False, hidden=False, default_value=''):
        self.key = key
        self.name = name
        self.prop_type = prop_type
        self.required = required
        self.example_value = example_value
        self.ignored = ignored
        self.hidden = hidden
        self.default_value = default_value


class MetaNamesBase:
    def __init__(self, meta_props_definitions):
        self._meta_props_definitions = meta_props_definitions

        # if self.__class__.__name__ is not MetaNamesBase.__name__:
        #     for meta_prop in self._meta_props_definitions:
        #         meta_prop.name = list(self.__class__.__dict__.keys())[list(self.__class__.__dict__.values()).index(meta_prop.key)]

    def _validate(self, meta_props):
        for meta_prop in self._meta_props_definitions:
            if meta_prop.ignored is False:
                WMLResource._validate_meta_prop(meta_props, meta_prop.key, meta_prop.prop_type, meta_prop.required)
            else:
                logger.warning('\'{}\' meta prop is deprecated. It will be ignored.'.format(meta_prop.name))

    def _check_types_only(self, meta_props):
        for meta_prop in self._meta_props_definitions:
            if meta_prop.ignored is False:
                WMLResource._validate_meta_prop(meta_props, meta_prop.key, meta_prop.prop_type, False)
            else:
                logger.warning('\'{}\' meta prop is deprecated. It will be ignored.'.format(meta_prop.name))

    def get(self):
        return sorted(list(map(lambda x: x.name, filter(lambda x: not x.ignored and not x.hidden, self._meta_props_definitions))))

    def show(self):
        print(self._generate_table())

    def _generate_doc_table(self):
        return self._generate_table('MetaName', 'Type', 'Required', 'Default value', 'Example value',
                                    show_examples=True, format='grid', values_format='``{}``')

    def _generate_doc(self, resource_name):
        return """
Set of MetaNames for {}.

Available MetaNames:

{}

""".format(resource_name, MetaNamesBase(self._meta_props_definitions)._generate_doc_table())


    def _generate_table(self, name_label='META_PROP NAME', type_label='TYPE',
                       required_label='REQUIRED', default_value_label='DEFAULT_VALUE',
                       example_value_label='EXAMPLE_VALUE', show_examples=False, format='simple', values_format='{}'):

        show_defaults = any(meta_prop.default_value is not '' for meta_prop in filter(lambda x: not x.ignored and not x.hidden, self._meta_props_definitions))

        header = [name_label, type_label, required_label]

        if show_defaults:
            header.append(default_value_label)

        if show_examples:
            header.append(example_value_label)

        table_content = []

        for meta_prop in filter(lambda x: not x.ignored and not x.hidden, self._meta_props_definitions):
            row = [meta_prop.name, meta_prop.prop_type.__name__, u'Y' if meta_prop.required else u'N']

            if show_defaults:
                row.append(values_format.format(meta_prop.default_value) if meta_prop.default_value is not '' else '')

            if show_examples:
                row.append(values_format.format(meta_prop.example_value) if meta_prop.example_value is not '' else '')

            table_content.append(row)

        table = tabulate(
            [header] + table_content,
            tablefmt=format
        )
        return table

    def get_example_values(self):
        return dict((x.key, x.example_value) for x in filter(lambda x: not x.ignored and not x.hidden, self._meta_props_definitions))


class TrainingConfigurationMetaNames(MetaNamesBase):
    _COMPUTE_CONFIGURATION_DEFAULT = 'k80'
    NAME = "name"
    DESCRIPTION = "description"
    AUTHOR_NAME = "author_name"
    AUTHOR_EMAIL = "author_email"
    TRAINING_DATA_REFERENCE = "training_data"
    TRAINING_RESULTS_REFERENCE = "training_results"
    EXECUTION_COMMAND = "command"
    COMPUTE_CONFIGURATION = "compute_configuration_name"

    _meta_props_definitions = [
        MetaProp('NAME',                        NAME,                                  STR_TYPE,   True,   u'Hand-written Digit Recognition'),
        MetaProp('DESCRIPTION',                 DESCRIPTION,                           STR_TYPE,   False,  u'Hand-written Digit Recognition training'),
        MetaProp('AUTHOR_NAME',                 AUTHOR_NAME,                           STR_TYPE,   False,  u'John Smith'),
        MetaProp('AUTHOR_EMAIL',                AUTHOR_EMAIL,                          STR_TYPE,   False,  u'john.smith@x.com', ignored=True),
        MetaProp('TRAINING_DATA_REFERENCE',     TRAINING_DATA_REFERENCE,               dict,       True,   {u'connection': {u'endpoint_url': u'https://s3-api.us-geo.objectstorage.softlayer.net',u'access_key_id': u'***',u'secret_access_key': u'***'},u'source': {u'bucket': u'train-data'},u'type': u's3'}),
        MetaProp('TRAINING_RESULTS_REFERENCE',  TRAINING_RESULTS_REFERENCE,            dict,       True,   {u'connection': {u'endpoint_url': u'https://s3-api.us-geo.objectstorage.softlayer.net',u'access_key_id': u'***',u'secret_access_key': u'***'},u'target': {u'bucket': u'train-data'},u'type': u's3'}),
        MetaProp('EXECUTION_COMMAND',           EXECUTION_COMMAND,                     STR_TYPE,   False,  u'python3 tensorflow_mnist_softmax.py --trainingIters 20', default_value='<value from model definition>'),
        MetaProp('COMPUTE_CONFIGURATION',       COMPUTE_CONFIGURATION,                 dict,       False,  {u'name': _COMPUTE_CONFIGURATION_DEFAULT}, default_value={u'name': _COMPUTE_CONFIGURATION_DEFAULT})
    ]

    __doc__ = MetaNamesBase(_meta_props_definitions)._generate_doc('trainings')

    def __init__(self):
        MetaNamesBase.__init__(self, self._meta_props_definitions)


class ExperimentMetaNames(MetaNamesBase):
    NAME = "name"
    DESCRIPTION = "description"
    TAGS = "tags"
    AUTHOR_NAME = "author_name"
    AUTHOR_EMAIL = "author_email"
    EVALUATION_METHOD = "evaluation_method"
    EVALUATION_METRICS = "evaluation_metrics"
    TRAINING_REFERENCES = "training_references"
    TRAINING_DATA_REFERENCE = "training_data_reference"
    TRAINING_RESULTS_REFERENCE = "training_results_reference"

    _meta_props_definitions = [
        MetaProp('NAME',                        NAME,                        STR_TYPE,   True,     u'Hand-written Digit Recognitionu'),
        MetaProp('DESCRIPTION',                 DESCRIPTION,                 STR_TYPE,   False,    u'Hand-written Digit Recognition training'),
        MetaProp('TAGS',                        TAGS,                        list,       False,    [{u'value': 'dsx-project.<project-guid>',u'description': 'DSX project guid'}]),
        MetaProp('AUTHOR_NAME',                 AUTHOR_NAME,                 STR_TYPE,   False,    u'John Smith'),
        MetaProp('AUTHOR_EMAIL',                AUTHOR_EMAIL,                STR_TYPE,   False,    u'john.smith@x.com', ignored=True),
        MetaProp('EVALUATION_METHOD',           EVALUATION_METHOD,           STR_TYPE,   False,    u'multiclass'),
        MetaProp('EVALUATION_METRICS',          EVALUATION_METRICS,          list,       False,    [u'accuracy']),
        MetaProp('TRAINING_REFERENCES',         TRAINING_REFERENCES,         list,       True,     [{u'training_definition_url': u'https://ibm-watson-ml.mybluemix.net/v3/ml_assets/training_definitions/12345',u'compute_configuration': {u'name': TrainingConfigurationMetaNames._COMPUTE_CONFIGURATION_DEFAULT}},{u'training_definition_url': u'https://ibm-watson-ml.mybluemix.net/v3/ml_assets/training_definitions/67890'}]),
        MetaProp('TRAINING_DATA_REFERENCE',     TRAINING_DATA_REFERENCE,     dict,       True,     {u'connection': {u'endpoint_url': u'https://s3-api.us-geo.objectstorage.softlayer.net',u'access_key_id': u'***',u'secret_access_key': u'***'},u'source': {u'bucket': u'train-data'},u'type': u's3'}),
        MetaProp('TRAINING_RESULTS_REFERENCE',  TRAINING_RESULTS_REFERENCE,  dict,       True,     {u'connection': {u'endpoint_url': u'https://s3-api.us-geo.objectstorage.softlayer.net',u'access_key_id': u'***',u'secret_access_key': u'***'},u'target': {u'bucket': u'result-data'},u'type': 's3'})
    ]

    __doc__ = MetaNamesBase(_meta_props_definitions)._generate_doc('experiments')

    def __init__(self):
        MetaNamesBase.__init__(self, self._meta_props_definitions)


class ModelDefinitionMetaNames(MetaNamesBase):
    NAME = "name"
    DESCRIPTION = "description"
    AUTHOR_NAME = "author_name"
    AUTHOR_EMAIL = "author_email"
    FRAMEWORK_NAME = "framework_name"
    FRAMEWORK_VERSION = "framework_version"
    RUNTIME_NAME = "runtime_name"
    RUNTIME_VERSION = "runtime_version"
    EXECUTION_COMMAND = "command"

    _meta_props_definitions = [
        MetaProp('NAME',                NAME, STR_TYPE, True, u'my_training_definition'),
        MetaProp('DESCRIPTION',         DESCRIPTION, STR_TYPE, False, u'my_description'),
        MetaProp('AUTHOR_NAME',         AUTHOR_NAME, STR_TYPE, False, u'John Smith'),
        MetaProp('AUTHOR_EMAIL',        AUTHOR_EMAIL, STR_TYPE, False, u'john.smith@x.com', ignored=True),
        MetaProp('FRAMEWORK_NAME',      FRAMEWORK_NAME, STR_TYPE, True, u'tensorflow'),
        MetaProp('FRAMEWORK_VERSION',   FRAMEWORK_VERSION, STR_TYPE, True, u'1.5'),
        MetaProp('RUNTIME_NAME',        RUNTIME_NAME, STR_TYPE, True, u'python'),
        MetaProp('RUNTIME_VERSION',     RUNTIME_VERSION, STR_TYPE, True, u'3.5'),
        MetaProp('EXECUTION_COMMAND',   EXECUTION_COMMAND, STR_TYPE, True, u'python3 tensorflow_mnist_softmax.py --trainingIters 20')
    ]

    __doc__ = MetaNamesBase(_meta_props_definitions)._generate_doc('definitions')

    def __init__(self):
        MetaNamesBase.__init__(self, self._meta_props_definitions)


class ModelMetaNames(MetaNamesBase):
    NAME = "name"
    DESCRIPTION = MetaNames.DESCRIPTION
    AUTHOR_NAME = MetaNames.AUTHOR_NAME
    AUTHOR_EMAIL = "author_email"
    FRAMEWORK_NAME = MetaNames.FRAMEWORK_NAME
    FRAMEWORK_VERSION = MetaNames.FRAMEWORK_VERSION
    FRAMEWORK_LIBRARIES = MetaNames.FRAMEWORK_LIBRARIES
    RUNTIME_NAME = "runtime_name"
    RUNTIME_VERSION = "runtime_version"
    TRAINING_DATA_REFERENCE = MetaNames.TRAINING_DATA_REFERENCE
    EVALUATION_METHOD = MetaNames.EVALUATION_METHOD
    EVALUATION_METRICS = MetaNames.EVALUATION_METRICS
    OUTPUT_DATA_SCHEMA = MetaNames.OUTPUT_DATA_SCHEMA
    LABEL_FIELD = MetaNames.LABEL_FIELD
    TRANSFORMED_LABEL_FIELD = MetaNames.TRANSFORMED_LABEL_FIELD
    RUNTIME_UID = "runtime_uid"

    _meta_props_definitions = [
        MetaProp('NAME',                    NAME,                        STR_TYPE,   True,   "my_model"),
        MetaProp('DESCRIPTION',             DESCRIPTION,                 STR_TYPE,   False,  "my_description"),
        MetaProp('AUTHOR_NAME',             AUTHOR_NAME,                 STR_TYPE,   False,  u'John Smith'),
        MetaProp('AUTHOR_EMAIL',            AUTHOR_EMAIL,                STR_TYPE,   False,  u'john.smith@x.com', ignored=True),
        MetaProp('FRAMEWORK_NAME',          FRAMEWORK_NAME,              STR_TYPE,   False,  u'tensorflow'),
        MetaProp('FRAMEWORK_VERSION',       FRAMEWORK_VERSION,           STR_TYPE,   False,  u'1.5'),
        MetaProp('FRAMEWORK_LIBRARIES',     FRAMEWORK_LIBRARIES,         list,       False,  [{'name': 'keras', 'version': '2.1.3'}]),
        MetaProp('RUNTIME_NAME',            RUNTIME_NAME,                STR_TYPE,   False,  u'python'),
        MetaProp('RUNTIME_VERSION',         RUNTIME_VERSION,             STR_TYPE,   False,  u'3.5'),
        MetaProp('TRAINING_DATA_REFERENCE', TRAINING_DATA_REFERENCE,     dict,       False,  {}),
        MetaProp('EVALUATION_METHOD',       EVALUATION_METHOD,           STR_TYPE,   False,  "multiclass"),
        MetaProp('EVALUATION_METRICS',      EVALUATION_METRICS,          list,       False,  [{"name": "accuracy","value": 0.64,"threshold": 0.8}]),
        MetaProp('OUTPUT_DATA_SCHEMA',      OUTPUT_DATA_SCHEMA,          dict,       False,  {'fields': [{'metadata': {}, 'type': 'string', 'name': 'GENDER', 'nullable': True}, {'metadata': {'modeling_role': 'transformed-target'}, 'type': 'double', 'name': 'PRODUCT_LINE_IX', 'nullable': False}], 'type': 'struct'}),
        MetaProp('LABEL_FIELD',             LABEL_FIELD,                 STR_TYPE,   False,  'PRODUCT_LINE'),
        MetaProp('TRANSFORMED_LABEL_FIELD', TRANSFORMED_LABEL_FIELD,     STR_TYPE,   False,  'PRODUCT_LINE_IX'),
        MetaProp('RUNTIME_UID',             RUNTIME_UID,                 STR_TYPE,   False,  '53628d69-ced9-4f43-a8cd-9954344039a8')
    ]

    __doc__ = MetaNamesBase(_meta_props_definitions)._generate_doc('models')

    def __init__(self):
        MetaNamesBase.__init__(self, self._meta_props_definitions)


class LearningSystemMetaNames(MetaNamesBase):
    FEEDBACK_DATA_REFERENCE = "feedback_data_reference"
    SPARK_REFERENCE = "spark_instance"
    MIN_FEEDBACK_DATA_SIZE = "min_feedback_data_size"
    AUTO_RETRAIN = "auto_retrain"
    AUTO_REDEPLOY = "auto_redeploy"

    _meta_props_definitions = [
        MetaProp('FEEDBACK_DATA_REFERENCE', FEEDBACK_DATA_REFERENCE,     dict,       True, {}),
        MetaProp('SPARK_REFERENCE',         SPARK_REFERENCE,             dict,       True, {}),
        MetaProp('MIN_FEEDBACK_DATA_SIZE',  MIN_FEEDBACK_DATA_SIZE,      int,        True, 100),
        MetaProp('AUTO_RETRAIN',            AUTO_RETRAIN,                STR_TYPE,   True, "conditionally"),
        MetaProp('AUTO_REDEPLOY',           AUTO_REDEPLOY,               STR_TYPE,   True, "always")
    ]

    __doc__ = MetaNamesBase(_meta_props_definitions)._generate_doc('learning system')

    def __init__(self):
        MetaNamesBase.__init__(self, self._meta_props_definitions)


class PayloadLoggingMetaNames(MetaNamesBase):
    PAYLOAD_DATA_REFERENCE = "payload_store"
    LABELS = "labels"
    OUTPUT_DATA_SCHEMA = "output_data_schema"

    _meta_props_definitions = [
        MetaProp('PAYLOAD_DATA_REFERENCE',  PAYLOAD_DATA_REFERENCE,       dict, True,     {}),
        MetaProp('LABELS',                  LABELS,              list, False,    ['a', 'b', 'c']),
        MetaProp('OUTPUT_DATA_SCHEMA',      OUTPUT_DATA_SCHEMA,  dict, False,    {})
    ]

    __doc__ = MetaNamesBase(_meta_props_definitions)._generate_doc('payload logging system')

    def __init__(self):
        MetaNamesBase.__init__(self, self._meta_props_definitions)


class FunctionMetaNames(MetaNamesBase):
    NAME = "name"
    DESCRIPTION = "description"
    RUNTIME_UID = "runtime_uid"
    INPUT_DATA_SCHEMA = "input_data_schema"
    OUTPUT_DATA_SCHEMA = "output_data_schema"
    TAGS = "tags"

    _meta_props_definitions = [
        MetaProp('NAME',                NAME,                STR_TYPE,   True,   "ai_function"),
        MetaProp('DESCRIPTION',         DESCRIPTION,         STR_TYPE,   False,  "This is ai function"),
        MetaProp('RUNTIME_UID',         RUNTIME_UID,         STR_TYPE,   False,  '53628d69-ced9-4f43-a8cd-9954344039a8'),
        MetaProp('INPUT_DATA_SCHEMA',   INPUT_DATA_SCHEMA,   dict,       False,  {"type": "struct", "fields": [{"name": "x", "type": "double", "nullable": False, "metadata": {}}, {"name": "y", "type": "double", "nullable": False, "metadata": {}}]}),
        MetaProp('OUTPUT_DATA_SCHEMA',  OUTPUT_DATA_SCHEMA,  dict,       False,  {"type": "struct", "fields": [{"name": "multiplication", "type": "double", "nullable": False, "metadata": {}}]}),
        MetaProp('TAGS',                TAGS,                list,       False,  [{"value": "ProjectA", "description": "Functions created for ProjectA"}])
    ]

    __doc__ = MetaNamesBase(_meta_props_definitions)._generate_doc('AI functions')

    def __init__(self):
        MetaNamesBase.__init__(self, self._meta_props_definitions)


class RuntimeMetaNames(MetaNamesBase):
    NAME = "name"
    DESCRIPTION = "description"
    PLATFORM = "platform"
    LIBRARIES_UIDS = "libraries_uids"
    LIBRARIES_DEFINITIONS = "libraries_definitions"
    CONFIGURATION_FILEPATH = "configuration_filepath"

    _meta_props_definitions = [
        MetaProp('NAME',                            NAME,                            STR_TYPE,   True,   "runtime_spec_python_3.5"),
        MetaProp('DESCRIPTION',                     DESCRIPTION,                     STR_TYPE,   False,  "py35"),
        MetaProp('PLATFORM',                        PLATFORM,                        dict,       True,   {"name": "python", "version": "3.5"}),
        MetaProp('LIBRARIES_UIDS',                  LIBRARIES_UIDS,                 list, False, ["46dc9cf1-252f-424b-b52d-5cdd9814987f"]),
        MetaProp('LIBRARIES_DEFINITIONS',           LIBRARIES_DEFINITIONS,          list, False, [{"name": "libraries_custom", "description": "custom libraries for scoring", "filepath": "/home/lib.gz", "version": "1.0", "platform": "python", "platform_versions": ["3.5"]}]),
        MetaProp('CONFIGURATION_FILEPATH',          CONFIGURATION_FILEPATH,          STR_TYPE,   False,   "/home/env_config.yaml")
    ]

    __doc__ = MetaNamesBase(_meta_props_definitions)._generate_doc('Runtime Specs')

    def __init__(self):
        MetaNamesBase.__init__(self, self._meta_props_definitions)


class LibraryMetaNames(MetaNamesBase):
    NAME = "name"
    DESCRIPTION = "description"
    FILEPATH = "filepath"
    VERSION = "version"
    PLATFORM = "platform"

    _meta_props_definitions = [
        MetaProp('NAME',            NAME,          STR_TYPE,   True,   "my_lib"),
        MetaProp('DESCRIPTION',     DESCRIPTION,   STR_TYPE,   False,  "my lib"),
        MetaProp('PLATFORM',        PLATFORM,      dict,       True,   {"name": "python", "versions": ["3.5"]}),
        MetaProp('VERSION',         VERSION,       STR_TYPE,   True,   "1.0"),
        MetaProp('FILEPATH',        FILEPATH,      STR_TYPE,   True,  "/home/user/my_lib_1_0.zip")
    ]

    __doc__ = MetaNamesBase(_meta_props_definitions)._generate_doc('Custom Libraries')

    def __init__(self):
        MetaNamesBase.__init__(self, self._meta_props_definitions)