import itertools
import unittest

import transaction

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import Argument, User, MarkedArgument
from dbas.lib import Relations
from dbas.strings import text_generator as tg
from dbas.strings.keywords import Keywords as _
from dbas.strings.lib import start_with_capital
from dbas.strings.text_generator import remove_punctuation
from dbas.strings.translator import Translator
from dbas.tests.utils import TestCaseWithConfig


class TestTextGenerator(TestCaseWithConfig):
    def setUp(self):
        super().setUp()
        self.premise = 'some premise text'
        self.conclusion = 'some conclusion text'
        self.confrontation = 'some confrontation text'
        self.maxDiff = None

    def test_get_text_for_add_premise_container(self):
        _t = Translator('en')

        for is_supportive in [True, False]:
            confrontation = start_with_capital(self.confrontation)
            undermine = _t.get(_.itIsFalseThat) + ' ' + self.premise
            support = _t.get(_.itIsTrueThat) if is_supportive else _t.get(_.itIsFalseThat)
            support += ' ' + self.conclusion + ' '
            support += _t.get(_.hold) if is_supportive else _t.get(_.doesNotHold)
            undercut = confrontation + ', ' + _t.get(_.butIDoNotBelieveCounterFor).format(self.conclusion)
            rebut = confrontation + ' '
            rebut += _t.get(_.iAcceptCounterThat) if is_supportive else _t.get(_.iAcceptArgumentThat)
            rebut += ' ' + self.conclusion

            results = {
                Relations.UNDERMINE: undermine + ' ...',
                Relations.SUPPORT: support + ' ...',
                Relations.UNDERCUT: undercut + ' ...',
                Relations.REBUT: rebut + ' ...',
                '': '',
            }

            for r in results:
                self.assertEqual(results[r],
                                 tg.get_text_for_add_premise_container('en', self.confrontation, self.premise,
                                                                       r, self.conclusion, is_supportive))

    def test_get_header_for_users_confrontation_response(self):
        arg = DBDiscussionSession.query(Argument).get(2)

        is_supportive = True
        redirect_from_jump = False
        results = {
            Relations.UNDERMINE: 'that {}some premise text{}',
            Relations.SUPPORT: '{}it is true that some conclusion text hold{}.',
            Relations.UNDERCUT: 'right, some premise text. {}But I do not believe that this is a argument for some conclusion text{}',
            Relations.REBUT: '{}right, some premise text, and I do accept that this is a counter-argument for some conclusion text. However, I have a much stronger argument for rejecting that some conclusion text.{}',
            '': ''
        }
        for r in results:
            user_msg, system_msg = tg.get_header_for_users_confrontation_response(arg, 'en', self.premise, r,
                                                                                  self.conclusion, True, is_supportive,
                                                                                  False, redirect_from_jump)
            self.assertEqual(user_msg, results[r])
            self.assertEqual(system_msg, '')

        is_supportive = False
        results.update({
            Relations.SUPPORT: '{}it is false that some conclusion text does not hold{}.',
            Relations.REBUT: '{}right, some premise text, and I do accept that this is an argument for some conclusion text. However, I have a much stronger argument for accepting that some conclusion text.{}',
        })
        for r in results:
            user_msg, system_msg = tg.get_header_for_users_confrontation_response(arg, 'en', self.premise, r,
                                                                                  self.conclusion, True, is_supportive,
                                                                                  False, redirect_from_jump)
            self.assertEqual(user_msg, results[r])
            self.assertEqual(system_msg, '')

        redirect_from_jump = True
        results.update({
            Relations.UNDERCUT: 'Maybe it is true that some premise text. {}But I do not believe that this is a argument for some conclusion text{}',
            Relations.REBUT: '{}Maybe it is true that some premise text, and I do accept that this is an argument for some conclusion text. However, I have a much stronger argument for accepting that some conclusion text.{}',
        })
        for r in results:
            user_msg, system_msg = tg.get_header_for_users_confrontation_response(arg, 'en', self.premise, r,
                                                                                  self.conclusion, True, is_supportive,
                                                                                  False, redirect_from_jump)
            self.assertEqual(user_msg, results[r])
            self.assertEqual(system_msg, '')

        is_supportive = True
        results.update({
            Relations.SUPPORT: '{}it is true that some conclusion text hold{}.',
            Relations.REBUT: '{}Maybe it is true that some premise text, and I do accept that this is a counter-argument for some conclusion text. However, I have a much stronger argument for rejecting that some conclusion text.{}',
        })
        for r in results:
            user_msg, system_msg = tg.get_header_for_users_confrontation_response(arg, 'en', self.premise, r,
                                                                                  self.conclusion, True, is_supportive,
                                                                                  False, redirect_from_jump)
            self.assertEqual(user_msg, results[r])
            self.assertEqual(system_msg, '')

    def test_get_relation_text_dict_without_substitution(self):
        with_no_opinion_text = False
        is_dont_know = False
        res = tg.get_relation_text_dict_without_substitution('en', with_no_opinion_text, self.premise, self.conclusion,
                                                             is_dont_know)

        results = {
            'undermine_text': 'In my opinion, <span data-argumentation-type="attack">some premise text</span> is wrong and I would like to argue against it',
            'support_text': 'In my opinion, <span data-argumentation-type="attack">some premise text</span> is correct and it convinced me',
            'undercut_text': 'In my opinion, <span data-argumentation-type="attack">some premise text</span> is correct, but it does not support <span data-argumentation-type="argument">some conclusion text</span>',
            'rebut_text': 'In my opinion, <span data-argumentation-type="attack">some premise text</span> is correct and it supports <span data-argumentation-type="argument">some conclusion text</span>. However I want to defend <span data-argumentation-type="position">my point of view</span>'
        }

        self.assertEqual(len(res), 4)
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        with_no_opinion_text = True
        res = tg.get_relation_text_dict_without_substitution('en', with_no_opinion_text, self.premise, self.conclusion,
                                                             is_dont_know)
        self.assertEqual(len(res), 6)
        results.update({
            'step_back_text': 'Go one step back. (The system has no other counter-argument)',
            'no_opinion_text': 'Show me another argument.'
        })
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        is_dont_know = True
        res = tg.get_relation_text_dict_without_substitution('en', with_no_opinion_text, self.premise, self.conclusion,
                                                             is_dont_know)
        self.assertEqual(len(res), 6)
        results.update({
            'undercut_text': 'In my opinion, <span data-argumentation-type="attack">some premise text</span> is correct, but it is not supported by the <span data-argumentation-type="argument">reason</span>',
            'rebut_text': 'In my opinion, <span data-argumentation-type="argument">some conclusion text</span> is wrong and I would like to argue against it'
        })
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

    def test_get_relation_text_dict_with_substitution(self):
        with_no_opinion_text = False
        is_dont_know = False
        attack_type = ''
        gender = 'f'

        res = tg.get_relation_text_dict_with_substitution('en', with_no_opinion_text, is_dont_know, attack_type, gender)
        results = {
            'undermine_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is wrong and I would like to argue against it',
            'support_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is correct and it convinced me',
            'undercut_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is correct, but it does not support <span data-argumentation-type="argument">my argument</span>',
            'rebut_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is correct and it supports <span data-argumentation-type="argument">my argument</span>. However I want to defend <span data-argumentation-type="position">my point of view</span>'
        }
        self.assertEqual(len(res), 4)
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        with_no_opinion_text = True
        res = tg.get_relation_text_dict_with_substitution('en', with_no_opinion_text, is_dont_know, attack_type, gender)
        self.assertEqual(len(res), 6)
        results.update({
            'step_back_text': 'Go one step back. (The system has no other counter-argument)',
            'no_opinion_text': 'Show me another argument.'
        })
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        is_dont_know = True
        res = tg.get_relation_text_dict_with_substitution('en', with_no_opinion_text, is_dont_know, attack_type, gender)
        self.assertEqual(len(res), 6)
        results.update({
            'undermine_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is wrong and I would like to argue against it',
            'support_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is correct and it convinced me',
            'undercut_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is correct, but it is not supported by the <span data-argumentation-type="argument">reason</span>',
            'rebut_text': 'In my opinion, <span data-argumentation-type="argument">her opinion</span> is wrong and I would like to argue against it'
        })
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        attack_type = Relations.UNDERCUT
        res = tg.get_relation_text_dict_with_substitution('en', with_no_opinion_text, is_dont_know, attack_type, gender)
        self.assertEqual(len(res), 6)
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        attack_type = Relations.UNDERMINE
        res = tg.get_relation_text_dict_with_substitution('en', with_no_opinion_text, is_dont_know, attack_type, gender)
        self.assertEqual(len(res), 6)
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        attack_type = Relations.REBUT
        res = tg.get_relation_text_dict_with_substitution('en', with_no_opinion_text, is_dont_know, attack_type, gender)
        self.assertEqual(len(res), 6)
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        is_dont_know = False
        attack_type = Relations.UNDERCUT
        res = tg.get_relation_text_dict_with_substitution('en', with_no_opinion_text, is_dont_know, attack_type, gender)
        self.assertEqual(len(res), 6)
        results.update({
            'undercut_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is correct, but it does not support <span data-argumentation-type="argument">my argument</span>',
            'rebut_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is correct and it supports <span data-argumentation-type="argument">my argument</span>. However I want to defend <span data-argumentation-type="position">my point of view</span>'
        })
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        attack_type = Relations.UNDERMINE
        res = tg.get_relation_text_dict_with_substitution('en', with_no_opinion_text, is_dont_know, attack_type, gender)
        self.assertEqual(len(res), 6)
        results.update({
            'undercut_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is correct, but it does not support <span data-argumentation-type="argument">her point of view</span>',
            'rebut_text': 'In my opinion, <span data-argumentation-type="attack">her statement</span> is correct and it supports <span data-argumentation-type="argument">her point of view</span>. However I want to defend <span data-argumentation-type="position">my point of view</span>',
        })
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

        attack_type = Relations.REBUT
        res = tg.get_relation_text_dict_with_substitution('en', with_no_opinion_text, is_dont_know, attack_type, gender)
        self.assertTrue({k: self.assertEqual(res[k], v) for k, v in results.items()})

    def test_get_jump_to_argument_text_list(self):
        res = tg.get_jump_to_argument_text_list('en')
        self.assertEqual(len(res), 5)
        self.assertEqual(res[0],
                         'Right, I support the <span data-argumentation-type="argument">assertion</span> and accept the <span data-argumentation-type="attack">reason</span>')
        self.assertEqual(res[1],
                         'Right, I support the <span data-argumentation-type="argument">assertion</span>, but I want to add my own <span data-argumentation-type="attack">reason</span>')
        self.assertEqual(res[2],
                         'Right, I support the <span data-argumentation-type="argument">assertion</span>, but the <span data-argumentation-type="attack">reason</span> does not support it')
        self.assertEqual(res[3], 'Wrong, the <span data-argumentation-type="argument">assertion</span> is false')
        self.assertEqual(res[4], 'Wrong, the <span data-argumentation-type="attack">reason</span> does not hold')

    def test_get_support_to_argument_text_list(self):
        res = tg.get_support_to_argument_text_list('en')
        self.assertEqual(len(res), 4)
        print(res)
        self.assertEqual(res[0], 'I accept the <span data-argumentation-type="attack">reason</span>')
        self.assertEqual(res[1], 'The <span data-argumentation-type="attack">reason</span> does not hold')
        self.assertEqual(res[2],
                         'The <span data-argumentation-type="attack">reason</span> does not support the <span data-argumentation-type="argument">assertion</span>')
        self.assertEqual(res[3], 'I want to add a new <span data-argumentation-type="attack">reason</span>')

    def test_get_text_for_support(self):
        arg = DBDiscussionSession.query(Argument).get(2)
        argument_text = 'some argument text'
        _t = Translator('en')

        res = tg.get_text_for_support(arg, argument_text, 'Tobias', _t)
        self.assertEqual(res,
                         '<span class="bubbleauthor">Another Participant</span><span>This is a good point and I am interested in your conclusion, too. I say that</span> some argument text<br><br>What do you think about that?')

    def test_get_name_link_of_arguments_author(self):
        db_arg = DBDiscussionSession.query(Argument).get(2)
        db_user = DBDiscussionSession.query(User).get(db_arg.author_uid)

        with_link = True
        data = tg.get_name_link_of_arguments_author(db_arg, 'Christian', with_link)
        self.assertEqual(data['user'], None)
        self.assertEqual(data['link'], '')
        self.assertEqual(data['gender'], 'n')
        self.assertEqual(data['is_valid'], False)

        data = tg.get_name_link_of_arguments_author(db_arg, db_user.nickname, with_link)
        self.assertEqual(data['user'], None)
        self.assertEqual(data['link'], '')
        self.assertEqual(data['gender'], 'n')
        self.assertEqual(data['is_valid'], False)

        with_link = False
        data = tg.get_name_link_of_arguments_author(db_arg, 'Tobias', with_link)
        self.assertEqual(data['user'], None)
        self.assertEqual(data['link'], '')
        self.assertEqual(data['gender'], 'n')
        self.assertEqual(data['is_valid'], False)

    def test_get_author_or_first_supporter_of_element(self):
        arg, user1, user2 = 1, 2, 3

        self.assertIsNone(tg.get_author_or_first_supporter_of_element(arg, user1, True))

        DBDiscussionSession.add(MarkedArgument(argument=self.first_argument, user=self.user_tobi))
        transaction.commit()
        self.assertIsNone(tg.get_author_or_first_supporter_of_element(arg, user1, True))
        self.assertIsNotNone(tg.get_author_or_first_supporter_of_element(arg, user2, True))

        DBDiscussionSession.add(MarkedArgument(argument=self.first_argument, user=self.user_christian))
        transaction.commit()
        self.assertIsNotNone(tg.get_author_or_first_supporter_of_element(arg, user1, True))
        self.assertIsNotNone(tg.get_author_or_first_supporter_of_element(arg, user2, True))

        DBDiscussionSession.query(MarkedArgument).filter_by(argument_uid=arg, author_uid=user1).delete()
        DBDiscussionSession.query(MarkedArgument).filter_by(argument_uid=arg, author_uid=user2).delete()
        transaction.commit()

        self.assertIsNone(tg.get_author_or_first_supporter_of_element(arg, user1, True))
        self.assertIsNone(tg.get_author_or_first_supporter_of_element(arg, user2, True))

    def test_get_text_for_confrontation_without_attack(self):
        user_arg = DBDiscussionSession.query(Argument).get(8)
        sys_arg = DBDiscussionSession.query(Argument).get(10)

        attack = ''
        color_html, supportive, reply_for_argument, user_is_attacking = False, False, False, False
        sys_text, gender = tg.get_text_for_confrontation('en', 'Tobias', self.premise, self.conclusion,
                                                         'another conclusion', supportive, attack, self.confrontation,
                                                         reply_for_argument, user_is_attacking, user_arg, sys_arg,
                                                         color_html)
        self.assertEqual(gender, '')
        self.assertEqual(sys_text, '')

    def test_get_text_for_confrontation_with_undermine_for_en(self):
        user_arg = DBDiscussionSession.query(Argument).get(8)
        sys_arg = DBDiscussionSession.query(Argument).get(10)
        attack = Relations.UNDERMINE

        for combo in list(itertools.product([False, True], repeat=4)):
            color_html, supportive, reply_for_argument, user_is_attacking = combo
            text = '<span class="bubbleauthor">Another Participant</span> <span class="triangle-content-text">I think that</span> '
            if color_html:
                text += '<span data-argumentation-type="argument">some premise text</span><span data-attitude="con"> <span data-argumentation-type="argument">does not hold</span></span>, because <span data-argumentation-type="attack">some confrontation text</span>'
            else:
                text += 'some premise text<span data-attitude="con"> does not hold</span>, because some confrontation text'
            text += '.<br><br>What do you think about that?'

            sys_text, gender = tg.get_text_for_confrontation('en', 'Tobias', self.premise, self.conclusion,
                                                             'another conclusion', supportive, attack,
                                                             self.confrontation,
                                                             reply_for_argument, user_is_attacking, user_arg, sys_arg,
                                                             color_html)
            self.assertEqual(gender, '')
            self.assertEqual(sys_text, text)

    def test_get_text_for_confrontation_with_undercut_for_en(self):
        user_arg = DBDiscussionSession.query(Argument).get(8)
        sys_arg = DBDiscussionSession.query(Argument).get(10)
        attack = Relations.UNDERCUT

        for combo in list(itertools.product([False, True], repeat=4)):
            color_html, supportive, reply_for_argument, user_is_attacking = combo
            text = '<span class="bubbleauthor">Another Participant</span> <span class="triangle-content-text">I agree that some premise text. But I do <span data-attitude="con">not</span> believe that this is <span data-argumentation-type="argument">a good '
            if not color_html and not supportive:
                text += 'counter-argument for</span></span> some conclusion text. I think that some confrontation text.'
            elif not color_html and supportive:
                text += 'argument for</span></span> some conclusion text. I think that some confrontation text.'
            elif color_html and not supportive:
                text += 'counter-argument for</span></span> <span data-argumentation-type="argument">some conclusion text</span>. I think that <span data-argumentation-type="attack">some confrontation text</span>.'
            elif color_html and supportive:
                text += 'argument for</span></span> <span data-argumentation-type="argument">some conclusion text</span>. I think that <span data-argumentation-type="attack">some confrontation text</span>.'
            text += '<br><br>What do you think about that?'

            sys_text, gender = tg.get_text_for_confrontation('en', 'Tobias', self.premise, self.conclusion,
                                                             'another conclusion', supportive, attack,
                                                             self.confrontation, reply_for_argument, user_is_attacking,
                                                             user_arg, sys_arg, color_html)
            self.assertEqual(gender, '')
            self.assertEqual(sys_text, text)

    def test_get_text_for_confrontation_with_rebut_for_en(self):
        user_arg = DBDiscussionSession.query(Argument).get(8)
        sys_arg = DBDiscussionSession.query(Argument).get(10)
        attack = Relations.REBUT

        for combo in list(itertools.product([False, True], repeat=4)):
            color_html, supportive, reply_for_argument, user_is_attacking = combo
            text = '<span class="bubbleauthor">Another Participant</span> '
            if not color_html and not reply_for_argument and not user_is_attacking:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, False, False, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, True, False, False)
                text += '<span class="triangle-content-text">I have no opinion regarding some premise text. But I claim to have a stronger <span data-attitude="con">statement for rejecting </span> some conclusion text. I say some confrontation text.'

            elif not color_html and not reply_for_argument and user_is_attacking:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, False, False, True)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, True, False, True)
                text += '<span class="triangle-content-text">I have no opinion regarding some premise text. But I claim to have a stronger <span data-attitude="pro">statement for accepting </span> some conclusion text. I say some confrontation text.'

            elif not color_html and reply_for_argument:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, False, True, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, False, True, True)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, True, True, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, True, True, True)
                text += '<span class="triangle-content-text"><span>I claim to have a stronger statement to reject</span> some conclusion text. I say: some confrontation text.'

            elif color_html and not reply_for_argument and not user_is_attacking:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, False, False, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, True, False, False)
                text += '<span class="triangle-content-text">I have no opinion regarding some premise text. But I claim to have a stronger <span data-attitude="con">statement for <span data-argumentation-type="argument">rejecting</span> </span> <span data-argumentation-type="argument">some conclusion text</span>. I say <span data-argumentation-type="attack">some confrontation text</span>.'

            elif color_html and not reply_for_argument and user_is_attacking:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, True, False, True)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, False, False, True)
                text += '<span class="triangle-content-text">I have no opinion regarding some premise text. But I claim to have a stronger <span data-attitude="pro">statement for <span data-argumentation-type="argument">accepting</span> </span> <span data-argumentation-type="argument">some conclusion text</span>. I say <span data-argumentation-type="attack">some confrontation text</span>.'

            elif color_html and reply_for_argument:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, False, True, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, False, True, True)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, True, True, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, True, True, True)
                text += '<span class="triangle-content-text"><span>I claim to have a stronger statement to <span data-argumentation-type="argument">reject</span></span> <span data-argumentation-type="argument">some conclusion text</span>. I say: <span data-argumentation-type="attack">some confrontation text</span>.'

            text += '<br><br>What do you think about that?'

            sys_text, gender = tg.get_text_for_confrontation('en', 'Tobias', self.premise, self.conclusion,
                                                             'another conclusion', supportive, attack,
                                                             self.confrontation, reply_for_argument, user_is_attacking,
                                                             user_arg, sys_arg, color_html)
            self.assertEqual(gender, 'n')
            self.assertEqual(sys_text, text)

    def test_get_text_for_confrontation_with_undermine_for_de(self):
        user_arg = DBDiscussionSession.query(Argument).get(8)
        sys_arg = DBDiscussionSession.query(Argument).get(10)
        attack = Relations.UNDERMINE

        for combo in list(itertools.product([False, True], repeat=4)):
            color_html, supportive, reply_for_argument, user_is_attacking = combo

            text = '<span class="bubbleauthor">Jemand anders</span> <span class="triangle-content-text">Ich denke, dass</span> '
            if color_html:
                text += '<span data-argumentation-type="argument">some premise text</span><span data-attitude="con"> <span data-argumentation-type="argument">keine gute Idee ist</span></span>, weil <span data-argumentation-type="attack">some confrontation text</span>'
            else:
                text += 'some premise text<span data-attitude="con"> keine gute Idee ist</span>, weil some confrontation text'
            text += '.<br><br>Was denken Sie darüber?'

            sys_text, gender = tg.get_text_for_confrontation('de', 'Tobias', self.premise, self.conclusion,
                                                             'another conclusion', supportive, attack,
                                                             self.confrontation,
                                                             reply_for_argument, user_is_attacking, user_arg, sys_arg,
                                                             color_html)
            self.assertEqual(gender, '')
            self.assertEqual(sys_text, text)

    def test_get_text_for_confrontation_with_undercut_for_de(self):
        user_arg = DBDiscussionSession.query(Argument).get(8)
        sys_arg = DBDiscussionSession.query(Argument).get(10)
        attack = Relations.UNDERCUT

        for combo in list(itertools.product([False, True], repeat=4)):
            color_html, supportive, reply_for_argument, user_is_attacking = combo

            text = '<span class="bubbleauthor">Jemand anders</span> <span class="triangle-content-text">Ich stimme zu, dass some premise text. Aber ich glaube, dass es <span data-attitude="con">keine gute Begründung '
            if not color_html and not supportive:
                text += 'dagegen</span> ist, <span data-argumentation-type="argument">dass</span></span> some conclusion text. Ich denke, dass some confrontation text.'
            elif not color_html and supportive:
                text += 'dafür</span> ist, <span data-argumentation-type="argument">dass</span></span> some conclusion text. Ich denke, dass some confrontation text.'
            elif color_html and not supportive:
                text += 'dagegen</span> ist, <span data-argumentation-type="argument">dass</span></span> <span data-argumentation-type="argument">some conclusion text</span>. Ich denke, dass <span data-argumentation-type="attack">some confrontation text</span>.'
            elif color_html and supportive:
                text += 'dafür</span> ist, <span data-argumentation-type="argument">dass</span></span> <span data-argumentation-type="argument">some conclusion text</span>. Ich denke, dass <span data-argumentation-type="attack">some confrontation text</span>.'
            text += '<br><br>Was denken Sie darüber?'

            sys_text, gender = tg.get_text_for_confrontation('de', 'Tobias', self.premise, self.conclusion,
                                                             'another conclusion', supportive, attack,
                                                             self.confrontation, reply_for_argument, user_is_attacking,
                                                             user_arg, sys_arg, color_html)
            self.assertEqual(gender, '')
            self.assertEqual(sys_text, text)

    def test_get_text_for_confrontation_with_rebut_for_de(self):
        user_arg = DBDiscussionSession.query(Argument).get(8)
        sys_arg = DBDiscussionSession.query(Argument).get(10)
        attack = Relations.REBUT

        for combo in list(itertools.product([False, True], repeat=4)):
            color_html, supportive, reply_for_argument, user_is_attacking = combo

            text = '<span class="bubbleauthor">Jemand anders</span> <span class="triangle-content-text">'
            if not color_html and not reply_for_argument and not user_is_attacking:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, False, False, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, True, False, False)
                text += 'Ich habe bisher keine Meinung dazu, dass some premise text. Aber ich habe einen <span data-attitude="con">Grund dagegen, dass </span> some conclusion text. Ich sage, dass some confrontation text'

            elif not color_html and not reply_for_argument and user_is_attacking:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, False, False, True)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, True, False, True)
                text += 'Ich habe bisher keine Meinung dazu, dass some premise text. Aber ich habe einen <span data-attitude="pro">Grund dafür, dass </span> some conclusion text. Ich sage, dass some confrontation text'

            elif not color_html and reply_for_argument:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, False, True, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, False, True, True)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, True, True, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (False, True, True, True)
                text += '<span>Ich habe eine stärkere Aussage zur Ablehnung davon, dass</span> some conclusion text. Ich sage, dass some confrontation text'

            elif color_html and not reply_for_argument and not user_is_attacking:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, False, False, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, True, False, False)
                text += 'Ich habe bisher keine Meinung dazu, dass some premise text. Aber ich habe einen <span data-attitude="con">Grund <span data-argumentation-type="argument">dagegen</span>, dass </span> <span data-argumentation-type="argument">some conclusion text</span>. Ich sage, dass <span data-argumentation-type="attack">some confrontation text</span>'

            elif color_html and not reply_for_argument and user_is_attacking:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, True, False, True)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, False, False, True)
                text += 'Ich habe bisher keine Meinung dazu, dass some premise text. Aber ich habe einen <span data-attitude="pro">Grund <span data-argumentation-type="argument">dafür</span>, dass </span> <span data-argumentation-type="argument">some conclusion text</span>. Ich sage, dass <span data-argumentation-type="attack">some confrontation text</span>'

            elif color_html and reply_for_argument:
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, False, True, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, False, True, True)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, True, True, False)
                # valid for color_html, supportive, reply_for_argument, user_is_attacking = (True, True, True, True)
                text += '<span>Ich habe eine stärkere Aussage zur <span data-argumentation-type="argument">Ablehnung</span> davon, dass</span> <span data-argumentation-type="argument">some conclusion text</span>. Ich sage, dass <span data-argumentation-type="attack">some confrontation text</span>'

            text += '.<br><br>Was denken Sie darüber?'

            sys_text, gender = tg.get_text_for_confrontation('de', 'Tobias', self.premise, self.conclusion,
                                                             'another conclusion', supportive, attack,
                                                             self.confrontation, reply_for_argument, user_is_attacking,
                                                             user_arg, sys_arg, color_html)
            self.assertEqual(gender, 'n')
            self.assertEqual(sys_text, text)


