# -*- coding: utf-8 -*-

from uiutil.tk_names import ttk, HORIZONTAL, EW
from uiutil.helper.arguments import COLUMN_SPAN, ROW_SPAN, COLUMN, ROW, Position
from .base_widget import BaseWidget


class Separator(BaseWidget):
    WIDGET = ttk.Separator
    STYLE = u"TSeparator"
    VAR_PARAM = None
    VAR_TYPE = None

    def __init__(self,
                 orient=HORIZONTAL,
                 sticky=EW,
                 padx=5,
                 pady=5,
                 *args,
                 **kwargs):
        """
        If orient is HORIZONTAL (default):
            The separator is placed on the next row automatically.
            The separator spans all columns configured automatically,
            If more columns are added later, or you want to span fewer
            columns, you should supply columnspan.
        If orient is VERTICAL:
            The separator is placed on the next column automatically.
            The separator spans all rows configured automatically,
            If more rows are added later, or you want to span fewer
            rows, you should supply rowspan.

        :param args: 
        :param kwargs: 
        """
        span_arg, vector = (COLUMN_SPAN, ROW) if orient == HORIZONTAL else (ROW_SPAN, COLUMN)

        kwargs[span_arg] = kwargs.get(span_arg, Position.MAX)
        kwargs[vector] = kwargs.get(vector, Position.NEXT)

        super(Separator, self).__init__(orient=orient,
                                        sticky=sticky,
                                        padx=padx,
                                        pady=pady,
                                        *args,
                                        **kwargs)
