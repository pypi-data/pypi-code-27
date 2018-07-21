from pygments.token import Token
from prompt_toolkit.layout.containers import Window
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.controls import TokenListControl

def clear(layout, default_layout):
    layout.children.clear()
    layout.children.extend(default_layout)

def add_header(layout, max_desc_len):
    # setup screen layout
    layout.children.extend([
        Window(
            height=D.exact(1),
            content=TokenListControl(lambda cli: get_hostdata_header(max_desc_len, upper=True))
        ),
        Window(
            height=D.exact(1),
            content=TokenListControl(lambda cli: get_hostdata_header(max_desc_len, lower=True))
        )
    ])

def add_line_of_data(layout, hostdata):
    hostdatatokens = HostdataTokens(hostdata)
    layout.children.append(
        Window(
            height=D.exact(1),
            content=TokenListControl(hostdatatokens)
        )
    )

def get_hostdata_header(max_desc_len, upper=False, lower=False, line=False):
    if upper:
        return [
            (Token.Header.Bold, ' '.ljust(max_desc_len, " ")),
            (Token.Header.Bold, '          ──── Minute ────  ───── Hour ─────  ───── Total ────')
        ]
    elif lower:
        return [
            (Token.Header.Bold, 'Hosts '.ljust(max_desc_len, " ")),
            (Token.Header.Bold, '  Now     Avg.  Max.  Err.  Avg.  Max.  Err.  Avg.  Max.  Err.')
        ]
    elif line:
        return [
            (Token.Header.Normal, ''.ljust(max_desc_len, "─")),
            (Token.Header.Normal, '    ────  ────────────────  ────────────────  ────────────────')
        ]

class HostdataTokens():
    def __init__(self, hostdata):
        self.hostdata = hostdata
        self.tokenlist = []

    def __call__(self, cli):
        # tokenlist expect a callable
        self.update_tokenlist()
        return self.tokenlist

    def update_tokenlist(self):
        host = self.hostdata.host
        desc = self.hostdata.desc
        last_value = self.hostdata.last_value

        if last_value is None:
            # at startup only hostname is visible in list
            self.tokenlist.extend([(Token.Host, host), (Token.Desc, desc)])
            return

        max_desc_len = self.hostdata.max_desc_len
        desc_len = self.hostdata.desc_len
        fault_limit = self.hostdata.fault_limit
        warning_limit = self.hostdata.warning_limit

        minute_avg = self.hostdata.minute.avg
        minute_max = self.hostdata.minute.max
        minute_err = self.hostdata.minute.err
        hour_avg = self.hostdata.hour.avg
        hour_max = self.hostdata.hour.max
        hour_err = self.hostdata.hour.err
        total_avg = self.hostdata.total.avg
        total_max = self.hostdata.total.max
        total_err = self.hostdata.total.err

        # use clear and extend to preserve object-id
        self.tokenlist.clear()
        self.tokenlist.extend([
            (Token.Host, host),
            (Token.Desc, desc),
            (Token.Desc, " " * (2 + max_desc_len - desc_len)),
            self.format_value(last_value, "{:<8.0f}", fault_limit, warning_limit),
            self.format_value(minute_avg, "{:<6.0f}", fault_limit, warning_limit),
            self.format_value(minute_max, "{:<6.0f}", fault_limit, warning_limit),
            self.format_value(minute_err, "{:<6d}", fault_limit=1, warning_limit=2),
            self.format_value(hour_avg, "{:<6.0f}", fault_limit, warning_limit),
            self.format_value(hour_max, "{:<6.0f}", fault_limit, warning_limit),
            self.format_value(hour_err, "{:<6d}", fault_limit=1, warning_limit=2),
            self.format_value(total_avg, "{:<6.0f}", fault_limit, warning_limit),
            self.format_value(total_max, "{:<6.0f}", fault_limit, warning_limit),
            self.format_value(total_err, "{:<3d}", fault_limit=1, warning_limit=2)
        ])

    @staticmethod
    def format_value(value, formatstr, fault_limit, warning_limit):
        if value >= fault_limit:
            token = Token.Fault
        elif value >=warning_limit:
            token = Token.Warning
        else:
            token = Token.Normal

        return token, formatstr.format(value)
