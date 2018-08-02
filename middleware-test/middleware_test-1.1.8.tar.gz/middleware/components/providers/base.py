from middleware.components.service import SyncUtils
from middleware.model import System, Log

ACTIVE_DIRECTORY_USER_ID = "active_directory_user_id"
ACTIVE_DIRECTORY_SYSTEM_ID = "1"

class BaseProvider:
    def __init__(self, system_id, component_info, sync_id):
        component_info.update({"system_id": system_id, "sync_id": sync_id, "component_name": self.__class__.__name__})
        self.component_info = component_info
        self.system_id = system_id
        self.sync_id = sync_id
        self.is_enabled = BaseProvider.is_enabled(system_id)

    @staticmethod
    def is_enabled(system_id):
        provider = System.get_system_by_system_id(system_id=system_id)
        return provider["sync_enabled"] if provider else None

    def download_raw_data_per_user(self, user):
        pass

    def __transform__(self, data, user):
        return data

    def __reverse_transform__(self, data, user):
        return data

    def upload_raw_data_per_user(self, user, data):
        return data

    def get_json(self, user):
        try:
            time, row = SyncUtils.mesure(lambda: self.download_raw_data_per_user(user))
            self.log({"message": "Collected data result for user",
                      "operation": "collect data",
                      "active_directory_user_id": user["active_directory_user_id"],
                      "success": True,
                      "data_1": SyncUtils.strigify(row),
                      "execution_time": time})

            time, result = SyncUtils.mesure(lambda: self.__transform__(row, user))
            self.log({"message": "Normalized data result for user",
                      "operation": "normalization data",
                      "active_directory_user_id": user["active_directory_user_id"],
                      "success": True,
                      "data_1": SyncUtils.strigify(result),
                      "execution_time": time})
            return result
        except Exception as e:
            self.log({"message": "Error in collecting or normalization data",
                      "active_directory_user_id": user["active_directory_user_id"],
                      "success": False,
                      "operation": "get_json",
                      "data_1": str(e)})

    def upload_data(self, user, data):
        try:
            time, row = SyncUtils.mesure(lambda: self.__reverse_transform__(data, user))
            self.log({"message": "Merged data transformed to specific json",
                      "operation": "transform data",
                      "active_directory_user_id": user["active_directory_user_id"],
                      "success": True,
                      "data_1": SyncUtils.strigify(row),
                      "execution_time": time})

            time, result = SyncUtils.mesure(lambda: self.upload_raw_data_per_user(user, row))
            self.log({"message": "Updated remote data for user",
                      "operation": "update remote data",
                      "active_directory_user_id": user["active_directory_user_id"],
                      "success": True,
                      "data_1": SyncUtils.strigify(result),
                      "execution_time": time})

            return result
        except Exception as e:
            self.log({"message": "Error in updating or transforming data",
                      "active_directory_user_id": user["active_directory_user_id"],
                      "operation": "upload_data",
                      "data_1": str(e),
                      "success": False})

    def merge_with_component_info(self, args):
        return dict(args.items() + self.component_info.items())

    def log(self, args):
        Log.add_log(**self.merge_with_component_info(args))

    def build_request(self, url, data=None, user_id=None):
        pass



