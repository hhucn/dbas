"""
Provides functions for te internal messaging system

.. codeauthor:: Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de
"""

import transaction

import dbas.handler.email as email_helper
from dbas.database import DBDiscussionSession
from dbas.database.discussion_model import User, TextVersion, Message, Language, Argument, \
    sql_timestamp_pretty_print
from dbas.handler import user as user_handler
from dbas.lib import escape_string, get_profile_picture
from dbas.strings.keywords import Keywords as _
from dbas.strings.text_generator import get_text_for_edit_text_message, get_text_for_add_text_message, \
    get_text_for_add_argument_message
from dbas.strings.translator import Translator
from websocket.lib import send_request_for_info_popup_to_socketio


def send_users_notification(author, recipient, title, text, ui_locales) -> dict:
    """
    Send a notification from user a to user b

    :param recipient: User
    :param title: Title of the notification
    :param text: Text of the notification
    :param author: User
    :param ui_locales: Current used language
    :rtype: dict
    :return: prepared collection with status information
    """
    db_notification = send_notification(author, recipient, title, text, author.nickname)
    prepared_dict = {
        'timestamp': sql_timestamp_pretty_print(db_notification.timestamp, ui_locales),
        'uid': db_notification.uid,
        'recipient_avatar': get_profile_picture(recipient, 20)
    }
    return prepared_dict


def send_edit_text_notification(db_user, textversion, path, mailer):
    """
    Sends an notification to the root-author and last author, when their text was edited.

    :param db_user: Current User
    :param textversion: new Textversion
    :param path: curren path
    :param mailer: Instance of pyramid mailer
    :return: None
    """
    all_textversions = DBDiscussionSession.query(TextVersion).filter_by(
        statement_uid=textversion.statement_uid).order_by(TextVersion.uid.desc()).all()
    oem = all_textversions[-1]
    root_author = oem.author_uid
    new_author = textversion.author_uid
    last_author = all_textversions[-2].author_uid if len(all_textversions) > 1 else root_author
    settings_root_author = root_author.settings
    settings_last_author = last_author.settings

    # create content
    db_editor = DBDiscussionSession.query(User).get(new_author)
    db_settings = db_editor.settings
    editor_ui_locales = db_settings.lang

    # add some information for highlights
    if path is not None:
        path += '?edited_statement=' + str(textversion.statement_uid)

    if settings_root_author.should_send_mails is True \
            and root_author != db_user.uid \
            and path is not None:
        email_helper.send_mail_due_to_edit_text(textversion.statement_uid, root_author, db_editor, path, mailer)

    if new_author != last_author \
            and settings_last_author.should_send_mails is True \
            and new_author != db_user.uid \
            and path is not None:
        email_helper.send_mail_due_to_edit_text(textversion.statement_uid, last_author, db_editor, path, mailer)

    # check for different authors
    if root_author == new_author:
        return None

    # send notifications
    user_lang1 = DBDiscussionSession.query(Language).get(settings_root_author.lang_uid).ui_locales
    user_lang2 = DBDiscussionSession.query(Language).get(settings_last_author.lang_uid).ui_locales
    if settings_root_author.should_send_notifications \
            and root_author != db_user.uid:
        _t_user = Translator(user_lang1)
        db_root_author = DBDiscussionSession.query(User).get(root_author)
        send_request_for_info_popup_to_socketio(db_root_author.nickname, _t_user.get(_.textChange), path,
                                                increase_counter=True)

    if last_author != root_author \
            and last_author != new_author \
            and last_author != db_user.uid \
            and settings_last_author.should_send_notifications:
        _t_user = Translator(user_lang2)
        db_last_author = DBDiscussionSession.query(User).get(last_author)
        send_request_for_info_popup_to_socketio(db_last_author.nickname, _t_user.get(_.textChange), path,
                                                increase_counter=True)

    _t1 = Translator(user_lang1)
    topic1 = _t1.get(_.textversionChangedTopic)
    content1 = get_text_for_edit_text_message(editor_ui_locales, db_editor.public_nickname, textversion.content,
                                              oem.content, path)

    _t2 = Translator(user_lang2)
    topic2 = _t2.get(_.textversionChangedTopic)
    content2 = get_text_for_edit_text_message(editor_ui_locales, db_editor.public_nickname, textversion.content,
                                              oem.content, path)

    notifications = []
    if new_author != root_author:
        notifications.append(Message(from_author_uid=new_author,
                                     to_author_uid=root_author,
                                     topic=topic1,
                                     content=content1,
                                     is_inbox=True))
    if new_author != last_author:
        notifications.append(Message(from_author_uid=new_author,
                                     to_author_uid=last_author,
                                     topic=topic2,
                                     content=content2,
                                     is_inbox=True))
    if len(notifications) > 0:
        DBDiscussionSession.add_all(notifications)
        DBDiscussionSession.flush()


