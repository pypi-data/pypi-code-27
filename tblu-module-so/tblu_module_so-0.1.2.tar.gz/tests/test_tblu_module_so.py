#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tblu_module_so` package."""


import unittest

from tblu_module_so import TBLuModule


class TestTblu_module_so(unittest.TestCase):
    """Tests for `tblu_module_so` package."""
    agent = None

    def setUp(self):
        """Set up test fixtures, if any."""
        self.agent = TBLuModule()

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_cpuTimes(self):
        """Get cpu_times"""
        result = self.agent.cpu_times()
        print('Result: ' + str(result))
        self.assertTrue(len(result) > 0)

    def test_001_cpu_freq(self):
        """Get cpu_freq"""
        result = self.agent.cpu_freq()
        print('Result: ' + str(result))
        self.assertTrue(len(result) > 0)

    def test_002_virtual_memory(self):
        """Get virtual_memory"""
        result = self.agent.virtual_memory()
        print('Result: ' + str(result))
        self.assertTrue(len(result) > 0)

    def test_003_swap_memory(self):
        """Get swap_memory"""
        result = self.agent.swap_memory()
        print('Result: ' + str(result))
        self.assertTrue(len(result) > 0)

    def test_004_cpu_info(self):
        """Get cpu_info"""
        result = self.agent.cpu_info()
        print('Result: ' + str(result))
        self.assertTrue(len(result) > 0)

    def test_005_disk_usage(self):
        """Get disk_usage"""
        result = self.agent.disk_usage()
        print('Result: ' + str(result))
        self.assertTrue(len(result) > 0)

    def test_006_disk_io_counters(self):
        """Get disk_io_counters"""
        result = self.agent.disk_io_counters()
        print('Result: ' + str(result))
        self.assertTrue(len(result) > 0)

    def test_007_net_io_counters(self):
        """Get net_io_counters"""
        result = self.agent.net_io_counters()
        print('Result: ' + str(result))
        self.assertTrue(len(result) > 0)

    def test_007_net_if_addrs(self):
        """Get net_if_addrs"""
        result = self.agent.net_if_addrs()
        print('Result: ' + str(result))
        self.assertTrue(len(result) > 0)

    def test_999_run(self):
        """Get By Call"""
        self.assertTrue(len(self.agent.call('cpu_times')) > 0)

    # def test_000_something(self):
    #     """Test something."""
    #     self.assertEqual(tblu_module_so.get_hmm(), 'hmmm...')
