"""
Test the Terminate/GPONLink Product Order

The product order takes a serial number, calls LST-ONTDETAIL to get the details of the ONT then DEL-ONT to remove it.
This test case ensures that the right commands happen in the right order

"""
import fptest


class TerminateGponLinkTest(fptest.FpTest):
    def test_workorders(self):
        expected_workorders = [('LST-ONTDETAIL', 'WOS_Completed'), ('DEL-ONT', 'WOS_Completed')]
        actual_workorders = [(wo.name, wo.status) for wo in self.cart_order_tracing.outgoing_workorders]
        self.assertListEqual(expected_workorders, actual_workorders)

    def test_command_for_lst_ontdetail(self):
        self.assertEqual(['LST-ONTDETAIL::ALIAS=9999999999999999:0::;'],
                         self.cart_order_tracing.outgoing_workorders[0].params['#NE_COMMAND'])

    def test_alias(self):
        lst_ontdetail = self.get_first_wo('LST-ONTDETAIL')
        self.assertRegex(lst_ontdetail.params['#NE_COMMAND'][0], r'ALIAS=9999999999999999')

    def test_status(self):
        self.assertEqual('OK', self.get_fp_status())

    def request(self):
        return """
<request>
    <so>
        <orderId>1412685518565</orderId>
        <sod>
            <domain>GPON</domain>
            <verb>Terminate</verb>
            <customerId>RegressionTesting</customerId>
            <originator>WGET</originator>
            <priority>10</priority>
            <doCheckpoint>false</doCheckpoint>
            <dataset>
                <param>
                    <name>routerName</name>
                    <index>0</index>
                    <value>router</value>
                </param>
            </dataset>
            <pod>
                <productName>GPONLink</productName>
                <productVerb>Terminate</productVerb>
                <dataset>
                    <param>
                        <name>ElementManager</name>
                        <index>0</index>
                        <value>Huawei_U2000</value>
                    </param>
                    <param>
                        <name>serialNumber</name>
                        <index>0</index>
                        <value>9999999999999999</value>
                    </param>
                    <param>
                        <name>pppUsername</name>
                        <index>0</index>
                        <value>foo@example.com</value>
                    </param>
                </dataset>
            </pod>
        </sod>
    </so>
</request>
"""