__author__ = 'oxle019'

import unittest
from unittest.mock import Mock, call
from os import path

import fptest


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.the_test = fptest.FpTest()
        fptest.FpTest.zero_file = Mock(return_value=None)
        self.the_test.request = '<request />'
        #self.the_test.run_test()

    def test_files_zeroed(self):
        calls = [call(path.join(self.the_test.fp_node_dir, 'cartOrderTracing.00000.log')),
                 call(path.join(self.the_test.fp_node_dir, 'kpsaOrderTracing.00000.log'))]
        #self.the_test.zero_file.assert_has_calls(calls)

