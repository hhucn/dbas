/*global $, _t, _t_discussion */
/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */


function Main() {
}

/**
 * Sets all click functions
 *
 * @param guiHandler
 * @param popupHandler
 * @param ajaxHandler
 */
Main.prototype.setClickFunctions = function (guiHandler, popupHandler, ajaxHandler) {
    'use strict';

    this.__setClFunctionsSomeElements(guiHandler);
    this.__setClickFunctionsPopupElements(guiHandler, popupHandler);
    this.__setClickFunctionsShareElements(guiHandler, popupHandler);
    this.__setClickFunctionsDisplayElements(guiHandler);
    this.__setClickFunctionsTriangleElements(guiHandler, popupHandler, ajaxHandler);
    this.__setClickFunctionsListElements(guiHandler, popupHandler);
    this.__setClickFunctionsDiscussionSpace(guiHandler, popupHandler, ajaxHandler);
};

Main.prototype.__setClFunctionsSomeElements = function (guiHandler) {
    'use strict';
    $('.icon-add-premise').each(function () {
        $(this).click(function () {
            guiHandler.appendAddPremiseRow($(this));
            $(this).hide().prev().show();
            $('#' + sendNewPositionId).val(_t(saveMyStatements));
        });
    });

    // admin list all users button
    $('#' + listAllUsersButtonId).click(function listAllUsersButtonId() {
        if ($(this).val() === _t(showAllUsers)) {
            ajaxHandler.getUsersOverview();
            $(this).val(_t(hideAllUsers));
        } else {
            $('#' + adminsSpaceForUsersId).empty();
            $(this).val(_t(showAllUsers));
        }
    });

    // admin list all attacks button
    $('#' + listAllArgumentId).click(function listAllUsersAttacksId() {
        if ($(this).val() === _t(showAllAttacks)) {
            ajaxHandler.getArgumentOverview();
        } else {
            $('#' + adminsSpaceForArgumentsId).empty();
        }
    });

    // hiding the argument container, when the X button is clicked
    $('#' + closeStatementContainerId).click(function closeStatementContainerId() {
        $('#' + addStatementContainerId).hide();
        $('#' + addStatementErrorContainer).hide();
        $('#' + discussionSpaceId + ' li:last-child input').prop('checked', false).enable = true;
    });

    // hides container
    $('#' + closePremiseContainerId).click(function closeStatementContainerId() {
        $('#' + addPositionContainerId).hide();
        $('#' + addPremiseErrorContainer).hide();
        $('#' + discussionSpaceId + ' li:last-child input').prop('checked', false).enable = true;
    });

    // hiding the island view, when the X button is clicked
    $('#' + closeGraphViewContainerId).click(function () {
        guiHandler.resetChangeDisplayStyleBox();
    });
};

Main.prototype.__setClickFunctionsDisplayElements = function (guiHandler) {
    'use strict';

    $('#' + displayStyleIconGuidedId).click(function displayStyleIconGuidedFct() {
        guiHandler.setDisplayStyleAsDiscussion();
        clearAnchor();
    });
    $('#' + displayStyleIconGraphId).click(function displayStyleIconExpertFct() {
        guiHandler.setDisplayStyleAsGraphView();
        new DiscussionGraph({}, false).showGraph(false);
        setAnchor('graph');
    });

    // opinion barometer
    $('#' + opinionBarometerImageId).show().click(function opinionBarometerFunction() {
        new DiscussionBarometer().showBarometer();
        setAnchor('barometer');
    });

    // issues
    $('#' + issueDropdownListID + ' .enabled').each(function () {
        if ($(this).children().length > 0) {
            $(this).children().click(function () {
                var href = $(this).attr('href');
                var text = _t(switchDiscussionText).replace('XXX', $(this).attr('data-value'));
                $(this).attr('href', '#');
                displayConfirmationDialogWithCheckbox(_t(switchDiscussion), text, _t.keepSetting, href, true);
            });
        }
    });
    $('#' + issueDropdownListID + ' .disabled a').off('click').unbind('click').removeAttr('href');
};

