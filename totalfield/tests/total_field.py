# -*- coding: utf-8 -*-

import unittest

from trac.test import EnvironmentStub, Mock, MockPerm
from trac.ticket.model import Ticket
from trac.web.href import Href

from total_field.total_field import TotalField


class TotalFieldTestCase(unittest.TestCase):
    
    def setUp(self):
        self.env = EnvironmentStub(default_data = True)
        self.env.config.set('ticket-custom', 'my_field', 'text')
        self.env.config.set('totalfield', 'total_field', 'my_field')
        self.req = Mock(href = Href('/'),
                        abs_href = Href('http://www.example.com/'),
                        locale=None,
                        perm = MockPerm(),
                        authname='anonymous',
                        tz='')
        self.formatter = Mock(req=self.req)
       
    def _insert_ticket(self, field_value, fields=None):
        fields = fields or {}
        ticket = Ticket(self.env)
        ticket['summary'] = 'Test Ticket'
        ticket['my_field'] = field_value
        ticket['milestone'] = 'milestone1'
        ticket['status'] = 'open'
        for field, value in fields.items():
            ticket[field] = value
        ticket.insert()
        return ticket

    def test_basic(self):
        totalField = TotalField(self.env)
        self._insert_ticket('10')
        self._insert_ticket('20')
        self._insert_ticket('30')
        result = totalField.expand_macro(self.formatter, "", "milestone=milestone1")
        self.assertEqual(result, '60')

    def test_real(self):
        totalField = TotalField(self.env)
        self._insert_ticket('10')
        self._insert_ticket('20.1')
        self._insert_ticket('30')
        result = totalField.expand_macro(self.formatter, "", "milestone=milestone1")
        self.assertEqual(result, '60.1')

    def test_invalid(self):
        totalField = TotalField(self.env)
        self._insert_ticket('10')
        self._insert_ticket('20')
        self._insert_ticket('30')
        self._insert_ticket('xxx')
        result = totalField.expand_macro(self.formatter, "", "milestone=milestone1")
        self.assertEqual(result, '60')

    def test_to_many_tickets(self):
        totalField = TotalField(self.env)
        for _ in range(200):
            self._insert_ticket('1')
        result = totalField.expand_macro(self.formatter, "", "milestone=milestone1")
        self.assertEqual(result, '200')

    def test_url_encode(self):
        totalField = TotalField(self.env)
        self._insert_ticket('10', fields={'summary': 'Test#One'})
        result = totalField.expand_macro(self.formatter, "", "summary=Test#One")
        self.assertEquals(result, '10')


def suite():
    return unittest.makeSuite(TotalFieldTestCase)


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
