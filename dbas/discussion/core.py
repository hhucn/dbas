import dbas.helper.history as history_helper
import dbas.helper.issue as issue_helper
from dbas.helper.dictionary.discussion import DiscussionDictHelper
from dbas.helper.dictionary.items import ItemDictHelper
from dbas.helper.dictionary.main import DictionaryHelper
from dbas.helper.language import (get_language_from_cookie,
                                  set_language_for_first_visit)
from dbas.lib import get_discussion_language, resolve_issue_uid_to_slug


def init(request, nickname, history, for_api=False) -> dict:
    """
    Initialize the discussion. Creates helper and returns a dictionary containing the first elements needed for the
    discussion. 
    
    :param request: pyramid's request object
    :param nickname: the user's nickname creating the request
    :param history: get user's history
    :param for_api: boolean if requests came via the API
    :rtype: dict
    :return: prepared collection with first elements for the discussion
    """
    match_dict = request.matchdict
    request_authenticated_userid = request.authenticated_userid
    set_language_for_first_visit(request)

    if for_api:
        slug = match_dict['slug'] if 'slug' in match_dict else ''
    else:
        slug = match_dict['slug'][0] if 'slug' in match_dict and len(match_dict['slug']) > 0 else ''

    last_topic = history_helper.get_saved_issue(nickname)
    if len(slug) == 0 and last_topic != 0:
        issue = last_topic
    else:
        issue = issue_helper.get_id_of_slug(slug, request, True)

    slug = resolve_issue_uid_to_slug(last_topic)
    if not slug:
        slug = ''
    history_helper.save_path_in_database(nickname, slug, request.path, history)

    disc_ui_locales = get_discussion_language(request, issue)
    issue_dict = issue_helper.prepare_json_of_issue(issue, request.application_url, disc_ui_locales, for_api)
    item_dict = ItemDictHelper(disc_ui_locales, issue, request.application_url, for_api).get_array_for_start(nickname)
    history_helper.save_issue_uid(issue, nickname)

    discussion_dict = DiscussionDictHelper(disc_ui_locales, nickname=nickname, main_page=request.application_url, slug=slug).get_dict_for_start(position_count=(len(item_dict['elements'])))
    extras_dict = DictionaryHelper(get_language_from_cookie(request), disc_ui_locales).prepare_extras_dict(slug, False, True, False, True,
                                                                                                           request, for_api=for_api, nickname=request_authenticated_userid)

    if len(item_dict['elements']) == 1:
        DictionaryHelper(disc_ui_locales, disc_ui_locales).add_discussion_end_text(discussion_dict, extras_dict,
                                                                                   nickname, at_start=True)

    prepared_discussion = dict()
    prepared_discussion['issues'] = issue_dict
    prepared_discussion['discussion'] = discussion_dict
    prepared_discussion['items'] = item_dict
    prepared_discussion['extras'] = extras_dict
    prepared_discussion['title'] = issue_dict['title']

    return prepared_discussion
