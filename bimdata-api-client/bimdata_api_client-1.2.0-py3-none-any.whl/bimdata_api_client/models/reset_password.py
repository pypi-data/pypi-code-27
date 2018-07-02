# coding: utf-8

"""
    BIMData API

    BIMData API documentation  # noqa: E501

    OpenAPI spec version: v1
    Contact: contact@bimdata.io
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six


class ResetPassword(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'reset_token': 'str',
        'new_password': 'str'
    }

    attribute_map = {
        'reset_token': 'reset_token',
        'new_password': 'new_password'
    }

    def __init__(self, reset_token=None, new_password=None):  # noqa: E501
        """ResetPassword - a model defined in OpenAPI"""  # noqa: E501

        self._reset_token = None
        self._new_password = None
        self.discriminator = None

        self.reset_token = reset_token
        self.new_password = new_password

    @property
    def reset_token(self):
        """Gets the reset_token of this ResetPassword.  # noqa: E501


        :return: The reset_token of this ResetPassword.  # noqa: E501
        :rtype: str
        """
        return self._reset_token

    @reset_token.setter
    def reset_token(self, reset_token):
        """Sets the reset_token of this ResetPassword.


        :param reset_token: The reset_token of this ResetPassword.  # noqa: E501
        :type: str
        """
        if reset_token is None:
            raise ValueError("Invalid value for `reset_token`, must not be `None`")  # noqa: E501
        if reset_token is not None and len(reset_token) < 1:
            raise ValueError("Invalid value for `reset_token`, length must be greater than or equal to `1`")  # noqa: E501

        self._reset_token = reset_token

    @property
    def new_password(self):
        """Gets the new_password of this ResetPassword.  # noqa: E501


        :return: The new_password of this ResetPassword.  # noqa: E501
        :rtype: str
        """
        return self._new_password

    @new_password.setter
    def new_password(self, new_password):
        """Sets the new_password of this ResetPassword.


        :param new_password: The new_password of this ResetPassword.  # noqa: E501
        :type: str
        """
        if new_password is None:
            raise ValueError("Invalid value for `new_password`, must not be `None`")  # noqa: E501
        if new_password is not None and len(new_password) < 1:
            raise ValueError("Invalid value for `new_password`, length must be greater than or equal to `1`")  # noqa: E501

        self._new_password = new_password

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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
        if not isinstance(other, ResetPassword):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
