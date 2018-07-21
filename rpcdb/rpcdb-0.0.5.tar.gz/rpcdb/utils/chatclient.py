from tkinter import *
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
import sys

from socket import *
import time
from datetime import datetime
import threading
import os

now = datetime.now()
localetime = now.strftime("%I: %M: %S %p")
localetime = bytes(localetime.encode('utf-8'))

base = os.path.dirname(os.path.abspath(__file__))


class Client:
    def __init__(self, server, parent=None):
        self.server = server
        self.parent = parent
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.sock.bind(('0.0.0.0', 0))
        self.sock.setblocking(0)

        self.shutdown = False
        self.lock = threading.Lock()

    def receiving(self):
        while not self.shutdown:
            while True:
                with self.lock:
                    try:
                        data, addr = self.sock.recvfrom(1024)
                        self.parent.outPut.configure(state=NORMAL)
                        data = data.decode()
                        self.parent.outPut.insert(END, data)
                        self.parent.outPut.configure(state=DISABLED)
                        self.parent.outPut.yview(END)

                    except BlockingIOError:
                        pass
                    except:
                        sys.exit(0)

    def sending(self, *args):
        name = bytes(self.parent.name.encode('utf-8'))
        text = self.parent.inPut.get('1.0', END)
        data = bytes(text.encode('utf-8'))
        msg = b'(' + name + b') @' + localetime + b"\n" + data
        self.sock.sendto(msg, self.server)
        self.parent.inPut.delete("1.0", END)

    def close(self):
        msg = b"OFFLINE " + bytes(str(self.parent.name).encode('utf-8'))
        self.sock.sendto(msg, self.server)
        self.sock.close()

    def init_server(self, msg):
        self.sock.sendto(msg, self.server)


class ChatClient:
    def __init__(self, parent, host, port):
        self.parent = parent
        self.parent.title("eChat")
        self.parent.resizable(0,0)
        self.host = host
        self.port  = int(port)


        self.entries = dict()
        self.client = None

        self.dlg = Toplevel()
        self.dlg.configure(background='powderblue')
        self.dlg.geometry('320x150')
        self.dlg.iconposition(100, 10)
        try:
            self.dlg.iconbitmap(os.path.abspath(os.path.join(base, 'comp.ico')))
        except:
            pass
        self.dlg.resizable(0, 0)
        self.dlg.transient()
        self.parent.withdraw()
        self.parent.protocol("WM_DELETE_WINDOW", self.close)
        self.parent.configure(bg='powderblue', padx=5)

        label = Label(self.dlg, 
            text='Enter your name & Connect to chat', 
            font='Consolas 12', fg='blue', bg='powderblue')
        label.grid(row=0, column=0, columnspan=2, pady=8)

        label = Label(self.dlg, text="NAME", font='Arial 16', bg='powderblue')
        self.name = ttk.Entry(self.dlg, width=25)
        label.grid(row=1, column=0)
        self.name.grid(row=1, column=1)
        self.name.configure(font='Consolas 12')

        self.dlg.bind("<Return>", self.connect)

        connect = ttk.Button(self.dlg, text="Connect", command=self.connect)
        connect.grid(row=3, column=1, columnspan=2, pady=10, sticky='e')


    def connect(self, event=None):
        name = self.name.get()
        self.name = name

        if name:
            # Start Receiving from server
            self.client = Client((self.host, self.port), self)
            rt = threading.Thread(target=self.client.receiving, daemon=True)
            rt.start()

            # Create Interface
            self.interface()
            name = bytes(name.encode('utf-8'))
            msg = b"USERNAME"

            self.dlg.destroy()
            self.parent.deiconify()

            # Sends Names
            self.client.init_server(msg + b" " + name)


    def interface(self):
        top = Frame(self.parent, background='powderblue')
        top.pack()

        self.outPut = ScrolledText(top, font='Calibri 14',
                                   wrap=WORD, width=60, height=15)
        self.outPut.pack(pady=10)

        bottom = Frame(self.parent, background='powderblue', relief='sunken')
        bottom.pack()

        self.inPut = ScrolledText(bottom, font='Calibri 14',wrap=WORD, width=60, height=3)
        self.inPut.pack(pady=5)

        frm = Frame(bottom, bg='powderblue')
        frm.pack(fill=X)

        self.var = IntVar()
        check = Checkbutton(frm, text = '*Send message when I press Enter on Keyboard', 
            font='Consolas 14')
        check.pack(side=LEFT)
        check.config(bg='powderblue', variable=self.var, command = self.onEnterToggle)
        self.var.set(1)

        send = Button(frm, text=" SEND >>", command=self.client.sending, fg='green', cursor='hand2')
        send.pack(side=RIGHT, padx=2)
        send.configure(font='Consolas 14')
        self.onEnterToggle()

    def onEnterToggle(self):
        ON = self.var.get()
        if ON:
            self.inPut.bind("<KeyRelease-Return>", self.client.sending)
        else:
            self.inPut.unbind("<KeyRelease-Return>")

    def close(self):
        self.parent.destroy()
        if self.client:
            self.client.close()


def run(host, port):
    root = Tk()
    try:
        root.iconbitmap(os.path.abspath(os.path.join(base, 'comp.ico')))
    except:
        pass
    cli = ChatClient(root, host, port)
    root.mainloop()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='IP Address of the server')
    parser.add_argument('port', help='Port', type=int)

    args = parser.parse_args()
    run(args.host, args.port)