def send_add_text_notification(url, conclusion_id, db_user: User, mailer):
    """
    Send notifications and mails to related users.

    :param url: current url
    :param conclusion_id: Statement.uid
    :param db_user: current users nickname
    :param mailer: Instance of pyramid mailer
    :return: None
    """
    # getting all text versions, the overview author, last editor and settings ob both authors as well as their languages
    db_textversions = DBDiscussionSession.query(TextVersion).filter_by(statement_uid=conclusion_id).all()
    db_root_author = DBDiscussionSession.query(User).get(db_textversions[0].author_uid)
    db_last_editor = DBDiscussionSession.query(User).get(db_textversions[-1].author_uid)
    db_root_author_settings = db_root_author.settings
    db_last_editor_settings = db_last_editor.settings
    root_lang = DBDiscussionSession.query(Language).get(db_root_author_settings.lang_uid).ui_locales
    editor_lang = DBDiscussionSession.query(Language).get(db_last_editor_settings.lang_uid).ui_locales
    _t_editor = Translator(editor_lang)
    _t_root = Translator(root_lang)

    # send mail to overview author
    if db_root_author_settings.should_send_mails \
            and db_user != db_root_author:
        email_helper.send_mail_due_to_added_text(root_lang, url, db_root_author, mailer)

    # send mail to last author
    if db_last_editor_settings.should_send_mails \
            and db_last_editor != db_root_author \
            and db_last_editor != db_user:
        email_helper.send_mail_due_to_added_text(editor_lang, url, db_last_editor, mailer)

    # send notification via websocket to overview author
    if db_root_author_settings.should_send_notifications and db_root_author != db_user:
        send_request_for_info_popup_to_socketio(db_root_author.nickname, _t_root.get(_.statementAdded), url,
                                                increase_counter=True)

    # send notification via websocket to last author
    if db_last_editor_settings.should_send_notifications \
            and db_last_editor != db_root_author \
            and db_last_editor != db_user:
        send_request_for_info_popup_to_socketio(db_last_editor.nickname, _t_editor.get(_.statementAdded), url,
                                                increase_counter=True)

    # find admin, because generic mails are being sent by the admin
    db_admin = user_handler.get_list_of_admins()[0]

    # get topic and content for messages to both authors
    topic1 = _t_root.get(_.statementAdded)
    content1 = get_text_for_add_text_message(db_root_author.firstname, root_lang, url, True)

    topic2 = _t_editor.get(_.statementAdded)
    content2 = get_text_for_add_text_message(db_last_editor.firstname, editor_lang, url, True)

    if db_root_author != db_user:
        DBDiscussionSession.add(Message(from_author_uid=db_admin.uid,
                                        to_author_uid=db_root_author.uid,
                                        topic=topic1,
                                        content=content1,
                                        is_inbox=True))
    if db_root_author != db_last_editor and db_user != db_last_editor:
        DBDiscussionSession.add(Message(from_author_uid=db_admin.uid,
                                        to_author_uid=db_last_editor.uid,
                                        topic=topic2,
                                        content=content2,
                                        is_inbox=True))
    DBDiscussionSession.flush()
    transaction.commit()


