import os
from ipywidgets import widgets, Layout, HBox

# widgets
xnatserver = widgets.Text(description="XNAT SERVER", tooltip='URL to XNAT', value='', width=200)
prjid = widgets.Text(
    description="PRJID",
    tooltip='Leave this empty when defining non-project dicom dir',
    value='PRJ1607_TEPT',
    width=200,
    layout=Layout(disabled='disabled')
)
dicomdir = widgets.Text(description="DICOM DIR", value='', width=200, layout=Layout(width='70%'))
subject    = widgets.Text(description="SUBJECT ID (prefix)", value='S', width=200)

# event handling
def on_change(b):
    dicomdir.value = ""

prjid.observe(on_change,names='value')
on_change(None)

def update_ss(b):
    p = dicomdir.value
    ss = [(x, os.path.join(p,x)) for x in sorted(os.listdir(p), reverse=True) if x.startswith(subject.value) and os.path.isdir(os.path.join(p,x))]
    selectedss.options = dict(ss)

subjbutton = widgets.Button(
    description='List subject matches',
    disabled=False,
    button_style='', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='',
    icon='refresh',
    layout=Layout(width='30%'),
)
subjbutton.on_click(update_ss)

selectedss = widgets.SelectMultiple(
    options=[],
    value=[],
    #rows=10,
    description='Subjects to send',
    disabled=False,
    layout={'height': '200px'}
)
subject.observe(update_ss,names='value')
    
login    = widgets.Text(description="XNAT login", value='', width=200)
password = widgets.Password(description="PASSWORD", value='', width=200)

sendbutton = widgets.Button(
    description='Send to XNAT',
    disabled=False,
    button_style='warning', # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Sends selected subjects to xnat',
    icon='check',
    layout=Layout(width='30%')
)

def on_send_clicked(b):
    ss_fp = [(k,v) for k,v in selectedss.options.items() if v in selectedss.value]
    print("Sending to XNAT")
    print(ss_fp)
    print(prjid.value)
    print(login.value)
    #send_to_xnat(ss_fp, xnatserver.value, prjid.value, login.value, password.value)
    #send_logs_to_xnat(ss_fp, xnatserver.value, prjid.value, login.value, password.value)
    
sendbutton.on_click(on_send_clicked)

# display
def display_form():
    display(xnatserver)
    display(prjid)
    display(dicomdir)
    display(subject)
    display(subjbutton)
    display(selectedss)
    display(HBox([login, password]))
    display(sendbutton)