Main.prototype.__setClickFunctionsPopupElements = function (guiHandler, popupHandler) {
    'use strict';
    // close popups
    $('#' + popupEditStatementCloseButtonXId).click(function popupEditStatementCloseButtonXId() {
        popupHandler.hideAndClearEditStatementsPopup();
    });
    $('#' + popupEditStatementCloseButtonId).click(function popupEditStatementCloseButtonId() {
        popupHandler.hideAndClearEditStatementsPopup();
    });
    $('#' + popupUrlSharingCloseButtonXId).click(function popupUrlSharingCloseButtonXId() {
        popupHandler.hideAndClearUrlSharingPopup();
    });
    $('#' + popupUrlSharingCloseButtonId).click(function popupUrlSharingCloseButtonId() {
        popupHandler.hideAndClearUrlSharingPopup();
    });

    $('#' + popupEditStatementSubmitButtonId).click(function popupEditStatementSubmitButton() {
        var elements = [];
        $('#' + popupEditStatementInputSpaceId).find('input').each(function () {
            elements.push({'text': $(this).val(), 'uid': $(this).data('statement-uid')});
        });
        new AjaxDiscussionHandler().sendCorrectionOfStatement(elements);
    });

    /**
     * Switch between shortened and long url
     */
    $('#' + popupUrlSharingLongUrlButtonID).click(function () {
        var input_field = $('#' + popupUrlSharingInputId);

        if ($(this).data('is-short-url') === '0') {
            input_field.val(input_field.data('short-url'));
            $(this).data('is-short-url', '1').text(_t_discussion(fetchLongUrl));
        } else {
            input_field.val(window.location);
            $(this).data('is-short-url', '0').text(_t_discussion(fetchShortUrl));
        }
    });

};

Main.prototype.__setClickFunctionsListElements = function (guiHandler, popupHandler) {
    'use strict';
    var list = $('#' + discussionSpaceListId);
    list.find('.item-flag').click(function () {
        var uid = $(this).parents('.premise-input').find('.premise-title').attr('id').replace('item_', '');
        var text = [];
        var txt;
        $.each($(this).parent().find('label'), function () {
            txt = $(this).text();
            if (txt.match(/\.$/)) { // remove a dot at the end
                txt = txt.substr(0, txt.length - 1);
            }
            text.push(txt);
        });
        popupHandler.showFlagStatementPopup(parseInt(uid), false, text.join(' '));
    });

    list.find('.item-edit').click(function () {
        var uids = [];
        $(this).closest('.premise-input').find('.premise-title').each(function () {
            uids.push($(this).attr('id'));
        });
        popupHandler.showEditStatementsPopup(uids);
    });

    list.find('.item-trash').click(function () {
        var uid = $(this).closest('.premise-input').find('.premise-title').attr('id');
        popupHandler.showDeleteContentPopup(uid, false);
    });

    list.find('.item-reference').click(function () {
        var uids = [];
        $(this).closest('.premise-input').find('.premise-title').each(function () {
            uids.push(parseInt($(this).attr('id')));
        });
        new AjaxReferenceHandler().getReferences(uids, false);
    });
};

