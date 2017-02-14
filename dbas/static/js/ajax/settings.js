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
		var csrf_token = $('#hidden_csrf_token').val();
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
		var csrf_token = $('#hidden_csrf_token').val();
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
		var settings_value = toggle_element.prop('checked');
		var csrf_token = $('#hidden_csrf_token').val();
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
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_user_language',
			method: 'POST',
			data:{'ui_locales': ui_locales},
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function setUserSettingDone(data) {
			var parsedData = $.parseJSON(data);

			if (parsedData.error.length == 0){
				var lang_image = $('#current-lang-images');
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

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_edits',
			method: 'GET',
			dataType: 'json',
			async: true,
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
		if ($('#' + statementsDoneCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_posted_statements',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getStatementsSendDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allStatementsPosted), false);
		}).fail(function getStatementsSendFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 * Ajax request for getting all arguments, which the user voted for
	 */
	this.getArgumentClicks = function(){
		if ($('#' + discussionArgClickCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_argument_clicks',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getArgumentClicksDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function getArgumentClicksFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 * Ajax request for getting all edits done by the user
	 */
	this.getStatementClicks = function(){
		if ($('#' + discussionStatVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_statement_clicks',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getStatementClicksDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function getStatementClicksFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 * Ajax request for getting all arguments, which the user voted for
	 */
	this.getArgumentVotes = function(){
		alert('TODO 3');
		return;
		if ($('#' + discussionArgVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_argument_votes',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getArgumentVotesDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function getArgumentVotesFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 * Ajax request for getting all edits done by the user
	 */
	this.getStatementVotes = function(){
		alert('TODO 4');
		return;
		if ($('#' + discussionStatVoteCountId).text() == '0'){
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
			return;
		}

		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_get_all_statement_votes',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function getStatementVotesDone(data) {
			new StatisticsHandler().callbackGetStatisticsDone(data, _t(allGivenVotes), true);
		}).fail(function getStatementVotesFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotFetched));
		});
	};

	/**
	 * Ajax request for deleting the statitistics
	 */
	this.deleteStatisticsRequest = function() {
		var csrf_token = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_delete_statistics',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: { 'X-CSRF-Token': csrf_token }
		}).done(function deleteStatisticsRequestDone(data) {
			new StatisticsHandler().callbackDeleteStatisticsDone(data);
		}).fail(function deleteStatisticsRequestFail() {
			new StatisticsHandler().callbackStatisticsFail(_t(statisticsNotThere));
		});
	};
}
