function AjaxSettingsHandler() {
    "use strict";

    /**
     * Ajax request for getting the users history
     */
    this.getUserHistoryData = function () {
        var url = 'get_user_history';
        var done = function getUserHistoryDataDone(data) {
            new HistoryHandler().getUserHistoryDataDone(data);
        };
        var fail = function getUserHistoryDataFail(xhr) {
            new HistoryHandler().getDataFail(xhr.status);
        };
        ajaxSkeleton(url, 'GET', {}, done, fail);
    };

    /**
     * Ajax request for deleting the users history
     */
    this.deleteUserHistoryData = function () {
        var url = 'delete_user_history';
        var done = function ajaxGetUserHistoryDone() {
            new HistoryHandler().removeUserHistoryDataDone();
        };
        var fail = function ajaxGetUserHistoryFail(data) {
            setGlobalInfoHandler('Ohh', data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'GET', {}, done, fail);
    };

    /**
     * Ajax request for setting a setting
     *
     * @param toggle_element
     * @param service
     */
    this.setUserSetting = function (toggle_element, service) {
        var settings_value = toggle_element.prop('checked');
        var url = 'set_user_setting';
        var data = {
            'settings_value': settings_value,
            'service': service
        };
        var done = function setUserSettingDone(data) {
            new SettingsHandler().callbackDone(data, toggle_element, settings_value, service);
        };
        var fail = function setUserSettingFail() {
            new SettingsHandler().callbackFail(toggle_element, settings_value, service);
        };
        ajaxSkeleton(url, 'POST', data, done, fail);
    };

    /**
     * Ajax request for the change of the notification language
     *
     * @param ui_locales
     */
    this.setNotifcationLanguage = function (ui_locales) {
        var url = 'set_user_language';
        var data = {'ui_locales': ui_locales};
        var done = function setUserSettingDone(data) {
            if (data.error.length === 0) {
                var lang_image = $('#current-lang-images');
                $('#' + settingsSuccessDialog).fadeIn();
                setTimeout(function () {
                    $('#' + settingsSuccessDialog).fadeOut();
                }, 3000);
                $.each($('#settings-language-dropdown').find('li'), function () {
                    $(this).removeClass('active');
                });
                $.each(lang_image.find('img'), function () {
                    $(this).hide();
                });
                $('#link-settings-' + data.ui_locales).addClass('active');
                $('#indicator-' + data.ui_locales).show();
                lang_image.find('span').eq(0).text(data.current_lang);
            } else {
                $('#' + settingsAlertDialog).fadeIn();
                setTimeout(function () {
                    $('#' + settingsAlertDialog).fadeOut();
                }, 3000);
            }
        };
        var fail = function setUserSettingFail() {
            $('#' + settingsAlertDialog).fadeIn();
            setTimeout(function () {
                $('#' + settingsAlertDialog).fadeOut();
            }, 3000);
        };
        ajaxSkeleton(url, 'POST', data, done, fail);
    };

    /**
     * Ajax request for getting all edits done by the user
     */
    this.getEditsDone = function () {
        if ($('#' + editsDoneCountId).text() === '0') {
            new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
            return;
        }

        var url = 'get_all_edits';
        var done = function getEditsDoneDone(data) {
            new StatisticsHandler().callbackGetStatisticsDone(data, _t(allEditsDone), false);
        };
        var fail = function getEditsDoneFail(data) {
            new StatisticsHandler().callbackStatisticsFail(data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'GET', {}, done, fail);
    };

    /**
     * Ajax request for getting all statements send by the user
     */
    this.getStatementsSend = function () {
        if ($('#' + statementsDoneCountId).text() === '0') {
            new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
            return;
        }

        var url = 'get_all_posted_statements';
        var done = function getStatementsSendDone(data) {
            new StatisticsHandler().callbackGetStatisticsDone(data, _t(allStatementsPosted), false);
        };
        var fail = function getStatementsSendFail(data) {
            new StatisticsHandler().callbackStatisticsFail(data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'GET', {}, done, fail);
    };

    this.__getInfoWrapper = function (id, url, is_clicked_element) {
        if ($('#' + id).text() === '0') {
            new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
            return;
        }

        var done = function __getInfoWrapperDone(data) {
            new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenInterests), is_clicked_element);
        };
        var fail = function __getInfoWrapperFail(data) {
            setGlobalInfoHandler('Ohh', data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'GET', {}, done, fail);
    };

    /**
     * Ajax request for getting all arguments, which the user voted for
     */
    this.getArgumentClicks = function () {
        this.__getInfoWrapper(discussionArgClickCountId, 'get_all_argument_clicks', true);
    };

    /**
     * Ajax request for getting all edits done by the user
     */
    this.getStatementClicks = function () {
        this.__getInfoWrapper(discussionStatClickCountId, 'get_all_statement_clicks', true);
    };

    /**
     * Ajax request for getting all arguments, which the user voted for
     */
    this.getMarkedArguments = function () {
        this.__getInfoWrapper(discussionArgVoteCountId, 'get_all_marked_arguments', false);
    };

    /**
     * Ajax request for getting all edits done by the user
     */
    this.getMarkedStatements = function () {
        this.__getInfoWrapper(discussionStatVoteCountId, 'get_all_marked_statements', false);
    };

    /**
     * Ajax request for deleting the statistics
     */
    this.deleteStatisticsRequest = function () {
        var url = 'delete_statistics';
        var done = function deleteStatisticsRequestDone() {
            new StatisticsHandler().callbackDeleteStatisticsDone();
        };
        var fail = function deleteStatisticsRequestFail(data) {
            new StatisticsHandler().callbackStatisticsFail(data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'GET', {}, done, fail);
    };

    /**
     *
     */
    this.deleteAccount = function () {
        redirectAfterAjax('/user/delete');
    };
}
