from cloudcix.client import Client


class Scheduler:
    """
    Scheduler is an application that allows the User to create recurring
    transactions. A recurring transaction is a transaction that will be
    recreated one or several times according to the rules the User gives.
    """
    _application_name = 'Scheduler'

    execute_task = Client(
        application=_application_name,
        service_uri='Task/{idTask}/execute/',
    )
    task = Client(
        application=_application_name,
        service_uri='Task/',
    )
    task_log = Client(
        application=_application_name,
        service_uri='TaskLog/',
    )
