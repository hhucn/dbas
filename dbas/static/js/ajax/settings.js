/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxSettingsHandler(){
	/**
	 * Ajax request for getting the users history
	 */
	this.getUserHistoryData = function(){
		'use strict';
		const csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_user_history',
			method: 'GET',
			dataType: 'json',
			async: true,
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
		'use strict';
		const csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_delete_user_history',
			method: 'POST',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function ajaxGetUserHistoryDone(data) {
			new HistoryHandler().removeUserHistoryDataDone(data);
		}).fail(function ajaxGetUserHistoryFail(xhr) {
			new HistoryHandler().getDataFail(xhr.status);
		});
	};

	/**
	 * Ajax request for setting a setting
	 *
	 * @param toggle_element
	 * @param service
	 */
	this.setUserSetting = function(toggle_element, service) {
		const settings_value = toggle_element.prop('checked');
		const csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_user_setting',
			method: 'POST',
			data:{'settings_value': settings_value ? 'True': 'False', 'service': service},
			dataType: 'json',
			async: true,
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
		const csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_user_language',
			method: 'POST',
			data:{'ui_locales': ui_locales},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function setUserSettingDone(data) {
			const parsedData = $.parseJSON(data);

			if (parsedData.error.length == 0){
				const lang_image = $('#current-lang-images');
				$('#' + settingsSuccessDialog).fadeIn();
				setTimeout(function() { $('#' + settingsSuccessDialog).fadeOut(); }, 3000);
				$.each($('#settings-language-dropdown').find('li'), function(){
					$(this).removeClass('active');
				});
				$.each(lang_image.find('img'), function(){ $(this).hide()});
				$('#link-settings-' + parsedData.ui_locales).addClass('active');
				$('#indicator-' + parsedData.ui_locales).show();
				lang_image.find('span').eq(0).text(parsedData.current_lang);
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
		if ($('#' + editsDoneCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		const csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_edits',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allEditsDone), false);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 * Ajax request for getting all statements send by the user
	 */
	this.getStatementsSend = function() {
		if ($('#' + statementsDoneCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		const csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_posted_statements',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allStatementsPosted), false);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 * Ajax request for getting all arguments, which the user voted for
	 */
	this.getArgumentVotes = function(){
		if ($('#' + discussionArgVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		const csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_argument_votes',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});

	};

	/**
	 * Ajax request for getting all edits done by the user
	 */
	this.getStatementVotes = function(){
		if ($('#' + discussionStatVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		const csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_statement_votes',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});

	};

	/**
	 * Ajax request for deleting the statitistics
	 */
	this.deleteStatisticsRequest = function() {
		const csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_delete_statistics',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackDeleteStatisticsDone(data);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail();
		});
	};
}