class TestTextGeneration(unittest.TestCase):
    def setUp(self):
        self.name = 'Coconut'
        self.url = '/Coconut/Seagull'

    def test_get_text_for_add_text_message(self):
        for language, is_html, message in list(itertools.product(['en', 'de'],
                                                                 [True, False],
                                                                 [_.statementAddedMessageContent,
                                                                  _.argumentAddedMessageContent])):
            text = tg.get_text_for_message(self.name, language, self.url, message, is_html)
            if is_html:
                self.assertNotIn("\n", text)
                self.assertIn("<br>", text)
            else:
                self.assertNotIn("<br>", text)
                self.assertIn("\n", text)


class TestRemovePunctuation(TestCaseWithConfig):
    def test_multiple_punctuations(self):
        multiples = ["foo!", "foo!!", "foo!!!", "foo!!!!"]
        removed_punctuations = [remove_punctuation(s) for s in multiples]
        unique_strings = set(removed_punctuations)
        self.assertEqual(len(unique_strings), 1)
        self.assertEqual(unique_strings.pop(), "foo!")

    def test_no_punctuation_no_removal(self):
        dont_touch_me = "dont_touch_me"
        untouched = remove_punctuation(dont_touch_me)
        self.assertEqual(dont_touch_me, untouched)

    def test_empty_input_should_not_be_touched(self):
        input = ""
        output = remove_punctuation(input)
        self.assertEqual(input, output)
