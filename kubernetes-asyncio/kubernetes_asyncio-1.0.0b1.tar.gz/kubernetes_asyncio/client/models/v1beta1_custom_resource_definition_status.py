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



class V1beta1CustomResourceDefinitionStatus(object):
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
        'accepted_names': 'V1beta1CustomResourceDefinitionNames',
        'conditions': 'list[V1beta1CustomResourceDefinitionCondition]'
    }

    attribute_map = {
        'accepted_names': 'acceptedNames',
        'conditions': 'conditions'
    }

    def __init__(self, accepted_names=None, conditions=None):  # noqa: E501
        """V1beta1CustomResourceDefinitionStatus - a model defined in Swagger"""  # noqa: E501

        self._accepted_names = None
        self._conditions = None
        self.discriminator = None

        self.accepted_names = accepted_names
        self.conditions = conditions

    @property
    def accepted_names(self):
        """Gets the accepted_names of this V1beta1CustomResourceDefinitionStatus.  # noqa: E501

        AcceptedNames are the names that are actually being used to serve discovery They may be different than the names in spec.  # noqa: E501

        :return: The accepted_names of this V1beta1CustomResourceDefinitionStatus.  # noqa: E501
        :rtype: V1beta1CustomResourceDefinitionNames
        """
        return self._accepted_names

    @accepted_names.setter
    def accepted_names(self, accepted_names):
        """Sets the accepted_names of this V1beta1CustomResourceDefinitionStatus.

        AcceptedNames are the names that are actually being used to serve discovery They may be different than the names in spec.  # noqa: E501

        :param accepted_names: The accepted_names of this V1beta1CustomResourceDefinitionStatus.  # noqa: E501
        :type: V1beta1CustomResourceDefinitionNames
        """
        if accepted_names is None:
            raise ValueError("Invalid value for `accepted_names`, must not be `None`")  # noqa: E501

        self._accepted_names = accepted_names

    @property
    def conditions(self):
        """Gets the conditions of this V1beta1CustomResourceDefinitionStatus.  # noqa: E501

        Conditions indicate state for particular aspects of a CustomResourceDefinition  # noqa: E501

        :return: The conditions of this V1beta1CustomResourceDefinitionStatus.  # noqa: E501
        :rtype: list[V1beta1CustomResourceDefinitionCondition]
        """
        return self._conditions

    @conditions.setter
    def conditions(self, conditions):
        """Sets the conditions of this V1beta1CustomResourceDefinitionStatus.

        Conditions indicate state for particular aspects of a CustomResourceDefinition  # noqa: E501

        :param conditions: The conditions of this V1beta1CustomResourceDefinitionStatus.  # noqa: E501
        :type: list[V1beta1CustomResourceDefinitionCondition]
        """
        if conditions is None:
            raise ValueError("Invalid value for `conditions`, must not be `None`")  # noqa: E501

        self._conditions = conditions

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
        if not isinstance(other, V1beta1CustomResourceDefinitionStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
