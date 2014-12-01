__author__ = 'oxle019'

import unittest


class FpTest(unittest.TestCase):
    def __init__(self, request):
        super().__init__()
        self.request = request
        self.fp_url = 'http://localhost:55000/aff'
        self.fp_node_dir = './FPNode'

    def setUp(self):
        print('Emptying cartOrderTracing.00000.log')
        print('Emptying kpsaOrderTracing.00000.log')
        print('Linearizing XML')
        print('Posting XML')
        self.response = None
        self.cart_order_tracing = None
        self.kpsa_order_tracing = None
