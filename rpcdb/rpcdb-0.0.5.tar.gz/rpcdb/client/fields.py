from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from tkinter import font
from tkinter.scrolledtext import ScrolledText
from tkinter import constants
from collections import OrderedDict
from calwidget import DateField, DateTimeField
from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import pyautogui
import ast
import decimal


def compute_age(dob, deceased=False, dod=""):
    today = datetime.today().date()
    dob = dob.replace("/", "-")
    try:
        start = datetime.strptime(str(dob), '%Y-%m-%d')
    except ValueError:
        return ("", "", "")

    end = datetime.strptime(str(today),'%Y-%m-%d')
    if deceased and dod:
        end = datetime.strptime(str(dod), '%Y-%m-%d %H:%M')

    rdelta = relativedelta(end, start)

    years = rdelta.years
    months= rdelta.months
    days= rdelta.days
    return (years, months, days)


class TextField(ScrolledText):
    def __init__(self, parent,  *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            borderwidth=2,
            wrap = WORD,
            padx=4, pady=4, 
            width=40,
            height=4)

    def insert(self, index=None, val=None):
        super().insert("1.0", val)

    def get(self, index=None, end=None):
        return super().get('1.0', 'end')

    def delete(self, index, end):
        super().delete("1.0", 'end')


class LongTextField(TextField):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.configure(
            borderwidth=2,wrap = WORD,
            padx=4, pady=4, 
            width=40, height=12
            )

class EntryField(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(width=40)


class IntegerField(ttk.Entry):
    ty = int
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.bind("<KeyRelease>", self.validate)

    def get(self):
        value = super().get()
        if value:
            val = self.ty(value)
            return val


    def validate(self, e):
        value = super().get()
        if not value:
            return
        try:
            val = self.ty(value)
        except (ValueError, decimal.InvalidOperation, decimal.InvalidContext):
            showinfo('ValueError', "%s is not of type %s"%(super().get(), self.ty))
            self.focus_set()
            pyautogui.hotkey('BACKSPACE')


class BlobField(ttk.Entry):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(width=40)

    def get(self):
        val = bytes(super().get(), 'utf-8')
        return val

    def insert(self, index, bytes_obj):
        bytes_str = bytes_obj.decode('utf-8')
        super().insert(0, bytes_str)


class DecimalField(IntegerField):
    ty = decimal.Decimal

    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

class FloatField(IntegerField):
    ty = float
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

class BooleanField(IntegerField):
    ty = bool
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)


