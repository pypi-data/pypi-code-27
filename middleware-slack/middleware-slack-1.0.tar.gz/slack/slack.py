from datetime import datetime

import pytz
from tornado.options import options

from middleware import utils
from middleware.components.providers.base import BaseProvider, ACTIVE_DIRECTORY_USER_ID
from middleware.components.service import SyncUtils
from middleware.model import SlackUserGroup, ActiveDirectoryUser

SLACK_SYSTEM_ID = '2'

class Slack(BaseProvider):
    def __init__(self, sync_id):
        BaseProvider.__init__(self, SLACK_SYSTEM_ID, {}, sync_id)

    def build_request(self, url, data, user_id):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        result = utils.make_request(options.slack_api_url, url, data, headers, "POST",
                                    json_type=False, json_response=True, user_id=user_id)
        return result

    def get_custom_fields(self, user):
        user_id = user[ACTIVE_DIRECTORY_USER_ID]
        try:
            data = {"token": Slack.get_slack_token_by_user_group(user_id),
                    "visibility": "visible"}
            response = self.build_request("team.profile.get", data, user_id)

            result = [field['id'] for field in response['profile']['fields']]
            self.log({"operation": "get custom fields from slack",
                      "success": True,
                      ACTIVE_DIRECTORY_USER_ID: user_id,
                      "data_1": SyncUtils.strigify(result)})
            return result
        except Exception as e:
            self.log({"operation": "get custom fields from slack",
                      "success": False,
                      ACTIVE_DIRECTORY_USER_ID: user_id,
                      "data_1": str(e)})
            return []

    def get_additional_fields(self, slack_user_id, ad_user_id):
        data = {"token": Slack.get_slack_token_by_user_group(ad_user_id), "user": slack_user_id}
        result = self.build_request("users.profile.get", data, ad_user_id)

        self.log({"operation": "normalization data",
                  ACTIVE_DIRECTORY_USER_ID: ad_user_id,
                  "success": True,
                  "data_1": SyncUtils.strigify(result)})

        return result['profile'] if result['ok'] else {}

    def download_user_data(self, user, slack_token):
        data = {"token": str(slack_token), "email": user["email"]}
        result = self.build_request("users.lookupByEmail", data, user[ACTIVE_DIRECTORY_USER_ID])
        return result if result['ok'] else None

    def add_or_update_slack_user_group(self, default_group, user_id, group_name):
        if default_group:
            SlackUserGroup.update_slack_user_group(group_name, user_id)
        else:
            SlackUserGroup.add_slack_user_group(group_name, user_id)

        self.log({"operation": "cached slack user user group",
                  ACTIVE_DIRECTORY_USER_ID: user_id,
                  "success": True,
                  "message": "Slack group for user was added or updated",
                  "data_1": group_name})

    def get_user_data_by_workspace(self, user):
        user_id = user[ACTIVE_DIRECTORY_USER_ID]
        cached_location = SlackUserGroup.get_slack_user_group_name(user_id)
        slack_zone_to_token = options.slack_api_tokens_dict
        slack_zones = Slack.get_zones_by_priority(cached_location, slack_zone_to_token)
        errors = []
        for zone in slack_zones:
            try:
                token = slack_zone_to_token.get(zone)
                result = self.download_user_data(user, token)
                if result:
                    self.add_or_update_slack_user_group(cached_location, user_id, zone)
                    return result
            except Exception as e:
                # print e
                errors.append(str(e))

        self.log({"operation": "find slack token for user",
                  ACTIVE_DIRECTORY_USER_ID: user_id,
                  "success": False,
                  "message": "Slack token wasn't found for current user",
                  "data_1": SyncUtils.strigify(errors)})
        raise RuntimeError('Slack user is not found')

    @staticmethod
    def get_zones_by_priority(cached_location, slack_zone_to_token):
        slack_zones = slack_zone_to_token.keys()
        if cached_location:
            slack_zones = [zone for zone in slack_zones if zone != cached_location]
            slack_zones.insert(0, cached_location)
        return slack_zones

    @staticmethod
    def get_slack_token_by_user_group(user_id):
        user_group = SlackUserGroup.get_slack_user_group_name(user_id)
        if not user_group:
            raise RuntimeError(
                'get_slack_token_by_user_group has been called from incorrect place. '
                'Please be sure that token has been already cached')
        return options.slack_api_tokens_dict.get(user_group)

    def download_raw_data_per_user(self, user):
        result = self.get_user_data_by_workspace(user)
        id = result.get('user')['id']
        if id:
            result['user']['profile'].update(self.get_additional_fields(id, user[ACTIVE_DIRECTORY_USER_ID]))
            fields = result['user']['profile']['fields']
            fields_dict = fields if fields else {}
            for field_id in self.get_custom_fields(user):
                field = fields_dict.get(field_id, None)
                if not field:
                    fields_dict[field_id] = {'value': '', 'alt': ''}

        self.log({"operation": "normalization data",
                  ACTIVE_DIRECTORY_USER_ID: user[ACTIVE_DIRECTORY_USER_ID],
                  "success": True,
                  "data_1": SyncUtils.strigify(result)})
        return result

    def __transform__(self, data, user):
        date = data['user']['updated']
        data['user']['updated'] = pytz.UTC.localize(datetime.fromtimestamp(date)).isoformat()
        try:
            manager_id = data['user']['profile']['fields']['Xf9QCRHNM9']
            manager = self.get_additional_fields(manager_id['value'], user[ACTIVE_DIRECTORY_USER_ID])['real_name']
            manager_id['value'] = manager
            return data
        except Exception as e:
            self.log({"success": False,
                      "message": "Cannot get manager name",
                      ACTIVE_DIRECTORY_USER_ID: user[ACTIVE_DIRECTORY_USER_ID],
                      "data_1": str(e)})
            return data

    def get_manager_id_by_name(self, manager_full_name, user):
        try:
            db_user = ActiveDirectoryUser.get_manager(manager_full_name)
            user_data = self.download_raw_data_per_user(db_user)
            return user_data.get('user')['id']
        except Exception as e:
            self.log({"success": False,
                      "message": "Invalid manager name",
                      ACTIVE_DIRECTORY_USER_ID: user[ACTIVE_DIRECTORY_USER_ID],
                      "data_1": str(e)})
            return ""

    def __reverse_transform__(self, data, user):
        try:
            profile = data['profile']['fields']['Xf9QCRHNM9']
            manager = profile['value']
            if manager:
                profile['value'] = self.get_manager_id_by_name(manager, user)
            return data
        except Exception as e:
            self.log({"success": False,
                      "message": "Error when __reverse_transform__",
                      "operation": "get field",
                      ACTIVE_DIRECTORY_USER_ID: user[ACTIVE_DIRECTORY_USER_ID],
                      "data_1": str(e)})
            return data

    def upload_raw_data_per_user(self, user, data):
        user_id = user[ACTIVE_DIRECTORY_USER_ID]
        # we need id to update user, I can only update myprofile via email
        token = Slack.get_slack_token_by_user_group(user_id)
        user_data = self.download_user_data(user, token)
        id = user_data.get('user')['id']
        json_data = {"user": id,
                     'Authorization': 'Bearer ' + token}
        json_data.update(data)
        result = self.build_request("users.profile.set", json_data, user_id)
        return result
