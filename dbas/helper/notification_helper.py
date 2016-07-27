"""
Provides functions for te internal messaging system

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import requests
import dbas.user_management as UserHandler
import dbas.helper.email_helper as EmailHelper

from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, TextVersion, Notification, Settings, Language
from dbas.lib import sql_timestamp_pretty_print, escape_string
from dbas.strings import Translator, TextGenerator
from dbas.logger import logger

from sqlalchemy import and_


def send_edit_text_notification(textversion, path, request):
    """
    Sends an notification to the root-author and last author, when their text was edited.

    :param textversion: new Textversion
    :param path: curren path
    :param request: curren request
    :return: None
    """
    all_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=textversion.statement_uid).order_by(TextVersion.uid.desc()).all()
    oem = all_textversions[-1]
    root_author = oem.author_uid
    new_author = textversion.author_uid
    last_author = all_textversions[-2].author_uid if len(all_textversions) > 1 else root_author
    settings_root_author = DBDiscussionSession.query(Settings).filter_by(author_uid=root_author).first()
    settings_last_author = DBDiscussionSession.query(Settings).filter_by(author_uid=last_author).first()

    # create content
    db_editor = DBDiscussionSession.query(User).filter_by(uid=new_author).first()
    db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=db_editor.uid).first()
    db_language = DBDiscussionSession.query(Language).filter_by(uid=db_settings.lang_uid).first()

    logger('NotificationHelper', 'send_edit_text_notification', 'root author: ' + str(oem.author_uid))
    logger('NotificationHelper', 'send_edit_text_notification', 'last author: ' + str(last_author))
    logger('NotificationHelper', 'send_edit_text_notification', 'current author: ' + str(new_author))

    # add some information
    path += '?edited_statement=' + textversion.statement_uid

    if settings_root_author.should_send_mails is True:
        EmailHelper.send_mail_due_to_edit_text(textversion.statement_uid, root_author, db_editor, path, request)

    if new_author != last_author and settings_last_author.should_send_mails is True:
        EmailHelper.send_mail_due_to_edit_text(textversion.statement_uid, last_author, db_editor, path, request)

    # check for different authors
    if root_author == new_author:
        return None

    _t = Translator(db_language.ui_locales)
    topic = _t.get(_t.textversionChangedTopic)
    content = TextGenerator.get_text_for_edit_text_message(db_language.ui_locales, db_editor.public_nickname, textversion.content, oem.content, path)

    # send notifications
    if settings_root_author.should_send_notifications:
        user_lang = DBDiscussionSession.query(Language).filter_by(uid=settings_root_author.lang_uid).first().ui_locales
        _t_user = Translator(user_lang)
        db_root_author = DBDiscussionSession.query(User).filter_by(uid=root_author).first()
        __send_request_to_socketio('edittext', db_root_author.nickname, _t_user.get(_t_user.textChange), path)

    if last_author != root_author and last_author != new_author and settings_last_author.should_send_notifications:
        user_lang = DBDiscussionSession.query(Language).filter_by(uid=settings_last_author.lang_uid).first().ui_locales
        _t_user = Translator(user_lang)
        db_last_author = DBDiscussionSession.query(User).filter_by(uid=last_author).first()
        __send_request_to_socketio('edittext', db_last_author.nickname, _t_user.get(_t_user.textChange), path)

    notification1  = Notification(from_author_uid=new_author,
                                  to_author_uid=root_author,
                                  topic=topic,
                                  content=content,
                                  is_inbox=True)
    notification2  = Notification(from_author_uid=new_author,
                                  to_author_uid=last_author,
                                  topic=topic,
                                  content=content,
                                  is_inbox=True)
    DBDiscussionSession.add_all([notification1, notification2])

    DBDiscussionSession.flush()


def send_welcome_notification(transaction, user, lang='en'):
    """
    Creates and send the welcome message to a new user.

    :param transaction: transaction
    :param user: User.uid
    :param lang: ui_locales
    :return: None
    """
    _tn = Translator(lang)
    topic = _tn.get(_tn.welcome)
    content = _tn.get(_tn.welcomeMessage)
    notification = Notification(from_author_uid=1, to_author_uid=user, topic=topic, content=content, is_inbox=True)
    DBDiscussionSession.add(notification)
    DBDiscussionSession.flush()
    transaction.commit()


def send_notification(from_user, to_user, topic, content, transaction):
    """
    Sends message to an user and places a copy in the outbox of current user. Returns the uid and timestamp

    :param from_user: User
    :param to_user: User
    :param topic: String
    :param content: String
    :param transaction: transaction
    :return:
    """
    content = escape_string(content)
    notification_in  = Notification(from_author_uid=from_user.uid, to_author_uid=to_user.uid, topic=topic, content=content, is_inbox=True)
    notification_out = Notification(from_author_uid=from_user.uid, to_author_uid=to_user.uid, topic=topic, content=content, is_inbox=False, read=True)
    DBDiscussionSession.add_all([notification_in, notification_out])
    DBDiscussionSession.flush()
    transaction.commit()

    db_settings = DBDiscussionSession.query(Settings).filter_by(author_uid=to_user.uid).first()
    if db_settings.should_send_notifications:
        user_lang = DBDiscussionSession.query(Language).filter_by(uid=db_settings.lang_uid).first().ui_locales
        _t_user = Translator(user_lang)
        __send_request_to_socketio('notification', to_user.nickname, _t_user.get(_t_user.newNotification))

    db_inserted_notification = DBDiscussionSession.query(Notification).filter(and_(Notification.from_author_uid == from_user.uid,
                                                                                   Notification.to_author_uid == to_user.uid,
                                                                                   Notification.topic == topic,
                                                                                   Notification.content == content,
                                                                                   Notification.is_inbox == True)).order_by(Notification.uid.desc()).first()

    return db_inserted_notification


def count_of_new_notifications(user):
    """
    Returns the count of unread messages of the given user

    :param user: User.nickname
    :return: integer
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
    if db_user:
        return len(DBDiscussionSession.query(Notification).filter(and_(Notification.to_author_uid == db_user.uid,
                                                                       Notification.read == False,
                                                                       Notification.is_inbox == True)).all())
    else:
        return 0


