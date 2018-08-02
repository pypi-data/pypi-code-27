# -*- coding: utf-8 -*-

# python imports
import uuid

from tornado.options import options

from middleware.mysqlmodel import MysqlModel

# project imports


class MiddlewareModel(MysqlModel):
    DATABASE_INSTANCE = options.middleware_db_instance
    DATABASE_GENERATION = "2"
    DATABASE_NAME = options.middleware_db_name
    HOSTNAME = options.middleware_db_ip


class Sync(MiddlewareModel):
    TABLE = 'sync'

    @classmethod
    def add_sync(cls):
        sync_uuid = uuid.uuid4().hex
        with cls.transaction() as cursor:
            cursor.callproc("add_sync", (sync_uuid,))
        return sync_uuid


class SlackUserGroup(MiddlewareModel):
    TABLE = 'slack_user_group'

    @classmethod
    def add_slack_user_group(cls, group_name, active_directory_user_id):
        with cls.transaction() as cursor:
            slack_user_group_id = cursor.callproc("add_slack_user_group", (group_name, active_directory_user_id))
        return slack_user_group_id

    @classmethod
    def get_slack_user_group_name(cls, active_directory_user_id):
        proc_result = cls.call_proc("get_slack_user_group_name", (active_directory_user_id,))
        return proc_result[0]['slack_group_name'] if proc_result else None

    @classmethod
    def update_slack_user_group(cls, group_name, active_directory_user_id):
        with cls.transaction() as cursor:
            slack_user_group_id = cursor.callproc("update_slack_user_group", (group_name, active_directory_user_id))
        return slack_user_group_id

class System(MiddlewareModel):
    TABLE = 'system'

    @classmethod
    def add_system(cls, name, description, sync_enabled):
        system_uuid = uuid.uuid4().hex
        with cls.transaction() as cursor:
            cursor.callproc("add_system", (system_uuid, name, description, sync_enabled))
            return system_uuid

    @classmethod
    def get_system_by_system_id(cls, system_id):
        system = cls.call_proc("get_system_by_system_id", system_id)
        return system[0] if system else None


class ActiveDirectoryUser(MiddlewareModel):
    TABLE = 'active_directory_user'

    @classmethod
    def add_active_directory_user(cls, first_name, last_name, login, email,
                                  metadata):
        active_directory_user_uuid = uuid.uuid4().hex
        with cls.transaction() as cursor:
            cursor.callproc("add_active_directory_user",
                            (active_directory_user_uuid, first_name, last_name, login, email, metadata))
        return active_directory_user_uuid

    @classmethod
    def update_active_directory_user(cls, active_directory_user_id, first_name, last_name, login, email,
                                     metadata):
        with cls.transaction() as cursor:
            cursor.callproc("update_active_directory_user",
                            (active_directory_user_id, first_name, last_name, login, email, metadata))
        return active_directory_user_id

    @classmethod
    def get_user_by_login(cls, login):
        user = cls.call_proc("get_user_by_login", (login,))
        return user[0] if user else None

    @classmethod
    def get_user_by_id(cls, active_directory_user_id):
        user = cls.call_proc("get_user_by_id", (active_directory_user_id,))
        return user[0] if user else None

    @classmethod
    def get_user_by_first_name_last_name(cls, first_name, last_name):
        user = cls.call_proc("get_user_by_first_name_last_name", (first_name, last_name))
        return user[0] if user else None

    @classmethod
    def get_all_users(cls):
        users = cls.call_proc("get_all_users", ())
        return users

    @classmethod
    def delete_active_directory_user(cls, active_directory_user_id):
        with cls.transaction() as cursor:
            return cursor.callproc("delete_active_directory_user",
                                   (active_directory_user_id,))

    @classmethod
    def get_manager(cls, manager_full_name):
        combinations = ActiveDirectoryUser.__create_manager_name_combinations__(manager_full_name)
        for first_name, last_name in combinations:
            manager = cls.get_user_by_first_name_last_name(first_name=first_name, last_name=last_name)
            if manager:
                return manager

        return None

    @staticmethod
    def __create_manager_name_combinations__(manager):
        result = []

        parts = manager.split(' ')
        count = len(parts)
        if count == 1:
            raise RuntimeError("Manager name contains only first_name (without last_name)")
        elif count == 2:
            result.append((parts[0], parts[1]))
        else:
            '''
            for example manager name is:  aaa bbb ccc ddd eee
            then possible combinations are:

            aaa --- bbb ccc ddd eee
            aaa bbb --- ccc ddd eee
            aaa bbb ccc --- ddd eee
            aaa bbb ccc ddd --- eee
            '''

            for position in range(count - 1):
                shift = position + 1
                result.append((' '.join(parts[:shift]), ' '.join(parts[shift:])))

        return result


