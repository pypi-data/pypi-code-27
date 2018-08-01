from . import server  # server.py
from . import clnt_gui  # clnt_gui.py
from . import clnt_cli  # clnt_cli.py
from . import console  # console.py


def main():
    console_params = console.args()
    if console_params.mode == 'server':
        server.run()
    elif console_params.mode == 'clnt_gui':
        clnt_gui.run()
    else:
        clnt_cli.run()


if __name__ == "__main__":
    main()
