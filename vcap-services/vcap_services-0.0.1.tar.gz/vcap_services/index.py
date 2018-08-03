import os
import json

def load_from_vcap_services(service_name, plan=None, iname=None):
    """
        if VCAP_SERVICES exists or the instance name exists in the
        environemnt, then it returns the credentials
        for the last service that starts with 'name' or {} otherwise
        If plan is specified it will return the credentials for
        the service instance that match that plan or {} otherwise
        :param  String name: service name
        :param  String plan: (Optional) service plan
        :param  String iname: (Optional) instance name
        return {Object} the service credentials or {} if
        name is not found in VCAP_SERVICES or instance name
        is set as an environmental variable. Env var must be
        upper case.
    """
    vcap_services = os.getenv('VCAP_SERVICES')
    if vcap_services is not None:
        services = json.loads(vcap_services)
        for service in services:
            if service_name in service:
                for instance in services[service_name]:
                    if (plan is None or plan == instance['plan']) and (iname is None or iname == instance['name']):
                        return instance['credentials']

    if iname is not None:
        instance = {}
        if os.environ[iname]:
            try:
                instance = json.loads(os.environ[iname])
            except:
                raise KeyError
        return instance


def parse_credentials(service_label, credentials):
    """
        Returns the credentials that match the service label
        pass credentials in the following format:
        {
        "watson_conversation_username": "username",
        "watson_conversation_password": "password",
        }
        :param string serviceLabel: The service label
        :param object credentials: The credentials from starterkit
    """
    key = 'watson_' + service_label + '_'
    creds = {}
    if credentials is not None:
        cred_keys = credentials.keys()
        filtered_keys = list(filter(lambda x: x.find(key) != -1, cred_keys))
        for k in filtered_keys:
            creds[k.replace(key, '')] = credentials[k]
    return creds

def get_credentials_from_file(service_label, credentials_from_local_config=None):
    """
        Returns all the credentials that match the service label from env variables
        :param string serviceLabel: The service label
        :param object credentialsFromFile: (OPTIONAL) The credentials for starterkit from local file
    """
    creds = {}
    kube_tag = 'service_watson_' + service_label
    creds_from_vcap = load_from_vcap_services(service_label)
    if credentials_from_local_config is not None:
        creds = parse_credentials(service_label, credentials_from_local_config)
    elif creds_from_vcap is not None:
        creds = creds_from_vcap
    elif os.getenv(kube_tag) is not None:
        creds = json.loads(os.getenv(kube_tag))
    return creds