class Log(MiddlewareModel):
    TABLE = 'log'

    @classmethod
    def add_log(cls, system_id=None, sync_id=None, data_1=None, data_2=None, data_3=None, data_4=None, data_5=None,
                success=None, message=None, operation=None, active_directory_user_id=None, execution_time=None,
                component_id=None, component_name=None):
        with cls.transaction() as cursor:
            return cursor.callproc("add_log",
                                   (sync_id, component_id, component_name, data_1, data_2,
                                    data_3, data_4, data_5,
                                    success, message, operation, system_id, active_directory_user_id, execution_time
                                    ))

    @classmethod
    def delete_logs(cls, days):
        with cls.transaction() as cursor:
            return cursor.callproc("delete_logs", (days,))


class FieldReadConfiguration(MiddlewareModel):
    TABLE = 'field_read_configuration'

    @classmethod
    def get_configurations_by_system(cls, system_id):
        return cls.call_proc("get_field_read_configuration_by_system", (system_id, 1))


class ActualUserData(MiddlewareModel):
    TABLE = 'actual_user_data'

    @classmethod
    def add_actual_user_data(cls, active_directory_user_id, data):
        actual_user_data_uuid = uuid.uuid4().hex
        with cls.transaction() as cursor:
            cursor.callproc("add_actual_user_data",
                            (actual_user_data_uuid, active_directory_user_id, data))
        return actual_user_data_uuid

    @classmethod
    def update_actual_user_data(cls, actual_user_data_id, active_directory_user_id, data):
        with cls.transaction() as cursor:
            cursor.callproc("update_actual_user_data",
                            (actual_user_data_id, active_directory_user_id, data))
        return actual_user_data_id

    @classmethod
    def get_actual_user_by_ad_user_id(cls, active_directory_user_id):
        result = cls.call_proc("get_actual_user_data", (active_directory_user_id,))
        return result[0] if result else None


class FieldWriteConfiguration(MiddlewareModel):
    TABLE = 'field_write_configuration'

    @classmethod
    def get_configurations_by_system(cls, system_id):
        return cls.call_proc("get_field_write_configuration_by_system", (system_id, 1))


class WriteForbiddenField(MiddlewareModel):
    TABLE = 'write_forbidden_field'

    @classmethod
    def get_forbidden_fields_by_system(cls, system_id):
        return cls.call_proc("get_write_forbidden_field_by_system", (system_id))


class WriteRequiredField(MiddlewareModel):
    TABLE = 'write_required_field'

    @classmethod
    def get_required_fields_by_system(cls, system_id):
        return cls.call_proc("get_write_required_field_by_system", (system_id))


class WriteEmptyFieldByUser(MiddlewareModel):
    TABLE = 'write_empty_field_by_user'

    @classmethod
    def get_write_empty_field_by_user_by_system(cls, system_id, user_email):
        return cls.call_proc("get_write_empty_field_by_user_by_system", (system_id, user_email))


class UserFieldChange(MiddlewareModel):
    TABLE = 'user_field_change'

    @classmethod
    def add_user_field_change(cls, sync_id, system, field_name, active_directory_user_id, first_name, last_name,
                              user_email, old_value, changed_to):
        user_field_change_id = uuid.uuid4().hex
        with cls.transaction() as cursor:
            cursor.callproc("add_user_field_change",
                            (user_field_change_id, sync_id, system, field_name, active_directory_user_id, first_name,
                             last_name, user_email, old_value, changed_to))

    @classmethod
    def get_user_field_change_by_date(cls, date):
        return cls.call_proc("get_user_field_change_by_date", (date,))

    @classmethod
    def get_user_field_change_by_date_email(cls, date, email):
        return cls.call_proc("get_user_field_change_by_date_email", (date, email))

    @classmethod
    def get_user_field_change_by_date_email_system(cls, date, email, system):
        return cls.call_proc("get_user_field_change_by_date_email_system", (date, email, system))

    @classmethod
    def get_user_field_change_by_date_system(cls, date, system):
        return cls.call_proc("get_user_field_change_by_date_system", (date, system))
