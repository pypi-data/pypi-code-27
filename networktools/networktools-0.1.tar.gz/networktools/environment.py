import os

def get_env_variable(var_name):
    #print(var_name)
    try:
        return os.environ[var_name]
    except Exception as exec:
        error_msg = "Set the %s environment variable" % var_name
        raise exec

