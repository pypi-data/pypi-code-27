from chp.mdc import Grid, Row
from chp.django import Form


def F(name, *children, **kwargs):
    return chp.Checkbox(
        kwargs['form'].cleaned_data.get(name, None),
        kwargs['form'].fields[name].errors,
    )
