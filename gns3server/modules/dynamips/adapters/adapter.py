# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Adapter(object):
    """
    Base class for adapters.

    :param interfaces: number of interfaces supported by this adapter.
    :param wics: number of wics supported by this adapter.
    """

    def __init__(self, interfaces=0, wics=0):

        self._interfaces = interfaces

        self._ports = {}
        for port_id in range(0, interfaces):
            self._ports[port_id] = None
        self._wics = wics * [None]

    def removable(self):
        """
        Returns True if the adapter can be removed from a slot
        and False if not.

        :returns: boolean
        """

        return True

    def port_exists(self, port_id):
        """
        Checks if a port exists on this adapter.

        :returns: True is the port exists,
        False otherwise.
        """

        if port_id in self._ports:
            return True
        return False

    def wic_slot_available(self, wic_slot_id):
        """
        Checks if a WIC slot is available

        :returns: True is the WIC slot is available,
        False otherwise.
        """

        if self._wics[wic_slot_id] == None:
            return True
        return False

    def install_wic(self, wic_slot_id, wic):
        """
        Installs a WIC on this adapter.

        :param wic_slot_id: WIC slot ID (integer)
        :param wic: WIC object
        """

        self._wics[wic_slot_id] = wic

        # Dynamips WICs ports start on a multiple of 16 + port number
        # WIC1 port 1 = 16, WIC1 port 2 = 17
        # WIC2 port 1 = 32, WIC2 port 2 = 33
        # WIC3 port 1 = 48, WIC3 port 2 = 49
        base = 16 * (wic_slot_id + 1)
        for wic_port in range(0, wic.interfaces):
            port_id = base + wic_port
            self._ports[port_id] = None

    def uninstall_wic(self, wic_slot_id):
        """
        Removes a WIC from this adapter.

        :param wic_slot_id: WIC slot ID (integer)
        """

        wic = self._wics[wic_slot_id]

        # Dynamips WICs ports start on a multiple of 16 + port number
        # WIC1 port 1 = 16, WIC1 port 2 = 17
        # WIC2 port 1 = 32, WIC2 port 2 = 33
        # WIC3 port 1 = 48, WIC3 port 2 = 49
        base = 16 * (wic_slot_id + 1)
        for wic_port in range(0, wic.interfaces):
            port_id = base + wic_port
            del self._ports[port_id]
        self._wics[wic_slot_id] = None

    def add_nio(self, port_id, nio):
        """
        Adds a NIO to a port on this adapter.

        :param port_id: port ID (integer)
        :param nio: NIO object
        """

        self._ports[port_id] = nio

    def remove_nio(self, port_id):
        """
        Removes a NIO from a port on this adapter.

        :param port_id: port ID (integer)
        """

        self._ports[port_id] = None

    def get_nio(self, port_id):
        """
        Returns the NIO assigned to a port.

        :params port_id: port ID (integer)

        :returns: NIO object
        """

        return self._ports[port_id]

    @property
    def ports(self):
        """
        Returns port to NIO mapping

        :returns: dictionary port -> NIO
        """

        return self._ports

    @property
    def interfaces(self):
        """
        Returns the number of interfaces supported by this adapter.

        :returns: number of interfaces
        """

        return self._interfaces

    @property
    def wics(self):
        """
        Returns the wics adapters inserted in this adapter.

        :returns: list WIC objects
        """

        return self._wics