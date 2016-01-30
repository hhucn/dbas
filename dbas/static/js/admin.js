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
			_this.setDataToContent($.parseJSON(data));
		}).fail(function ajaxGetAllUsersFail() {
			// new GuiHandler().setErrorDescription(_t(internalError));
			new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 9). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
		});
	};

	/**
	 * Requests all attacks
	 */
	this.getArgumentOverview = function () {
		var csrfToken = $('#' + hiddenCSRFTokenId).val(), settings_data, url, _this = this;
		$.ajax({
			url: 'ajax_get_argument_overview',
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
		}).done(function getArgumentOverviewDone(data) {
			_this.setArgumentOverviewDataContent($.parseJSON(data));
			$('#' + listAllUsersArgumentId).val(_t(hideAllArguments));
			new GuiHandler().hideErrorDescription();
		}).fail(function getArgumentOverviewFail() {
			// new GuiHandler().setErrorDescription(_t(internalError));
			new GuiHandler().showDiscussionError(_t(requestFailed) + ' (' + new Helper().startWithLowerCase(_t(errorCode)) + ' 10). '
				 + _t(doNotHesitateToContact) + '. ' + _t(restartOnError) + '.');
			$('#' + listAllUsersArgumentId).val(_t(showAllArguments));
		});
	};

	/**
	 * Sets given json data to admins content
	 * @param jsonData
	 */
	this.setDataToContent = function (jsonData) {
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
	this.setArgumentOverviewDataContent = function (jsonData) {
		var tableElement, trElement, tdElement, tbody, thead, spanElement, i, img;

		tdElement   = ['', '', '', '', '', ''];
		spanElement = ['', '', '', '', '', ''];
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
		spanElement[0].text('#');
		spanElement[1].text(_t(text));
		spanElement[2].text('#Votes');
		spanElement[3].text('#Upvotes');
		spanElement[4].text('#Valid Upotes');
		spanElement[4].text('');

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

			img = $('<img>').addClass('glyphicon-local center info-glyphicon');
			img.attr('id', 'info_' + value.uid).attr('src', mainpage + "static/images/transparent.gif");
			img.click(function(){
				alert('todo infos about argument ' + value.uid);
			});

			tdElement[0].text(key).attr('argument_' + value.uid);
			tdElement[1].text(value.text);
			tdElement[2].text(value.votes);
			tdElement[3].text(value.valid_votes);
			tdElement[4].text(value.valid_upvotes);
			tdElement[5].append(img);

			for (i = 0; i < tdElement.length; i += 1) {
				trElement.append(tdElement[i]);
			}
			trElement.hover(function () {
				$(this).toggleClass('text-hover');
			});
			tbody.append(trElement);
		});
		tableElement.append(tbody);

		$('#' + adminsSpaceForArgumentsId).empty().append(tableElement);
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
	$('#' + listAllUsersArgumentId).click(function listAllUsersAttacksId() {
		if ($(this).val() === _t(showAllArguments)) {
			ai.getArgumentOverview();
		} else {
			$('#' + adminsSpaceForArgumentsId).empty();
			$('#' + listAllUsersArgumentId).val(_t(showAllArguments));
		}
	});
});