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



class V1DownwardAPIVolumeSource(object):
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
        'default_mode': 'int',
        'items': 'list[V1DownwardAPIVolumeFile]'
    }

    attribute_map = {
        'default_mode': 'defaultMode',
        'items': 'items'
    }

    def __init__(self, default_mode=None, items=None):  # noqa: E501
        """V1DownwardAPIVolumeSource - a model defined in Swagger"""  # noqa: E501

        self._default_mode = None
        self._items = None
        self.discriminator = None

        if default_mode is not None:
            self.default_mode = default_mode
        if items is not None:
            self.items = items

    @property
    def default_mode(self):
        """Gets the default_mode of this V1DownwardAPIVolumeSource.  # noqa: E501

        Optional: mode bits to use on created files by default. Must be a value between 0 and 0777. Defaults to 0644. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set.  # noqa: E501

        :return: The default_mode of this V1DownwardAPIVolumeSource.  # noqa: E501
        :rtype: int
        """
        return self._default_mode

    @default_mode.setter
    def default_mode(self, default_mode):
        """Sets the default_mode of this V1DownwardAPIVolumeSource.

        Optional: mode bits to use on created files by default. Must be a value between 0 and 0777. Defaults to 0644. Directories within the path are not affected by this setting. This might be in conflict with other options that affect the file mode, like fsGroup, and the result can be other mode bits set.  # noqa: E501

        :param default_mode: The default_mode of this V1DownwardAPIVolumeSource.  # noqa: E501
        :type: int
        """

        self._default_mode = default_mode

    @property
    def items(self):
        """Gets the items of this V1DownwardAPIVolumeSource.  # noqa: E501

        Items is a list of downward API volume file  # noqa: E501

        :return: The items of this V1DownwardAPIVolumeSource.  # noqa: E501
        :rtype: list[V1DownwardAPIVolumeFile]
        """
        return self._items

    @items.setter
    def items(self, items):
        """Sets the items of this V1DownwardAPIVolumeSource.

        Items is a list of downward API volume file  # noqa: E501

        :param items: The items of this V1DownwardAPIVolumeSource.  # noqa: E501
        :type: list[V1DownwardAPIVolumeFile]
        """

        self._items = items

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
        if not isinstance(other, V1DownwardAPIVolumeSource):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
