[![PyPI version](https://badge.fury.io/py/FpTest.svg)](http://badge.fury.io/py/FpTest)
[![Build Status](https://travis-ci.org/oxo42/FpTest.svg?branch=master)](https://travis-ci.org/oxo42/FpTest)

Overview
========

```python
class TerminateGponLinkTest(fptest.FpTest):
    def test_workorders(self):
        expected_workorders = [('LST-ONTDETAIL', 'WOS_Completed'), ('DEL-ONT', 'WOS_Completed')]
        actual_workorders = [(wo.name, wo.status) for wo in self.cart_order_tracing.outgoing_workorders]
        self.assertListEqual(expected_workorders, actual_workorders)

    def request(self):
        return """
<request>
    <so>
        <orderId>1412685518565</orderId>
        <sod>
           <!-- Snipped for brevity -->
"""
```

`fptest.FpTest` extends `unittest.TestCase` and overrides the `setUp` method to post the contents of `request()` to FP.
It then parses `../runtime/FPNode/cartOrderTracing.00000.log` into a format where it is much easier to pull information
out of the trace file.

You can then write tests in Python that are expressive and repeatable.  I am using
[nosetests](https://nose.readthedocs.org/) and the `--with-xunit` flag to output a file of test results that Jenkins is
post-processing!

Installation
============

	pip install fptest

Setup
=====

The following file structure is assumed

    FP-Project/
    |-- IntegrationTests
    `-- runtime
        `-- FPNode

The directory structure is important as FpTest will look in `../runtime/FPNode` for the cartOrderTracing log file.

Samples
=======

There are two samples in the `/samples` directory of this project.  These are tests that I am successfully running
against my instance of FP.

Documentation to come
=====================

* Explanation of setting up cartridge simulators to pass / fail depending on input values
* Explanation of `raw_params` and `params` in the work order
* Explanation of `self.fp_url` and `self.fp_node_dir`
* Explanation of `Trace` and `WorkOrder`