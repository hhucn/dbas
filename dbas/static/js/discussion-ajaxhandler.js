/*global $, jQuery, alert, GuiHandler, InteractionHandler, internal_error, popupErrorDescriptionId */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function AjaxSiteHandler() {
	'use strict';
	var push=0,
		loca=0,
		hash=0,
		aler=0;

	/**
	 * Redirection before an ajax call
	 * @param uid current identifier
	 */
	this.callSiteForGetPremisseForStatement = function (uid) {
		this.redirectBrowser('uid=' + uid, 'get_premisses_for_statement');
	};

	/**
	 * Redirection before an ajax call
	 * @param pgroup_id
	 * @param conclusion_id
	 */
	this.callSiteForGetReplyForPremisseGroup = function (pgroup_id, conclusion_id) {
		this.redirectBrowser('pgroup_id=' + pgroup_id + '&conclusion_id=' + conclusion_id, 'reply_for_premissegroup');
	};

	/**
	 * Redirection before an ajax callpgroup_id
	 * @param id_text
	 * @param pgroup_id
	 */
	this.callSiteForGetReplyForArgument = function (id_text, pgroup_id) {
		this.redirectBrowser('id_text=' + id_text + '&pgroup_id=' + pgroup_id, 'reply_for_argument');
	};

	/**
	 * Redirection before an ajax call
	 * @param id current identifier
	 */
	this.callSiteForHandleReplyForResponseOfConfrontation = function (id) {
		this.redirectBrowser('id=' + id, 'reply_for_response_of_confrontation');
	};

	/**
	 * Redirection before an ajax call
	 * @param keyValuePair current key value pair
	 * @param service current service
	 */
	this.redirectBrowser = function (keyValuePair, service) {
		//alert(discussion_mainpage + key + '=' + value + '/' + service + '/go'):
		// window.location.replace(discussion_mainpage + key + '=' + value + '/' + service + '/go');
		window.location.href = discussion_mainpage + keyValuePair + '/' + service + '/go';
	};

	this.debugger = function ( data, url, settings_data ) {
		if (hash==1) window.location = '/' + url + '?' + settings_data;
		if (loca==1) window.location = '/content/' + url + '?' + settings_data;
		if (push==1) history.pushState(data, '', document.location);
		if (aler==1) alert('AJAX\n' + url + '/' + settings_data);
	};

	/**
	 * Send an ajax request for getting all positions as dicitonary uid <-> value
	 */
	this.getStartStatements = function () {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data, url;
		$.ajax({
			url: 'ajax_get_start_statements',
			type: 'GET',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetAllPositionsDone(data) {
			new InteractionHandler().callbackIfDoneForGetStartStatements(data);
			new AjaxSiteHandler().debugger(data, url, settings_data);
		}).fail(function ajaxGetAllPositionsFail(err) {
			new GuiHandler().setErrorDescription(internal_error);
			// new GuiHandler().showDiscussionError('Internal failure, could not find any start point.');
			new GuiHandler().showDiscussionError(JSON.stringify(err));
		});
	};

	/**
	 * Send an ajax request for getting all premisses for a givens tatement
	 * @param uid of clicked statement
	 */
	this.getPremisseForStatement = function (uid) {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data, url;
		$.ajax({
			url: 'ajax_get_premisses_for_statement',
			method: 'POST',
			data: {
				uid: uid
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetPremisseForStatementDone(data) {
			new InteractionHandler().callbackIfDoneForPremisseForStatement(data);
			new AjaxSiteHandler().debugger(data, url, settings_data);
		}).fail(function ajaxGetPremisseForStatementFail(err) {
			new GuiHandler().setErrorDescription(internal_error);
			// new GuiHandler().showDiscussionError('Internal failure while requesting data for your statement.');
			new GuiHandler().showDiscussionError(JSON.stringify(err));
		});
	};

	/**
	 * Sends an ajax request for getting all premisses for a given statement
	 * @param ids of clicked statement
	 */
	this.getReplyForPremisseGroup = function (ids) {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data, url;
		$.ajax({
			url: 'ajax_reply_for_premissegroup',
			method: 'POST',
			data: {
				ids: ids
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetReplyForPremisseDone(data) {
			new InteractionHandler().callbackIfDoneReplyForPremissegroup(data);
			new AjaxSiteHandler().debugger(data, url, settings_data);
		}).fail(function ajaxGetReplyForPremisseFail(err) {
			new GuiHandler().setErrorDescription(internal_error);
			// new GuiHandler().showDiscussionError('Internal failure while requesting another opininion.');
			new GuiHandler().showDiscussionError(JSON.stringify(err));
		});
	};

	/**
	 * Sends an ajax request for getting all confrotations for a given argument
	 * @param ids of the clicked premisse group
	 */
	this.getReplyForArgument = function (ids) {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data, url;
		$.ajax({
			url: 'ajax_reply_for_argument',
			method: 'POST',
			data: {
				ids: ids
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetReplyForArgumentDone(data) {
			new InteractionHandler().callbackIfDoneReplyForArgument(data);
			new AjaxSiteHandler().debugger(data, url, settings_data);
		}).fail(function ajaxGetReplyForArgumentFail(err) {
			new GuiHandler().setErrorDescription(internal_error);
			// new GuiHandler().showDiscussionError('Internal failure while requesting another opininion.');
			new GuiHandler().showDiscussionError(JSON.stringify(err));
		});
	};

	/**
	 * Sends an ajax request for handle the reaction of a confrontation
	 * @param id of clicked relation and statement
	 */
	this.handleReplyForResponseOfConfrontation = function (id) {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data, url;
		$.ajax({
			url: 'ajax_reply_for_response_of_confrontation',
			method: 'POST',
			data: {
				id: id
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxHandleReplyForResponseOfConfrontationDone(data) {
			new InteractionHandler().callbackIfDoneHandleReplyForResponseOfConfrontation(data);
			new AjaxSiteHandler().debugger(data, url, settings_data);
		}).fail(function ajaxHandleReplyForResponseOfConfrontationFail(err) {
			new GuiHandler().setErrorDescription(internal_error);
			// new GuiHandler().showDiscussionError('Internal failure while requesting another opininion.');
			new GuiHandler().showDiscussionError(JSON.stringify(err));
		});
	};

	/**
	 * Requests all users
	 */
	this.getUsersAndSetInGui = function () {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_all_users',
			type: 'GET',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxGetAllUsersDone(data) {
			new InteractionHandler().callbackIfDoneGetUsersAndSetInGui(data);
		}).fail(function ajaxGetAllUsersFail(err) {
			// new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().setErrorDescription(JSON.stringify(err));
		});
	};

	/**
	 * Sends new premisses to the server. Answer will be given to a callback
	 * @param argument_dictionary for inserting
	 */
	this.sendNewPremissesForArgument = function (argument_dictionary) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_new_premisses',
			type: 'POST',
			data: argument_dictionary,
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxSendNewPremissesDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewPremisses(data);
		}).fail(function ajaxSendNewPremissesFail(err) {
			// new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().setErrorDescription(JSON.stringify(err));
		});
	};

	/**
	 * Sends new position to the server. Answer will be given to a callback
	 * @param statement for sending
	 */
	this.sendNewStartStatement = function (statement) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_new_start_statement',
			type: 'POST',
			data: {
				statement: statement
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxSendStartStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendNewStartStatement(data);
		}).fail(function ajaxSendStartStatementFail(err) {
			// new GuiHandler().setErrorDescription(internal_error);
			new GuiHandler().setErrorDescription(JSON.stringify(err));
		});
	};

	/**
	 * Requests the logfile for the given uid
	 * @param statement_uid current uid of the statement
	 */
	this.getLogfileForStatement = function (statement_uid) {
		var csrfToken = $('#hidden_csrf_token').val(), settings_data, url;
		$.ajax({
			url: 'ajax_get_logfile_for_statement',
			type: 'GET',
			data: {
				uid: statement_uid
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetLogfileForStatementDone(data) {
			new InteractionHandler().callbackIfDoneForGetLogfileForStatement(data);
			new AjaxSiteHandler().debugger(data, url, settings_data);
		}).fail(function ajaxGetLogfileForStatementFail(err) {
			// $('#' + popupErrorDescriptionId).text('Unfortunately, the log file could not be requested (server offline or csrf check' +
			// 	' failed. Sorry!');
			$('#' + popupErrorDescriptionId).text(JSON.stringify(err));
		});
	};

	/**
	 * Sends a correcture of a statement
	 * @param uid
	 * @param edit_dialog_td_id
	 * @param corrected_text the corrected text
	 */
	this.sendCorrectureOfStatement = function (uid, edit_dialog_td_id, corrected_text) {
		var csrfToken = $('#hidden_csrf_token').val();
		$.ajax({
			url: 'ajax_set_correcture_of_statement',
			type: 'POST',
			data: {
				uid: uid,
				text: corrected_text
			},
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			}
		}).done(function ajaxSendCorrectureOfStatementDone(data) {
			new InteractionHandler().callbackIfDoneForSendCorrectureOfStatement(data, edit_dialog_td_id);
		}).fail(function ajaxSendCorrectureOfStatementFail(err) {
			// $('#' + popupErrorDescriptionId).text('Unfortunately, the correcture could not be send (server offline or csrf check' +
			// 	' failed. Sorry!');
			$('#' + popupErrorDescriptionId).text(JSON.stringify(err));
		});
	};

	/**
	 * Shortens url
	 * @param long_url for shortening
	 */
	this.getShortenUrl = function (long_url) {
		var encoded_url = encodeURI(long_url);
		$.ajax({
			url: 'ajax_get_shortened_url',
			type: 'GET',
			dataType: 'json',
			data: {
				url: encoded_url
			},
			async: true
		}).done(function ajaxGetShortenUrlDone(data) {
			new InteractionHandler().callbackIfDoneForShortenUrl(data);
		}).fail(function ajaxGetShortenUrl(err) {
			$('#' + popupUrlSharingInputId).val(long_url);
		});
	};
}