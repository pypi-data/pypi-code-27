"""
Package name: PythonToolkit (PTK) engine/console system.
-------------

Description:
-----------
This contains python modules/packages related to the engine/console interaction.
(requires message_bus package for communications)


modules:
--------

engine          -   Abstract base class.
internal_engine -   Internal engine subclass - an engine runnning in the 
                    controlling process.
socket_engine   -   Abstract base class for engines using socket communications
py_engine       - Process used for external engine using python mainloop.
wx_engine       - Process used for external engine with wx mainloop running.
tk_engine       - Process used for external engine with tk mainloop running.
gtk_engine      - Process used for external engine with gtk mainloop.
gtk3_engine     - Process used for external engine with gtk3 (pyGObject) mainloop.
qt4_engine      - Process used for external engine with Qt4 mainloop.
pyside_engie    - Process used for external engine with PySide Qt4 mainloop.

console         -   Abstract base class for a controlling console.

eng_compiler    - Compiles user source to code.
eng_debugger    - Debugger class
eng_profiler    - Profiler class
eng_messages    -   defines the engine/console communication message types.
eng_misc        -   helper functions/classes for engine management
eng_tasks       -   defines the engine task interfaces and some common tasks.


Overview:
---------
The engine module using the MessageBus system for communications.
1a) In the controlling process create a Console object (a subclass of the 
MessageBus MBLocalNode) and connect to the message bus.
1b) Call set_managed_engine() to set the engine node name this console should 
control.
2) Create Engine object - a subclass of a MessageBus node or client and connect
to the messagebus
3) If the console is already connected to the message bus it will see the 
connecting engine and take control. If the console is connected afterwards call
set_managed_engine() to take control of the engine.

"""
