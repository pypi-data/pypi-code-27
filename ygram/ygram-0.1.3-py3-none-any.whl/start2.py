from subprocess import Popen, CREATE_NEW_CONSOLE
import time
Popen(['python', 'server.py'], creationflags=CREATE_NEW_CONSOLE)
Popen(['python', 'image_server.py'], creationflags=CREATE_NEW_CONSOLE)

for _ in range(2):
    Popen(['python', 'client_gui.py'], creationflags=CREATE_NEW_CONSOLE)
    time.sleep(1)
