# coding: utf-8

"""
    Kubernetes

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: v1.10.1
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class V1ObjectReference(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'api_version': 'str',
        'field_path': 'str',
        'kind': 'str',
        'name': 'str',
        'namespace': 'str',
        'resource_version': 'str',
        'uid': 'str'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'field_path': 'fieldPath',
        'kind': 'kind',
        'name': 'name',
        'namespace': 'namespace',
        'resource_version': 'resourceVersion',
        'uid': 'uid'
    }

    def __init__(self, api_version=None, field_path=None, kind=None, name=None, namespace=None, resource_version=None, uid=None):  # noqa: E501
        """V1ObjectReference - a model defined in Swagger"""  # noqa: E501

        self._api_version = None
        self._field_path = None
        self._kind = None
        self._name = None
        self._namespace = None
        self._resource_version = None
        self._uid = None
        self.discriminator = None

        if api_version is not None:
            self.api_version = api_version
        if field_path is not None:
            self.field_path = field_path
        if kind is not None:
            self.kind = kind
        if name is not None:
            self.name = name
        if namespace is not None:
            self.namespace = namespace
        if resource_version is not None:
            self.resource_version = resource_version
        if uid is not None:
            self.uid = uid

    @property
    def api_version(self):
        """Gets the api_version of this V1ObjectReference.  # noqa: E501

        API version of the referent.  # noqa: E501

        :return: The api_version of this V1ObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._api_version

    @api_version.setter
    def api_version(self, api_version):
        """Sets the api_version of this V1ObjectReference.

        API version of the referent.  # noqa: E501

        :param api_version: The api_version of this V1ObjectReference.  # noqa: E501
        :type: str
        """

        self._api_version = api_version

    @property
    def field_path(self):
        """Gets the field_path of this V1ObjectReference.  # noqa: E501

        If referring to a piece of an object instead of an entire object, this string should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2]. For example, if the object reference is to a container within a pod, this would take on a value like: \"spec.containers{name}\" (where \"name\" refers to the name of the container that triggered the event) or if no container name is specified \"spec.containers[2]\" (container with index 2 in this pod). This syntax is chosen only to have some well-defined way of referencing a part of an object.  # noqa: E501

        :return: The field_path of this V1ObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._field_path

    @field_path.setter
    def field_path(self, field_path):
        """Sets the field_path of this V1ObjectReference.

        If referring to a piece of an object instead of an entire object, this string should contain a valid JSON/Go field access statement, such as desiredState.manifest.containers[2]. For example, if the object reference is to a container within a pod, this would take on a value like: \"spec.containers{name}\" (where \"name\" refers to the name of the container that triggered the event) or if no container name is specified \"spec.containers[2]\" (container with index 2 in this pod). This syntax is chosen only to have some well-defined way of referencing a part of an object.  # noqa: E501

        :param field_path: The field_path of this V1ObjectReference.  # noqa: E501
        :type: str
        """

        self._field_path = field_path

    @property
    def kind(self):
        """Gets the kind of this V1ObjectReference.  # noqa: E501

        Kind of the referent. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds  # noqa: E501

        :return: The kind of this V1ObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this V1ObjectReference.

        Kind of the referent. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds  # noqa: E501

        :param kind: The kind of this V1ObjectReference.  # noqa: E501
        :type: str
        """

        self._kind = kind

    @property
    def name(self):
        """Gets the name of this V1ObjectReference.  # noqa: E501

        Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa: E501

        :return: The name of this V1ObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this V1ObjectReference.

        Name of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#names  # noqa: E501

        :param name: The name of this V1ObjectReference.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def namespace(self):
        """Gets the namespace of this V1ObjectReference.  # noqa: E501

        Namespace of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/  # noqa: E501

        :return: The namespace of this V1ObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._namespace

    @namespace.setter
    def namespace(self, namespace):
        """Sets the namespace of this V1ObjectReference.

        Namespace of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/  # noqa: E501

        :param namespace: The namespace of this V1ObjectReference.  # noqa: E501
        :type: str
        """

        self._namespace = namespace

    @property
    def resource_version(self):
        """Gets the resource_version of this V1ObjectReference.  # noqa: E501

        Specific resourceVersion to which this reference is made, if any. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#concurrency-control-and-consistency  # noqa: E501

        :return: The resource_version of this V1ObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._resource_version

    @resource_version.setter
    def resource_version(self, resource_version):
        """Sets the resource_version of this V1ObjectReference.

        Specific resourceVersion to which this reference is made, if any. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#concurrency-control-and-consistency  # noqa: E501

        :param resource_version: The resource_version of this V1ObjectReference.  # noqa: E501
        :type: str
        """

        self._resource_version = resource_version

    @property
    def uid(self):
        """Gets the uid of this V1ObjectReference.  # noqa: E501

        UID of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids  # noqa: E501

        :return: The uid of this V1ObjectReference.  # noqa: E501
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this V1ObjectReference.

        UID of the referent. More info: https://kubernetes.io/docs/concepts/overview/working-with-objects/names/#uids  # noqa: E501

        :param uid: The uid of this V1ObjectReference.  # noqa: E501
        :type: str
        """

        self._uid = uid

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, V1ObjectReference):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