def get_box_for(user, lang, mainpage, is_inbox):
    """
    Returns all notifications for the user

    :param user: User.nickname
    :param lang: ui_locales
    :param mainpage: URL
    :param is_inbox: Boolean
    :return: [Notification]
    """
    db_user = DBDiscussionSession.query(User).filter_by(nickname=str(user)).first()
    if not db_user:
        return []

    if is_inbox:
        db_messages = DBDiscussionSession.query(Notification).filter(and_(Notification.to_author_uid == db_user.uid,
                                                                          Notification.is_inbox == is_inbox)).all()
    else:
        db_messages = DBDiscussionSession.query(Notification).filter(and_(Notification.from_author_uid == db_user.uid,
                                                                          Notification.is_inbox == is_inbox)).all()

    message_array = []
    for message in db_messages:
        tmp_dict = dict()
        if is_inbox:
            db_from_user                   = DBDiscussionSession.query(User).filter_by(uid=message.from_author_uid).first()
            tmp_dict['show_from_author']   = db_from_user.public_nickname != 'admin'
            tmp_dict['from_author']        = db_from_user.public_nickname
            tmp_dict['from_author_avatar'] = UserHandler.get_public_profile_picture(db_from_user, size=30)
            tmp_dict['from_author_url']    = mainpage + '/user/' + db_from_user.public_nickname
        else:
            db_to_user                   = DBDiscussionSession.query(User).filter_by(uid=message.to_author_uid).first()
            tmp_dict['to_author']        = db_to_user.public_nickname
            tmp_dict['to_author_avatar'] = UserHandler.get_public_profile_picture(db_to_user, size=30)
            tmp_dict['to_author_url']    = mainpage + '/user/' + db_to_user.public_nickname

        tmp_dict['id']            = str(message.uid)
        tmp_dict['timestamp']     = sql_timestamp_pretty_print(message.timestamp, lang)
        tmp_dict['read']          = message.read
        tmp_dict['topic']         = message.topic
        tmp_dict['content']       = message.content
        tmp_dict['collapse_link'] = '#collapse' + str(message.uid)
        tmp_dict['collapse_id']   = 'collapse' + str(message.uid)
        message_array.append(tmp_dict)

    return message_array[::-1]


def __send_request_to_socketio(type, nickname, message=None, url=None):
    """
    Sends an request to the socket io server

    :param type: String
    :param nickname: String
    :param message: String
    :param url: String
    :return: Status code of the request
    """
    params = '?type=' + type + '&nickname=' + nickname + '&'
    if message:
        params += 'msg=' + message + '&'
    if url:
        params += 'url=' + url + '&'

    resp = requests.get('http://localhost:5001/publish' + params[:-1])
    logger('NotificationHelper', 'send_edit_text_notification', 'status code for request ' + str(resp.status_code) + '(msg=' + str(message) + ')')

    return resp.status_code
