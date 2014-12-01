import unittest

from fptest.tracing import parse_trace_file
from fptest.tracing import WorkOrder


class TestCartOrderTracing(unittest.TestCase):
    def setUp(self):
        self.trace = parse_trace_file('cartOrderTracing-Terminate-GponLink.log')

    def test_outgoings(self):
        self.assertEquals(2, len(self.trace.outgoing_workorders))

    def test_outgoing_workorders_in_correct_order(self):
        self.assertEquals('LST-ONTDETAIL', self.trace.outgoing_workorders[0].name)
        self.assertEquals('DEL-ONT', self.trace.outgoing_workorders[1].name)

    def test_lst_ontdetail_necommand(self):
        self.assertEquals(['LST-ONTDETAIL::ALIAS=9999999999999999:0::;'],
                          self.trace.outgoing_workorders[0].params['#NE_COMMAND'])

    def test_group_with_brackets(self):
        self.assertEquals(['<foo>'], self.trace.outgoing_workorders[0].params['groupWithBrackets'])

    def test_response_token(self):
        response_token = self.trace.outgoing_workorders[0].params['responseToken']
        self.assertEquals(40, len(response_token))
        self.assertEquals('7340032', response_token[0])
        self.assertEquals('0', response_token[1])
        self.assertEquals('Active', response_token[5])

    def test_lst_ont_detail_status(self):
        self.assertEquals('WOS_Completed', self.trace.outgoing_workorders[0].status)


class TestWorkOrderParamsAdder(unittest.TestCase):
    def test_null(self):
        wo = WorkOrder()
        wo.add_param('foo', '')
        self.assertEquals(0, len(wo.params['foo']))

    def test_simple(self):
        wo = WorkOrder()
        wo.add_param('foo', '<bar>')
        self.assertEquals(['bar'], wo.params['foo'])

    def test_multiple(self):
        wo = WorkOrder()
        wo.add_param('foo', '<bar> <quux>')
        self.assertEquals(['bar', 'quux'], wo.params['foo'])

    def test_nested(self):
        wo = WorkOrder()
        wo.add_param('foo', '<bar> <quux> <<quirg>>')
        self.assertEquals(['bar', 'quux', '<quirg>'], wo.params['foo'])

    def test_complex(self):
        wo = WorkOrder()
        wo.add_param('foo', '<LST-ONTDETAIL::ALIAS=9999999999999999:0::;>')
        self.assertEquals(['LST-ONTDETAIL::ALIAS=9999999999999999:0::;'], wo.params['foo'])
