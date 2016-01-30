/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function AdminInterface(){

	/**
	 * Requests all users
	 */
	this.getUsersOverview = function () {
		var csrfToken = $('#' + hiddenCSRFTokenId).val(), settings_data, url, _this = this;
		$.ajax({
			url: 'ajax_all_users',
			method: 'GET',
			dataType: 'json',
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetAllUsersDone(data) {
			_this.setJsonUserDataToAdminContent($.parseJSON(data));
		}).fail(function ajaxGetAllUsersFail() {
			// new GuiHandler().setErrorDescription(_t(internalError));
			new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 9). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
		});
	};

	/**
	 * Requests all attacks
	 */
	this.getAttackOverview = function () {
		var csrfToken = $('#' + hiddenCSRFTokenId).val(), settings_data, url, _this = this;
		$.ajax({
			url: 'ajax_get_attack_overview',
			method: 'GET',
			dataType: 'json',
			data: { issue: new Helper().getCurrentIssueId() },
			async: true,
			headers: {
				'X-CSRF-Token': csrfToken
			},
			beforeSend: function(jqXHR, settings ){
				settings_data = settings.data;
				url = this.url;
			}
		}).done(function ajaxGetAllUsersDone(data) {
			_this.setJsonAttackDataToAdminContent($.parseJSON(data));
			$('#' + listAllUsersAttacksId).val(_t(hideAllAttacks));
			new GuiHandler().hideErrorDescription();
		}).fail(function ajaxGetAllUsersFail() {
			// new GuiHandler().setErrorDescription(_t(internalError));
			new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 10). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
			$('#' + listAllUsersAttacksId).val(_t(showAllAttacks));
		});
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setJsonUserDataToAdminContent = function (jsonData) {
		//var tableElement, trElement, tbody, thead, tdElement, spanElement, i;
		var tableElement, trElement, tElement, i, thead, tbody;
		tElement = ['', '', '', '', '', '', '', '', '', ''];
		tableElement = $('<table>');
		tableElement.attr({class: 'table table-striped table-hover',
						border: '0',
						style: 'border-collapse: separate; border-spacing: 0px;'});

		trElement = $('<tr>');
		thead = $('<thead>');
		tbody = $('<tbody>');

		for (i = 0; i < tElement.length; i += 1) {
			tElement[i] = $('<th>');
		}

		// add header row
		tElement[0] = $('<th>').text('#');
		tElement[1] = $('<th>').text(_t(firstname));
		tElement[2] = $('<th>').text(_t(surname));
		tElement[3] = $('<th>').text(_t(nickname));
		tElement[4] = $('<th>').text(_t(email));
		tElement[5] = $('<th>').text(_t(group_uid));
		tElement[6] = $('<th>').text(_t(last_action));
		tElement[7] = $('<th>').text(_t(last_login));
		tElement[8] = $('<th>').text(_t(registered));
		tElement[9] = $('<th>').text(_t(gender));

		for (i = 0; i < tElement.length; i += 1) {
			trElement.append(tElement[i]);
		}
		thead.append(trElement);
		tableElement.append(thead);

		// add each user element
		$.each(jsonData, function setJsonDataToAdminContentEach(key, value) {
			tElement[0] = $('<td>').text(value.uid);
			tElement[1] = $('<td>').text(value.firstname);
			tElement[2] = $('<td>').text(value.surname);
			tElement[3] = $('<td>').text(value.nickname);
			tElement[4] = $('<td>').text(value.email);
			tElement[5] = $('<td>').text(value.group_uid);
			tElement[6] = $('<td>').text(value.last_action);
			tElement[7] = $('<td>').text(value.last_login);
			tElement[8] = $('<td>').text(value.registered);
			tElement[9] = $('<td>').text(value.gender);

			trElement = $('<tr>');
			for (i = 0; i < tElement.length; i += 1) {
				trElement.append(tElement[i]);
			}
			tbody.append(trElement);
		});
		tableElement.append(tbody);

		$('#' + adminsSpaceForUsersId).empty().append(tableElement);
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setJsonAttackDataToAdminContent = function (jsonData) {
		var tableElement, trElement, tdElement, tbody, thead, spanElement, i, attacks = [], counter;

		tdElement = ['', '', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', '', ''];
		tableElement = $('<table>');
		tableElement.attr({class: 'table table-condensed tablesorter',
						border: '0',
						style: 'border-collapse: separate; border-spacing: 0px;'});
		tbody = $('<tbody>');
		thead = $('<thead>');

		trElement = $('<tr>');

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i] = $('<td>');
			spanElement[i] = $('<spand>');
			spanElement[i].attr({class: 'font-semi-bold'});
		}

		// add header row
		spanElement[0].text(_t(uid));
		spanElement[1].text(_t(text));
		counter = 2;
		$.each(jsonData.attacks, function setJsonAttackDataToAdminContentEach(key, value) {
			spanElement[counter].text(value);
			attacks[(counter-2)] = value;
			counter += 1;
		});

		for (i = 0; i < tdElement.length; i += 1) {
			tdElement[i].append(spanElement[i]);
			trElement.append(tdElement[i]);
			thead.append(trElement);
		}
		tableElement.append(thead);

		// add each attack element
		$.each(jsonData, function setJsonAttackDataToAdminContentEach(key, value) {
			trElement = $('<tr>');
			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
			}

			tdElement[0].text(value.id);
			tdElement[1].text(value.text);
			tdElement[2].text(value[attacks[0]]);
			tdElement[3].text(value[attacks[1]]);
			tdElement[4].text(value[attacks[2]]);
			tdElement[5].text(value[attacks[3]]);
			tdElement[6].text(value[attacks[4]]);

			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			trElement.hover(function () {
				$(this).toggleClass('text-hover');
			});
			tbody.append(trElement);
		});
		tableElement.append(tbody);

		$('#' + adminsSpaceForAttacksId).empty().append(tableElement);
	};

}

$(function () {
	var ai = new AdminInterface();

	// admin list all users button
	$('#' + listAllUsersButtonId).click(function listAllUsersButtonId() {
		if ($(this).val() === _t(showAllUsers)) {
			ai.getUsersOverview();
			$(this).val(_t(hideAllUsers));
		} else {
			$('#' + adminsSpaceForUsersId).empty();
			$(this).val(_t(showAllUsers));
		}
	});

	// admin list all attacks button
	$('#' + listAllUsersAttacksId).click(function listAllUsersAttacksId() {
		if ($(this).val() === _t(showAllAttacks)) {
			ai.getAttackOverview();
		} else {
			$('#' + adminsSpaceForAttacksId).empty();
		}
	});
});