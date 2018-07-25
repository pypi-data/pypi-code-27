#
# Copyright 2018 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#

import uuid

from libnmstate import nmclient


def create_profile(*settings):
    con_profile = nmclient.NM.SimpleConnection.new()
    for setting in settings:
        con_profile.add_setting(setting)

    return con_profile


def create_settings(name, iface_type):
    con_setting = nmclient.NM.SettingConnection.new()
    con_setting.id = name
    con_setting.interface_name = name
    con_setting.uuid = str(uuid.uuid4())
    con_setting.type = iface_type
    con_setting.autoconnect = True
    con_setting.autoconnect_slaves = (
        nmclient.NM.SettingConnectionAutoconnectSlaves.NO)
    return con_setting


def get_device_connection(nm_device):
    act_connection = nm_device.get_active_connection()
    if act_connection:
        return act_connection.props.connection
    return None
