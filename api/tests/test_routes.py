"""
Testing some routes which should be accessible.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""

from .lib import json_response_ok


def test_discussion_support():
    json_response_ok("town-has-to-cut-spending/support/40/39?history=/attitude/37-/justify/37/t")


def test_discussion_reactions():
    json_response_ok("town-has-to-cut-spending/reaction/39/rebut/65?history=/attitude/37-/justify/37/t-/support/40/39")
    json_response_ok("cat-or-dog/reaction/8/undermine/10?history=/attitude/4-/justify/4/t")


def test_discussion_justify():
    json_response_ok("cat-or-dog/justify/10/t/undermine?history=/attitude/4-/justify/4/t-/reaction/8/undermine/10")
