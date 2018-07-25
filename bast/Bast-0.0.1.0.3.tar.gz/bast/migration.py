import os
import subprocess
import sys
from configparser import ConfigParser

from orator.database_manager import DatabaseManager
from orator.migrations import MigrationCreator, Migrator, DatabaseMigrationRepository


class CreateMigration(MigrationCreator):
    def __init__(self):
        self.path = os.path.abspath('.') + '/database/migrations/'
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def create_file(self, name, table, create=True):
        return self.create(name, self.path, table=table, create=create)


class Migration(Migrator):
    def __init__(self):
        db_name, config = self.get_config()
        self.manager = DatabaseManager(config=config)
        self.path = os.path.abspath('.') + "/database/migrations/"
        self.repository = DatabaseMigrationRepository(resolver=self.manager, table='migrations')

        if not self.repository.repository_exists():
            self.repository.create_repository()

        super().__init__(self.repository, self.manager)

    def run_(self, pretend):
        self.run(self.path, pretend=pretend)

    def reset_(self, pretend):
        self.reset(self.path, pretend)

    def rollback_(self, pretend):
        return self.rollback(self.path, pretend)

    def reset_(self, pretend):
        return self.reset(self.path, pretend)

    @staticmethod
    def get_config():
        path = os.path.abspath('.') + '/config/config.ini'
        config = ConfigParser()
        config.read(path)

        db_type = config['CONFIG']['DB_TYPE']
        db_host = config['CONFIG']['DB_HOST']
        db_user = config['CONFIG']['DB_USER']
        db_database = config['CONFIG']['DB_NAME']
        db_password = config['CONFIG']['DB_PASSWORD']
        db_prefix = config['CONFIG']['DB_PREFIX']

        Migration.check_packages(db_type)

        return db_database, {
            db_type: {
                'driver': db_type.strip(),
                'host': db_host.strip(),
                'database': db_database.strip(),
                'user': db_user.strip(),
                'password': db_password.strip(),
                'prefix': db_prefix.strip()
            }
        }

    @staticmethod
    def check_packages(db_name):
        print('Checking for required Database Driver')

        reqs = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'])
        installed_packages = [r.decode().split('==')[0] for r in reqs.split()]

        if db_name.lower() == 'mysql':
            if 'pymysql' not in installed_packages:
                print('Installing required Database Driver')
                os.system('pip install pymysql')

        if db_name.lower() == 'postgresql':
            if 'psycopg2' not in installed_packages:
                print('Installing required Database Driver')
                os.system('pip install psycopg2')
