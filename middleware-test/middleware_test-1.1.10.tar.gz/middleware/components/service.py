import timeit

import jsonpath_rw

from middleware.model import Log, FieldReadConfiguration


class SyncUtils:
    @staticmethod
    def mesure(function):
        start_time = timeit.default_timer()
        result = function()
        return (timeit.default_timer() - start_time) * 1000, result

    @staticmethod
    def strigify(dictionary):
        import json
        return json.dumps(dictionary, default=lambda obj: obj.isoformat() if hasattr(obj, "isoformat") else obj)


class BaseComponent:
    def __init__(self, sync_id, component_info):
        self.sync_id = sync_id
        component_info.update({'sync_id': sync_id, 'component_name': self.__class__.__name__})
        self.component_info = component_info

    def merge_with_component_info(self, args):
        return dict(args.items() + self.component_info.items())

    def log(self, args):
        Log.add_log(**self.merge_with_component_info(args))


class GetInternalModel(BaseComponent):
    def __init__(self, sync_id, active_directory_user_id):
        BaseComponent.__init__(self, sync_id, {'component_id': 3, 'active_directory_user_id': active_directory_user_id})

    @staticmethod
    def find_value(js, from_path):
        # In database we have '$.' at begin of 'from path' field. For example '$.real_name'. We need it without '$.'
        jpath = from_path[2:]
        path = jsonpath_rw.parse(jpath)
        matches = path.find(js)
        return matches[0].value

    def transform(self, system_id, json):
        result = {}
        configurations = FieldReadConfiguration.get_configurations_by_system(system_id=system_id)
        for conf in configurations:
            try:
                value = self.find_value(json, conf['from_path'])
                result[conf['to_field_name']] = value
            except Exception as e:
                message = "incorrect 'from_path' %s value" % (conf['from_path'])
                data = {"field_read_configuration_id": conf['field_read_configuration_id'], }
                self.log({"success": False,
                          "message": message,
                          "system_id": system_id,
                          "data_1": SyncUtils.strigify(data),
                          "data_2": str(e)})
        return result

    def apply_mapping_configuration(self, map):
        result = []
        for system_id, json in map.iteritems():
            dictionary = self.transform(system_id, json)
            if dictionary:
                result.append({'system_id': system_id, 'dictionary': dictionary})
        return result

    def get_model(self, cfg):
        time, result = SyncUtils.mesure(lambda: self.apply_mapping_configuration(cfg))
        self.log({"success": True,
                  "message": "Internal model obtained",
                  "data_1": SyncUtils.strigify(cfg),
                  "data_2": SyncUtils.strigify(result),
                  "execution_time": time})
        return result
