/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function News() {
    'use strict';

    var BOOTSTRAP_COLLAPSE = 990;

    /**
     *
     */
    this.setNewsInRow = function () {
        var input = $('#raw-elements');
        var array = input.find('.col-md-4');
        var length = array.length;

        // build rows
        var row = 0;
        var div = $('<div>').attr('id', 'row_' + row).addClass('row');
        var counter;
        var container = $('<div>').attr('id', 'container_' + row).addClass('container');
        for (counter = 0; counter < length; counter++) {
            if (counter % 3 === 0) {
                if (div !== '') {
                    $('#' + newsBodyId).append(container);
                }
                div = $('<div>').attr('id', 'row_' + row).addClass('row');
                container = $('<div>').attr('id', 'container_' + row).addClass('container');
                row += 1;
            }
            div.append(array[counter]);
            container.append(div);
        }

        // set length of last row
        length = container.children().eq(0).children().length;
        $.each(container.children().eq(0).children(), function () {
            $(this).attr('class', '').attr('class', 'col-md-' + (12 / length));
        });

        // add last row
        if (counter % 3 !== 0) {
            $('#' + newsBodyId).append(container);
        }

        input.remove();
        $('#dummy-news').remove();
    };

    /**
     *
     */
    this.setMaxHeightOfNewsRows = function () {
        var counter, row = $('#' + newsBodyId).children().length, heights, maxHeight;

        // bootstrap collapse
        if ($(window).width() < BOOTSTRAP_COLLAPSE) {
            return;
        }

        var setHeight = function (children, mh) {
            $.each(children, function () {
                $(this).children().eq(0).css({'min-height': mh + 'px'});
            });
        };
        // find max height of each row and set it
        for (counter = 0; counter < row; counter++) {
            var children = $('#row_' + counter).children();
            heights = children.map(function () {
                return $(this).height();
            }).get();
            maxHeight = Math.max.apply(Math, heights);

            setHeight(children, maxHeight);
        }
    };

    // *********************
    //	SHARING IS CARING
    // *********************
    this.setSharingClickEvents = function () {
        var news = new News();
        /**
         * Sharing shortened url with mail
         */
        $('.' + shareButtonMail).click(function () {
            news.mailShare(this);
        });

        /**
         * Sharing shortened url on twitter
         */
        $('.' + shareButtonTwitter).click(function () {
            news.twitterShare(this);
        });

        /**
         * Sharing shortened url on google
         */
        $('.' + shareButtonGoogle).click(function () {
            news.googleShare(this);
        });

        /**
         * Sharing shortened url on facebook
         */
        $('.' + shareButtonFacebook).click(function () {
            news.facebookShare(this);
        });
    };

    /**
     * Sharing shortened url via mail
     */
    this.mailShare = function (_this) {
        if (typeof $(_this) === 'undefined') {
            return;
        }
        if ($(_this).attr('id') === shareUrlButtonMail) {
            return;
        }
        var id = $(_this).closest('.card-header').attr('id'),
            title = $('#' + id + '_title').text(),
            date = $('#' + id + '_date').text(),
            author = $('#' + id + '_author').text();

        new Sharing().emailShare('', "DBAS: " + title, _t(interestingNews) + ' ' + date + ", by " + author + " - " + window.location.href);
    };

    /**
     * Sharing shortened url on google
     */
    this.googleShare = function (_this) {
        if (typeof $(_this) === 'undefined') {
            return;
        }
        if ($(_this).attr('id') === shareUrlButtonGoogle) {
            return;
        }
        new Sharing().googlePlusShare(window.location.href);

    };

    /**
     * Sharing shortened url on facebook
     */
    this.facebookShare = function (_this) {
        if (typeof $(_this) === 'undefined') {
            return;
        }
        if ($(_this).attr('id') === shareUrlButtonFacebook) {
            return;
        }

        var id = $(_this).parent().attr('id'),
            title = $('#' + id + '_title').text(),
            date = $('#' + id + '_date').text(),
            author = $('#' + id + '_author').text(),
            message = "News '" + title + "', from " + date + ", by " + author + " on " + window.location.href;
        new Sharing().facebookShare(window.location.href, "FB Sharing", message, mainpage + "static/images/logo.png");
    };

    /**
     * Sharing shortened url on twitter
     */
    this.twitterShare = function (_this) {
        if (typeof $(_this) === 'undefined') {
            return;
        }
        if ($(_this).attr('id') === shareUrlButtonTwitter) {
            return;
        }
        var id = $(_this).parent().attr('id'),
            title = $('#' + id + '_title').text();
        new Sharing().twitterShare(title, window.location.href);
    };

}

$(document).ready(function () {
    'use strict';

    if (window.location.href.indexOf(mainpage + 'news') === -1) {
        return;
    }

    var news = new News();
    news.setNewsInRow();
    $('.panel-body').css('height', '');
    news.setMaxHeightOfNewsRows();
    news.setSharingClickEvents();
    news.setSharingClickEvents();

    $('#' + writingNewsFailedId).hide();
    $('#' + writingNewsSuccessId).hide();

    /**
     * Sharing shortened url on google
     */
    $('#' + sendNewsButtonId).click(function () {
        var url = 'send_news';
        var d = {
            title: $('#' + writingNewNewsTitleId).val(),
            text: $('#' + writingNewNewsTextId).val()
        };
        var done = function ajaxSendNewsDone() {
            location.reload(true);
        };
        var fail = function ajaxSendNewsFail(data) {
            $('#' + writingNewsFailedId).show();
            $('#' + writingNewsFailedMessageId).html(data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    });

    $('#icon-add-news').click(function () {
        $('#popup-writing-news').modal('show');
    });
});
