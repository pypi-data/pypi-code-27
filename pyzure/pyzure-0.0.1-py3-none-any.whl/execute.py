import pyodbc

from pyzure.connection import connect


def execute_query(instance, query, data=None):
    cnxn = connect(instance)
    cursor = cnxn.cursor()
    if data:
        print(query)
        print(data)
        cursor.execute(query, data)
        cnxn.commit()
        result = None
    else:
        cursor.execute(query)
        result = []
        try:
            for row in cursor.fetchall():
                result.append(row)
        except pyodbc.ProgrammingError:
            pass
        cnxn.commit()

    cursor.close()
    cnxn.close()

    return result
