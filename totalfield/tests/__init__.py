# -*- coding: utf-8 -*-

import unittest

from totalfield.tests import totalfield, utils


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(totalfield.suite())
    suite.addTest(utils.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
