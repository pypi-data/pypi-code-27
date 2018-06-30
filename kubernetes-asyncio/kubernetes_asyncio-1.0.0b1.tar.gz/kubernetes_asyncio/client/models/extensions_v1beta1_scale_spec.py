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


class ExtensionsV1beta1ScaleSpec(object):
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
        'replicas': 'int'
    }

    attribute_map = {
        'replicas': 'replicas'
    }

    def __init__(self, replicas=None):  # noqa: E501
        """ExtensionsV1beta1ScaleSpec - a model defined in Swagger"""  # noqa: E501

        self._replicas = None
        self.discriminator = None

        if replicas is not None:
            self.replicas = replicas

    @property
    def replicas(self):
        """Gets the replicas of this ExtensionsV1beta1ScaleSpec.  # noqa: E501

        desired number of instances for the scaled object.  # noqa: E501

        :return: The replicas of this ExtensionsV1beta1ScaleSpec.  # noqa: E501
        :rtype: int
        """
        return self._replicas

    @replicas.setter
    def replicas(self, replicas):
        """Sets the replicas of this ExtensionsV1beta1ScaleSpec.

        desired number of instances for the scaled object.  # noqa: E501

        :param replicas: The replicas of this ExtensionsV1beta1ScaleSpec.  # noqa: E501
        :type: int
        """

        self._replicas = replicas

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
        if not isinstance(other, ExtensionsV1beta1ScaleSpec):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
