__author__ = 'oxle019'

import unittest
import os

from fptest import FpTest


class TestUtilityMethods(unittest.TestCase):
    def test_zero_file(self):
        with open('tmpfile', 'w') as f:
            f.writelines(['hello', 'world'])

        self.assertTrue(os.stat('tmpfile').st_size > 0)
        FpTest.zero_file('tmpfile')

        self.assertEquals(0, os.stat('tmpfile').st_size)
        os.remove('tmpfile')

    def test_xml_linearize(self):
        actual = FpTest.linearize_xml(b"<?xml version='1.0' encoding='UTF-8'?>\n"
                                      b'\t<request>\n'
                                      b'    <so />\n'
                                      b'</request>')
        expected = b"<?xml version='1.0' encoding='ASCII'?>\n<request><so/></request>"
        self.assertEquals(expected, actual)

