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



class V1PodDNSConfig(object):
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
        'nameservers': 'list[str]',
        'options': 'list[V1PodDNSConfigOption]',
        'searches': 'list[str]'
    }

    attribute_map = {
        'nameservers': 'nameservers',
        'options': 'options',
        'searches': 'searches'
    }

    def __init__(self, nameservers=None, options=None, searches=None):  # noqa: E501
        """V1PodDNSConfig - a model defined in Swagger"""  # noqa: E501

        self._nameservers = None
        self._options = None
        self._searches = None
        self.discriminator = None

        if nameservers is not None:
            self.nameservers = nameservers
        if options is not None:
            self.options = options
        if searches is not None:
            self.searches = searches

    @property
    def nameservers(self):
        """Gets the nameservers of this V1PodDNSConfig.  # noqa: E501

        A list of DNS name server IP addresses. This will be appended to the base nameservers generated from DNSPolicy. Duplicated nameservers will be removed.  # noqa: E501

        :return: The nameservers of this V1PodDNSConfig.  # noqa: E501
        :rtype: list[str]
        """
        return self._nameservers

    @nameservers.setter
    def nameservers(self, nameservers):
        """Sets the nameservers of this V1PodDNSConfig.

        A list of DNS name server IP addresses. This will be appended to the base nameservers generated from DNSPolicy. Duplicated nameservers will be removed.  # noqa: E501

        :param nameservers: The nameservers of this V1PodDNSConfig.  # noqa: E501
        :type: list[str]
        """

        self._nameservers = nameservers

    @property
    def options(self):
        """Gets the options of this V1PodDNSConfig.  # noqa: E501

        A list of DNS resolver options. This will be merged with the base options generated from DNSPolicy. Duplicated entries will be removed. Resolution options given in Options will override those that appear in the base DNSPolicy.  # noqa: E501

        :return: The options of this V1PodDNSConfig.  # noqa: E501
        :rtype: list[V1PodDNSConfigOption]
        """
        return self._options

    @options.setter
    def options(self, options):
        """Sets the options of this V1PodDNSConfig.

        A list of DNS resolver options. This will be merged with the base options generated from DNSPolicy. Duplicated entries will be removed. Resolution options given in Options will override those that appear in the base DNSPolicy.  # noqa: E501

        :param options: The options of this V1PodDNSConfig.  # noqa: E501
        :type: list[V1PodDNSConfigOption]
        """

        self._options = options

    @property
    def searches(self):
        """Gets the searches of this V1PodDNSConfig.  # noqa: E501

        A list of DNS search domains for host-name lookup. This will be appended to the base search paths generated from DNSPolicy. Duplicated search paths will be removed.  # noqa: E501

        :return: The searches of this V1PodDNSConfig.  # noqa: E501
        :rtype: list[str]
        """
        return self._searches

    @searches.setter
    def searches(self, searches):
        """Sets the searches of this V1PodDNSConfig.

        A list of DNS search domains for host-name lookup. This will be appended to the base search paths generated from DNSPolicy. Duplicated search paths will be removed.  # noqa: E501

        :param searches: The searches of this V1PodDNSConfig.  # noqa: E501
        :type: list[str]
        """

        self._searches = searches

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
        if not isinstance(other, V1PodDNSConfig):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
