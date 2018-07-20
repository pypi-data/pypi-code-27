#!/usr/bin/python3
from PyQt5 import QtDBus
import sys


def main():
    bus = QtDBus.QDBusConnection.sessionBus()
    interface = QtDBus.QDBusInterface("org.qtpad.session", "/org/qtpad/session", "org.qtpad.session", bus)
    cmd = "%".join(str(arg) for arg in sys.argv[1:])

    # Pass the arguments to the existing bus
    if interface.isValid():
        interface.call("parse", cmd)
        sys.exit(0)

    # Create a new instance
    else:
        try:
            import qtpad.mother as qtpad
        except ImportError:
            import mother as qtpad
        qtpad.main(cmd)

if __name__ == '__main__':
    main()
