import urllib
import urllib2
from datetime import datetime
from time import strptime

from trac.config import Option, ListOption, BoolOption
from trac.core import TracError, Component, implements
from trac.ticket.query import Query
from trac.util.text import unicode_urlencode

# 0.12 stores timestamps as microseconds. Pre-0.12 stores as seconds.
from trac.util.datefmt import utc
try:
    from trac.util.datefmt import from_utimestamp as from_timestamp
except ImportError:
    def from_timestamp(ts):
        return datetime.fromtimestamp(ts, utc)

AVAILABLE_OPTIONS = ['startdate', 'enddate', 'today', 'width', 'height',
                     'color', 'bgcolor', 'wecolor', 'weekends', 'gridlines',
                     'expected', 'colorexpected', 'title']



def get_total_field():
    return Option('totalfield', 'total_field', 'totalhours',
        doc="""Defines what custom field should be used to calculate
        total hours. Defaults to 'totalhours'""")


class TotalFieldBase(Component):
    """ Base class TotalField components that auto-disables if
    total field is not properly configured. """

    abstract = True
    total_field = get_total_field()

    def __init__(self, *args, **kwargs):
        if not self.env.config.has_option('ticket-custom',
                                          self.total_field):
            # No total field configured. Disable plugin and log error.
            self.log.error("TotalField (%s): "
                           "Total field not configured. "
                           "Component disabled.", self.__class__.__name__)
            self.env.disable_component(self)



def execute_query(env, req, query_args):
    # set maximum number of returned tickets to 0 to get all tickets at once
    query_args['max'] = 0
    # urlencode the args, converting back a few vital exceptions:
    # see the authorized fields in the query language in
    # http://trac.edgewall.org/wiki/TracQuery#QueryLanguage
    query_string = unicode_urlencode(query_args).replace('%21=', '!=') \
                                                .replace('%21%7E=', '!~=') \
                                                .replace('%7E=', '~=') \
                                                .replace('%5E=', '^=') \
                                                .replace('%24=', '$=') \
                                                .replace('%21%5E=', '!^=') \
                                                .replace('%21%24=', '!$=') \
                                                .replace('%7C', '|') \
                                                .replace('+', ' ') \
                                                .replace('%23', '#') \
                                                .replace('%28', '(') \
                                                .replace('%29', ')')
    env.log.debug("query_string: %s", query_string)
    query = Query.from_string(env, query_string)

    tickets = query.execute(req)

    tickets = [t for t in tickets
               if ('TICKET_VIEW' or 'TICKET_VIEW_CC')
               in req.perm('ticket', t['id'])]

    return tickets



