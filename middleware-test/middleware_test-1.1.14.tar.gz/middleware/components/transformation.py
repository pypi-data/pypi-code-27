from  middleware import model
from middleware.components.service import BaseComponent, SyncUtils


class DataDeliveryProcess(BaseComponent):
    def __init__(self, sync_id):
        BaseComponent.__init__(self, sync_id, {'component_id': 5})

    def build_nested_helper(self, path, text, container):
        segments = path.split('.')
        head = segments[0]
        tail = segments[1:]
        if not tail:
            container[head] = text
        else:
            if head not in container:
                container[head] = {}
            self.build_nested_helper('.'.join(tail), text, container[head])

    def build_nested(self, paths):
        container = {}
        for key, value in paths.iteritems():
            self.build_nested_helper(key, value, container)
        return container

    def transform(self, system_id, user, prepared_data):
        result = {}
        configurations = model.FieldWriteConfiguration.get_configurations_by_system(system_id=system_id)
        forbidden_fields = [field['field_name'] for field in
                            model.WriteForbiddenField.get_forbidden_fields_by_system(system_id)]
        if prepared_data:
            config_dict = {}
            for conf in configurations:
                if conf['from_field_name'] not in forbidden_fields:
                    try:
                        config_dict[conf['to_path'][2:]] = prepared_data[conf['from_field_name']]
                    except Exception as e:
                        message = "incorrect 'from_field_name' %s value" % (conf['from_field_name'])
                        data = {"field_write_configuration_id": conf['field_write_configuration_id'], }
                        self.log({"success": False,
                                  "message": message,
                                  "system_id": system_id,
                                  "active_directory_user_id": user['active_directory_user_id'],
                                  "data_1": SyncUtils.strigify(data),
                                  "data_2": str(e)})
            result = self.build_nested(config_dict)
        return result

    def apply_mapping_configuration(self, system_id, user, prepared_data):
        time, result = SyncUtils.mesure(lambda: self.transform(system_id, user, prepared_data))
        self.log({"message": "Data transformed to specific json",
                  "data_1": SyncUtils.strigify(result),
                  "success": True,
                  "system_id": system_id,
                  "execution_time": time,
                  "active_directory_user_id": user['active_directory_user_id']})
        return result
