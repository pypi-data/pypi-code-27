from django.db.models import Func, F, Value


def db_replace(field_name, old, new=''):
    """
    Replace value in database, use it with amend or update.
    :param field_name: string
    :param old: string
    :param new: string
    :return: Func object
    :example: SomeModel.objects.all().update(some_field=db_replace('some_field', 'value1', 'supervalue1'))
    """
    return Func(F(field_name), Value(old), Value(new), function='replace')