Main.prototype.__setClickFunctionsTriangleElements = function (guiHandler, popupHandler, ajaxHandler) {
    'use strict';
    // get infos about the author
    var trianglel = $('.triangle-l');
    var uid;
    trianglel.find('.triangle-content-text').click(function () {
        var url = window.location.href;
        if (url.indexOf('/d?history') !== -1) {
            url = url.split('/d?history');
            url = url[0].split('/');
            uid = parseInt(url[url.length - 1]);
            ajaxHandler.getMoreInfosAboutArgument(uid, true);
        } else {
            if ($(this).closest('p').attr('id').indexOf(questionBubbleId) !== -1) {
                uid = $(this).closest('p').attr('id').replace(questionBubbleId + '-', '');
                ajaxHandler.getMoreInfosAboutArgument(parseInt(uid), true);
            }
        }
    });

    // do not hover the other spans on hovering the name
    this.__setTriangleHoverFunc(trianglel);

    var splitted_url = window.location.href.split('/');
    if (splitted_url.length > 5) {
        if (window.location.href.split('/')[5].indexOf('jump') !== -1) {
            trianglel.find('.triangle-content').hover(function () {
                $(this).css('color', '#000').css('cursor', 'default');

            }, function () {
                $(this).css('color', '');
            });
        }
    }

    // remove hover on start
    if (trianglel.length === 1 && trianglel.attr('id') === 'start') {
        trianglel.html(trianglel.text().trim());
    }

    trianglel.find('.triangle-flag').click(function () {
        var uid = $(this).closest('.triangle-l').attr('id').replace(questionBubbleId + '-', '');
        popupHandler.showFlagArgumentPopup(parseInt(uid));
    });

    trianglel.find('.triangle-reference').click(function () {
        var uid = $(this).parent().attr('id').replace(questionBubbleId + '-', '');
        new AjaxReferenceHandler().getReferences([parseInt(uid)], true);
    });

    trianglel.find('.triangle-trash').click(function () {
        var uid = $(this).parent().attr('id').replace(questionBubbleId + '-', '');
        popupHandler.showDeleteContentPopup(uid, true);
    });

    // user info click
    $('.triangle-r-info').each(function () {
        if ($(this).data('votecount') > 0) {
            $(this).click(function () {
                var data_type = $(this).data('type');
                var data_argument_uid = $(this).data('argument-uid');
                var data_statement_uid = $(this).data('statement-uid');
                new AjaxDiscussionHandler().getMoreInfosAboutOpinion(data_type, data_argument_uid, data_statement_uid);
            });
        } else {
            $(this).removeClass('triangle-r-info').addClass('triangle-r-info-nohover');
        }
    });

};

Main.prototype.__setTriangleHoverFunc = function (trianglel) {
    'use strict';
    trianglel.find('.triangle-content a').hover(function () {
        trianglel.find('.triangle-content-text').each(function () {
            if (!('argumentationType' in $(this).data())) {
                $(this).css('color', '#000');
            }
        });
    }, function () {
        trianglel.find('.triangle-content-text').each(function () {
            if (!('argumentationType' in $(this).data())) {
                $(this).css('color', '');
            }
        });
    });
};

Main.prototype.__setClickFunctionsShareElements = function (guiHandler, popupHandler) {
    'use strict';

    // share url for argument blogging
    $('#' + shareUrlId).click(function shareUrlClick() {
        popupHandler.showUrlSharingPopup();
    });

    /**
     * Sharing shortened url with mail
     */
    $('#' + shareUrlButtonMail).click(function shareUrlButtonMail() {
        new Sharing().emailShare('user@example.com', _t(interestingOnDBAS), _t(haveALookAt) + ' ' + $('#' + popupUrlSharingInputId).val());
    });

    /**
     * Sharing shortened url on twitter
     */
    $('#' + shareUrlButtonTwitter).click(function shareUrlButtonTwitter() {
        new Sharing().twitterShare($('#' + popupUrlSharingInputId).val(), '');
    });

    /**
     * Sharing shortened url on google
     */
    $('#' + shareUrlButtonGoogle).click(function shareUrlButtonGoogle() {
        new Sharing().googlePlusShare($('#' + popupUrlSharingInputId).val());
    });

    /**
     * Sharing shortened url on facebook
     */
    $('#' + shareUrlButtonFacebook).click(function shareUrlButtonFacebook() {
        var val = $('#' + popupUrlSharingInputId).val();
        new Sharing().facebookShare(val, "FB Sharing", _t(haveALookAt) + ' ' + val,
            mainpage + "static/images/logo.png");
    });

};

