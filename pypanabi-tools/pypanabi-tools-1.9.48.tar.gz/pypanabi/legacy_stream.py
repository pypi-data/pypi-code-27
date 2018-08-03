#!/usr/bin/env python

from .hydra import Hydra


class LegacyStream(Hydra):
    def __init__(self, brand, channel, rdl_schema, odl_schema, streaming, level):
        """
        Constructor
        :param brand: brand name OLX or Letgo [String]
        :param channel: channel name: Android, iOS or Web [String]
        :param rdl_schema: raw data layer schema [String]
        :param odl_schema: operation data layer schema [String]
        :param streaming: true is loading is coming from kinesis, false from file [Boolean]
        :param level: logging level [String]
        """
        # super initialization
        Hydra.__init__(self, brand, channel, rdl_schema, odl_schema, streaming, level)

        # prefix
        self._table_prefix = 'legacy{brand}'.format(brand=self._brand)
