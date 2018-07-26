'''
Excep Helper class to generate an excel list for the parameters
'''
import xlsxwriter
import datetime
import operator

class ExcelHelper(object):
    """docstring for ExcelHelper.
    """

    def __init__(self):
        """Initializer

        Args:
            N/A

        Returns:
            N/A

        """
        super(ExcelHelper, self).__init__()

    def create(self, args):
        '''Create an excel file with the data in it

        Args:
            N/A

        Returns:
            list
        '''
        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook("./data/ecs-auditor-{}.xlsx".format(datetime.datetime.now()))
        worksheet = workbook.add_worksheet()
        title_cell_format = workbook.add_format({'bold': True, 'font_color': 'red', 'font_size': '16'})
        entry_wrapping = workbook.add_format({'align': 'top'})
        cell_wrapping = workbook.add_format({'text_wrap': True, 'align': 'top'})

        row = 1

        for cluster in args:
            if 'services' not in cluster: continue

            print "*--------------------------------*"
            print "Writing to excel for {} {}".format(cluster['region'], cluster['env'])
            print "*--------------------------------*"
            cluster['services'].sort(key=operator.itemgetter('name'))
            for service in cluster['services']:
                col = 0

                for (key, value) in (service).iteritems():
                    # print key on row above
                    worksheet.set_column(col, col, 25)
                    key = key.replace('_', ' ').title()
                    worksheet.write(0, col, key, title_cell_format)

                    # print value row below
                    if isinstance(value, dict):
                        dict_data = ""
                        for i, (j, k) in enumerate((value).iteritems()):
                            dict_data += "{}={}".format(j, k)
                            if i != len(value)-1:
                                dict_data += "\n"
                        worksheet.write(row, col, dict_data, cell_wrapping)
                    else:
                        worksheet.write(row, col, value, entry_wrapping)
                        col += 1
                row += 1

        workbook.close()
