from prompt_toolkit.application import Application
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.enums import DEFAULT_BUFFER
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from prompt_toolkit.layout.containers import HSplit, Window, ConditionalContainer
from prompt_toolkit.layout.controls import FillControl, TokenListControl, BufferControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.layout.screen import Char
from prompt_toolkit.filters import Condition
from prompt_toolkit.layout.lexers import SimpleLexer
from prompt_toolkit.styles import PygmentsStyle
from pygments.token import Token

def get_titlebar_tokens(cli):

    def click_quit(cli, event):
        event.cli = cli
        quit_(event)

    def click_save(cli, event):
        event.cli = cli
        save_(event)

    messagebox = cli.messagebox
    cli.messagebox = ''
    return [
        (Token.Title, 'Ping++'),
        (Token.Sep, '  '),
        (Token.Title, 'Press '),
        (Token.Click, 'A'),
        (Token.Title, ' to add IP'),
        (Token.Sep, ', '),
        (Token.Click, 'S', click_save),
        (Token.Title, ' to save', click_save),
        (Token.Sep, ', '),
        (Token.Click, 'Q', click_quit),
        (Token.Title, ' to quit', click_quit),
        (Token.Sep, '    '),
        (Token.Messagebox, messagebox),
    ]

hasInputbox = Condition(lambda cli: cli.current_buffer_name == 'inputbox')

layout = HSplit([
    Window(height=D.exact(1), content=TokenListControl(get_titlebar_tokens, align_center=False)),
    Window(height=D.exact(1), content=FillControl(' ', token=Token.Line)),
    ConditionalContainer(
        Window(
            height=D.exact(1),
            content=BufferControl(
                buffer_name='inputbox',
                default_char=Char(token=Token.Inputbox),
                lexer=SimpleLexer(Token.Inputbox)
            )
        ),
        filter=hasInputbox
    )
])

manager = KeyBindingManager()


@manager.registry.add_binding('a', eager=True, filter=~hasInputbox)
def add_(event):
    event.cli.focus('inputbox')


@manager.registry.add_binding('s', eager=True, filter=~hasInputbox)
def save_(event):
    event.cli.messagebox = 'Saving ...'
    event.cli.settings.save()


@manager.registry.add_binding(Keys.ControlC, eager=True, filter=~hasInputbox)
@manager.registry.add_binding('q', eager=True, filter=~hasInputbox)
def quit_(event):
    event.cli.set_return_value(None)


@manager.registry.add_binding(Keys.Enter, eager=True, filter=hasInputbox)
def done_(event):
    event.cli.focus(DEFAULT_BUFFER)
    inputbox_buffer = event.cli.buffers['inputbox']
    host = inputbox_buffer.text
    if host:
        inputbox_buffer.cursor_position = 0
        inputbox_buffer.text = ''

        event.cli.settings.setstr('hosts', host, "")
        event.cli.interrupt_ping_worker.set()
        event.cli.messagebox = 'Adding host ...'


buffers = {
    DEFAULT_BUFFER: Buffer(is_multiline=False),
    'inputbox': Buffer(is_multiline=False)
}


text_style = PygmentsStyle.from_defaults({
    Token:          '#888888',
    Token.Literal.Number:  '#ffffff',
    Token.Click: 'underline bg:#000066 #ffffff',
    Token.Sep: '#333333',
    Token.Inputbox: 'bg:#333333 #ffffff',
    Token.Messagebox: 'bg:#3333ff #ffffff',
    Token.Title: 'bold #888888',
    Token.Header.Bold: 'bold #888888',
    Token.Header.Normal: '#888888',
    Token.Host: '#ffffff',
    Token.Desc: '#888888',
    Token.Normal: '#ffffff',
    Token.Warning: '#ffff88',
    Token.Fault: '#ff8888'
})


def get_application():
    application = Application(
        layout=layout,
        buffers=buffers,
        style=text_style,
        key_bindings_registry=manager.registry,
        mouse_support=True,
        use_alternate_screen=True
    )
    return application
