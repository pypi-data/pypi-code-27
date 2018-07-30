# -*- coding: utf-8 -*-
# @Author: sijanonly
# @Date:   2018-07-27 14:05:29
# @Last Modified by:   sijanonly
# @Last Modified time: 2018-07-27 15:14:17

from .base import SolutionByTextAPI


class Message(SolutionByTextAPI):
    """
    Send sms to subscriber.

    """
    service_end_point = 'MessageRSService.svc/SendMessage'

    def __init__(self, security_token, org_code, stage, phone, message, custom_data=None):
        super().__init__(
            security_token, org_code, stage
        )
        if custom_data:
            assert not isinstance(custom_data, dict), 'Custom data should be dictionary'
        self.phone = phone
        self.message = message
        self.custom_data = custom_data

    def post(self):
        """
        """
        recipient_list = []
        recipient = {
            "sendTo": self.phone,
            "CustomFields": None
        }
        if self.custom_data:
            custom_field_list = []
            for key, value in self.custom_data.items():
                custom_field = {}
                custom_field['Key'] = key
                custom_field['Value'] = value
                custom_field_list.append(custom_field)

            recipient["CustomFields"] = custom_field_list

        recipient_list.append(recipient)

        arg = {
            "sendTo": recipient_list,
            "message": self.message
        }
        return super().post(**arg)


class TemplateMessage(SolutionByTextAPI):
    """
    Send template sms to subscriber.

    """
    service_end_point = 'MessageRSService.svc/SendTemplateMessage'

    def __init__(self, security_token, org_code, stage, phone, message, template_id, custom_data=None):
        super().__init__(
            security_token, org_code, stage
        )
        assert not isinstance(template_id, int),'template id should be integer value.'
        if custom_data:
            assert not isinstance(custom_data, dict), 'Custom data should be dictionary'
        self.phone = phone
        self.message = message
        self.template_id = template_id
        self.custom_data = custom_data

    def post(self):
        """
        """
        recipient_list = []
        recipient = {
            "sendTo": self.phone,
            "CustomFields": None
        }
        if self.custom_data:
            custom_field_list = []
            for key, value in self.custom_data.items():
                custom_field = {}
                custom_field['Key'] = key
                custom_field['Value'] = value
                custom_field_list.append(custom_field)

            recipient["CustomFields"] = custom_field_list

        recipient_list.append(recipient)

        arg = {
            "sendTo": recipient_list,
            "templateID": self.template_id
        }
        return super().post(**arg)