Main.prototype.__setClickFunctionsDiscussionSpace = function (guiHandler, popupHandler, ajaxHandler) {
    'use strict';

    // adding issues
    $('#' + addTopicButtonId).click(function () {
        popupHandler.showAddTopicPopup();
    });

    $('#' + discussionSpaceShowItems).click(function () {
        $(this).hide();
        var hide_btn = $('#' + discussionSpaceHideItems);
        var space = $('#' + discussionSpaceListId);
        hide_btn.show();
        // send request if it was not send until now
        if ($(this).attr('data-send-request') !== 'true') {
            var uids = [];
            $.each(space.find('li:not(:visible)'), function () {
                $.each($(this).find('label:even'), function () {
                    uids.push($(this).attr('id'));
                });
            });
            new AjaxDiscussionHandler().setSeenStatements(uids);
        }
        // fade in after we collected the missed id's!
        space.find('li[style="display: none;"]').addClass('cropped').fadeIn();

        // guification, resize main container and sidebar
        var container = $('#' + discussionContainerId);
        var add_height = space.find('li.cropped').length * space.find('li:visible:first').outerHeight() + hide_btn.outerHeight();
        var container_height = parseInt(container.css('max-height').replace('px', ''));
        container.css('max-height', (add_height + container_height) + 'px');
        container.attr('data-add-height', add_height);
    });

    $('#' + discussionSpaceHideItems).click(function () {
        $(this).hide();
        $('#' + discussionSpaceShowItems).show();
        $('#' + discussionSpaceListId).find('li.cropped').fadeOut();
        var container = $('#' + discussionContainerId);
        var height = parseInt(container.css('max-height').replace('px', ''));
        var new_height = height - parseInt(container.attr('data-add-height'));
        // guification, resize main container and sidebar
        setTimeout(function () {
            container.css('max-height', new_height + 'px');
        }, 400);
    });

    // star click
    $('.' + checkAsUsersOpinion).click(function () {
        var id = 'star-' + new Date().getTime();
        $(this).attr('id', id);
        var info = $(this).parent().children().last();
        var is_argument = info.data('type') === 'argument';
        var uid = info.data(info.data('type') + '-uid');
        var is_supportive = info.data('is-supportive').toLocaleLowerCase() === 'true';
        var step = location.href.split('#')[0].split('?')[0].split('/').slice(5).join('/');
        var current_history = location.href.split('#')[0].split('?')[1];
        ajaxHandler.markStatementOrArgument(uid, is_argument, is_supportive, true, step, current_history, id);
    });

    $('.' + uncheckAsUsersOpinion).click(function () {
        var id = 'star-' + new Date().getTime();
        $(this).attr('id', id);
        var info = $(this).parent().children().last();
        var is_argument = info.data('type') === 'argument';
        var uid = info.data(info.data('type') + '-uid');
        var is_supportive = info.data('is-supportive').toLocaleLowerCase() === 'true';
        var step = location.href.split('#')[0].split('?')[0].split('/').slice(5).join('/');
        var current_history = location.href.split('#')[0].split('?')[1];
        ajaxHandler.markStatementOrArgument(uid, is_argument, is_supportive, false, step, current_history, id);
    });

    // styling
    $('.fa-star[data-is-users-opinion="True"]').show();
    $('.fa-star-o[data-is-users-opinion="False"]').show();

    // search statement
    $('#sidebar-search-statement').click(function () {
        popupHandler.showSearchStatementPop();
    });

    // search statement
    $('#sidebar-ask-a-friend').click(function () {
        new PopupHandler().showNotificationPopup();
        $('#popup-writing-notification-title').val(_t_discussion(askAFriendTitle)).trigger('keyup');
        $('#popup-writing-notification-text').html(_t_discussion(askAFriendText) + window.location.href).css('height', '120px').trigger('keyup');
        new Notifications().setGui();
    });

};

/**
 * Sets all keyUp functions
 * @param guiHandler
 * @param ajaxHandler
 */
Main.prototype.setKeyUpFunctions = function (guiHandler, ajaxHandler) {
    'use strict';
    // gui for the fuzzy search (position)
    $('#' + addStatementContainerMainInputPosId).keyup(function () {
        setTimeout(function () {
            var escapedText = escapeHtml($('#' + addStatementContainerMainInputPosId).val());
            ajaxHandler.fuzzySearch(escapedText, addStatementContainerMainInputPosId, fuzzy_start_statement, '', '');
        }, 200);
    });

    // gui for the fuzzy search (positions premise)
    $('#' + addStatementContainerMainInputResId).keyup(function () {
        setTimeout(function () {
            var escapedText = escapeHtml($('#' + addStatementContainerMainInputResId).val());
            ajaxHandler.fuzzySearch(escapedText, addStatementContainerMainInputResId, fuzzy_start_premise, '', '');
        }, 200);
    });

    // gui for the fuzzy search (premises)
    $('#' + addPositionContainerMainInputId).keyup(function () {
        setTimeout(function () {
            var escapedText = escapeHtml($('#' + addPositionContainerMainInputId).val());
            ajaxHandler.fuzzySearch(escapedText, addPositionContainerMainInputId, fuzzy_add_reason, '', '');
        }, 200);
    });
};

