import urllib

from tornado.options import options

from middleware import utils
from middleware.components.providers.base import BaseProvider, ACTIVE_DIRECTORY_USER_ID

OFFICEVIBE_SYSTEM_ID = '4'

class OfficeVibe(BaseProvider):
    def __init__(self, sync_id):
        BaseProvider.__init__(self, OFFICEVIBE_SYSTEM_ID, {}, sync_id)

    def build_request(self, url, data=None, user_id=None):
        headers = {'Authorization': 'Bearer ' + options.officevibe_key,
                   "Content-Type": "application/json"}
        if data:
            return utils.make_request(options.officevibe_url, url,
                                      data=data, headers=headers,
                                      method="POST", user_id=user_id)
        else:
            return utils.make_request(options.officevibe_url, url,
                                      headers=headers,
                                      method="GET", user_id=user_id)

    @staticmethod
    def is_fail(response):
        return type(response) != dict or not response.get('isSuccess')

    def office_vibe_log(self, user_id, response, success_message, error_message, operation):
        tuple = (False, error_message) if OfficeVibe.is_fail(response) else (True, success_message)
        self.log({"data_1": str(response),
                  "operation": operation,
                  "success": tuple[0],
                  "message": tuple[1],
                  ACTIVE_DIRECTORY_USER_ID: user_id})
        return tuple[0]

    def add_group(self, user, name):
        user_id = user[ACTIVE_DIRECTORY_USER_ID]
        data = {"name": name}
        result = self.build_request(url="/groups", data=data, user_id=user_id)
        self.office_vibe_log(user_id, result,
                             "New group was successfully added to OfficeVibe",
                             "Error in adding new group to OfficeVibe",
                             "add group")

    def add_user_to_group(self, user, groups, to_managers, to_members):
        user_id = user[ACTIVE_DIRECTORY_USER_ID]
        for group in groups:
            is_group_exists = self.find_group_by_name(group, user_id)
            # commented for now. Need to discuss creation process
            # if not is_group_exists:
            #    is_group_exists = self.add_group(user, group)

            if is_group_exists:
                data = {"groupId": group,
                        "emails": [user["email"]],
                        "toManagers": to_managers,
                        "toMembers": to_members}
                result = self.build_request(url="/groups/addUsers", data=data, user_id=user_id)
                self.office_vibe_log(user_id,
                                     result, "User was successfully added to group in OfficeVibe",
                                     "Error in adding user to group in OfficeVibe",
                                     "add user to group")

    def download_raw_data_per_user(self, user):
        user_email = user["email"]
        user_id = user[ACTIVE_DIRECTORY_USER_ID]
        result = self.build_request(url="/users/{}".format(user_email), user_id=user_id)
        if OfficeVibe.is_fail(result):
            self.log({"success": False,
                      "data_1": str(result),
                      "message": "Error in collecting data from OfficeVibe",
                      "operation": "collect data",
                      ACTIVE_DIRECTORY_USER_ID: user_id})
            raise RuntimeError('OfficeVibe user is not found')
        return result

    def __transform__(self, data, user):
        result = data.copy()
        # OfficeVibe doesn't return updated_at field,
        # so we assume that data are old as default
        # need to update this system every time if anything changes
        result['updated_at'] = '2000-05-05 12:00:00'
        result['manager'] = ''
        return result

    def find_group_by_name(self, group_name, user_id):
        result = self.build_request(
            url="/groups?groupId={}".format(urllib.pathname2url(group_name)), user_id=user_id)
        if OfficeVibe.is_fail(result):
            self.log({"success": False,
                      "data_1": str(result),
                      "message": "Error in getting group by name from OfficeVibe",
                      ACTIVE_DIRECTORY_USER_ID: user_id,
                      "operation": "get group by name"})
            return False
        return True

    def __reverse_transform__(self, data, user):
        result = data.copy()
        if data.get("manager"):
            group_name = "Labs: Direct Reports - {}".format(data["manager"].split(' ')[0] if data["manager"] else '')
            '''
            the method returns data that will be updated 
            for user. Manager is not specified field there.
            '''
            del data["manager"]
            member_groups = self.download_raw_data_per_user(user).get("data")["memberGroups"]
            if group_name not in member_groups:
                result["officevibe_groups"] = [group_name]
        return result

    def upload_image(self, user, link):
        user_id = user[ACTIVE_DIRECTORY_USER_ID]
        if link.startswith('http'):
            data = {"imageUrl": link}
            result = self.build_request("/users/{}".format(user['email']), data, user_id=user_id)
            self.office_vibe_log(user_id,
                                 result, "Image updated",
                                 "Error in uploading image to OfficeVibe",
                                 "add photo")
        else:
            self.log({"success": False,
                      "message": "Invalid image format",
                      "operation": "add photo",
                      ACTIVE_DIRECTORY_USER_ID: user_id})

    def upload_raw_data_per_user(self, user, data):
        user_id = user[ACTIVE_DIRECTORY_USER_ID]
        image = data.get("imageUrl")
        if image:
            self.upload_image(user, image)
            '''
                the method returns data that will be updated 
                for user. Manager is not specified field there.
            '''
            del data['imageUrl']
        user_groups = data.get("officevibe_groups")
        if user_groups:
            is_user_added_to_group = self.add_user_to_group(user, user_groups, False, True)
            '''
                the method returns data that will be updated 
                for user. Manager is not specified field there.
            '''
            del data['officevibe_groups']
        result = self.build_request("/users/{}".format(user['email']), data=data, user_id=user_id)
        if OfficeVibe.is_fail(result):
            self.log({"success": False,
                      "data_1": str(result),
                      "message": "Error in uploading data to OfficeVibe",
                      "operation": "upload data",
                      ACTIVE_DIRECTORY_USER_ID: user_id})
        return result