def send_add_argument_notification(url, attacked_argument_uid, user, mailer):
    """
    Sends an notification because an argument was added

    :param url: String
    :param attacked_argument_uid: Argument.uid
    :param user: User
    :param mailer: Instance of pyramid mailer
    :return:
    """
    # getting current argument, arguments author, current user and some settings
    db_argument = DBDiscussionSession.query(Argument).get(attacked_argument_uid)
    db_author = DBDiscussionSession.query(User).get(db_argument.author_uid)
    db_current_user = DBDiscussionSession.query(User).filter_by(nickname=user).first()
    if db_author == db_current_user:
        return None

    db_author_settings = db_author.settings
    user_lang = DBDiscussionSession.query(Language).get(db_author_settings.lang_uid).ui_locales

    # send notification via websocket to last author
    _t_user = Translator(user_lang)
    if db_author_settings.should_send_notifications:
        send_request_for_info_popup_to_socketio(db_author.nickname, _t_user.get(_.argumentAdded), url)

    # send mail to last author
    if db_author_settings.should_send_mails:
        email_helper.send_mail_due_to_added_text(user_lang, url, db_author, mailer)

    # find admin
    db_admin = user_handler.get_list_of_admins()[0]

    topic = _t_user.get(_.argumentAdded)
    content = get_text_for_add_argument_message(db_author.firstname, user_lang, url, True)

    DBDiscussionSession.add(Message(from_author_uid=db_admin.uid,
                                    to_author_uid=db_author.uid,
                                    topic=topic,
                                    content=content,
                                    is_inbox=True))
    transaction.commit()


def send_welcome_notification(user, translator):
    """
    Creates and send the welcome message to a new user.

    :param user: User.uid
    :param translator: translator
    :return: None
    """
    topic = translator.get(_.welcome)
    content = translator.get(_.welcomeMessage)
    db_user = user_handler.get_list_of_admins()[0]
    notification = Message(from_author_uid=db_user.uid, to_author_uid=user, topic=topic, content=content, is_inbox=True)
    DBDiscussionSession.add(notification)
    DBDiscussionSession.flush()
    transaction.commit()


def send_notification(from_user, to_user, topic, content, mainpage):
    """
    Sends message to an user and places a copy in the outbox of current user. Returns the uid and timestamp

    :param from_user: User
    :param to_user: User
    :param topic: String
    :param content: String
    :param mainpage: String
    :return:
    """
    content = escape_string(content)
    notification_in = Message(from_author_uid=from_user.uid, to_author_uid=to_user.uid, topic=topic, content=content,
                              is_inbox=True)
    notification_out = Message(from_author_uid=from_user.uid, to_author_uid=to_user.uid, topic=topic, content=content,
                               is_inbox=False, read=True)
    DBDiscussionSession.add_all([notification_in, notification_out])
    DBDiscussionSession.flush()
    transaction.commit()

    db_settings = to_user.settings
    if db_settings.should_send_notifications:
        user_lang = DBDiscussionSession.query(Language).get(db_settings.lang_uid).ui_locales
        _t_user = Translator(user_lang)
        send_request_for_info_popup_to_socketio(to_user.nickname, _t_user.get(_.newNotification),
                                                mainpage + '/notifications', increase_counter=True)

    db_inserted_notification = DBDiscussionSession.query(Message).filter(Message.from_author_uid == from_user.uid,
                                                                         Message.to_author_uid == to_user.uid,
                                                                         Message.topic == topic,
                                                                         Message.content == content,
                                                                         Message.is_inbox == True).order_by(
        Message.uid.desc()).first()

    return db_inserted_notification


def count_of_new_notifications(db_user):
    """
    Returns the count of unread messages of the given user

    :param db_user: User
    :return: integer
    """
    return len(DBDiscussionSession.query(Message).filter(Message.to_author_uid == db_user.uid,
                                                         Message.read == False,
                                                         Message.is_inbox == True).all())