/**
 *
 * @param guiHandler
 */
Main.prototype.setStyleOptions = function (guiHandler) {
    'use strict';
    guiHandler.setMaxHeightForBubbleSpace();
    guiHandler.hideSuccessDescription();
    guiHandler.hideErrorDescription();

    // no hover action on the systems bubble during the attitude question
    var trianglel = $('.triangle-l');
    var url = window.location.href.split('?')[0];
    if (url.indexOf('attitude') !== -1 || url.indexOf('justify') !== -1) {
        trianglel.find('.triangle-content').each(function () {
            $(this).hover(function () {
                $(this).css({'color': '#000', 'cursor': 'auto'});
            }, function () {
                $(this).css({'color': '#000', 'cursor': 'auto'});
            });
        });
    }

    // focus text of input elements
    $('#' + popupUrlSharingInputId).on("click", function () {
        $(this).select();
    });

    // hover effects on text elements
    var data = 'data-argumentation-type';
    var list = $('#' + discussionSpaceListId);
    var trianglel_last = trianglel.last();
    list.find('span[' + data + '!=""]').each(function () {
        var attr = $(this).attr(data);
        var tmp = $('<span>').addClass(attr + '-highlighter');
        tmp.appendTo(document.body);
        var old_color = $(this).css('color');
        var new_color = tmp.css('color');
        tmp.remove();
        $(this).hover(
            function () {
                $('#' + discussionBubbleSpaceId).find('span[' + data + '="' + attr + '"]')
                    .css({'color': new_color, 'background-color': '#edf3e6', 'border-radius': '2px'});
                if ($(this).attr(data) === 'argument') {
                    trianglel_last.find('span[data-attitude="pro"]').addClass('text-success').css({
                        'background-color': '#edf3e6',
                        'border-radius': '2px'
                    });
                    trianglel_last.find('span[data-attitude="con"]').addClass('text-danger').css({
                        'background-color': '#edf3e6',
                        'border-radius': '2px'
                    });
                }
            }, function () {
                $('#' + discussionBubbleSpaceId).find('span[' + data + '="' + attr + '"]')
                    .css({'color': old_color, 'background-color': '', 'border-radius': ''});
                trianglel_last.find('span[data-attitude="pro"]').removeClass('text-success').css({
                    'background-color': '',
                    'border-radius': ''
                });
                trianglel_last.find('span[data-attitude="con"]').removeClass('text-danger').css({
                    'background-color': '',
                    'border-radius': ''
                });
            }
        );
    });

    // hover on radio buttons
    guiHandler.hoverInputListOf($('#popup-flag-argument'));
    guiHandler.hoverInputListOf($('#popup-flag-statement'));
    guiHandler.hoverInputListOf(list);

    list.find('li').find('.fa').parent().hide();
    list.find('li').each(function () {
        $(this).hover(function () {
            $(this).find('.fa').parent().show();
        }, function () {
            $(this).find('.fa').parent().hide();
        });
    });
};

/**
 * Sets some style options for the window
 */
Main.prototype.setWindowOptions = function () {
    'use strict';
    // some hack
    $('#navbar-left').empty();

    var container = $('#' + discussionContainerId);
    var oldContainerSize = container.outerWidth();
    var burger = $('.hamburger');
    var wrapper = $('#dialog-wrapper');

    $(window).resize(function () {
        new GuiHandler().setMaxHeightForBubbleSpace();

        // resize main container
        var difference = oldContainerSize - container.outerWidth();
        if (difference > 0 && burger.hasClass('open')) {
            wrapper.width(wrapper.width() - difference);
        } else if (difference < 0 && burger.hasClass('open')) {
            wrapper.width(wrapper.width() - difference);
        }
        oldContainerSize = container.width();
    });
};

/**
 *
 */
