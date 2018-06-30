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


class V1PersistentVolumeClaimCondition(object):
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
        'last_probe_time': 'datetime',
        'last_transition_time': 'datetime',
        'message': 'str',
        'reason': 'str',
        'status': 'str',
        'type': 'str'
    }

    attribute_map = {
        'last_probe_time': 'lastProbeTime',
        'last_transition_time': 'lastTransitionTime',
        'message': 'message',
        'reason': 'reason',
        'status': 'status',
        'type': 'type'
    }

    def __init__(self, last_probe_time=None, last_transition_time=None, message=None, reason=None, status=None, type=None):  # noqa: E501
        """V1PersistentVolumeClaimCondition - a model defined in Swagger"""  # noqa: E501

        self._last_probe_time = None
        self._last_transition_time = None
        self._message = None
        self._reason = None
        self._status = None
        self._type = None
        self.discriminator = None

        if last_probe_time is not None:
            self.last_probe_time = last_probe_time
        if last_transition_time is not None:
            self.last_transition_time = last_transition_time
        if message is not None:
            self.message = message
        if reason is not None:
            self.reason = reason
        self.status = status
        self.type = type

    @property
    def last_probe_time(self):
        """Gets the last_probe_time of this V1PersistentVolumeClaimCondition.  # noqa: E501

        Last time we probed the condition.  # noqa: E501

        :return: The last_probe_time of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :rtype: datetime
        """
        return self._last_probe_time

    @last_probe_time.setter
    def last_probe_time(self, last_probe_time):
        """Sets the last_probe_time of this V1PersistentVolumeClaimCondition.

        Last time we probed the condition.  # noqa: E501

        :param last_probe_time: The last_probe_time of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :type: datetime
        """

        self._last_probe_time = last_probe_time

    @property
    def last_transition_time(self):
        """Gets the last_transition_time of this V1PersistentVolumeClaimCondition.  # noqa: E501

        Last time the condition transitioned from one status to another.  # noqa: E501

        :return: The last_transition_time of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :rtype: datetime
        """
        return self._last_transition_time

    @last_transition_time.setter
    def last_transition_time(self, last_transition_time):
        """Sets the last_transition_time of this V1PersistentVolumeClaimCondition.

        Last time the condition transitioned from one status to another.  # noqa: E501

        :param last_transition_time: The last_transition_time of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :type: datetime
        """

        self._last_transition_time = last_transition_time

    @property
    def message(self):
        """Gets the message of this V1PersistentVolumeClaimCondition.  # noqa: E501

        Human-readable message indicating details about last transition.  # noqa: E501

        :return: The message of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """Sets the message of this V1PersistentVolumeClaimCondition.

        Human-readable message indicating details about last transition.  # noqa: E501

        :param message: The message of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :type: str
        """

        self._message = message

    @property
    def reason(self):
        """Gets the reason of this V1PersistentVolumeClaimCondition.  # noqa: E501

        Unique, this should be a short, machine understandable string that gives the reason for condition's last transition. If it reports \"ResizeStarted\" that means the underlying persistent volume is being resized.  # noqa: E501

        :return: The reason of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this V1PersistentVolumeClaimCondition.

        Unique, this should be a short, machine understandable string that gives the reason for condition's last transition. If it reports \"ResizeStarted\" that means the underlying persistent volume is being resized.  # noqa: E501

        :param reason: The reason of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :type: str
        """

        self._reason = reason

    @property
    def status(self):
        """Gets the status of this V1PersistentVolumeClaimCondition.  # noqa: E501


        :return: The status of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this V1PersistentVolumeClaimCondition.


        :param status: The status of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def type(self):
        """Gets the type of this V1PersistentVolumeClaimCondition.  # noqa: E501


        :return: The type of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this V1PersistentVolumeClaimCondition.


        :param type: The type of this V1PersistentVolumeClaimCondition.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501

        self._type = type

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
        if not isinstance(other, V1PersistentVolumeClaimCondition):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
