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


class V1UserInfo(object):
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
        'extra': 'dict(str, list[str])',
        'groups': 'list[str]',
        'uid': 'str',
        'username': 'str'
    }

    attribute_map = {
        'extra': 'extra',
        'groups': 'groups',
        'uid': 'uid',
        'username': 'username'
    }

    def __init__(self, extra=None, groups=None, uid=None, username=None):  # noqa: E501
        """V1UserInfo - a model defined in Swagger"""  # noqa: E501

        self._extra = None
        self._groups = None
        self._uid = None
        self._username = None
        self.discriminator = None

        if extra is not None:
            self.extra = extra
        if groups is not None:
            self.groups = groups
        if uid is not None:
            self.uid = uid
        if username is not None:
            self.username = username

    @property
    def extra(self):
        """Gets the extra of this V1UserInfo.  # noqa: E501

        Any additional information provided by the authenticator.  # noqa: E501

        :return: The extra of this V1UserInfo.  # noqa: E501
        :rtype: dict(str, list[str])
        """
        return self._extra

    @extra.setter
    def extra(self, extra):
        """Sets the extra of this V1UserInfo.

        Any additional information provided by the authenticator.  # noqa: E501

        :param extra: The extra of this V1UserInfo.  # noqa: E501
        :type: dict(str, list[str])
        """

        self._extra = extra

    @property
    def groups(self):
        """Gets the groups of this V1UserInfo.  # noqa: E501

        The names of groups this user is a part of.  # noqa: E501

        :return: The groups of this V1UserInfo.  # noqa: E501
        :rtype: list[str]
        """
        return self._groups

    @groups.setter
    def groups(self, groups):
        """Sets the groups of this V1UserInfo.

        The names of groups this user is a part of.  # noqa: E501

        :param groups: The groups of this V1UserInfo.  # noqa: E501
        :type: list[str]
        """

        self._groups = groups

    @property
    def uid(self):
        """Gets the uid of this V1UserInfo.  # noqa: E501

        A unique value that identifies this user across time. If this user is deleted and another user by the same name is added, they will have different UIDs.  # noqa: E501

        :return: The uid of this V1UserInfo.  # noqa: E501
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this V1UserInfo.

        A unique value that identifies this user across time. If this user is deleted and another user by the same name is added, they will have different UIDs.  # noqa: E501

        :param uid: The uid of this V1UserInfo.  # noqa: E501
        :type: str
        """

        self._uid = uid

    @property
    def username(self):
        """Gets the username of this V1UserInfo.  # noqa: E501

        The name that uniquely identifies this user among all active users.  # noqa: E501

        :return: The username of this V1UserInfo.  # noqa: E501
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username):
        """Sets the username of this V1UserInfo.

        The name that uniquely identifies this user among all active users.  # noqa: E501

        :param username: The username of this V1UserInfo.  # noqa: E501
        :type: str
        """

        self._username = username

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
        if not isinstance(other, V1UserInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
