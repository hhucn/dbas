/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function InteractionHandler() {
}

/**
 * Callback, when the logfile was fetched
 * @param data of the ajax request
 */
InteractionHandler.prototype.callbackIfDoneForGettingLogfile = function (data) {
    'use strict';
    // status is the length of the content
    var description = $('#' + popupEditStatementErrorDescriptionId);
    if ('info' in data && data.info.length !== 0) {
        description.text(data.error);
        description.removeClass('text-danger');
        description.addClass('text-info');
        $('#' + popupEditStatementLogfileSpaceId).prev().hide();
    } else {
        new GuiHandler().showLogfileOfPremisegroup(data);
    }
};

/**
 * Callback, when a correcture could be send
 * @param data of the ajax request
 * @param statements_uids
 */
InteractionHandler.prototype.callbackIfDoneForSendCorrectureOfStatement = function (data, statements_uids) {
    'use strict';
    if (!data.error && data.info.length === 0) {
        setGlobalSuccessHandler('Yeah!', _t_discussion(proposalsWereForwarded));
        new PopupHandler().hideAndClearEditStatementsPopup();
        // find the list element and manipulate the edit buttons
        var parentStatement = $('#' + statements_uids[0]).parent();
        parentStatement.find('#item-edit-disabled-hidden-wrapper').show();
        parentStatement.find('.item-edit').remove();
    } else if (!data.error && data.info.length !== 0) {
        setGlobalInfoHandler('Ohh!', data.info);
    } else {
        setGlobalErrorHandler('Ohh!', data.info);
    }
};

/**
 * Callback for Fuzzy Search
 * @param data
 * @param callbackId
 * @param type
 * @param reason
 */
InteractionHandler.prototype.callbackIfDoneFuzzySearch = function (data, callbackId, type, reason) {
    'use strict';
    // if there is no returned data, we will clean the list

    if (Object.keys(data).length === 0) {
        new GuiHandler().clearProposalSpace(callbackId);
    } else {
        new GuiHandler().setStatementsAsProposal(data, callbackId, type, reason);
    }
};

/**
 *
 * @param data
 */
InteractionHandler.prototype.callbackIfDoneForGettingInfosAboutArgument = function (data) {
    'use strict';
    var text, author;
    if (data.author === 'anonymous') {
        author = _t_discussion(an_anonymous_user);
    } else {
        var img = '<img class="img-circle" style="height: 1em;" src="' + data.gravatar + '">';
        author = '<a href="' + data.author_url + '">' + img + ' ' + data.author + '</a>';
    }
    text = _t_discussion(messageInfoStatementCreatedBy) + ' ' + author;
    text += ' (' + data.timestamp + ') ';
    text += _t_discussion(messageInfoCurrentlySupported) + ' ' + data.vote_count + ' ';
    text += _t_discussion(messageInfoParticipant) + '.';

    var users_array = [];
    $.each(data.supporter, function (index, val) {
        users_array.push({
            'avatar_url': data.gravatars[val],
            'nickname': val,
            'public_profile_url': data.public_page[val]
        });
    });

    var gh = new GuiHandler();
    var tbody = $('<tbody>');
    var rows = gh.createUserRowsForOpinionDialog(users_array);
    $.each(rows, function (key, value) {
        tbody.append(value);
    });

    var body = gh.closePrepareTableForOpinionDialog(data.supporter, gh, text, tbody);

    displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(messageInfoTitle), body);
    $('#' + popupConfirmDialogId).find('.modal-dialog').addClass('modal-lg').on('hidden.bs.modal', function () {
        $(this).removeClass('modal-lg');
    });

    setTimeout(function () {
        var popup_table = $('#' + popupConfirmDialogId).find('.modal-body div');
        if ($(window).height() > 400 && popup_table.outerHeight(true) > $(window).height()) {
            popup_table.slimScroll({
                position: 'right',
                railVisible: true,
                alwaysVisible: true,
                height: ($(window).height() / 3 * 2) + 'px'
            });
        }
    }, 300);
};

/**
 *
 * @param data
 */
InteractionHandler.prototype.callbackIfDoneForSendNewIssue = function (data) {
    'use strict';
    $('#popup-add-topic').modal('hide');
    var li = $('<li>').addClass('enabled'),
        a = $('<a>').attr('href', data.issue.url).attr('value', data.issue.title),
        spanTitle = $('<span>').text(data.issue.title),
        spanBadge = $('<span>').addClass('badge').attr('style', 'float: right; margin-left: 1em;').text(data.issue.arg_count),
        divider = $('#' + issueDropdownListID).find('li.divider');
    li.append(a.append(spanTitle).append(spanBadge));
    if (divider.length > 0) {
        li.insertBefore(divider);
    }
    setGlobalSuccessHandler('Yeah!', _t(dataAdded));
};

/**
 *
 * @param data
 * @param is_argument
 */
