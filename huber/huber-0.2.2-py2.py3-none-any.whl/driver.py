"""Python driver for Huber recirculating baths, using asynchronous TCP.

Distributed under the GNU General Public License v2
Copyright (C) 2017 NuMat Technologies
"""
try:
    import asyncio
except ImportError:
    raise ImportError("TCP connections require python >=3.5.")

import logging
from huber import util

logger = logging.getLogger('huber')


class Bath(object):
    """Python driver for Huber recirculating baths."""

    port = 8101
    defaults = [
        'on',
        'temperature.internal',
        'temperature.setpoint',
        'pump.pressure',
        'pump.speed',
        'pump.setpoint',
        'fill',
        'maintenance',
        'status'
    ]

    def __init__(self, ip):
        """Initialize the connection with the bath's IP address."""
        self.ip = ip
        self.open = False
        self.reconnecting = False
        self.timeouts = 0
        self.max_timeouts = 10
        self.waiting = False
        self.connection = None

    def __enter__(self):
        """Provide entrance to context manager."""
        return self

    async def __aenter__(self):
        """Provide async entrance to context manager.

        Contrasting synchronous access, this will connect on initialization.
        """
        await self._connect()
        return self

    def __exit__(self, *args):
        """Provide exit to context manager."""
        self.close()

    async def __aexit__(self, *args):
        """Provide async exit to context manager."""
        self.close()

    async def get(self):
        """Get a pre-selected list of fields.

        Note that this is slow, as it chains multiple requests to construct
        a response. Look into the other `get` methods for single fields.
        """
        output = {}
        for default in self.defaults:
            util.set_nested(output, default, await self._get(default))
        return output

    async def start(self):
        """Start the controller and pump."""
        return await self._set('on', True)

    async def stop(self):
        """Stop the controller and pump."""
        return await self._set('on', False)

    async def toggle(self, on):
        """Start or stop the controller and pump."""
        return await self._set('on', on)

    async def get_setpoint(self):
        """Get the temperature setpoint of the bath, in C."""
        return await self._get('temperature.setpoint')

    async def set_setpoint(self, value):
        """Set the temperature setpoint of the bath, in C."""
        return await self._set('temperature.setpoint', value)

    async def get_internal(self):
        """Get the internal temperature of the bath, in C."""
        return await self._get('temperature.internal')

    async def get_pump_pressure(self):
        """Get the bath pump outlet pressure, in mbar."""
        return await self._get('pump.pressure')

    async def get_pump_speed(self):
        """Get the bath pump speed, in RPM."""
        return await self._get('pump.speed')

    async def set_pump_speed(self, value):
        """Set the bath pump speed, in RPM."""
        return await self._set('pump.setpoint', value)

    async def get_fill_level(self):
        """Get the thermostat fluid fill level, in [0, 1]."""
        return await self._get('fill')

    async def get_next_maintenance(self):
        """Get the number of days until next maintenance alarm."""
        return await self._get('maintenance')

    async def get_status(self):
        """Get bath status indicators. Useful for triggering alerts."""
        return await self._get('status')

    def close(self):
        """Close the TCP connection."""
        if self.open:
            self.connection['writer'].close()
        self.open = False

    async def _connect(self):
        """Asynchronously open a TCP connection with the server."""
        self.open = False
        reader, writer = await asyncio.open_connection(self.ip, self.port)
        self.connection = {'reader': reader, 'writer': writer}
        self.open = True

    async def _get(self, key):
        """Get a property as specified by the corresponding key."""
        settings = util.get_field(key)
        response = await self._write_and_read(settings['address'])
        value = util.parse(response, settings)
        if ('range' in settings and value is not None and not
                settings['range'][0] <= value <= settings['range'][1]):
            raise ValueError(f'Value {value} outside allowed range.')
        return value

    async def _set(self, key, value):
        """Set property as specified by key."""
        settings = util.get_field(key)
        if 'writable' not in settings or not settings['writable']:
            raise ValueError(f'Can not write to {key}.')
        if ('range' in settings and not
                settings['range'][0] <= value <= settings['range'][1]):
            raise ValueError(f'Value {value} outside allowed range.')
        encoded = int(100 * value if settings['format'] == 'f' else value)
        response = await self._write_and_read(settings['address'], encoded)
        new = util.parse(response, settings)
        if abs(new - value) > .1:
            raise IOError(f'Could not set {key}.')

    async def _write_and_read(self, address, value=None):
        """Write a command and reads a response from the bath.

        As these baths are commonly moved around, this has been expanded to
        handle recovering from disconnects.
        """
        if self.waiting:
            return None
        self.waiting = True

        value = util.int_to_hex(value) if value else '****'
        command = f'{{M{address:02X}{value}\r\n'

        await self._handle_connection()
        response = await self._handle_communication(command)
        self.waiting = False

        if (response is None or len(response) != 8 or
                response[:4] != f'{{S{address:02X}'):
            return None
        return util.hex_to_int(response[4:])

    async def _handle_connection(self):
        """Automatically maintain TCP connection."""
        try:
            if not self.open:
                await asyncio.wait_for(self._connect(), timeout=0.25)
            self.reconnecting = False
        except (asyncio.TimeoutError, OSError):
            if not self.reconnecting:
                logger.error(f'Connecting to {self.ip} timed out.')
            self.reconnecting = True

    async def _handle_communication(self, command):
        """Manage communication, including timeouts and logging."""
        try:
            self.connection['writer'].write(command.encode())
            future = self.connection['reader'].readuntil(b'\r\n')
            line = await asyncio.wait_for(future, timeout=0.25)
            result = line.decode().strip()
            self.timeouts = 0
        except (asyncio.TimeoutError, TypeError):
            self.timeouts += 1
            if self.timeouts == self.max_timeouts:
                logger.error(f'Reading from {self.ip} timed out '
                             f'{self.timeouts} times.')
            result = None
        return result
