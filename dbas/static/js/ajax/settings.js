/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function AjaxSettingsHandler(){
	"use strict";

	/**
	 * Ajax request for getting the users history
	 */
	this.getUserHistoryData = function(){
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_user_history',
			method: 'GET',
			dataType: 'json',
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function ajaxGetUserHistoryDone(data) {
			new HistoryHandler().getUserHistoryDataDone(data);
		}).fail(function ajaxGetUserHistoryFail(xhr) {
			new HistoryHandler().getDataFail(xhr.status);
		});
	};

	/**
	 * Ajax request for deleting the users history
	 */
	this.deleteUserHistoryData = function(){
		var url = 'ajax_delete_user_history';
		var done = function ajaxGetUserHistoryDone() {
			new HistoryHandler().removeUserHistoryDataDone();
		};
		var fail = function ajaxGetUserHistoryFail(data) {
			setGlobalInfoHandler('Ohh', data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', {}, done, fail);
	};

	/**
	 * Ajax request for setting a setting
	 *
	 * @param toggle_element
	 * @param service
	 */
	this.setUserSetting = function(toggle_element, service) {
		var settings_value = toggle_element.prop('checked');
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_user_setting',
			method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'settings_value': settings_value,
                'service': service
            }),
			dataType: 'json',
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function setUserSettingDone(data) {
			new SettingsHandler().callbackDone(data, toggle_element, settings_value, service);
		}).fail(function setUserSettingFail() {
			new SettingsHandler().callbackFail(toggle_element, settings_value, service);
		});
	};

	/**
	 * Ajax request for the change of the notification language
	 *
	 * @param ui_locales
	 */
	this.setNotifcationLanguage = function(ui_locales){
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_user_language',
			method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'ui_locales': ui_locales}),
			dataType: 'json',
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function setUserSettingDone(data) {
			if (data.error.length === 0){
				var lang_image = $('#current-lang-images');
				$('#' + settingsSuccessDialog).fadeIn();
				setTimeout(function() { $('#' + settingsSuccessDialog).fadeOut(); }, 3000);
				$.each($('#settings-language-dropdown').find('li'), function(){
					$(this).removeClass('active');
				});
				$.each(lang_image.find('img'), function(){ $(this).hide();});
				$('#link-settings-' + data.ui_locales).addClass('active');
				$('#indicator-' + data.ui_locales).show();
				lang_image.find('span').eq(0).text(data.current_lang);
			} else {
				$('#' + settingsAlertDialog).fadeIn();
				setTimeout(function() { $('#' + settingsAlertDialog).fadeOut(); }, 3000);
			}
		}).fail(function setUserSettingFail() {
			$('#' + settingsAlertDialog).fadeIn();
			setTimeout(function() { $('#' + settingsAlertDialog).fadeOut(); }, 3000);
		});
	};

	/**
	 * Ajax request for getting all edits done by the user
	 */
	this.getEditsDone = function() {
		if ($('#' + editsDoneCountId).text() === '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_edits',
			method: 'GET',
			dataType: 'json',
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getEditsDoneDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allEditsDone), false);
		}).fail(function getEditsDoneFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 * Ajax request for getting all statements send by the user
	 */
	this.getStatementsSend = function() {
		if ($('#' + statementsDoneCountId).text() === '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_posted_statements',
			method: 'GET',
			dataType: 'json',
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getStatementsSendDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allStatementsPosted), false);
		}).fail(function getStatementsSendFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};
	
	this.__getInfoWrapper = function(id, url, is_clicked_element){
		if ($('#' + id).text() === '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var done = function __getInfoWrapperDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenInterests), is_clicked_element);
		};
		var fail = function __getInfoWrapperFail(data) {
			setGlobalInfoHandler('Ohh', data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', {}, done, fail);
	};

	/**
	 * Ajax request for getting all arguments, which the user voted for
	 */
	this.getArgumentClicks = function(){
		this.__getInfoWrapper(discussionArgClickCountId, 'ajax_get_all_argument_clicks', true);
	};

	/**
	 * Ajax request for getting all edits done by the user
	 */
	this.getStatementClicks = function(){
		this.__getInfoWrapper(discussionStatClickCountId, 'ajax_get_all_statement_clicks', true);
	};

	/**
	 * Ajax request for getting all arguments, which the user voted for
	 */
	this.getMarkedArguments = function(){
		this.__getInfoWrapper(discussionArgVoteCountId, 'ajax_get_all_marked_arguments', false);
	};

	/**
	 * Ajax request for getting all edits done by the user
	 */
	this.getMarkedStatements = function(){
		this.__getInfoWrapper(discussionStatVoteCountId, 'ajax_get_all_marked_statements', false);
	};

	/**
	 * Ajax request for deleting the statitistics
	 */
	this.deleteStatisticsRequest = function() {
		var url = 'ajax_delete_statistics';
		var done = function deleteStatisticsRequestDone() {
			new StatisticsHandler().callbackDeleteStatisticsDone();
		};
		var fail = function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(data.responseJSON.errors[0].description);
		};
		ajaxSkeleton(url, 'POST', {}, done, fail);
	};
}