InteractionHandler.prototype.callbackIfDoneForGettingMoreInfosAboutOpinion = function (data, is_argument) {
    'use strict';
    var usersArray, popupTable;
    if (data.info.length !== 0) {
        setGlobalInfoHandler('Hey', data.info);
        return;
    }

    var gh = new GuiHandler();
    var tbody = $('<tbody>');
    var span = is_argument ? $('<span>').text(data.opinions.message) : $('<span>').text(data.opinions[0].message);

    usersArray = is_argument ? data.opinions.users : data.opinions[0].users;
    var rows = gh.createUserRowsForOpinionDialog(usersArray);
    $.each(rows, function (key, value) {
        tbody.append(value);
    });

    var body = gh.closePrepareTableForOpinionDialog(usersArray, gh, span, tbody);

    displayConfirmationDialogWithoutCancelAndFunction(_t_discussion(usersWithSameOpinion), body);
    $('#' + popupConfirmDialogId).find('.modal-dialog').addClass('modal-lg').on('hidden.bs.modal', function (e) {
        $(this).removeClass('modal-lg');
    });
    setTimeout(function () {
        popupTable = $('#' + popupConfirmDialogId).find('.modal-body div');
        if ($(window).height() > 400 && popupTable.outerHeight(true) > $(window).height()) {
            popupTable.slimScroll({
                position: 'right',
                railVisible: true,
                alwaysVisible: true,
                height: ($(window).height() / 3 * 2) + 'px'
            });
        }
    }, 300);

};

/**
 *
 * @param toggle_element
 * @param data
 */
InteractionHandler.prototype.callbackForSetAvailabilityOfDiscussion = function (toggle_element, data) {
    'use strict';
    if (data.error.length === 0) {
        setGlobalSuccessHandler('Yeah!', _t(discussionsPropertySet));
    } else {
        setGlobalErrorHandler(_t(ohsnap), data.error);
    }
};

/**
 *
 * @param position
 * @param reason
 * @param feature_data
 */
InteractionHandler.prototype.sendArgument = function (position, reason, feature_data) {
    "use strict";

    feature_data = (typeof feature_data !== 'undefined') ? feature_data : {};

    if (position.length === 0 || reason.length === 0) {
        $('#' + addStatementErrorContainer).show();
        $('#' + addStatementErrorMsg).text(_t(inputEmpty));
    } else {
        $('#' + addStatementErrorContainer).hide();
        const data = {
            position: position,
            reason: reason,
            feature_data: feature_data
        };
        new AjaxDiscussionHandler().sendNewStartArgument(data);
    }
};

/**
 *
 * @param t_array
 * @param conclusion
 * @param supportive
 * @param arg
 * @param relation
 * @param type
 */
InteractionHandler.prototype.sendStatement = function (t_array, conclusion, supportive, arg, relation, type) {
    'use strict';
    // error on "no text"
    if (t_array.length === 0) {
        $('#' + addPremiseErrorContainer).show();
        $('#' + addPremiseErrorMsg).text(_t(inputEmpty));
        return false;
    }
    var undecidedTexts = [], decidedTexts = [];
    if ($.isArray(t_array)) {
        for (var i = 0; i < t_array.length; i++) {
            // replace multiple whitespaces
            t_array[i] = t_array[i].replace(/\s\s+/g, ' ');

            // cutting all 'and ' and 'and'
            this.__cuttingAnds(t_array, i);

            // whitespace at the end
            this.__cuttingWhitespaces(t_array, i);

            // sorting the statements, whether they include the keyword 'AND'
            this.__sortStatement(t_array, i, decidedTexts, undecidedTexts);
        }
    }

    if (undecidedTexts.length > 0) {
        for (var j = 0; j < undecidedTexts.length; j++) {
            if (undecidedTexts[j].match(/\.$/)) {
                undecidedTexts[j] = undecidedTexts[j].substr(0, undecidedTexts[j].length - 1);
            }
        }
        new GuiHandler().showSetStatementContainer(undecidedTexts, decidedTexts, supportive, type, arg, relation, conclusion);
        return true;
    }

    // pack the data
    $.each(t_array, function (index, value) {
        if ($.type(value) !== "array") {
            t_array[index] = [value];
        }
    });

    if (type === fuzzy_start_premise) {
        new AjaxDiscussionHandler().sendNewStartPremise(t_array, conclusion, supportive);
    } else if (type === fuzzy_add_reason) {
        new AjaxDiscussionHandler().sendNewPremiseForArgument(parseInt(arg), relation, t_array);
    }
    return true;
};

InteractionHandler.prototype.__cuttingAnds = function (t_array, i) {
    'use strict';
    // cutting all 'and ' and 'and'
    while (t_array[i].indexOf((_t_discussion(and) + ' '), t_array[i].length - (_t_discussion(and) + ' ').length) !== -1 ||
    t_array[i].indexOf((_t_discussion(and)), t_array[i].length - (_t_discussion(and)).length) !== -1) {
        if (t_array[i].indexOf((_t_discussion(and) + ' '), t_array[i].length - (_t_discussion(and) + ' ').length) !== -1) {
            t_array[i] = t_array[i].substr(0, t_array[i].length - (_t_discussion(and) + ' ').length);
        } else {
            t_array[i] = t_array[i].substr(0, t_array[i].length - (_t_discussion(and)).length);
        }
    }
};

InteractionHandler.prototype.__cuttingWhitespaces = function (t_array, i) {
    'use strict';
    while (t_array[i].indexOf((' '), t_array[i].length - (' ').length) !== -1) {
        t_array[i] = t_array[i].substr(0, t_array[i].length - (' ').length);
    }

};

InteractionHandler.prototype.__sortStatement = function (t_array, i, decidedTexts, undecidedTexts) {
    'use strict';
    if (t_array[i].toLocaleLowerCase().indexOf(' ' + _t_discussion(and) + ' ') === -1) {
        decidedTexts.push(t_array[i]);
    } else {
        undecidedTexts.push(t_array[i]);
    }

};