Main.prototype.setGuiOptions = function () {
    'use strict';

    // highlight edited statement
    var pos = window.location.href.indexOf('edited_statement=');
    if (pos !== -1) {
        var ids = window.location.href.substr(pos + 'edited_statement='.length);
        var splitted = ids.split(',');
        $.each(splitted, function (index, value) {
            $('#' + value).css('background-color', '#FFF9C4');
        });
    }
};

/**
 *
 * @param guiHandler
 * @param interactionHandler
 */
Main.prototype.setInputExtraOptions = function (guiHandler, interactionHandler) {
    'use strict';
    var textArray = [], splits, conclusion, supportive, arg, relation;
    splits = window.location.href.split('?')[0].split('/');
    var push = function (_this) {
        if ($(_this).val().length > 0) {
            textArray.push($(_this).val());
        }
    };
    var sendStartStatement = function () {
        var data = $("#add-statement-container-body :input").toArray()
            .map(input => [input.dataset.key, input.value])
            .reduce((accumulator, currentValue) => {
                accumulator[currentValue[0]] = currentValue[1];
                return accumulator;
            }, {});
        var position = $('#' + addStatementContainerMainInputPosId).val();
        var reason = $('#' + addStatementContainerMainInputResId).val();
        interactionHandler.sendArgument(position, reason, data);
    };
    var sendStartPremise = function () {
        conclusion = splits[splits.length - 2];
        supportive = splits[splits.length - 1] === 'agree';
        textArray = [];
        $('#' + addPositionContainerBodyId + ' input').each(function () {
            push(this);
        });
        interactionHandler.sendStatement(textArray, conclusion, supportive, '', '', fuzzy_start_premise);
    };
    var sendArgumentsPremise = function () {
        textArray = [];
        $('#' + addPositionContainerBodyId + ' input').each(function () {
            push(this);
        });
        var url = window.location.href.split('?')[0];
        var add = url.indexOf('support') === -1 ? 0 : 1;
        arg = splits[splits.length - 3 - add];
        supportive = splits[splits.length - 2 - add] === 'agree';
        relation = splits[splits.length - 1 - add];
        interactionHandler.sendStatement(textArray, '', supportive, arg, relation, fuzzy_add_reason);
    };

    if (window.location.href.indexOf('/r/') !== -1) {
        $('#' + discussionSpaceId + ' label').each(function () {
            $(this).css('width', '95%');
        });
    }
    this.__setInputExtraFuncs(guiHandler, sendStartStatement, sendStartPremise, sendArgumentsPremise);
};

Main.prototype.__setInputExtraFuncs = function (guiHandler, sendStartStatement, sendStartPremise, sendArgumentsPremise) {
    'use strict';
    var spaceList = $('#' + discussionSpaceListId);
    var input = spaceList.find('li:last-child input');
    $('#' + sendNewStatementId).off("click").click(function () {
        if ($(this).attr('name').indexOf('start') !== -1) {
            sendStartStatement();
        }
    });

    $('#' + sendNewPositionId).off("click").click(function () {
        if (input.attr('id').indexOf('start_statement') !== -1) {
            sendStartStatement();
        } else if (input.attr('id').indexOf('start_premise') !== -1) {
            sendStartPremise();
        } else if (input.attr('id').indexOf('justify_premise') !== -1) {
            sendArgumentsPremise();
        }
    });

    // hide one line options
    var children = spaceList.find('input');
    var ids = ['start_statement', 'start_premise', 'justify_premise', 'login'];
    var id;
    var _this = this;
    if (children.length > 0) {
        id = children.eq(0).attr('id');
        id = id.replace('item_', '');
        _this.__setContainerSidebarForOneLiner(children, id, ids);
    }

    // options for the extra buttons, where the user can add input!
    if (input.length === 0) {
        var el = $('.line-wrapper-l').last().find('span');
        el.hover(function () {
            $(this).css('color', '#000').css('pointer', 'default');
        });
        el.off('click');
        return true;
    }
    if (spaceList.find('li').length === 1 && input.data('url') === 'add') {
        input.prop('checked', true);
    }
    id = input.attr('id').indexOf('item_') === 0 ? input.attr('id').substr('item_'.length) : input.attr('id');
    if ($.inArray(id, ids) !== -1) {
        input.click(function () {
            _this.setInputExtraBox(input, guiHandler, sendStartStatement, sendStartPremise, sendArgumentsPremise);
        });
    }
    return true;
};

