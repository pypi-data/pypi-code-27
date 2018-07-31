import os
import sys
import base64
import shutil
import argparse
import json

from .tpl.base_tpl import SETTINGS_TPL


class Generator:

    _check = lambda self, x: os.path.exists(x)

    def __init__(self):
        self.project_name = None
        self.BASE_DIR, self.SETTINGS_PATH, self.secret_file = self._get_path()

    def _get_proj_name(self):
        description = (
            "Start generator with your project name\n"
            "in project root dir\n"
            "like: generator <project_name>\n"
        )
        parser = argparse.ArgumentParser(description=description)
        parser.add_argument("project_name", type=str, help="Django project name")
        args = parser.parse_args()
        return args.project_name

    def _get_path(self):
        self.project_name = self._get_proj_name()
        path = os.getcwd()
        base_dir_settings = os.path.join(path, self.project_name)
        if not self._check(os.path.join(base_dir_settings, 'wsgi.py')):
            msg = (
                "***************************************\n"
                "Sorry, project not found!\n"
                "Are you shure that you in PROJECT ROOT?\n"
                "***************************************\n"
            )
            exit(msg)
        settings_path = os.path.join(base_dir_settings, 'settings')
        secret_file = os.path.join(settings_path, 'secrets.json')
        return base_dir_settings, settings_path, secret_file

    def _create_settings(self):
        if self._check(self.SETTINGS_PATH):
            return False
        os.mkdir(self.SETTINGS_PATH)
        TPL_PATH = os.path.join(
                os.path.dirname(
                    os.path.abspath(__file__)), 'tpl')
        TPL = (
            ('init_tpl.py', '__init__.py'),
            ('development_tpl.py', 'development.py'),
            ('production_tpl.py', 'production.py'),
        )
        for file in TPL:
            tpl = os.path.join(TPL_PATH, file[0])
            dist = os.path.join(self.SETTINGS_PATH, file[1])
            try:
                shutil.copy(tpl, dist)
            except FileNotFoundError:
                exit(f'Critical Error: template does not exist > {tpl}')
        self._create_base()
        return True

    def _create_base(self):
        base_path = os.path.join(self.SETTINGS_PATH, 'base.py')
        with open(base_path, 'w') as file:
            file.write(SETTINGS_TPL.format(PROJ_NAME=self.project_name))

    def _create_file(self):
        if self._check(self.secret_file):
            return False
        secrets = {
            'NAME': '',
            'USER': '',
            'PASSWORD': '',
            'SECRET_KEY': base64.b64encode(os.urandom(60)).decode(),
        }
        with open(self.secret_file, 'w') as file:
            json.dump(secrets, file)
        return True

    def _remove_default(self):
        default = os.path.join(self.BASE_DIR, 'settings.py')
        old = os.path.join(self.BASE_DIR, 'settings.old')
        try:
            shutil.move(default, old)
        except FileNotFoundError:
            print('*** File "settings.py" already deleted! ***')

    def handle(self):
        if self._create_settings():
            msg_set = "The settings was created successly."
        else:
            msg_set = "You have already created the settings."
        if self._create_file():
             msg_file = "The secrets.json was created successly."
        else:
            msg_file = "The secrets.json already exists."
        # rename default settings file
        self._remove_default()
        msg = (
            "***************************************************************\n"
            f"{msg_set}\n"
            "***************************************************************\n"
            f"{msg_file}\n"
        )
        print(msg)