def get_box_for(db_user, lang, main_page, is_inbox):
    """
    Returns all notifications for the user

    :param db_user: User
    :param lang: ui_locales
    :param main_page: URL
    :param is_inbox: Boolean
    :return: [Notification]
    """
    if is_inbox:
        db_messages = DBDiscussionSession.query(Message).filter(Message.to_author_uid == db_user.uid,
                                                                Message.is_inbox == is_inbox).order_by(
            Message.uid.desc()).all()
    else:
        db_messages = DBDiscussionSession.query(Message).filter(Message.from_author_uid == db_user.uid,
                                                                Message.is_inbox == is_inbox).order_by(
            Message.uid.desc()).all()

    message_array = []
    for message in db_messages:
        tmp_dict = dict()
        if is_inbox:
            db_from_user = DBDiscussionSession.query(User).get(message.from_author_uid)
            tmp_dict['show_from_author'] = db_from_user.global_nickname != 'admin'
            tmp_dict['from_author'] = db_from_user.global_nickname
            tmp_dict['from_author_avatar'] = get_profile_picture(db_from_user, size=30)
            tmp_dict['from_author_url'] = main_page + '/user/' + str(db_from_user.uid)
        else:
            db_to_user = DBDiscussionSession.query(User).get(message.to_author_uid)
            tmp_dict['to_author'] = db_to_user.global_nickname
            tmp_dict['to_author_avatar'] = get_profile_picture(db_to_user, size=30)
            tmp_dict['to_author_url'] = main_page + '/user/' + str(db_to_user.uid)

        tmp_dict['id'] = str(message.uid)
        tmp_dict['timestamp'] = sql_timestamp_pretty_print(message.timestamp, lang)
        tmp_dict['read'] = message.read
        tmp_dict['topic'] = message.topic
        tmp_dict['content'] = message.content
        tmp_dict['collapse_link'] = '#collapse' + str(message.uid)
        tmp_dict['collapse_id'] = 'collapse' + str(message.uid)
        message_array.append(tmp_dict)

    return message_array[::-1]


def read_notifications(uids_list, db_user) -> dict:
    """
    Simply marks a notification as read

    :param uids_list: List of message ids notification which should be marked as read
    :param db_user: User
    :return: Dictionary with info and/or error
    """
    prepared_dict = dict()
    user_handler.update_last_action(db_user)

    for uid in uids_list:
        DBDiscussionSession.query(Message).filter(Message.uid == uid,
                                                  Message.to_author_uid == db_user.uid,
                                                  Message.is_inbox == True).first().set_read(True)
    transaction.commit()
    prepared_dict['unread_messages'] = count_of_new_notifications(db_user)
    prepared_dict['error'] = ''

    return prepared_dict


def delete_notifications(uids_list, db_user, ui_locales, application_url) -> dict:
    """
    Simply deletes a specific notification

    :param uids_list: List of message ids which should be deleted
    :param db_user: User
    :param ui_locales: Language of current users session
    :param application_url: Url of the App
    :return: Dictionary with info and/or error
    """
    user_handler.update_last_action(db_user)
    _tn = Translator(ui_locales)

    for uid in uids_list:
        # inbox
        DBDiscussionSession.query(Message).filter(Message.uid == uid,
                                                  Message.to_author_uid == db_user.uid,
                                                  Message.is_inbox == True).delete()
        # send
        DBDiscussionSession.query(Message).filter(Message.uid == uid,
                                                  Message.from_author_uid == db_user.uid,
                                                  Message.is_inbox == False).delete()
    transaction.commit()
    prepared_dict = dict()
    prepared_dict['unread_messages'] = count_of_new_notifications(db_user)
    prepared_dict['total_in_messages'] = str(len(get_box_for(db_user, ui_locales, application_url, True)))
    prepared_dict['total_out_messages'] = str(len(get_box_for(db_user, ui_locales, application_url, False)))
    prepared_dict['success'] = _tn.get(_.messageDeleted)

    return prepared_dict
