# -*- coding: utf-8 -*-

import unittest

from total_field.tests import total_field, utils


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(total_field.suite())
    suite.addTest(utils.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')