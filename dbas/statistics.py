import argparse
import json
import os
import sys
from collections import Counter

from sqlalchemy import engine_from_config

from dbas import get_db_environs, load_discussion_database
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import StatementToIssue, TextVersion, Issue, Argument, SeenArgument, Premise

# Set up the database session. Without this, you can not use DBDiscussionSession!
settings = {}  # Add console script specific configuration here.
settings.update(get_db_environs("sqlalchemy.discussion.url", db_name="discussion"))

discussion_engine = engine_from_config(settings, "sqlalchemy.discussion.")
load_discussion_database(discussion_engine)


def get_all_participating_users_of_issue() -> dict:
    issues_dict = {}
    issues_uids = [el.uid for el in
                   DBDiscussionSession.query(Issue).all()]

    for issue_uid in issues_uids:

        issues_statements_uids = [el.statement_uid for el in
                                  DBDiscussionSession.query(StatementToIssue).filter_by(issue_uid=issue_uid).all()]

        participating_users = []
        for statement in issues_statements_uids:
            participating_users += [
                "User_" + str(
                    DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement).first().author_uid)
            ]
        if len(participating_users) > 0:
            issues_dict["Issue_" + str(issue_uid)] = list(set(participating_users))

    return issues_dict


def get_statements_which_have_been_used_more_than_once() -> dict:
    issues_uids = [el.uid for el in
                   DBDiscussionSession.query(Issue).all()]

    statements_per_issue = {}
    for issue_uid in issues_uids:
        statements = [el.statement_uid for el in
                      DBDiscussionSession.query(Premise).filter_by(issue_uid=issue_uid).all()]
        statements_per_issue["Issue_" + str(issue_uid)] = statements

    for key in statements_per_issue.keys():
        statements = Counter(statements_per_issue[key])
        statement_count = {}
        for statement_key in statements.keys():
            statement_count["Statement_uid_" + str(statement_key)] = statements[statement_key]
        statements_per_issue[key] = statement_count

    return statements_per_issue


def get_all_statements_for_user_of_issues() -> dict:
    participation_dict = {}
    issues = get_all_participating_users_of_issue()
    for issue_uid in issues.keys():
        participating_users = issues[issue_uid]
        if len(participating_users) == 0:
            continue
        issues_statements_uids = [el.statement_uid for el in DBDiscussionSession.query(StatementToIssue).filter_by(
            issue_uid=int(issue_uid.replace("Issue_", ""))).all()]

        all_statements_of_participating_users = []
        for statement in issues_statements_uids:
            res = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=statement).first().author_uid
            if "User_" + str(res) in participating_users:
                all_statements_of_participating_users += ["User_" + str(res) + "_number_of_statements"]

        participation_dict[issue_uid] = dict(Counter(all_statements_of_participating_users))

    return participation_dict


def get_amount_of_support_and_attack_per_issue() -> dict:
    relations_dict = {}
    issues = get_all_participating_users_of_issue()
    for issue_uid in issues.keys():
        if len(issues[issue_uid]) == 0:
            continue
        arguments_relations = ["support" if el.is_supportive else "attack" for el in
                               DBDiscussionSession.query(Argument).filter_by(
                                   issue_uid=int(issue_uid.replace("Issue_", ""))).all()
                               if not el.is_disabled]
        relations_dict[issue_uid] = dict(Counter(arguments_relations))

    return relations_dict


def get_amount_of_support_and_attack_per_issue_per_user() -> dict:
    issues_dict = {}
    issues = get_all_participating_users_of_issue()
    for issue_uid in issues.keys():
        if len(issues[issue_uid]) == 0:
            continue
        user_dict = {}
        for user in issues[issue_uid]:
            arguments_relations = ["support" if el.is_supportive else "attack" for el in
                                   DBDiscussionSession.query(Argument).filter_by(
                                       issue_uid=int(issue_uid.replace("Issue_", ""))).filter_by(
                                       author_uid=int(user.replace("User_", ""))).all()
                                   if not el.is_disabled]

            res = dict(Counter(arguments_relations))
            user_dict[user] = res

        issues_dict[issue_uid] = user_dict

    return issues_dict


def get_number_of_seen_arguments_per_user_per_issue() -> dict:
    all_seen_arguments = [(el.user_uid, el.argument_uid) for el in DBDiscussionSession.query(SeenArgument).all()]
    all_arguments_per_issue = [(el.uid, el.issue_uid) for el in DBDiscussionSession.query(Argument).all()]
    all_seen_arguments_per_issue = []
    for user_uid, argument_uid_seen in all_seen_arguments:
        for argument_uid, issue_uid in all_arguments_per_issue:
            if argument_uid_seen == argument_uid:
                all_seen_arguments_per_issue += [(user_uid, argument_uid, issue_uid)]
    res = {}
    issue_uids = list(set([x[2] for x in all_seen_arguments_per_issue]))
    for issue_uid in issue_uids:
        if "Issue_" + str(issue_uid) not in res.keys():
            res["Issue_" + str(issue_uid)] = {}
        for user_uid, argument_uid, issue_uid_to_match in all_seen_arguments_per_issue:
            if issue_uid_to_match == issue_uid:
                if "User_" + str(user_uid) not in res["Issue_" + str(issue_uid)]:
                    res["Issue_" + str(issue_uid)]["User_" + str(user_uid)] = 0
                res["Issue_" + str(issue_uid)]["User_" + str(user_uid)] += 1
    return res


def write_file_to(prefix: str, name: str, input: str):
    path = "./experiment_results/"
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open("{}{}_{}.json".format(path, prefix, name), "w") as json_file:
        json.dump(input, json_file, indent=4)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("run",
                        help="To run this script, use \"docker exec dbas_web_1 python dbas/statistics.py <prefix> \" ")
    args = parser.parse_args()
    if len(sys.argv) != 2:
        print("Add the prefix as argument for this script")
        sys.exit(1)
    prefix = str(sys.argv[1])

    write_file_to(prefix, "participating_user", get_all_participating_users_of_issue())
    write_file_to(prefix, "all_statements_per_user", get_all_statements_for_user_of_issues())
    write_file_to(prefix, "amount_of_supports_attacks_per_issue", get_amount_of_support_and_attack_per_issue())
    write_file_to(prefix, "amount_of_supports_attacks_per_user", get_amount_of_support_and_attack_per_issue_per_user())
    write_file_to(prefix, "number_of_seen_arguments_per_user", get_number_of_seen_arguments_per_user_per_issue())
    write_file_to(prefix, "reused_statements", get_statements_which_have_been_used_more_than_once())
