import datetime

from tornado.options import options

import config
import model

config.initialize()


class Report:
    def __init__(self, date=None, email=None, system=None):
        self.date = date if date else datetime.date.today().strftime('%Y-%m-%d')
        self.email = email
        self.system = system

    def write_csv(self, filename, data):
        import csv
        try:
            with open(filename, 'w') as csvfile:
                fieldnames = ['ACTIVE DIRECTORY USER ID', 'FIRST NAME', 'LAST NAME', 'EMAIL', 'FIELD', 'SYSTEM',
                              'OLD VALUE', 'CHANGED TO', 'SYNC ID', 'DATE']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', dialect='excel',
                                        lineterminator='\n')

                writer.writeheader()
                for row in data:
                    writer.writerow({'ACTIVE DIRECTORY USER ID': row['active_directory_user_id'],
                                     'FIRST NAME': row['first_name'], 'LAST NAME': row['last_name'],
                                     'EMAIL': row['user_email'], 'FIELD': row['field_name'],
                                     'SYSTEM': row['system'], 'OLD VALUE': row['old_value'],
                                     'CHANGED TO': row['changed_to'],
                                     'SYNC ID': row['sync_id'], 'DATE': row['create_dttm']})
        except Exception as e:
            args = {"message": "Error in generating report", "operation": "report generation", "success": False,
                    "data_1": str(e)}
            model.Log.add_log(**args)
            raise e
        else:
            args = {"message": "Report was successfully added", "operation": "report generation", "success": True}
            model.Log.add_log(**args)

    def make_report(self):
        if self.date and self.email and self.system:
            field_changes = model.UserFieldChange.get_user_field_change_by_date_email_system(date=self.date,
                                                                                             email=self.email,
                                                                                             system=self.system)
        elif self.date and self.system:
            field_changes = model.UserFieldChange.get_user_field_change_by_date_system(date=self.date,
                                                                                       system=self.system)
        elif self.date and self.email:
            field_changes = model.UserFieldChange.get_user_field_change_by_date_email(date=self.date, email=self.email)
        else:
            field_changes = model.UserFieldChange.get_user_field_change_by_date(date=self.date)
        filename = '{}{}--{}--{}.csv'.format(options.csv_path, self.date, self.email, self.system)
        self.write_csv(filename, field_changes)
