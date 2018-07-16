from __future__ import absolute_import, print_function, division

import proton
import proton.reactor
import proton.handlers

from cli_proton_python import sender, options


class DirectSend(sender.Send):

    def __init__(self, msg_durable):
        msg_durable = True
        parser = options.SenderOptions()
        opts, _ = parser.parse_args()
        opts.msg_durable = msg_durable
        super(sender.Send, self).__init__(opts)


def main():
    container = proton.reactor.Container(DirectSend(msg_durable=True))
    container.run()

if __name__ == '__main__':
    main()
