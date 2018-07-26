from pyzure.azure_credentials import credential
import pyodbc


def connect(instance):
    credentials = credential(instance)
    driver = credentials.get("driver")
    server = credentials.get("server")
    port = credentials.get("port")
    database = credentials.get("database")
    username = credentials.get("username")
    password = credentials.get("password")

    cnxn = pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=' + port + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

    return cnxn

