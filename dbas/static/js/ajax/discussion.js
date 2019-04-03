/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function AjaxDiscussionHandler() {
}

/**
 * Sends new premises to the server. Answer will be given to a callback
 * @param arg_uid
 * @param relation
 * @param premisegroups
 */
AjaxDiscussionHandler.prototype.sendNewPremiseForArgument = function (arg_uid, relation, premisegroups) {
    'use strict';
    $('#' + addPremiseErrorContainer).hide();
    $('#' + addPremiseErrorMsg).text('');
    var url = 'set_new_premises_for_argument';
    var d = {
        argument_id: arg_uid,
        attack_type: relation,
        premisegroups: premisegroups
    };
    var done = function ajaxSendNewPremisesForArgumentDone(data) {
        if (data.error.length > 0) {
            $('#' + addPremiseErrorContainer).show();
            $('#' + addPremiseErrorMsg).text(data.error);
        } else {
            window.location.href = data.url;
        }
    };
    var fail = function ajaxSendNewPremisesForArgumentFail(data) {
        $('#' + addPremiseErrorContainer).show();
        $('#' + addPremiseErrorMsg).text(data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 *
 * @param data
 */
AjaxDiscussionHandler.prototype.sendNewStartArgument = function (data) {
    'use strict';
    const url = 'set_new_start_argument';
    const done = function ajaxSendNewStartArgumentDone(data) {
        window.location.href = data.url;
    };
    const fail = function ajaxSendNewStartArgumentFail(data) {
        $('#' + addStatementErrorContainer).show();
        $('#' + addStatementErrorMsg).text(data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', data, done, fail);
};

/**
 * Sends new premises to the server. Answer will be given to a callback
 * @param premisegroups List of premisegroups
 * @param conclusion_id id of the conclusion
 * @param supportive boolean, whether it is supportive
 */
AjaxDiscussionHandler.prototype.sendNewStartPremise = function (premisegroups, conclusion_id, supportive) {
    'use strict';
    $('#' + addPremiseErrorContainer).hide();
    $('#' + addPremiseErrorMsg).text('');
    var url = 'set_new_start_premise';
    var d = {
        premisegroups: premisegroups,
        conclusion_id: parseInt(conclusion_id),
        supportive: supportive
    };
    var done = function ajaxSendNewStartPremiseDone(data) {
        if ('error' in data && data.error && data.error.length > 0) {
            $('#' + addPremiseErrorContainer).show();
            $('#' + addPremiseErrorMsg).text(data.error);
        } else {
            window.location.href = data.url;
        }
    };
    var fail = function ajaxSendNewStartPremiseFail(data) {
        $('#' + addPremiseErrorContainer).show();
        $('#' + addPremiseErrorMsg).text(data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 *
 * @param info
 * @param long_info
 * @param title
 * @param is_public
 * @param is_read_only
 * @param language
 */
AjaxDiscussionHandler.prototype.sendNewIssue = function (info, long_info, title, is_public, is_read_only, language) {
    'use strict';
    $('#add-topic-error').hide();
    var url = 'set_new_issue';
    var d = {
        info: info,
        long_info: long_info,
        title: title,
        is_public: is_public,
        is_read_only: is_read_only,
        lang: language
    };
    var done = function ajaxSendnewIssueDone(data) {
        new InteractionHandler().callbackIfDoneForSendNewIssue(data);
    };
    var fail = function ajaxSendnewIssueFail(data) {
        $('#' + addTopicPopupError).removeClass('hidden');
        $('#' + addTopicPopupErrorText).text(data.responseJSON.errors[0].description);
        setTimeout(function () {
            $('#' + addTopicPopupError).addClass('hidden');
            $('#' + addTopicPopupErrorText).text('');
        }, 2500);
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 * Requests the logfile for the given uid
 * @param statements_uids current uid of the statement
 */
AjaxDiscussionHandler.prototype.getLogfileForStatements = function (statements_uids) {
    'use strict';
    var url = 'get_logfile_for_statements';
    var d = {
        uids: statements_uids,
        issue: getCurrentIssueId()
    };
    var done = function ajaxGetLogfileForStatementsDone(data) {
        new InteractionHandler().callbackIfDoneForGettingLogfile(data);
    };
    var fail = function ajaxGetLogfileForStatementsFail(data) {
        var description = $('#' + popupEditStatementErrorDescriptionId);
        description.text(data.responseJSON.errors[0].description);
        description.addClass('text-danger');
        description.removeClass('text-info');
        $('#' + popupEditStatementLogfileSpaceId).prev().hide();
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 * Sends a correction of statements
 * @param elements
 * @param statements_uids
 */
AjaxDiscussionHandler.prototype.sendCorrectionOfStatement = function (elements, statements_uids) {
    'use strict';
    var url = 'set_correction_of_statement';
    var d = {
        'elements': elements
    };
    var done = function ajaxSendCorrectureOfStatementDone(data) {
        new InteractionHandler().callbackIfDoneForSendCorrectureOfStatement(data, statements_uids);
    };
    var fail = function ajaxSendCorrectureOfStatementFail(data) {
        setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 * Shortens url
 * @param long_url for shortening
 */
AjaxDiscussionHandler.prototype.getShortenUrl = function (long_url) {
    'use strict';
    var url = 'get_shortened_url';
    var d = {
        url: encodeURI(long_url),
        issue: getCurrentIssueId()
    };
    var done = function ajaxGetShortenUrlDone(data) {
        var service = '<a href="' + data.service_url + '" title="' + data.service + '" target="_blank">' + data.service_text + '</a>';
        $('#' + popupUrlSharingDescriptionPId).html(_t_discussion(feelFreeToShareUrl) + ' (' + _t_discussion(shortenedBy) + ' ' + service + '):');
        $('#' + popupUrlSharingInputId).val(data.url).data('short-url', data.url);
    };
    var fail = function ajaxGetShortenUrl(data) {
        setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        new PopupHandler().hideAndClearUrlSharingPopup();
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 *
 * @param uid
 */
AjaxDiscussionHandler.prototype.getMoreInfosAboutArgument = function (uid) {
    'use strict';
    var url = 'get_infos_about_argument';
    var d = {
        argument_id: uid,
        lang: getDiscussionLanguage()
    };
    var done = function ajaxGetMoreInfosAboutArgumentDone(data) {
        new InteractionHandler().callbackIfDoneForGettingInfosAboutArgument(data);
    };
    var fail = function ajaxGetMoreInfosAboutArgumentFail(data) {
        var element = $('<p>').html(data.responseJSON.errors[0].description);
        displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(messageInfoTitle), element);
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 *
 * @param type
 * @param argument_uid
 * @param statement_uid
 */
AjaxDiscussionHandler.prototype.getMoreInfosAboutOpinion = function (type, argument_uid, statement_uid) {
    'use strict';
    var is_argument = type === 'argument';
    var is_position = type === 'position' || type === 'statement';
    var uid = typeof argument_uid === 'undefined' ? statement_uid : argument_uid;

    var url = 'get_user_with_same_opinion';
    var d = {
        uid: uid,
        is_argument: is_argument,
        is_attitude: false,
        is_reaction: false,
        is_position: is_position,
        lang: getDiscussionLanguage()
    };
    var done = function ajaxGetMoreInfosAboutOpinionDone(data) {
        new InteractionHandler().callbackIfDoneForGettingMoreInfosAboutOpinion(data, is_argument);
    };
    var fail = function ajaxGetMoreInfosAboutOpinionFail(data) {
        setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
    };

    ajaxSkeleton(url, 'POST', d, done, fail);

};

/***
 * Ajax request for the fuzzy search
 * @param value
 * @param callbackId
 * @param type
 * @param statement_uid optional integer
 * @param reason optional
 */
AjaxDiscussionHandler.prototype.fuzzySearch = function (value, callbackId, type, statement_uid, reason) {
    'use strict';
    var callback = $('#' + callbackId);
    var tmpid = callbackId.split('-').length === 6 ? callbackId.split('-')[5] : '0';
    var bubble_value = value;
    if (tmpid === 'reason' || tmpid === 'position') {
        var pos = escapeHtml($('#' + addStatementContainerMainInputPosId).val());
        var res = escapeHtml($('#' + addStatementContainerMainInputResId).val());
        pos = pos.length === 0 ? '...' : pos;
        res = res.length === 0 ? '...' : res;
        bubble_value = pos + ' ' + _t_discussion(because) + ' ' + res;
        tmpid = 'reason_position';
    }

    if (statement_uid.length === 0) {
        statement_uid = 0;
    }

    // clear lists if input is empty
    if (callback.val().length === 0) {
        new GuiHandler().clearProposalSpace(callbackId);
        $('p[id^="current_"]').each(function () {
            $(this).parent().remove();
        });
        return;
    }

    if (!$.inArray(type, [fuzzy_find_user, fuzzy_find_statement, fuzzy_duplicate])) {
        this.__someGuiModification(tmpid, bubble_value);
    }

    var url = type === fuzzy_find_user ? 'fuzzy_nickname_search' : 'fuzzy_search';
    var d = {
        value: value,
        type: type,
        statement_uid: statement_uid,
        issue: getCurrentIssueId()
    };
    var done = function ajaxFuzzySearchDone(data) {
        new InteractionHandler().callbackIfDoneFuzzySearch(data, callbackId, type, reason);
    };
    var fail = function ajaxFuzzySearchFail() {
        new GuiHandler().clearProposalSpace(callbackId);
    };
    callback.focus();
    ajaxSkeleton(url, 'POST', d, done, fail);
};

AjaxDiscussionHandler.prototype.__someGuiModification = function(tmpid, bubble_value){
    'use strict';
    var bubbleSpace = $('#' + discussionBubbleSpaceId);
    var pencil = ' <i class="fa fa-pencil" aria-hidden="true"></i>';
    var opener = $('#' + addPositionContainerMainInputIntroId).text().replace('...', _t_discussion(because) + ' ');
    // add or remove bubble only iff we are not in an popup
    if (type !== fuzzy_statement_popup) {
        if (bubbleSpace.find('#current_' + tmpid).length === 0) {
            var text = $('<p>').addClass('triangle-r').attr('id', 'current_' + tmpid).html(opener + bubble_value + '...' + pencil);
            var current = $('<div>').addClass('line-wrapper-r').append(text).hide().fadeIn();
            current.insertAfter(bubbleSpace.find('div:last-child'));
            setInterval(function () { // fading pencil
                bubbleSpace.find('.fa-pencil').fadeTo('slow', 0.2, function () {
                    bubbleSpace.find('.fa-pencil').fadeTo('slow', 1.0, function () {
                    });
                });
            }, 1000);
        } else {
            $('#current_' + tmpid).html(opener + ' ' + bubble_value + '...' + pencil);
        }
    }
    var gh = new GuiHandler();
    var resize = gh.setMaxHeightForBubbleSpace();
    gh.setMaxHeightForDiscussionContainer(resize);
};

/**
 *
 * @param uid
 * @param is_argument
 */
AjaxDiscussionHandler.prototype.revokeContent = function (uid, is_argument) {
    'use strict';
    var url = is_argument ? 'revoke_argument_content' : 'revoke_statement_content';
    var d = {uid: parseInt(uid)};
    var done = function ajaxRevokeContentDone(data) {
        if (data.success) {
            setGlobalSuccessHandler('Yeah!', _t_discussion(dataRemoved) + ' ' + _t_discussion(yourAreNotTheAuthorOfThisAnymore));
        } else {
            setGlobalSuccessHandler('Yeah!', _t_discussion(contentWillBeRevoked));
        }
    };
    var fail = function ajaxRevokeContentFail(data) {
        setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
        new PopupHandler().hideAndClearUrlSharingPopup();
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 * Marks given statements as read
 *
 * @param uids of the statements
 */
AjaxDiscussionHandler.prototype.setSeenStatements = function (uids) {
    'use strict';
    var url = 'set_seen_statements';
    var d = {
        uids: uids
    };
    var done = function () {
    };
    var fail = function () {
        $('#' + discussionSpaceShowItems).attr('data-send-request', 'true');
        $('#' + discussionSpaceHideItems).attr('data-send-request', 'true');
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 *
 * @param uid
 * @param is_argument
 * @param is_supportive
 * @param should_mark
 * @param step
 * @param history
 * @param callback_id
 */
AjaxDiscussionHandler.prototype.markStatementOrArgument = function (uid, is_argument, is_supportive, should_mark, step, history, callback_id) {
    'use strict';
    var url = 'mark_statement_or_argument';
    var d = {
        uid: uid,
        is_argument: is_argument,
        is_supportive: is_supportive,
        should_mark: should_mark,
        step: step,
        history: history
    };
    var done = function ajaxMarkStatementOrArgumentDone(data) {
        setGlobalSuccessHandler('Yeah!', data.success);
        var el = $('#' + callback_id);
        el.hide();
        if (data.text.length > 0) {
            el.parent().find('.triangle-content').html(data.text);
        }
        if (should_mark) {
            el.prev().show();
        } else {
            el.next().show();
        }
    };
    var fail = function ajaxMarkStatementOrArgumentFail(data) {
        setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

/**
 * Set properties for every discussion on the private discussion page
 * @param toggle_element
 */
AjaxDiscussionHandler.prototype.setDiscussionSettings = function (toggle_element) {
    'use strict';
    var _this = this;
    var checked = toggle_element.prop('checked');
    var url = 'set_discussion_properties';
    var d = {
        property: checked,
        issue: toggle_element.data('uid'),
        value: toggle_element.data('keyword')
    };
    var done = function setDiscussionSettingsDone(data) {
        new InteractionHandler().callbackForSetAvailabilityOfDiscussion(toggle_element, data);
        if (toggle_element.attr('class') === 'discussion-enable-toggle') {
            _this.replaceTitleOfDiscussionOverview(checked, toggle_element);
            _this.replaceShortLinkOfDiscussionOverview(checked, toggle_element);
        }
    };
    var fail = function setDiscussionSettingsFail(data) {
        setGlobalErrorHandler(_t(ohsnap), data.responseJSON.errors[0].description);
    };
    ajaxSkeleton(url, 'POST', d, done, fail);
};

AjaxDiscussionHandler.prototype.replaceTitleOfDiscussionOverview = function (checked, toggle_element) {
    'use strict';
    var tr = $('tr[data-uid="' + toggle_element.data('uid') + '"]');
    var child = $(tr.find('td:first'));
    var url = child.data('url');
    var text = child.text().trim();
    if (checked) {
        child.find('span').replaceWith('<a href="' + url + '">' + text + '</a>');
    } else {
        child.find('a').replaceWith('<span>' + text + '</span>');
    }
};

AjaxDiscussionHandler.prototype.replaceShortLinkOfDiscussionOverview = function (checked, toggle_element) {
    'use strict';
    var tr = $('tr[data-uid="' + toggle_element.data('uid') + '"]');
    var child = $(tr.find('td:last'));
    var clipboard = $('<i>').attr({
        'class': 'fa fa-clipboard',
        'aria-hidden': 'true', 'style':
            'margin-left: 0.5em; cursor: pointer;'
    });
    var text = child.text().trim();
    if (checked) {
        child.empty();
        child.append($('<a>').attr('href', text).text(text));
        child.append(clipboard);
        new MyDiscussion().set_clipboard(clipboard);
    } else {
        child.empty();
        child.append($('<span>').text(text));
    }
};
