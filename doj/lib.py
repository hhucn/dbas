# Common library for Admin Component
#
# @author Tobias Krauthoff
# @email krautho66@cs.uni-duesseldorf.de


from dbas.query_wrapper import get_not_disabled_statement_as_query, get_not_disabled_arguments_as_query
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Premise


def get_map():
    """
    Returns type of tables column

    :param table: current table
    :param col_name: current columns name
    :return: String or raise NameError
    """
    db_statements = get_not_disabled_statement_as_query().all()
    db_arguments = get_not_disabled_arguments_as_query().all()

    nodes = [s.uid for s in db_statements]

    inferences = []
    undercuts = []

    # getting all arguments
    for arg in db_arguments:
        # getting premises of current argument
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisesgroup_uid=arg.premisesgroup_uid).all()
        premises = [p.statement_uid for p in db_premises]

        if arg.conclusion_uid is None:
            # undercut
            undercuts.append({'id': arg.uid,
                              'premises': premises,
                              'conclusion': arg.conclusion_uid})
        else:
            # not an undercut
            inferences.append({'id': arg.uid,
                               'premises': premises,
                               'conclusion': arg.argument_uid})

    return {'nodes': nodes,
            'inferences': inferences,
            'undercuts': undercuts}
