import itertools
import json

from middleware.components.providers.base import ACTIVE_DIRECTORY_SYSTEM_ID

from middleware.components.service import BaseComponent, SyncUtils
from middleware.model import ActualUserData


class MergeProcess(BaseComponent):
    def __init__(self, sync_id, active_directory_user_id):
        BaseComponent.__init__(self, sync_id, {"component_id": 4, "active_directory_user_id": active_directory_user_id})
        self.active_directory_user_id = active_directory_user_id

    @staticmethod
    def find_first(data_set, default, key):
        default_value = default.get(key, None)
        for system_data in data_set:
            value = system_data["dictionary"].get(key, None)
            if value is not None and value != default_value:
                return value
        return default_value

    @staticmethod
    def get_unique_keys(data):
        return set(itertools.chain(*[dict["dictionary"].keys() for dict in data]))

    def get_initial_model(self, data):
        initial_model = ActualUserData.get_actual_user_by_ad_user_id(self.active_directory_user_id)
        if initial_model:
            return json.loads(initial_model["data"])

        '''
        If we didn't find cached data in ActualUserData table then we assume that
        top priority model is ActiveDirectory object. Trying to find in downloaded data
        '''
        default_model = filter(lambda arg: str(arg["system_id"]) == str(ACTIVE_DIRECTORY_SYSTEM_ID), data)
        if default_model:
            return default_model[0]["dictionary"]

        message = "Default Active Directory data doesn't exists"
        self.log({"message": message,
                  "system_id": ACTIVE_DIRECTORY_SYSTEM_ID,
                  "success": False,
                  "active_directory_user_id": self.active_directory_user_id})
        raise RuntimeError(message)

    def __merge__(self, json_data):
        default_model = self.get_initial_model(json_data)

        # Sort and filter jsons by updated_at required field
        new_data = filter(lambda json: json["dictionary"]["updated_at"] > default_model["updated_at"],
                          sorted(json_data, key=lambda x: x["dictionary"]["updated_at"], reverse=True))
        updated = {}
        unique_keys = MergeProcess.get_unique_keys(new_data)
        for key in unique_keys:
            new_value = MergeProcess.find_first(new_data, default_model, key)
            if new_value is not None:
                updated[key] = new_value

        merged = default_model.copy()
        merged.update(updated)
        return {"merged": merged, "updated": updated}

    def merge(self, data):
        time, result = SyncUtils.mesure(lambda: self.__merge__(data))
        self.log({"message": "Merged data result",
                  "data_1": SyncUtils.strigify(result["merged"]),
                  "data_2": SyncUtils.strigify(result["updated"]),
                  "active_directory_user_id": self.active_directory_user_id,
                  "success": True,
                  "execution_time": time})
        return result["merged"]