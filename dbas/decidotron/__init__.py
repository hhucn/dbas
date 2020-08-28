import os
import sys

import transaction
from pyramid.paster import get_appsettings, setup_logging

from dbas.database import DiscussionBase, DBDiscussionSession, get_dbas_db_configuration
from dbas.database.discussion_model import Issue, User, DecisionProcess, Language


def usage(argv):
    """
    Initialize the usage for the database by the given ini-file

    :param argv: standard argv
    :return: None
    """
    cmd = os.path.basename(argv[0])
    print('usage: %s <config_uri>\n(example: "%s development.ini")' % (cmd, cmd))
    sys.exit(1)


def init_budget_discussion(argv=sys.argv):
    budget = 20000_00  # 20.000€ in cents

    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)

    discussion_engine = get_dbas_db_configuration(settings=get_appsettings(config_uri))
    DBDiscussionSession.remove()
    DBDiscussionSession.configure(bind=discussion_engine)
    DiscussionBase.metadata.create_all(discussion_engine)

    with transaction.manager:
        issue = Issue(title="Distribution of quality improvement funds in the study course",
                      info="There are 20,000 euros available that we can distribute in the study course",
                      slug="verteilung-von-qualitatsverbesserungsmitteln",
                      long_info="""
                      The Scientific Institution of Computer Science would like to give the student body the opportunity to decide on so-called quality improvement funds over 20,000 €. For this purpose, proposals with a cost estimate can be submitted here, which you can then discuss.
                      """,
                      author=User.by_nickname("Björn"),
                      language=Language.by_locale("en"))
        DBDiscussionSession.add(issue)
        DBDiscussionSession.flush()
        DBDiscussionSession.add(DecisionProcess(issue, budget, "http://0.0.0.0:3000"))

        transaction.commit()
