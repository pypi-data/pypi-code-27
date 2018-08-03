# ------------------------------------------------------------------------------
# Copyright IBM Corp. 2018
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
#
import logging
import ibm_boto3
from ibm_botocore.client import Config

def Connection(api_key, service_endpoint):
    """ create a connection to COS """

    try:
        cos = ibm_boto3.client('s3',
                    ibm_api_key_id=api_key,
                    ibm_auth_endpoint='https://iam.bluemix.net/oidc/token',
                    config=Config(signature_version='oauth'),
                    endpoint_url="https://{}".format(service_endpoint))

        return cos

    except Exception:
        logging.error("Error connecting to COS")