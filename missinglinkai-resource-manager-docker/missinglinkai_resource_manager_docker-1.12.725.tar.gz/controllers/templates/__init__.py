import os

from jinja2 import Environment, FileSystemLoader
from mlcrypto import Asymmetric

cur_path = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(cur_path))


def render(name, **kwargs):
    template = env.get_template(name)
    result = template.render(**kwargs)
    return result


def build_user_command(
        command=None, commands=None, ssh_identity_pub_b64=None,
        ssh_identity_b64=None, mali_data_b64=None,
        mali_file_name=None, requirements_txt_path=None):
    bootstrap_data = render(
        'machine_bootstrap.sh.jinja2',
        command=command, commands=commands, ssh_identity_pub=ssh_identity_pub_b64,
        ssh_identity=ssh_identity_b64, mali_data=mali_data_b64,
        mali_file=mali_file_name, requirements_txt=requirements_txt_path)
    return Asymmetric.bytes_to_b64str(bootstrap_data)
