from trac.wiki.api import parse_args
from trac.wiki.macros import WikiMacroBase

from totalfield.utils import TotalFieldBase, execute_query



class TotalField(TotalFieldBase, WikiMacroBase):
    """Calculates the sum of total hours for the queried tickets.

    The macro accepts a comma-separated list of query parameters for the ticket selection,
    in the form "key=value" as specified in TracQuery#QueryLanguage.

    Example:
    {{{
        [[TotalField(milestone=Sprint 1)]]
    }}}
    """

    def expand_macro(self, formatter, name, content):
        req = formatter.req
        _ignore, options = parse_args(content, strict=False)

        # we have to add custom field to query so that field is added to
        # resulting ticket list
        options[self.total_field + "!"] = None

        tickets = execute_query(self.env, req, options)

        sum = 0.0
        for t in tickets:
            try:
                sum += float(t[self.total_field])
            except:
                pass

        return "%g" % round(sum, 2)