class DropdownField(ttk.Combobox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.configure(width=38)


    def insert(self, index, value):
        self.set(value)


class AgeField(Frame):
    def __init__(self, parent, **kwargs):
        self.parent = parent
        super(AgeField, self).__init__(parent)

        fields = ('Years', "Months", "Days")
        self.entries = OrderedDict()
    
        for field in fields:
            label = Label(self, text=field)
            ent = ttk.Entry(self, width=13)
            label.pack(side=LEFT, padx=2)
            ent.pack(side=LEFT)
            self.entries[field] = ent
            ent.configure(**kwargs)

    def configure(self, **kwargs):
        try:
            for ent in self.entries.values():
                ent.configure(**kwargs)
        except Exception as e:
            pass

    def get(self):
        try:
            return tuple(ent.get() for ent in self.entries.values())
        except ValueError:
            return (None, None, None)

    def insert(self, age):
        try:
            assert len(age) ==3, 'Age should be in  a tuple of (years, months, days)'
        except AssertionError:
            try:
                age = ast.literal_eval(age)
            except TypeError as e:
                print(e)
        else:
            self.delete()
            self.entries['Years'].insert(0, age[0])
            self.entries['Months'].insert(0, age[1])
            self.entries['Days'].insert(0, age[2])

    def delete(self, *args):
        for ent in self.entries.values():
            ent.delete(0, END)

    @property
    def years(self):
        return int(self.entries['Years'].get())

    @property
    def months(self):
        return int(self.entries['Months'].get())

    @property
    def days(self):
        return int(self.entries['Days'].get())


class FullAgeField(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        super().configure(relief='raised', bd=2)

        f1 = Frame(self)
        f2= Frame(self)        
        label = Label(f1, text="Date Of Birth", font='Consolas 12')
        label.pack(side=LEFT)
        self.dob = DateField(f1, entrywidth=30)
        self.dob.pack(pady=2, padx=2, side=LEFT)
        self.dob.bind("<FocusOut>", self.insert_age)

        self.age = AgeField(f2, font='Consolas 12',width=8)
        self.age.pack(pady=2, side=BOTTOM)
        f1.pack(anchor='w')
        f2.pack()

    def insert_age(self, e):
        self.age.insert(compute_age(self.dob.get()))

    def configure(self, **kwargs):
        try:
            super().configure(**kwargs)
        except:
            pass

    def insert(self, index, val):
        if isinstance(val, str):
            dob, age = ast.literal_eval(val)
        elif isinstance(val, tuple):
            dob, age = val

        self.dob.insert(0, dob)
        self.age.insert(compute_age(dob))
        
    def get(self):
        age = self.age.get()
        dob = self.dob.get()
        return (dob, age)


    def delete(self, ind, to):
        self.age.delete(0, 'end')
        self.dob.delete(0, 'end')


class Diagnosis(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent = parent

        self.entries=OrderedDict()
        self.fields=["Primary Diagnosis",
        "Secondary Diagnosis", "Co-morbidities"]
        for i, field in enumerate(self.fields):
            Label(self, text=field, font="Consolas 14").grid(row=i, column=0, sticky='w')
            entry = ttk.Entry(self, font="Arial 14 bold",width=80)
            entry.grid(row=i, column=1,
                padx=4,pady=2, sticky='ew')
            self.entries[field] = entry

    def get(self):
        DIAGNOSES=[]
        for entry in self.entries.values():
            DIAGNOSES.append(entry.get())
        return DIAGNOSES

    def delete(self,*args):
        [entry.delete(0,'end') for entry in self.entries.values()]

    def insert(self, index, items):
        try:
            items=ast.literal_eval(items)
        except:
            items=["","",""]
        if isinstance(items, list):
            self.entries["Primary Diagnosis"].insert(0, items[0])
            self.entries["Secondary Diagnosis"].insert(0, items[1])
            self.entries["Co-morbidities"].insert(0, items[2])



class BP(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.parent=parent

        self.entries=OrderedDict()
        self.fields=["SBP", "DBP", "MAP"]
        for i, field in enumerate(self.fields):
            Label(self, text=field, font="Consolas 12").pack(side=LEFT)
            entry = ttk.Entry(self, width=5, font="Arial 13 bold")
            entry.pack(side=LEFT, padx=4,pady=2)
            entry.bind("<FocusOut>", self.compute_map)
            self.entries[field] = entry

        self.entries["MAP"].config(state=DISABLED)

    def compute_map(self, event=None):
        try:
            SBP= int(self.entries["SBP"].get())
            DBP= int(self.entries["DBP"].get())
        except ValueError:
            return
        else:
            PULSE_BP = SBP-DBP
            MAP = int(float(DBP) + float(PULSE_BP)/3)
            self.entries["MAP"].config(state=NORMAL)
            self.entries["MAP"].delete(0,"end")
            self.entries["MAP"].insert(0, MAP)
            self.entries["MAP"].config(state=DISABLED)

            self.analyse_BPS(SBP, DBP)

    def analyse_BPS(self, sbp, dbp):
        try:
            assert 90 <sbp<140, "Systolic BP is abnormal"
        except AssertionError as e:
            self.entries["SBP"].config(foreground='red')
        else:
            self.entries["SBP"].config(foreground='green')

        try:
            assert 60 <dbp<90, "Diastolic BP is abnormal"
        except AssertionError as e:
            self.entries["DBP"].config(foreground='red')
        else:
            self.entries["DBP"].config(foreground='green')


    def get(self):
        self.entries["MAP"].config(state=NORMAL)
        BPS=[]
        for entry in self.entries.values():
            BPS.append(entry.get())
        self.entries["MAP"].config(state=DISABLED)
        return BPS

    def delete(self,*args):
        self.entries["MAP"].config(state=NORMAL)
        [entry.delete(0,'end') for entry in self.entries.values()]
        self.entries["MAP"].config(state=DISABLED)

    def insert(self, index, items):
        if isinstance(items, str):
            try:
                items=ast.literal_eval(items)
            except:
                items=["","",""]
        elif isinstance(items, list):
            items=items

        self.entries["SBP"].insert(0, items[0])
        self.entries["DBP"].insert(0, items[1])
        self.entries["MAP"].config(state=NORMAL)
        self.entries["MAP"].insert(0, items[2])
        self.compute_map()
        self.entries["MAP"].config(state=DISABLED)



class GUIFramework(object):

    def __init__(self, root, menuitems=None):
        self.root = root
        self.menuitems = menuitems
        self.build_menu()

    def build_menu(self):
        if not hasattr(self, 'menuitems'):
            raise AttributeError("Define a list/tuple of menuitems in your class."
                " Use format method for sample data")

        self.menubar = Menu(self.root)
        for v in self.menuitems:
            menu = Menu(self.menubar, tearoff=0)
            label, items = v.split('-')
            items = map(str.strip, items.split(','))
            for item in items:
                self.__add_menu_command(menu, item)
            self.menubar.add_cascade(label=label, menu=menu)
        self.root.config(menu=self.menubar)
        
    def __add_menu_command(self, menu, item):
        if item == 'Sep':
            menu.add_separator()
        else:
            name, acc, cmd = item.split('/')
            try:
                underline = name.index('&')
                name = name.replace('&', '', 1)
            except ValueError:
                underline = None
            menu.add_command(label=name, underline=underline,
                            accelerator=acc, command=eval(cmd))

    def format(self):
        menuitems=(
        """
        Database- &Clear/Ctrl+N/self.clear, Delete/Ctrl+X/self.delete,
        Update/Ctrl+U/self.update, Sep, Exit/Alt+F4/self.close
        """,

        """
        Find-&Find By ID/Ctrl+F/self.find_by_id""",
        """
        Print- Medical Form//self.print_report, Laboratory Request//self.print_lab_request""",
        """
        View-View Register//self.patient_register, Login Logs//self.view_login_logs""",
        """
        Configurations- Confugure CBC Normal Ranges//self.cbc_normal_ranges,
        General Lab Ref Ranges//self.general_lab_ranges
        """,

        """Preferences- Preferences//self.set_preferences""",
        """Help- View Help//self.help""",
        """About- About Developer//self.about""")

        return menuitems


class SearchEngine(Frame):
    def __init__(self, parent,  headers, iterable_to_search, item_index, onSelectCommand):
        super().__init__(parent)
        self.pack(expand=1, fill=BOTH)

        self.parent = parent
        self.iterable = iterable_to_search
        self.index = item_index
        self.onSelectCommand = onSelectCommand
        self.treeheaders = headers
        self.InitUI()

    def InitUI(self):
        style = ttk.Style()
        style.configure("T.TEntry", foreground="green")
        self.var = StringVar()
        self.ent = ttk.Entry(self, textvariable=self.var, width=40, style='T.TEntry')
        self.ent.configure(font="Calibri 16 bold")
        self.ent.focus()
        self.ent.pack(side='top', fill=Y, pady=2, anchor='w')

        if self.var == '':
            self.var = self.ent["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.TreeUp = False

    def entry_config(self, **kwargs):
        self.ent.configure(**kwargs)

    def set_padding(self, padx=5, pady=5):
        self.ent.pack_configure(padx=padx, pady=pady)

    def changed(self, name, index, mode):

        if self.var.get() == '':
            try:
                self.tree.destroy()
                self.TreeUp = False
            except:
                pass
        else:
            words = self.comparison()
            if words:
                if not self.TreeUp:
                    self.tree = Treeview(self, self.treeheaders, self)
                    self.tree.pack(expand=1, fill=BOTH,padx=5, pady=5)
                    self.tree.bind("<<TreeviewSelect>>", self.selection)
                    self.TreeUp = True
                self.tree.set_register(words)
            else:
                if self.TreeUp:
                    self.tree.destroy()
                    self.TreeUp = False


    def selection(self, event):
        if self.TreeUp:
            current_selection = event.widget.focus()
            selection = event.widget.item(current_selection)['values']
            self.tree.destroy()
            self.onSelectCommand(selection)
            self.TreeUp = False
            try:
                self.ent.delete(0, 'end')
            except TclError:
                pass 

    def match(self, name):
        pat = re.compile(".*{}.*".format(name), re.I|re.M)
        return [item for item in self.iterable if re.match(pat, item[self.index])]

    def comparison(self):
        '''Queries the database and returns dynamically results with each keypress'''
        return self.match(self.var.get())


    def example(self):
        """
        names = [(20, "Abiira Nathan", 'Male'),(22, "Nathan Abiira", 'Female'),(21, 'Kwikiriza Dan', "Male")]

        class MyClass:
            def __init__(self, parent):
                s = SearchEngine(root, ['Age', "Name", "Sex"], names, 1,  self.printer)

            def printer(self, selection, event=None):
                print(selection)

        root = Tk()
        cl = MyClass(root)
        root.mainloop()
        """

class Treeview(ttk.Treeview):
    def __init__(self, parent, headers, instance):
        ttk.Treeview.__init__(self, parent,  columns = headers, show="headings")

        self.vsb = ttk.Scrollbar(parent, orient="vertical", command=self.yview)
        self.hsb = ttk.Scrollbar(parent, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)
        self.vsb.pack(side='right', fill="y", anchor='w')
        self.hsb.pack(side='bottom', fill="x")

        self.parent = parent
        self.headers = headers
        self.current_selection = None
        self.instance = instance

        self.bind("<<TreeviewSelect>>", self.get_selection)
        self._build_tree()

    def set_headers(self, headers):
        self.headers = headers

    def destroy(self):
        super().destroy()
        self.hsb.destroy()
        self.vsb.destroy()

    def set_col_width(self, w):
        for col in self.headers:
            if col=="ID":
                self.column(col, width=50)
            else:
                self.column(col, width=w)

    def _build_tree(self):
        for col in self.headers:
            self.heading(col, text=col, anchor='w', command=lambda c=col: self.sortby(self, c, 0))
            self.column(col, anchor='w')

    def sortby(self, tree, col, descending):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=descending)
        for ix, item in enumerate(data):
            tree.move(item[1], '', ix)
        tree.heading(col, command=lambda col=col: self.sortby(tree, col, int(not descending)))

    def fill_tree(self):
        from collections import Iterable
        if self.register is not None:
            for item in self.register:
                self.insert('', 'end', values=item)
                # adjust column's width if necessary to fit each value
                if isinstance(item, Iterable):
                    for ix, val in enumerate(item):
                        try:
                            col_w = tkFont.Font().measure(val)
                            if self.column(self.headers[ix], width=None) < col_w:
                                self.column(self.headers[ix], width=col_w)
                        except:
                            pass

    def get_selection(self, event=None):
        if event:
            current_selection = event.widget.focus()
            row= self.item(current_selection)['values']
            if hasattr(self.instance, 'onTreeSelect'):
                self.instance.onTreeSelect(row)
            else:
                print("Method onTreeSelect(self, selected_row)\
                    is not defined in class %s"%self.instance.__class__)

    def insert_row(self, row):
        '''Insert a tuple of data to table'''
        self.insert('', 'end', values=row)

    def set_register(self, register):
        '''Updates the treeview with the new register
        >>Register should be a list of tuples
        e.g [(1, "First Name", "Last Name","Sex"), (2, "Second Name", "Third Name", "Male")]'''
        self.register = register
        self.update_tree()

    def update_tree(self):
        '''Clears the treeview and update it with the new register.
        This method should not be called directly but rather
        calling set_register(register) calls update method.
        '''
        self.clear()
        self.fill_tree()
        

    def clear(self):
        '''Deletes all children of the widget'''
        try:
            self.delete(*self.get_children())
        except:
            pass

    def get_all(self):
        """Returns a list of all treeview items"""
        return [item for item in self.get_children()]


class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.x = self.y = 0

    def showtip(self, text):
        self.text = text
        if self.tipwindow or not self.text:
            return

        x, y, _cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 100
        y = y + cy + self.widget.winfo_rooty() +5

        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                        background="#ffffe0", relief=SOLID,
                        borderwidth=1,
                        font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


def showToolTip(widget, text):
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)



class Mapper:
    maps = {
        'INTEGER':IntegerField,
        'CHAR': EntryField,
        'VARCHAR':EntryField,
        'TEXT': TextField,
        'ENUM': DropdownField,
        'DATE': DateField,
        'DATETIME': DateTimeField,
        'AGEFIELD': AgeField,
        'FULLAGEFIELD': FullAgeField,
        'FLOAT': FloatField,
        'BLOB': BlobField,
        'LONGTEXT': LongTextField,
        'DECIMAL': DecimalField,
    }

