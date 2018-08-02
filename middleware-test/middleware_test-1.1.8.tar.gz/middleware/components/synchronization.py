from ldap3 import SUBTREE
from ldap3.core.exceptions import LDAPInvalidCredentialsResult, LDAPExceptionError
from tornado.options import options

from middleware.model import ActiveDirectoryUser
from service import SyncUtils, BaseComponent

AD_PICTURE_FIELD = "thumbnailPhoto"

class ActiveDirectoryUserSync(BaseComponent):
    def __init__(self, sync_id):
        BaseComponent.__init__(self, sync_id, {"component_id": 1, "system_id": "1"})

    def start_sync(self):
        from ldap3 import Server, Connection, ALL
        s = Server(options.AD_server, get_info=ALL)
        connection = None
        try:
            connection = Connection(s, options.AD_admin, options.AD_password, auto_encode=False, check_names=True,
                                    auto_bind="NONE", version=3, authentication="SIMPLE",
                                    client_strategy="SYNC", auto_referrals=True, read_only=False, lazy=False,
                                    raise_exceptions=True)

            connection.open()
            connection.bind()
        except LDAPInvalidCredentialsResult as e:
            self.log({"success": False, "message": "LDAP invalid credentials", "operation": "connection to AD server",
                      "data_1": str(e)})
            raise e
        except LDAPExceptionError as e:
            self.log({"success": False, "message": "LDAP exception", "operation": "connection to AD server",
                      "data_1": str(e)})
            raise e
        else:
            users = self.add_log(lambda: ActiveDirectoryUserSync.get_active_directory_users(connection), "Get")
            modified = self.add_log(lambda: ActiveDirectoryUserSync.create_or_update_users(users), "Create or Update")
            deleted = self.add_log(lambda: ActiveDirectoryUserSync.delete_users(users), "Delete")
            return {"sync_data": {"created": modified['created'], "updated": modified['updated'], "deleted": deleted}}
        finally:
            if connection:
                connection.unbind()

    @staticmethod
    def get_photo_link(email, photo):
        if photo:
            import os
            file_path = os.path.join(options.save_picture_path, '{}_AD.jpg'.format(email))
            photo = ActiveDirectoryUserSync.safe_list_get(photo)
            with open(file_path, 'wb') as output:
                output.write(photo)
            return "file://" + file_path
        return ''

    @staticmethod
    def get_active_directory_users(connection):
        base_dn = options.AD_base_dn
        search_filter = "(&(mail=*)(objectClass=user)(!(userAccountControl=514))(!(userAccountControl=66050))(|(msExchRecipientTypeDetails=1)(msExchRecipientTypeDetails=2147483648)))"
        attributes = ["cn", "co", "company", "department", "displayName", "distinguishedName",
                      "facsimileTelephoneNumber", "givenName", "isDeleted", "jpegPhoto", "mail", "manager",
                      "middleName", "mobile", "name", "objectCategory", "physicalDeliveryOfficeName", "objectGUID",
                      "postalAddress", "postalCode", "sAMAccountName", "sn", "l", "street", "streetAddress",
                      "telephoneNumber", "title", "userPrincipalName", "whenChanged", "wWWHomePage", "objectclass",
                      "employeeID", AD_PICTURE_FIELD]
        entry_generator = connection.extend.standard.paged_search(search_base=base_dn, search_filter=search_filter,
                                                                  search_scope=SUBTREE, attributes=attributes,
                                                                  paged_size=50, generator=True)
        results = []
        for entry in entry_generator:
            attributes = entry.get('attributes', None)
            if attributes:
                attributes[AD_PICTURE_FIELD] = ActiveDirectoryUserSync.get_photo_link(attributes['mail'],
                                                                                      attributes[AD_PICTURE_FIELD])
                results.append(dict(attributes))
        return results

    @staticmethod
    def safe_list_get(array, idx=0, default=''):
        """Active directory returns [] when value is empty, [1,2,3] when value is list or "string" if value"""
        # TODO refactoring
        if type(array) == list:
            try:
                return array[idx]
            except IndexError:
                return default
        else:
            return array

    @staticmethod
    def create_or_update_users(users):
        result = {"updated": [], "created": []}
        for user in users:
            attributes = user.copy()
            email = ActiveDirectoryUserSync.safe_list_get(attributes["mail"].lower())
            if email:
                user_data = {"first_name": ActiveDirectoryUserSync.safe_list_get(attributes["givenName"]),
                             "last_name": ActiveDirectoryUserSync.safe_list_get(attributes["sn"]),
                             "login": ActiveDirectoryUserSync.safe_list_get(attributes["sAMAccountName"]),
                             "email": email}

                manager = attributes['manager']
                if manager:
                    attributes['manager'] = manager.split('CN=')[1].split(',OU')[0]
                user_data["metadata"] = SyncUtils.strigify(attributes)

                ad_user = ActiveDirectoryUser.get_user_by_login(login=user_data["login"])

                if ad_user:
                    uuid = ActiveDirectoryUser.update_active_directory_user(
                        ad_user["active_directory_user_id"], **user_data)
                    result["updated"].append(uuid)
                else:
                    uuid = ActiveDirectoryUser.add_active_directory_user(**user_data)
                    result["created"].append(uuid)
        return result

    @staticmethod
    def delete_users(users):
        result = []
        logins = [user["sAMAccountName"] for user in users]
        for db_user in ActiveDirectoryUser.get_all_users():
            login = db_user["login"]
            if login not in logins:
                ActiveDirectoryUser.delete_active_directory_user(db_user["active_directory_user_id"])
                result.append(db_user["active_directory_user_id"])
        return result

    def add_log(self, function, operation):
        time, result = SyncUtils.mesure(function)
        self.log({"message": "Success {} operation for {} users".format(operation, len(result)),
                  "data_1": SyncUtils.strigify(result), "success": True, "operation": operation,
                  "execution_time": time})
        return result
