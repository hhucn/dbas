# Adaptee for the split queue.
import random

import transaction
from beaker.session import Session

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerSplit, ReviewSplit, ReviewSplitValues, Premise, Issue, \
    Statement, PremiseGroup, PremiseGroupSplitted, Argument, ArgumentsAddedByPremiseGroupSplit, \
    StatementReplacementsByPremiseGroupSplit
from dbas.handler.statements import set_statement
from dbas.lib import get_text_for_premisegroup_uid
from dbas.logger import logger
from dbas.review.queue import max_votes, min_difference, key_split
from dbas.review.lib import get_reputation_reason_by_action
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import add_vote_for, add_reputation_and_check_review_access, \
    get_all_allowed_reviews_for_user, get_issues_for_statement_uids, get_reporter_stats_for_review
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator


class SplitQueue(QueueABC):

    def __init__(self):
        super().__init__()
        self.key = key_split

    def key(self, key=None):
        """

        :param key:
        :return:
        """
        if not key:
            return key
        else:
            self.key = key

    def get_queue_information(self, db_user: User, session: Session, application_url: str, translator: Translator):
        """
        Setup the subpage for the split queue

        :param db_user: User
        :param session: session of current webserver request
        :param application_url: current url of the app
        :param translator: Translator
        :return: dict()
        """
        logger('SplitQueue', 'main')
        all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{self.key}', db_user, ReviewSplit,
                                                        LastReviewerSplit)

        extra_info = ''
        # if we have no reviews, try again with fewer restrictions
        if not all_rev_dict['reviews']:
            logger('SplitQueue', 'no unseen reviews')
            all_rev_dict['already_seen_reviews'] = list()
            extra_info = 'already_seen' if not all_rev_dict['first_time'] else ''
            db_reviews = DBDiscussionSession.query(ReviewSplit).filter(ReviewSplit.is_executed == False,
                                                                       ReviewSplit.detector_uid != db_user.uid)
            if len(all_rev_dict['already_voted_reviews']) > 0:
                logger('SplitQueue', 'everything was seen')
                db_reviews = db_reviews.filter(~ReviewSplit.uid.in_(all_rev_dict['already_voted_reviews']))
                all_rev_dict['reviews'] = db_reviews.all()

        if not all_rev_dict['reviews']:
            logger('SplitQueue', 'no reviews')
            return {
                'stats': None,
                'text': None,
                'reason': None,
                'issue': None,
                'extra_info': None,
                'issue_titles': [],
                'session': session
            }

        rnd_review = random.choice(all_rev_dict['reviews'])
        premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=rnd_review.premisegroup_uid).all()
        text = get_text_for_premisegroup_uid(rnd_review.premisegroup_uid)
        db_review_values = DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=rnd_review.uid).all()
        if db_review_values:
            splitted_text = [rsv.content for rsv in db_review_values]
            pgroup_only = False
        else:
            splitted_text = [premise.get_text() for premise in premises]
            pgroup_only = True
        issue = DBDiscussionSession.query(Issue).get(premises[0].issue_uid).title
        reason = translator.get(_.argumentFlaggedBecauseSplit)

        statement_uids = [p.statement_uid for p in premises]
        issue_titles = [issue.title for issue in get_issues_for_statement_uids(statement_uids)]

        stats = get_reporter_stats_for_review(rnd_review, translator.get_lang(), application_url)

        all_rev_dict['already_seen_reviews'].append(rnd_review.uid)
        session[f'already_seen_{self.key}'] = all_rev_dict['already_seen_reviews']

        return {
            'stats': stats,
            'text': text,
            'splitted_text': splitted_text,
            'reason': reason,
            'issue': issue,
            'extra_info': extra_info,
            'pgroup_only': pgroup_only,
            'issue_titles': issue_titles,
            'session': session
        }

    def add_vote(self, db_user: User, db_review: ReviewSplit, is_okay: bool, application_url: str,
                 translator: Translator,
                 **kwargs):
        """

        :param db_user:
        :param db_review:
        :param is_okay:
        :param application_url:
        :param translator:
        :param kwargs:
        :return:
        """
        logger('SplitQueue', 'main {}'.format(db_review.uid))
        db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
        rep_reason = None

        # add new vote
        add_vote_for(db_user, db_review, is_okay, LastReviewerSplit)

        # get all keep and delete votes
        count_of_split, count_of_keep = self.get_review_count(db_review.uid)

        # do we reached any limit?
        reached_max = max(count_of_split, count_of_keep) >= max_votes
        if reached_max:
            if count_of_split > count_of_keep:  # split pgroup
                self.__split_premisegroup(db_review)
                rep_reason = get_reputation_reason_by_action('success_flag')
            else:  # just close the review
                rep_reason = get_reputation_reason_by_action('bad_flag')
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_keep - count_of_split >= min_difference:  # just close the review
            rep_reason = get_reputation_reason_by_action('bad_flag')
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_split - count_of_keep >= min_difference:  # split pgroup
            self.__split_premisegroup(db_review)
            rep_reason = get_reputation_reason_by_action('success_flag')
            db_review.set_executed(True)
            db_review.update_timestamp()

        add_reputation_and_check_review_access(db_user_created_flag, rep_reason, application_url, translator)
        DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()

        return True

    @staticmethod
    def __split_premisegroup(db_review: ReviewSplit):
        """
        Splits a premisegroup into the items, which are mapped with the given review

        :param db_review: ReviewSplit.uid
        :return: None
        """
        db_values = DBDiscussionSession.query(ReviewSplitValues).filter_by(review_uid=db_review.uid).all()
        db_old_premises = DBDiscussionSession.query(Premise).filter_by(
            premisegroup_uid=db_review.premisegroup_uid).all()
        db_issue = DBDiscussionSession.query(Issue).get(db_old_premises[0].issue_uid)
        db_old_statement_ids = [p.statement_uid for p in db_old_premises]
        db_first_old_statement = DBDiscussionSession.query(Statement).get(db_old_premises[0].uid)
        db_user = DBDiscussionSession.query(User).get(db_review.detector_uid)

        if db_values:
            logger('SplitQueue', 'split given premisegroup into the mapped, new statements')
            db_statements = []
            for value in db_values:
                new_statement, tmp = set_statement(value.content, db_user, db_first_old_statement.is_position, db_issue)
                db_statements.append(new_statement)
        else:
            logger('SplitQueue', 'just split the premisegroup')
            db_statements = DBDiscussionSession.query(Statement).filter(Statement.uid.in_(db_old_statement_ids)).all()

        # new premisegroups, for each statement a new one
        new_premisegroup_ids = []
        new_premise_ids = []
        for statement in db_statements:
            db_new_premisegroup = PremiseGroup(author=db_user.uid)
            DBDiscussionSession.add(db_new_premisegroup)
            DBDiscussionSession.flush()
            new_premisegroup_ids.append(db_new_premisegroup.uid)

            db_new_premise = Premise(db_new_premisegroup.uid, statement.uid, False, db_user.uid, db_issue.uid)
            DBDiscussionSession.add(db_new_premise)
            DBDiscussionSession.flush()
            new_premise_ids.append(db_new_premise.uid)

            # note new added pgroup
            DBDiscussionSession.add(
                PremiseGroupSplitted(db_review.uid, db_review.premisegroup_uid, db_new_premisegroup.uid))

        # swap the premisegroup occurence in every argument and add new arguments for the new premises
        db_arguments = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=db_review.premisegroup_uid).all()
        for argument in db_arguments:
            argument.set_premisegroup(new_premisegroup_ids[0])
            DBDiscussionSession.add(argument)

            for uid in new_premisegroup_ids[1:]:
                argument = Argument(uid, argument.is_supportive, argument.author_uid, argument.issue_uid,
                                    argument.conclusion_uid, argument.argument_uid, argument.is_disabled)
                DBDiscussionSession.add(argument)
                DBDiscussionSession.flush()
                DBDiscussionSession.add(ArgumentsAddedByPremiseGroupSplit(db_review.uid, argument.uid))

        # swap the conclusion in every argument
        new_statements_uids = [s.uid for s in db_statements]
        for old_statement_uid in db_old_statement_ids:
            db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=old_statement_uid).all()
            for argument in db_arguments:
                argument.set_conclusion(new_statements_uids[0])
                DBDiscussionSession.add(argument)
                DBDiscussionSession.add(
                    StatementReplacementsByPremiseGroupSplit(db_review.uid, old_statement_uid, new_statements_uids[0]))
                DBDiscussionSession.flush()

                for statement_uid in new_statements_uids[1:]:
                    db_argument = Argument(argument.premisegroup_uid, argument.is_supportive, argument.author_uid,
                                           argument.issue_uid, statement_uid, argument.argument_uid,
                                           argument.is_disabled)
                    DBDiscussionSession.add(db_argument)
                    DBDiscussionSession.add(
                        StatementReplacementsByPremiseGroupSplit(db_review.uid, old_statement_uid, statement_uid))
                    DBDiscussionSession.flush()

        # finish
        DBDiscussionSession.flush()
        transaction.commit()

    def add_review(self, db_user: User):
        pass

    def get_review_count(self, review_uid: int):
        db_reviews = DBDiscussionSession.query(LastReviewerSplit).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(should_split=True).count()
        count_of_not_okay = db_reviews.filter_by(should_split=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User):
        pass

    def revoke_ballot(self, db_user: User):
        pass
