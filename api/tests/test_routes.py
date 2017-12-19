"""
Testing some routes which should be accessible.

.. codeauthor:: Christian Meter <meter@cs.uni-duesseldorf.de>
"""

from .lib import json_response_ok


def test_discussion_support():
    json_response_ok("cat-or-dog/support/2/12?history=/attitude/2-/justify/2/t")


def test_discussion_reactions():
    json_response_ok("cat-or-dog/reaction/4/rebut/5?history=/attitude/3-/justify/3/t")
    json_response_ok("cat-or-dog/reaction/8/undermine/10?history=/attitude/4-/justify/4/t")


def test_discussion_justify():
    json_response_ok("cat-or-dog/justify/10/t/undermine?history=/attitude/4-/justify/4/t-/reaction/8/undermine/10")
