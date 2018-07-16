# -*- coding: utf-8 -*-
import pandas as pd










def validate(df,coerce_numeric,coerce_dt,coerce_categorical): # validates input
    assert type(df) is pd.DataFrame
    column_dict = {}
    for element in coerce_numeric + coerce_dt + coerce_categorical: # these lists must be mutually exclusive
        assert type(element) is str
        assert not element in column_dict
        column_dict[element] = True