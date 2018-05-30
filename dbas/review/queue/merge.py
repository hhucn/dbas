# Adaptee for the merge queue
import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerMerge, ReviewMerge, \
    StatementReplacementsByPremiseGroupMerge, PremiseGroupMerged, Argument, PremiseGroup, Premise, Issue, \
    ReviewMergeValues, Statement
from dbas.handler.statements import set_statement
from dbas.logger import logger
from dbas.review import rep_reason_success_flag, rep_reason_bad_flag
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import min_difference, max_votes, add_vote_for
from dbas.review.reputation import add_reputation_for
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_info_popup_to_socketio


class MergeQueue(QueueABC):
    def get_queue_information(self):
        pass

    def add_vote(self, db_user: User, db_review: ReviewMerge, is_okay: bool, main_page: str, translator: Translator,
                 **kwargs):
        """

        :param db_user:
        :param db_review:
        :param is_okay:
        :param main_page:
        :param translator:
        :param kwargs:
        :return:
        """
        logger('SplitQueue', 'main {}'.format(db_review.uid))

        db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
        # add new vote
        add_vote_for(db_user, db_review, is_okay, LastReviewerMerge)
        broke_limit = False

        # get all keep and delete votes
        count_of_merge, count_of_keep = self.get_review_count(db_review.uid)
        logger('SplitQueue', 'result ' + str(count_of_merge) + ':' + str(count_of_keep))

        # do we reached any limit?
        reached_max = max(count_of_merge, count_of_keep) >= max_votes
        if reached_max:
            if count_of_merge > count_of_keep:  # split pgroup
                logger('SplitQueue', 'max reached for review {}'.format(db_review.uid))
                self.__merge_premisegroup(db_review)
                add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
            else:  # just close the review
                logger('SplitQueue', 'max reached / forget about review {}'.format(db_review.uid))
                add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_keep - count_of_merge >= min_difference:  # just close the review
            logger('SplitQueue', 'vote says forget about review {}'.format(db_review.uid))
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_bad_flag)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_merge - count_of_keep >= min_difference:  # split pgroup
            logger('SplitQueue', 'vote says merge for review {}'.format(db_review.uid))
            self.__merge_premisegroup(db_review)
            add_rep, broke_limit = add_reputation_for(db_user_created_flag, rep_reason_success_flag)
            db_review.set_executed(True)
            db_review.update_timestamp()

        DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()

        if broke_limit:
            send_request_for_info_popup_to_socketio(db_user_created_flag.nickname,
                                                    translator.get(_.youAreAbleToReviewNow),
                                                    main_page + '/review')

        return True

    @staticmethod
    def __merge_premisegroup(db_review: ReviewMerge):
        """
        Merges a premisegroup into the items, which are mapped with the given review

        :param db_review: ReviewSplit.uid
        :return: None
        """
        db_values = DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=db_review.uid).all()
        db_old_premises = DBDiscussionSession.query(Premise).filter_by(
            premisegroup_uid=db_review.premisegroup_uid).all()
        db_issue = DBDiscussionSession.query(Issue).get(db_old_premises[0].issue_uid)
        db_first_old_statement = DBDiscussionSession.query(Statement).get(db_old_premises[0].uid)
        discussion_lang = db_first_old_statement.lang
        db_user = DBDiscussionSession.query(User).get(db_review.detector_uid)

        if db_values:
            logger('SplitQueue', 'merge given premisegroup with the mapped, new statements')
            texts = [values.content for values in db_values]
            translator_discussion = Translator(discussion_lang)
            new_text = ' {} '.format(translator_discussion.get(_.aand)).join(texts)
        else:
            logger('SplitQueue', 'just merge the premisegroup')
            new_text = DBDiscussionSession.query(PremiseGroup).get(db_review.premisegroup_uid).get_text()

        # now we have new text as a variable, let's set the statement
        new_statement, tmp = set_statement(new_text, db_user, db_first_old_statement.is_position, db_issue)

        # new premisegroup for the statement
        db_new_premisegroup = PremiseGroup(author=db_user.uid)
        DBDiscussionSession.add(db_new_premisegroup)
        DBDiscussionSession.flush()

        # new premise
        db_new_premise = Premise(db_new_premisegroup.uid, new_statement.uid, False, db_user.uid, db_issue.uid)
        DBDiscussionSession.add(db_new_premise)
        DBDiscussionSession.flush()
        logger('SplitQueue',
               'Added new premise {} with pgroup {}'.format(db_new_premise.uid, db_new_premisegroup.uid))

        # swap the premisegroup occurence in every argument
        db_arguments = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=db_review.premisegroup_uid).all()
        for argument in db_arguments:
            logger('SplitQueue',
                   'Reset argument {} from pgroup {} to new pgroup {}'.format(argument.uid, argument.premisegroup_uid,
                                                                              db_new_premisegroup.uid))
            argument.set_premisegroup(db_new_premisegroup.uid)
            DBDiscussionSession.add(argument)
            DBDiscussionSession.flush()

        # add swap to database
        DBDiscussionSession.add(PremiseGroupMerged(db_review.uid, db_review.premisegroup_uid, db_new_premisegroup.uid))

        # swap the conclusion in every argument
        old_statement_ids = [p.statement_uid for p in db_old_premises]
        for old_statement_id in old_statement_ids:
            db_arguments = DBDiscussionSession.query(Argument).filter_by(conclusion_uid=old_statement_id).all()
            for argument in db_arguments:
                logger('SplitQueue',
                       'Reset arguments {} from conclusion {} to new merges statement {}'.format(argument.uid,
                                                                                                 argument.conclusion_uid,
                                                                                                 new_statement.uid))
                argument.set_conclusion(new_statement.uid)
                DBDiscussionSession.add(argument)
                DBDiscussionSession.add(
                    StatementReplacementsByPremiseGroupMerge(db_review.uid, old_statement_id, new_statement.uid))
                DBDiscussionSession.flush()

        # finish
        DBDiscussionSession.flush()
        transaction.commit()

    def add_review(self, db_user: User):
        pass

    def get_review_count(self, review_uid: int):
        db_reviews = DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(should_merge=True).count()
        count_of_not_okay = db_reviews.filter_by(should_merge=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User):
        pass

    def revoke_ballot(self, db_user: User):
        pass
