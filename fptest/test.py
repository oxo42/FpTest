import requests

__author__ = 'oxle019'

from os import path
from fptest.tracing import parse_trace_file

from lxml import etree
import unittest


class FpTest(unittest.TestCase):
    @classmethod
    def zero_file(cls, filename):
        """
        Zero out a file.  Used to clear cartOrderTracing and kpsaOrderTracing before running the tests
        :param filename: File to clear
        """
        with open(filename, 'w'):
            pass

    @classmethod
    def linearize_xml(cls, xml_string):
        """
        Strips insignificant whitespace and adds the xml declaration (unpretty-print)

        This is because FP needs the input to be in this format
        :param xml_string: Pretty-printed xml string
        :return: Headered, unpretty-printed xml string
        """
        parser = etree.XMLParser(remove_blank_text=True)
        elem = etree.XML(xml_string, parser=parser)
        return etree.tostring(elem, xml_declaration=True)

    @classmethod
    def readfile(cls, filename):
        with open(filename, 'r') as f:
            return f.read()

    def __init__(self, *args, **kwargs):
        super(FpTest, self).__init__(*args, **kwargs)
        self.fp_url = 'http://localhost:55000/aff'
        self.fp_node_dir = './FPNode'
        self.response = None
        self.cart_order_tracing = None
        self.kpsa_order_tracing = None
        self.has_run = False

    def request(self):
        """
        Gets the request to post to FP for the test.  There is the helper class method readfile
        :return: XML String of the request
        """
        raise NotImplementedError('The request() method must return the request to send to FP')

    def do_work(self):
        self.has_run = True
        self.zero_file(path.join(self.fp_node_dir, 'cartOrderTracing.00000.log'))
        self.zero_file(path.join(self.fp_node_dir, 'kpsaOrderTracing.00000.log'))

        data = self.linearize_xml(self.request())
        self.response = requests.post(self.fp_url, data=data)
        self.response.connection.close()
        self.cart_order_tracing = parse_trace_file(path.join(self.fp_node_dir, 'cartOrderTracing.00000.log'))
        self.kpsa_order_tracing = parse_trace_file(path.join(self.fp_node_dir, 'kpsaOrderTracing.00000.log'))

    def setUp(self):
        if not self.has_run:
            self.do_work()


