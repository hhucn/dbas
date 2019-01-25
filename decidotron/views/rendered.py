from dbas.views import *


@view_config(route_name='discussion_init_with_slug', renderer='../../templates/discussion/main.pt',
             permission='everybody')
@view_config(route_name='discussion_init_with_slug_with_slash', renderer='../../templates/discussion/main.pt',
             permission='everybody')
@validate(check_authentication, valid_issue_by_slug, valid_user_optional)
def init(request):
    """
    View configuration for the initial discussion.

    :param request: request of the web server
    :return: dictionary
    """
    LOG.debug("Configuration for initial discussion. %s", request.matchdict)
    emit_participation(request)

    prepared_discussion = discussion.init(request.validated['issue'], request.validated['user'])
    modify_discussion_url(prepared_discussion)
    modify_discussion_bubbles(prepared_discussion, request.registry)

    rdict = prepare_request_dict(request)

    # redirect to oauth url after login and redirecting
    if request.authenticated_userid and 'service' in request.params and request.params['service'] in oauth_providers:
        url = request.session['oauth_redirect_url']
        return HTTPFound(location=url)

    append_extras_dict(prepared_discussion, rdict, request.authenticated_userid, False)
    if len(prepared_discussion['items']['elements']) == 1:
        _dh = DictionaryHelper(rdict['ui_locales'], prepared_discussion['issues']['lang'])
        nickname = request.authenticated_userid if request.authenticated_userid else nick_of_anonymous_user
        _dh.add_discussion_end_text(prepared_discussion['discussion'], prepared_discussion['extras'], nickname,
                                    at_start=True)

    return prepared_discussion