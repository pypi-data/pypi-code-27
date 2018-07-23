import os


class Cfg:
    def __init__(self, leo_config):
        self.cfg = self.__by_environment(leo_config)

    def value(self, key: str) -> str:
        config_attr = getattr(self.cfg, key, None)
        return str(config_attr).strip() if self.__is_valid_str(config_attr) else None

    def int_value(self, key: str) -> int:
        config_attr = getattr(self.cfg, key, None)
        return config_attr if self.__is_valid_int(config_attr) else None

    def value_or_else(self, key: str, or_else: str) -> str:
        val = self.value(key)
        return val if val is not None else str(or_else)

    def int_value_or_else(self, key: str, or_else: int) -> int:
        val = self.int_value(key)
        return val if val is not None else or_else

    @staticmethod
    def __by_environment(leo_config):
        env = os.getenv('PYTHON_ENV', 'dev')
        config_attr = getattr(leo_config, env, None)
        if config_attr is not None:
            return config_attr()
        else:
            raise AssertionError("'%s' class is missing in leo_config.py" % env)

    @staticmethod
    def __is_valid_str(val):
        return val is not None and str(val).strip().__len__() > 0

    @staticmethod
    def __is_valid_int(val):
        return val is not None and Cfg.__is_int(val)

    @staticmethod
    def __is_int(val):
        try:
            int(val)
            return True
        except ValueError:
            return False
