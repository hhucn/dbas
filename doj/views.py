"""
Introducing an interface for DOJ.

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import json

import doj.lib as lib
from cornice import Service
from dbas.logger import logger

#
# CORS configuration
#
cors_policy = dict(enabled=True,
                   headers=('Origin', 'X-Requested-With', 'Content-Type', 'Accept'),
                   origins=('*',),
                   max_age=42)


# =============================================================================
# SERVICES - Define services for several actions of D-BAS
# =============================================================================

main = Service(name='main_page',
               path='/',
               description="Export for DoJ",
               renderer='json',
               permission='everybody',  # or permission='use'
               cors_policy=cors_policy)


@main.get()
def main_doj():
    """

    """
    logger('- - - - - - - - - - - -', '- - - - - - - - - - - -', '- - - - - - - - - - - -')
    logger('DOJ', 'main', 'def')

    return json.dumps(lib.get_map(), True)
