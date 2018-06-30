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



class V1ReplicationControllerList(object):
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
        'items': 'list[V1ReplicationController]',
        'kind': 'str',
        'metadata': 'V1ListMeta'
    }

    attribute_map = {
        'api_version': 'apiVersion',
        'items': 'items',
        'kind': 'kind',
        'metadata': 'metadata'
    }

    def __init__(self, api_version=None, items=None, kind=None, metadata=None):  # noqa: E501
        """V1ReplicationControllerList - a model defined in Swagger"""  # noqa: E501

        self._api_version = None
        self._items = None
        self._kind = None
        self._metadata = None
        self.discriminator = None

        if api_version is not None:
            self.api_version = api_version
        self.items = items
        if kind is not None:
            self.kind = kind
        if metadata is not None:
            self.metadata = metadata

    @property
    def api_version(self):
        """Gets the api_version of this V1ReplicationControllerList.  # noqa: E501

        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#resources  # noqa: E501

        :return: The api_version of this V1ReplicationControllerList.  # noqa: E501
        :rtype: str
        """
        return self._api_version

    @api_version.setter
    def api_version(self, api_version):
        """Sets the api_version of this V1ReplicationControllerList.

        APIVersion defines the versioned schema of this representation of an object. Servers should convert recognized schemas to the latest internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#resources  # noqa: E501

        :param api_version: The api_version of this V1ReplicationControllerList.  # noqa: E501
        :type: str
        """

        self._api_version = api_version

    @property
    def items(self):
        """Gets the items of this V1ReplicationControllerList.  # noqa: E501

        List of replication controllers. More info: https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller  # noqa: E501

        :return: The items of this V1ReplicationControllerList.  # noqa: E501
        :rtype: list[V1ReplicationController]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this V1ReplicationControllerList.

        List of replication controllers. More info: https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller  # noqa: E501

        :param items: The items of this V1ReplicationControllerList.  # noqa: E501
        :type: list[V1ReplicationController]
        """
        if items is None:
            raise ValueError("Invalid value for `items`, must not be `None`")  # noqa: E501

        self._items = items

    @property
    def kind(self):
        """Gets the kind of this V1ReplicationControllerList.  # noqa: E501

        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds  # noqa: E501

        :return: The kind of this V1ReplicationControllerList.  # noqa: E501
        :rtype: str
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """Sets the kind of this V1ReplicationControllerList.

        Kind is a string value representing the REST resource this object represents. Servers may infer this from the endpoint the client submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds  # noqa: E501

        :param kind: The kind of this V1ReplicationControllerList.  # noqa: E501
        :type: str
        """

        self._kind = kind

    @property
    def metadata(self):
        """Gets the metadata of this V1ReplicationControllerList.  # noqa: E501

        Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds  # noqa: E501

        :return: The metadata of this V1ReplicationControllerList.  # noqa: E501
        :rtype: V1ListMeta
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this V1ReplicationControllerList.

        Standard list metadata. More info: https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds  # noqa: E501

        :param metadata: The metadata of this V1ReplicationControllerList.  # noqa: E501
        :type: V1ListMeta
        """

        self._metadata = metadata

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
        if not isinstance(other, V1ReplicationControllerList):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
