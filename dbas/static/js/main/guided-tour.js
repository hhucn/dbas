/**
 * Created by tobias on 26.01.17.
 */

function GuidedTour() {
    'use strict';

    this.guided_tour_template =
        '<div class="popover tour">' +
        '<div class="arrow"></div>' +
        '<h3 class="popover-title"></h3>' +
        '<div class="popover-content"></div>' +
        '<div class="popover-navigation">' +
        '<div class="btn-group">' +
        '<button class="btn btn-sm btn-secondary" data-role="prev">&#xab; ' + _t(prev) + '</button>' +
        '<button class="btn btn-sm btn-success" data-role="next">' + _t(next) + ' &#xbb;</button>' +
        '</div>' +
        '<button class="btn btn-sm btn-secondary" data-role="end">' + _t(tourEnd) + '</button>' +
        '</div>';

    this.guided_tour_template_end =
        '<div class="popover tour">' +
        '<div class="arrow"></div>' +
        '<h3 class="popover-title"></h3>' +
        '<div class="popover-content"></div>' +
        '<div class="popover-navigation">' +
        '<div class="btn-group">' +
        '<button class="btn btn-sm btn-secondary" data-role="prev">&#xab; ' + _t(prev) + '</button>' +
        '<button class="btn btn-sm btn-success" data-role="next">' + _t(next) + ' &#xbb;</button>' +
        '</div>' +
        '<button class="btn btn-sm btn-secondary" data-role="end">' + _t(tourEnd) + '</button>' +
        '</div>';

    this.langSwitcher = '';
    this.flag = $('#header-language-selector').find('img').attr('src');
    if (getLanguage() === 'en') {
        this.langSwitcher = '<a id="switch-to-de" class="pull-right" style="cursor: pointer;">' +
            '<img class="language_selector_img" src="' + this.flag + '" alt="flag_ge" style="width:25px;"></a>';
    } else {
        this.langSwitcher = '<a id="switch-to-en" class="pull-right" style="cursor: pointer;">' +
            '<img class="language_selector_img" src="' + this.flag + '" alt="flag_us-gb" style="width:25px;"></a>';
    }

    // click function for lang switch
    this.setLangClick = function () {
        setTimeout(function () {
            // language switch
            var switcher = getLanguage() === 'en' ? $('#switch-to-de') : $('#switch-to-en');
            var lang = getLanguage() === 'en' ? 'de' : 'en';
            switcher.click(function () {
                new AjaxMainHandler().switchDisplayLanguage(lang);
            });
            switcher.find('img').click(function () {
                new AjaxMainHandler().switchDisplayLanguage(lang);
            });
        }, 500);
    };

    this.stepList = this.__prepareSteps();

    var _this = this;
    this.tour = new Tour({
        steps: _this.stepList,
        framework: "bootstrap4",
        backdrop: true,
        backdropPadding: 5,
        // template: _this.guided_tour_template,
        onEnd: _this.endFn
    });

    // function on start
    this.startFn = function () {
        _this.tour.init(); // Initialize the tour
        _this.tour.restart(); // Start the tour
        _this.setLangClick();
    };

    // function on end
    this.endFn = function () {
        Cookies.set(GUIDED_TOUR, true, {expires: 60});
    };
}

/**
 * Prepares the steps of the tour as well as the tour itself
 */
GuidedTour.prototype.__prepareSteps = function () {
    'use strict';

    var issue = {
        element: '#header-container',
        title: _t(tourIssueTitle) + this.langSwitcher,
        content: _t(tourIssueContent),
        placement: 'bottom',
    };
    var startDiscussion = {
        element: '#dialog-speech-bubbles-space',
        title: _t(tourStartDiscussionTitle) + this.langSwitcher,
        content: _t(tourStartDiscussionContent),
        placement: 'bottom'
    };
    var markOpinion = {
        element: '#some-element-bubble .triangle-r',
        title: _t(tourMarkOpinionTitle) + this.langSwitcher,
        content: _t(tourMarkOpinionContent),
        placement: 'bottom',
        onShow: function () {
            var element = '<div class="line-wrapper-r" id="some-element-bubble">' +
                '<p class="triangle-r"><i class="fa fa-star text-warning" aria-hidden="true" style="padding-right: 0.5em;"></i>' +
                '<span class="triangle-content">' + _t(tourMarkOpinionText) + '</span></p></div>';
            $('#' + discussionBubbleSpaceId).prepend($.parseHTML(element));
        },
        onHide: function () {
            $('#some-element-bubble').remove();
        }
    };
    var chooseAnswer = {
        element: '#discussions-space-list',
        title: _t(tourSelectAnswertTitle) + this.langSwitcher,
        content: _t(tourSelectAnswertContent),
        placement: 'bottom'
    };
    var setInput = {
        element: '#discussions-space-list li:last-child',
        title: _t(tourEnterStatementTitle) + this.langSwitcher,
        content: _t(tourEnterStatementContent),
        placement: 'bottom'
    };
    var firstChild = $('#discussions-space-list li:first');
    var statementAction = {
        element: '#discussions-space-list li:first',
        title: _t(tourStatementActionTitle) + this.langSwitcher,
        content: _t(tourStatementActionContent),
        placement: 'bottom',
        onShow: function () {
            var elements = '<span class="fa-fufu">' +
                '<i class="text-danger fa fa-pencil-square-o" aria-hidden="true" style="margin-left: 0.3em;"></i>' +
                '<i class="text-danger fa fa-flag" aria-hidden="true" style="margin-left: 0.3em;"></i>' +
                '<i class="text-danger fa fa-trash-o" aria-hidden="true" style="margin-left: 0.3em;"></i>' +
                '<i class="text-danger fa fa-bomb" aria-hidden="true" style="margin-left: 0.3em;"></i>' +
                '<i class="text-danger fa fa-link" aria-hidden="true" style="margin-left: 0.3em;"></i>' + '</span>';
            firstChild.append($.parseHTML(elements));
        },
        onHide: function () {
            $('.fa-fufu').remove();
        }
    };
    var haveFun = {
        element: '#discussion-container',
        title: _t(tourHaveFunTitle) + this.langSwitcher,
        content: _t(tourHaveFunContent),
        placement: 'bottom',
        template: this.guided_tour_template_end
    };

    return [
        issue,
        startDiscussion,
        markOpinion,
        chooseAnswer,
        setInput,
        statementAction,
        haveFun
    ];
};

/**
 * Starts tour from the beginning
 */
GuidedTour.prototype.start = function () {
    'use strict';

    // build dialog
    var title = _t(tourWelcomeTitle);
    var text = '<p class="lead">' + _t(welcomeDialogBody) + '</p>' + this.langSwitcher.replace('style="', 'style="display: none; ');
    var dialog = $('#' + popupConfirmDialogId);

    // add language switcher
    dialog.on('shown.bs.modal', function () {
        var switcher = getLanguage() === 'en' ? $('#switch-to-de') : $('#switch-to-en');
        switcher.detach();
        switcher.removeClass('pull-right').addClass('pull-left');
        switcher.insertBefore($('#' + popupConfirmDialogAcceptBtn)).show();
    });
    dialog.on('hide.bs.modal', function () {
        var switcher = getLanguage() === 'en' ? $('#switch-to-de') : $('#switch-to-en');
        switcher.remove();
    });

    // display dialog and set click events
    displayConfirmationDialog(title, text, this.startFn, this.endFn, false);
    dialog.find('#confirm-dialog-accept-btn').text(_t(yes));
    dialog.find('#confirm-dialog-refuse-btn').text(_t(no));
    this.setLangClick();
};