Main.prototype.__setContainerSidebarForOneLiner = function (children, id, ids) {
    'use strict';
    // if we have just one list element AND the list element has a special function AND we are logged in
    if (children.length === 1 && $.inArray(id, ids) !== -1 && $('#link_popup_login').text().trim().indexOf(_t(login)) === -1) {
        children.eq(0).prop('checked', true).parent().hide();
        $('#' + discussionSpaceId).remove();
    }
};

/**
 *
 * @param input
 * @param guiHandler
 * @param sendStartStatement
 * @param sendStartPremise
 * @param sendArgumentsPremise
 */
Main.prototype.setInputExtraBox = function (input, guiHandler, sendStartStatement, sendStartPremise, sendArgumentsPremise) {
    'use strict';
    // new position at start
    if (input.attr('id').indexOf('start_statement') !== -1) {
        guiHandler.showAddPositionContainer();
        $('#' + sendNewStatementId).off("click").click(function () {
            sendStartStatement();
        });
    }
    // new premise for the start
    else if (input.attr('id').indexOf('start_premise') !== -1) {
        guiHandler.showaddPositionContainer();
        $('#' + sendNewPositionId).off("click").click(function () {
            sendStartPremise();
        });
    }
    // new premise while judging
    else if (input.attr('id').indexOf('justify_premise') !== -1) {
        guiHandler.showaddPositionContainer();
        $('#' + sendNewPositionId).off("click").click(function () {
            sendArgumentsPremise();
        });
    }
    // login
    else if (input.attr('id').indexOf('login') !== -1 && typeof $('#' + popupLogin) !== 'undefined') {
        new PopupHandler().showLoginPopup();
    }
};

/**
 * main function
 */
$(document).ready(function mainDocumentReady() {
    'use strict';
    var guiHandler = new GuiHandler();
    var ajaxHandler = new AjaxDiscussionHandler();
    var interactionHandler = new InteractionHandler();
    var popupHandler = new PopupHandler();
    var main = new Main();
    var tmp;

    main.setStyleOptions(guiHandler);
    // sidebar of the graphview is set in GuiHandler:setDisplayStyleAsGraphView()
    main.setClickFunctions(guiHandler, popupHandler, ajaxHandler);
    main.setKeyUpFunctions(guiHandler, ajaxHandler);
    main.setWindowOptions();
    main.setGuiOptions();
    main.setInputExtraOptions(guiHandler, interactionHandler);

    // some extras
    // get restart url and cut the quotes
    var btn = $('#discussion-restart-btn');
    if (window.location.href.indexOf('/discuss') !== -1 && btn.length !== 0) {
        tmp = btn.attr('href').substr('location.href='.length);
        tmp = tmp.substr(1, tmp.length - 2);
        $('#' + discussionEndRestart).attr('href', tmp);
        $('#' + discussionEndReview).attr('href', mainpage + 'review');
    }

    // check anchors
    if (location.hash.indexOf('graph') !== -1) {
        new GuiHandler().setDisplayStyleAsGraphView();
        new DiscussionGraph({}, false).showGraph(false);
    }
    if (location.hash.indexOf('barometer') !== -1) {
        new DiscussionBarometer().showBarometer();
    }
    if (location.hash.indexOf('sharing') !== -1) {
        new PopupHandler().showUrlSharingPopup();
    }
    if (location.hash.indexOf('access-review') !== -1 || $('#review-link').attr('data-broke-limit') === 'true') {
        var link = '<a href="' + mainpage + 'review">' + _t(youAreAbleToReviewNow) + '</a>';
        setGlobalInfoHandler('Hey!', link);
    }

    $(document).delegate('.open', 'click', function (event) {
        $(this).addClass('opened');
        event.stopPropagation();
    });
    $(document).delegate('body', 'click', function () {
        var open = $('.open');
        if (open.length !== 0) {
            open.removeClass('opened');
        }
    });
    $(document).delegate('.cls', 'click', function (event) {
        var open = $('.open');
        if (open.length !== 0) {
            event.stopPropagation();
        }
    });
});
