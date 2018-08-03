from providers.providers_list import PROVIDERS_LIST
from middleware.components.service import BaseComponent, SyncUtils
from middleware.components.transformation import DataDeliveryProcess
from middleware.model import WriteEmptyFieldByUser, WriteRequiredField, System, UserFieldChange, ActualUserData, \
    ActiveDirectoryUser


class SendDataProcess(BaseComponent):
    def __init__(self, sync_id):
        BaseComponent.__init__(self, sync_id, {'component_id': 6})

    @staticmethod
    def set_empty_fields_per_user(system_id, user, data):
        result = {}
        new_data = data.copy()
        configurations = WriteEmptyFieldByUser.get_write_empty_field_by_user_by_system(
            system_id=system_id, user_email=user['email'])
        if configurations:
            for conf in configurations:
                result[conf['field_name']] = conf['default_value']
            new_data.update(result)
        return new_data

    @staticmethod
    def add_required_field(actual_data, json_data):
        new_data = actual_data.copy()
        for d in json_data:
            configurations = WriteRequiredField.get_required_fields_by_system(system_id=d['system_id'])
            for conf in configurations:
                new_data[conf['field_name']] = d['dictionary'].get(conf['field_name'], '')
        return new_data

    def write_changes_to_report_table(self, system_data, actual_data, user):
        system_name = System.get_system_by_system_id(system_data['system_id'])['name']
        for key, value in actual_data.iteritems():
            # We use empty string instead of None because AD doesn't support null values
            old_value = system_data['dictionary'].get(key, '')
            if value != old_value:
                UserFieldChange.add_user_field_change(self.sync_id, system_name, user['active_directory_user_id'],
                                                            user['first_name'], user['last_name'], key,
                                                            user['email'],
                                                            old_value, value)

    @staticmethod
    def delete_unchanged(actual_data, system_data):
        result = {}
        for key, value in actual_data.iteritems():
            # We use empty string instead of None because AD doesn't support null values
            v = system_data.get(key, '')
            if value != v:
                result[key] = value
        return result

    @staticmethod
    def delete_default_image(actual_data):
        result = actual_data.copy()
        for key, value in actual_data.iteritems():
            # there is another server for default slack images
            if key == 'photo' and value.find('secure.gravatar.com') > 0:
                del result[key]
        return result

    def get_diff_by_system(self, user, actual_data, system_data):
        data_with_empty_fields = SendDataProcess.set_empty_fields_per_user(system_data['system_id'], user, actual_data)

        self.write_changes_to_report_table(system_data, data_with_empty_fields, user)
        updated_data = SendDataProcess.delete_unchanged(data_with_empty_fields, system_data['dictionary'])
        data = SendDataProcess.delete_default_image(updated_data)
        return data

    @staticmethod
    def write_actual_data(user, data):
        actual_data = ActualUserData.get_actual_user_by_ad_user_id(
            active_directory_user_id=user['active_directory_user_id'])
        if actual_data:
            ActualUserData.update_actual_user_data(actual_data['actual_user_data_id'],
                                                         active_directory_user_id=user['active_directory_user_id'],
                                                         data=SyncUtils.strigify(data))
        else:
            ActualUserData.add_actual_user_data(active_directory_user_id=user['active_directory_user_id'],
                                                      data=SyncUtils.strigify(data))

    def prepare_data_for_transform(self, data, system_id, user, json_data):
        prepared_data = data.copy()
        for system_data in json_data:
            if system_data['system_id'] == system_id:
                time, prepared_data = SyncUtils.mesure(
                    lambda: self.get_diff_by_system(user, data, system_data))
                self.log({"message": "Data successfully prepared for transformation",
                          "data_1": SyncUtils.strigify(prepared_data),
                          "data_2": SyncUtils.strigify(system_data['dictionary']),
                          "data_3": SyncUtils.strigify(data),
                          "operation": "get diff per system",
                          "system_id": system_id,
                          "success": True,
                          "execution_time": time,
                          "active_directory_user_id": user['active_directory_user_id']})
        return prepared_data

    def send_data_to_remote_system(self, actual_data, user_id, systems_data):
        result = {}
        user = ActiveDirectoryUser.get_user_by_id(active_directory_user_id=user_id)
        system_result = {}
        data_with_required_fields = SendDataProcess.add_required_field(actual_data, systems_data)
        for provider in PROVIDERS_LIST:
            system = provider(self.sync_id)
            if system.is_enabled:
                response = {}
                process = DataDeliveryProcess(self.sync_id)
                prepared_data = self.prepare_data_for_transform(data_with_required_fields, system.system_id, user,
                                                                systems_data)
                data = process.apply_mapping_configuration(system.system_id, user, prepared_data)
                if data:
                    response = system.upload_data(user, data)
                else:
                    self.log({"success": False,
                              "message": "There aren't data  changes for this user",
                              "data_1": SyncUtils.strigify(data),
                              "system_id": system.system_id,
                              "active_directory_user_id": user['active_directory_user_id']})

                system_result[system.system_id] = response
        result[user["active_directory_user_id"]] = system_result
        SendDataProcess.write_actual_data(user, actual_data)
        return result
