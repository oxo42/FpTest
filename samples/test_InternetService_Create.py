__author__ = 'oxle019'

import fptest


class CreateInternetServiceSuccess(fptest.FpTest):
    def test_outgoing_workorders_in_correct_order(self):
        expected_workorders = ['radcheck_delete', 'radreply_delete', 'radcheck_insert', 'radreply_insert',
                               'CreateSubscriber', 'SetPlan', 'ProvisionEntity']
        actual_workorders = [wo.name for wo in self.cart_order_tracing.outgoing_workorders]
        self.assertListEqual(expected_workorders, actual_workorders)

    def test_status(self):
        self.assertEqual('OK', self.get_fp_status())

    def request(self):
        return """
<request>
    <so>
        <orderId>1001</orderId>
        <sod>
            <domain>GPON</domain>
            <verb>Create</verb>
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
                <param>
                    <name>package</name>
                    <index>0</index>
                    <value>ZM_HOME_BASIC</value>
                </param>
            </dataset>
            <pod>
                <productName>InternetService</productName>
                <productVerb>Create</productVerb>
                <dataset>
                    <param>
                        <name>pppUsername</name>
                        <index>0</index>
                        <value>helpdeskgponvoiptest@example.com</value>
                    </param>
                    <param>
                        <name>pppPassword</name>
                        <index>0</index>
                        <value>123412</value>
                    </param>
                </dataset>
            </pod>
        </sod>
    </so>
</request>
"""


class CreateInternetService_SubscriberServices_CreateSubscriberFail(fptest.FpTest):
    def test_outgoing_workorders_in_correct_order(self):
        expected_workorders = [('radcheck_delete', 'WOS_Completed'), ('radreply_delete', 'WOS_Completed'),
                               ('radcheck_insert', 'WOS_Completed'), ('radreply_insert', 'WOS_Completed'),
                               ('CreateSubscriber', 'WOS_FunctionalError'), ('radcheck_delete', 'WOS_Completed'),
                               ('radreply_delete', 'WOS_Completed')]

        actual_workorders = [(wo.name, wo.status) for wo in self.cart_order_tracing.outgoing_workorders]
        self.assertListEqual(expected_workorders, actual_workorders)

    def test_status(self):
        self.assertEqual('KO', self.get_fp_status())

    def request(self):
        return """
<request>
    <so>
        <orderId>1001</orderId>
        <sod>
            <domain>GPON</domain>
            <verb>Create</verb>
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
                <param>
                    <name>package</name>
                    <index>0</index>
                    <value>ZM_HOME_BASIC</value>
                </param>
            </dataset>
            <pod>
                <productName>InternetService</productName>
                <productVerb>Create</productVerb>
                <dataset>
                    <param>
                        <name>pppUsername</name>
                        <index>0</index>
                        <value>fail@example.com</value>
                    </param>
                    <param>
                        <name>pppPassword</name>
                        <index>0</index>
                        <value>123412</value>
                    </param>
                </dataset>
            </pod>
        </sod>
    </so>
</request>
"""


class CreateInternetService_SubscriberServices_SetPlanFail(fptest.FpTest):
    def test_outgoing_workorders_in_correct_order(self):
        """
        Expect to see a failed SetPlan followed by rollback of the subscriber, radcheck and radreply
        """
        expected_workorders = [('radcheck_delete', 'WOS_Completed'), ('radreply_delete', 'WOS_Completed'),
                               ('radcheck_insert', 'WOS_Completed'), ('radreply_insert', 'WOS_Completed'),
                               ('CreateSubscriber', 'WOS_Completed'), ('SetPlan', 'WOS_FunctionalError'),
                               ('DeleteSubscriber', 'WOS_Completed'), ('radcheck_delete', 'WOS_Completed'),
                               ('radreply_delete', 'WOS_Completed')]
        actual_workorders = [(wo.name, wo.status) for wo in self.cart_order_tracing.outgoing_workorders]
        self.assertListEqual(expected_workorders, actual_workorders)

    def test_status(self):
        self.assertEqual('KO', self.get_fp_status())

    def request(self):
        return """
<request>
    <so>
        <orderId>1001</orderId>
        <sod>
            <domain>GPON</domain>
            <verb>Create</verb>
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
                <param>
                    <name>package</name>
                    <index>0</index>
                    <value>ZM_HOME_BASIC</value>
                </param>
            </dataset>
            <pod>
                <productName>InternetService</productName>
                <productVerb>Create</productVerb>
                <dataset>
                    <param>
                        <name>pppUsername</name>
                        <index>0</index>
                        <value>failsetplan@example.com</value>
                    </param>
                    <param>
                        <name>pppPassword</name>
                        <index>0</index>
                        <value>123412</value>
                    </param>
                </dataset>
            </pod>
        </sod>
    </so>
</request>
"""