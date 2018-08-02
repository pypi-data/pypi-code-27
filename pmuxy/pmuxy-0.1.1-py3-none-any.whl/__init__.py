import libtmux

from pmuxy.config import Config


class Pmuxy:

    def __init__(self, config: Config, session: libtmux.Session):
        self.config = config
        self.session = session

    def config_options(self):
        return self.config.config_options()

    def open(self, config_file):
        props = self.config.read_config(config_file)

        window = self.session.new_window(
            window_name=props.get('window_name', config_file),
            attach=props.get('attach', True)
        )

        tmux_cmds = props.get('tmux_commands', [])
        for cmd in tmux_cmds:
            head, *tail = cmd.split(' ')
            window.cmd(head, *tail)

        pane = window.panes[0]
        shell_cmds = props.get('shell_commands', [])

        for cmd in shell_cmds: pane.send_keys(cmd)
        if shell_cmds: pane.send_keys('clear')

    def list_windows(self):
        return self.session.windows
