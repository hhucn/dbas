# Adaptee for the merge queue
import logging
import random
import transaction
from beaker.session import Session
from typing import Union, Tuple

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, LastReviewerMerge, ReviewMerge, \
    StatementReplacementsByPremiseGroupMerge, PremiseGroupMerged, Argument, PremiseGroup, Premise, Issue, \
    ReviewMergeValues, Statement, ReviewCanceled
from dbas.handler.statements import set_statement
from dbas.review import FlaggedBy, txt_len_history_page
from dbas.review.queue import max_votes, min_difference, key_merge
from dbas.review.queue.abc_queue import QueueABC
from dbas.review.queue.lib import get_all_allowed_reviews_for_user, get_issues_for_statement_uids, \
    get_reporter_stats_for_review, undo_premisegroups, add_vote_for, get_user_dict_for_review
from dbas.review.reputation import get_reason_by_action, ReputationReasons, \
    add_reputation_and_send_popup
from dbas.strings.keywords import Keywords as _
from dbas.strings.translator import Translator

LOG = logging.getLogger(__name__)


class MergeQueue(QueueABC):

    def __init__(self):
        super().__init__()
        self.key = key_merge

    def key(self, key=None):
        """
        Getter/setter for the key of the queue which is just the name

        :param key:
        :return:
        """
        if not key:
            return self.key
        else:
            self.key = key

    def get_queue_information(self, db_user: User, session: Session, application_url: str, translator: Translator):
        """
        Setup the subpage for the merge queue

        :param db_user: User
        :param session: session of current webserver request
        :param application_url: current url of the app
        :param translator: Translator
        :return: dict()
        """
        LOG.debug("Setting up the subpage for merge queue")
        all_rev_dict = get_all_allowed_reviews_for_user(session, f'already_seen_{self.key}', db_user, ReviewMerge,
                                                        LastReviewerMerge)

        extra_info = ''
        # if we have no reviews, try again with fewer restrictions
        if not all_rev_dict['reviews']:
            LOG.debug("No unseen reviews")
            all_rev_dict['already_seen_reviews'] = list()
            extra_info = 'already_seen' if not all_rev_dict['first_time'] else ''
            db_reviews = DBDiscussionSession.query(ReviewMerge).filter(ReviewMerge.is_executed == False,
                                                                       ReviewMerge.detector_uid != db_user.uid)
            if len(all_rev_dict['already_voted_reviews']) > 0:
                LOG.debug("Every review-case was seen")
                db_reviews = db_reviews.filter(~ReviewMerge.uid.in_(all_rev_dict['already_voted_reviews']))
            all_rev_dict['reviews'] = db_reviews.all()

        if not all_rev_dict['reviews']:
            LOG.debug("No reviews present")
            return {
                'stats': None,
                'text': None,
                'reason': None,
                'issue_titles': [],
                'extra_info': None,
                'session': session
            }

        rnd_review = random.choice(all_rev_dict['reviews'])
        premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=rnd_review.premisegroup_uid).all()
        text = [premise.get_text() for premise in premises]
        db_review_values = DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=rnd_review.uid).all()

        discussion_lang = DBDiscussionSession.query(Statement).get(premises[0].uid).lang
        translator_discussion = Translator(discussion_lang)

        if db_review_values:
            aand = translator_discussion.get(_.aand)
            merged_text = ' {} '.format(aand).join([rsv.content for rsv in db_review_values])
            pgroup_only = False
        else:
            merged_text = DBDiscussionSession.query(PremiseGroup).get(rnd_review.premisegroup_uid).get_text()
            pgroup_only = True

        statement_uids = [p.statement_uid for p in premises]
        issue_titles = [issue.title for issue in get_issues_for_statement_uids(statement_uids)]
        reason = translator.get(_.argumentFlaggedBecauseMerge)

        stats = get_reporter_stats_for_review(rnd_review, translator.get_lang(), application_url)

        all_rev_dict['already_seen_reviews'].append(rnd_review.uid)
        session[f'already_seen_{self.key}'] = all_rev_dict['already_seen_reviews']

        return {
            'stats': stats,
            'text': text,
            'merged_text': merged_text,
            'reason': reason,
            'issue_titles': issue_titles,
            'extra_info': extra_info,
            'pgroup_only': pgroup_only,
            'session': session
        }

    def add_vote(self, db_user: User, db_review: ReviewMerge, is_okay: bool, application_url: str,
                 translator: Translator,
                 **kwargs):
        """
        Adds an vote for this queue. If any (positive or negative) limit is reached, the flagged elements will be merged
        together

        :param db_user: current user who votes
        :param db_review: the review, which is voted vor
        :param is_okay: True, if the element is rightly flagged
        :param application_url: the app url
        :param translator: a instance of a translator
        :param kwargs: optional, keyworded arguments
        :return:
        """
        LOG.debug("Adding a vote for %s", db_review.uid)
        db_user_created_flag = DBDiscussionSession.query(User).get(db_review.detector_uid)
        rep_reason = None

        # add new vote
        add_vote_for(db_user, db_review, is_okay, LastReviewerMerge)

        # get all keep and delete votes
        count_of_merge, count_of_keep = self.get_review_count(db_review.uid)

        # do we reached any limit?
        reached_max = max(count_of_merge, count_of_keep) >= max_votes
        if reached_max:
            if count_of_merge > count_of_keep:  # split pgroup
                self.__merge_premisegroup(db_review)
                rep_reason = get_reason_by_action(ReputationReasons.success_flag)
            else:  # just close the review
                rep_reason = get_reason_by_action(ReputationReasons.bad_flag)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_keep - count_of_merge >= min_difference:  # just close the review
            rep_reason = get_reason_by_action(ReputationReasons.bad_flag)
            db_review.set_executed(True)
            db_review.update_timestamp()

        elif count_of_merge - count_of_keep >= min_difference:  # split pgroup
            self.__merge_premisegroup(db_review)
            rep_reason = get_reason_by_action(ReputationReasons.success_flag)
            db_review.set_executed(True)
            db_review.update_timestamp()

        if rep_reason:
            add_reputation_and_send_popup(db_user_created_flag, rep_reason, application_url, translator)
            DBDiscussionSession.add(db_review)
        DBDiscussionSession.flush()
        transaction.commit()

        return True

    def add_review(self, db_user: User):
        """
        Just adds a new element

        :param db_user: current user
        :return:
        """
        pass

    def get_review_count(self, review_uid: int) -> Tuple[int, int]:
        """
        Returns total pro and con count for the given review.uid

        :param review_uid: Review.uid
        :return:
        """
        db_reviews = DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=review_uid)
        count_of_okay = db_reviews.filter_by(should_merge=True).count()
        count_of_not_okay = db_reviews.filter_by(should_merge=False).count()

        return count_of_okay, count_of_not_okay

    def cancel_ballot(self, db_user: User, db_review: ReviewMerge):
        """
        Cancels any ongoing vote

        :param db_user: current user
        :param db_review: any element from a review queue
        :return:
        """
        DBDiscussionSession.query(ReviewMerge).get(db_review.uid).set_revoked(True)
        DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=db_review.uid).delete()
        DBDiscussionSession.query(PremiseGroupMerged).filter_by(review_uid=db_review.uid).delete()
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_merge: db_review.uid},
                                            was_ongoing=True)

        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()
        return True

    def revoke_ballot(self, db_user: User, db_review: ReviewMerge):
        """
        Revokes/Undo the implications of any successfull reviewed element

        :param db_user:
        :param db_review:
        :return:
        """
        db_review = DBDiscussionSession.query(ReviewMerge).get(db_review.uid)
        db_review.set_revoked(True)
        db_pgroup_merged = DBDiscussionSession.query(PremiseGroupMerged).filter_by(review_uid=db_review.uid).all()
        replacements = DBDiscussionSession.query(StatementReplacementsByPremiseGroupMerge).filter_by(
            review_uid=db_review.uid).all()
        undo_premisegroups(db_pgroup_merged, replacements)
        DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=db_review.uid).delete()
        DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=db_review.uid).delete()
        DBDiscussionSession.query(StatementReplacementsByPremiseGroupMerge).filter_by(review_uid=db_review.uid).delete()
        db_review_canceled = ReviewCanceled(author=db_user.uid, review_data={key_merge: db_review.uid})
        DBDiscussionSession.add(db_review_canceled)
        DBDiscussionSession.flush()
        transaction.commit()
        return True

    def element_in_queue(self, db_user: User, **kwargs) -> Union[None, FlaggedBy]:
        """
        Check if the element described by kwargs is in any queue. Return a FlaggedBy object or none

        :param db_user: current user
        :param kwargs: "magic" -> atm keywords like argument_uid, statement_uid and premisegroup_uid. Please update
        this!
        """
        db_review = DBDiscussionSession.query(ReviewMerge).filter_by(
            premisegroup_uid=kwargs.get('premisegroup_uid'),
            is_executed=False,
            is_revoked=False)
        if db_review.filter_by(detector_uid=db_user.uid).count() > 0:
            return FlaggedBy.user
        if db_review.count() > 0:
            return FlaggedBy.other
        return None

    def get_history_table_row(self, db_review: ReviewMerge, entry, **kwargs):
        """
        Returns a row the the history/ongoing page for the given review element

        :param db_review: current element which is the source of the row
        :param entry: dictionary with some values which were already set
        :param kwargs: "magic" -> atm keywords like is_executed, short_text and full_text. Please update this!
        :return:
        """
        db_premises = DBDiscussionSession.query(Premise).filter_by(premisegroup_uid=db_review.premisegroup_uid).all()
        oem_fulltext = str([DBDiscussionSession.query(Statement).get(p.statement_uid).get_text() for p in db_premises])
        full_text = oem_fulltext
        db_values = DBDiscussionSession.query(ReviewMergeValues).filter_by(review_uid=db_review.uid).all()
        if db_values:
            full_text = str([value.content for value in db_values])
        full_text = ' and '.join(full_text)
        entry['argument_oem_shorttext'] = (oem_fulltext[0:txt_len_history_page] + '...') if len(
            oem_fulltext) > txt_len_history_page else oem_fulltext
        entry['argument_oem_fulltext'] = oem_fulltext
        entry['argument_shorttext'] = (full_text[0:txt_len_history_page] + '...') if len(
            full_text) > txt_len_history_page else full_text
        entry['argument_fulltext'] = full_text
        return entry

    def get_text_of_element(self, db_review: ReviewMerge) -> str:
        """
        Returns full text of the given element

        :param db_review: current review element
        :return:
        """
        return DBDiscussionSession.query(PremiseGroup).get(db_review.premisegroup_uid).get_text()

    def get_all_votes_for(self, db_review: ReviewMerge, application_url: str) -> Tuple[list, list]:
        """
        Returns all pro and con votes for the given element

        :param db_review: current review element
        :param application_url: The applications URL
        """
        db_all_votes = DBDiscussionSession.query(LastReviewerMerge).filter_by(review_uid=db_review.uid)
        pro_votes = db_all_votes.filter_by(should_merge=True).all()
        con_votes = db_all_votes.filter_by(should_merge=False).all()

        pro_list = [get_user_dict_for_review(pro.reviewer_uid, application_url) for pro in pro_votes]
        con_list = [get_user_dict_for_review(con.reviewer_uid, application_url) for con in con_votes]

        return pro_list, con_list

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
            LOG.debug("Merge was given premisegroup with the mapped, new statements")
            texts = [values.content for values in db_values]
            translator_discussion = Translator(discussion_lang)
            new_text = ' {} '.format(translator_discussion.get(_.aand)).join(texts)
        else:
            LOG.debug("Just merge the premisegroup")
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
        LOG.debug("Added new premise %s with pgroup %s", db_new_premise.uid, db_new_premisegroup.uid)

        # swap the premisegroup occurence in every argument
        db_arguments = DBDiscussionSession.query(Argument).filter_by(premisegroup_uid=db_review.premisegroup_uid).all()
        for argument in db_arguments:
            LOG.debug("Reset argument %s from pgroup %s to new pgroup %s", argument.uid, argument.premisegroup_uid,
                      db_new_premisegroup.uid)
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
                LOG.debug("Reset arguments %s from conclusions %s to new merges statement %s", argument.uid,
                          argument.conclusion_uid, new_statement.uid)
                argument.set_conclusion(new_statement.uid)
                DBDiscussionSession.add(argument)
                DBDiscussionSession.add(
                    StatementReplacementsByPremiseGroupMerge(db_review.uid, old_statement_id, new_statement.uid))
                DBDiscussionSession.flush()

        # finish
        DBDiscussionSession.flush()
        transaction.commit()
