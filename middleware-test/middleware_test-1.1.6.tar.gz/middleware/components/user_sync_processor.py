from middleware.components.merging import MergeProcess
from providers.providers_list import PROVIDERS_LIST
from middleware.components.service import BaseComponent, GetInternalModel, SyncUtils
from middleware.components.updating import SendDataProcess
from middleware.model import ActiveDirectoryUser


class UserSyncProcessor(BaseComponent):
    def __init__(self, sync_id):
        BaseComponent.__init__(self, sync_id, {"component_id": 2})

    def __sync_user__(self, user):
        user_id = user["active_directory_user_id"]

        try:
            data_from_all_providers = self.collect_data_for_all_providers(user)
            prepared_data = GetInternalModel(self.sync_id, user_id).get_model(data_from_all_providers)
            merged_data = MergeProcess(self.sync_id, user_id).merge(prepared_data)
            SendDataProcess(self.sync_id).send_data_to_remote_system(merged_data, user_id, prepared_data)
            return True
        except Exception as e:
            self.log({"message": "Error syncing user",
                      "active_directory_user_id": user_id,
                      "success": False,
                      "operation": "__collect__",
                      "data_1": str(e)})

            # DON'T RAISE EXCEPTION. TRYING TO SYNC OTHER USER
            return False

    def collect_data_for_all_providers(self, user):
        system_result = {}
        for provider_class in PROVIDERS_LIST:
            provider = provider_class(self.sync_id)
            if provider.is_enabled:
                data = provider.get_json(user)
                if data:
                    system_result[provider.system_id] = data
        return system_result

    def __sync_users__(self):
        for user in ActiveDirectoryUser.get_all_users():
            if user['email']:
                time, result = SyncUtils.mesure(lambda: self.__sync_user__(user))
                self.log({"message": "sync user",
                          "success": result,
                          "operation": "sync user process",
                          "active_directory_user_id": user["active_directory_user_id"],
                          "execution_time": time})

        return True

    def start_sync(self):
        time, result = SyncUtils.mesure(lambda: self.__sync_users__())
        self.log({"message": "Users successfully synced",
                  "success": True,
                  "operation": "syncing users",
                  "execution_time": time})
