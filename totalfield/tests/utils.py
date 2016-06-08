# -*- coding: utf-8 -*-

import unittest
from trac.test import EnvironmentStub, Mock

from totalfield.utils import TotalFieldBase


class TotalFieldBaseTestCase(unittest.TestCase):

    def test_disabled_without_total_field(self):
        if not hasattr(EnvironmentStub, 'is_enabled'):
            return # 0.12+ feature of mock env
        class TestTool(TotalFieldBase):
            pass
        env = EnvironmentStub(enable=['totalfield.*'])
        messages = []
        env.log = Mock(error=lambda msg, *args: messages.append(msg % args))
        TestTool(env)
        self.assertEquals(False, env.is_enabled(TestTool))
        self.assertEquals(messages,
                ['TotalField (TestTool): Total field not configured. Component disabled.'])

    def test_enabled_with_total_field(self):
        if not hasattr(EnvironmentStub, 'is_enabled'):
            return # 0.12+ feature of mock env
        class TestTool(TotalFieldBase):
            pass
        env = EnvironmentStub()
        self.env.config.set('ticket-custom', 'my_field', 'text')
        self.env.config.set('totalfield', 'total_field', 'my_field')
        env.config.set('components', 'totalfield.*', 'enabled')
        messages = []
        env.log = Mock(error=lambda msg, *args: messages.append(msg))
        TestTool(env)
        self.assertEquals(True, env.is_enabled(TestTool))
        self.assertEquals(messages, [])


def suite():
    return unittest.makeSuite(TotalFieldBaseTestCase)


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
