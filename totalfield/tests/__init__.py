# -*- coding: utf-8 -*-

import unittest

from totalfield.tests import total_field


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(total_field.suite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
