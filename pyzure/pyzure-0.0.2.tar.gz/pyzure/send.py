# -*- coding: utf-8 -*-
from pyzure.connection import connect
from pyzure.execute import execute_query
from . import create
from . import azure_credentials


def send_to_azure(instance, data, replace=True, batch_size=1000, types=None, primary_key=(), create_boolean=False):
    """
    data = {
        "table_name" 	: 'name_of_the_azure_schema' + '.' + 'name_of_the_azure_table' #Must already exist,
        "columns_name" 	: [first_column_name,second_column_name,...,last_column_name],
        "rows"		: [[first_raw_value,second_raw_value,...,last_raw_value],...]
    }
    """

    if (not create.existing_test(instance, data["table_name"])) or (types is not None) or (primary_key != ()):
        create_boolean = True

    if create_boolean:
        create.create_table(instance, data, primary_key, types)

    print("Initiate send_to_azure...")

    if replace:
        cleaning_request = '''DELETE FROM ''' + data["table_name"] + ''';'''
        print("Cleaning")
        execute_query(instance, cleaning_request)
        print("Cleaning Done")

    # cnxn = connect(instance)
    # cursor = cnxn.cursor()

    boolean = True
    index = 0
    while boolean:
        temp_row = []
        for i in range(batch_size):
            if not data["rows"]:
                boolean = False
                continue
            temp_row.append(data["rows"].pop())

        final_data = []
        for x in temp_row:
            for y in x:
                final_data.append(y)

        temp_string = ','.join(map(lambda a: '(' + ','.join(map(lambda b: '?', a)) + ')', tuple(temp_row)))

        inserting_request = '''INSERT INTO ''' + data["table_name"] + ''' (''' + ", ".join(
            data["columns_name"]) + ''') VALUES ''' + temp_string + ''';'''
        if final_data:
            print("Execute")
            execute_query(instance, inserting_request,final_data)
        index = index + 1
        print(index)
    # cnxn.commit()
    #
    # cursor.close()
    # cnxn.close()

    print("data sent to azure")
    return 0


def test():
    data = {
        "table_name": 'test.test2',
        "columns_name": ["nom", "prenom", "age", "date"],
        "rows": [["pif", "pif", 12, "2017-02-23"]]
    }
    primary_key = ()

    types = None
    send_to_azure(
        "MH_TEST",
        data,
        types=types,
        primary_key=primary_key,
        create_boolean=False,
        replace=True,
        batch_size=1000
    )
