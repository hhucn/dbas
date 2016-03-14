/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AdminInterface(){

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
	this.setArgumentOverviewDataContent = function (jsonData) {
		var space = $('#' + adminsSpaceForArgumentsId),
			list = $('#dropdown-issue-list');
		space.empty();
		list.find('li:not(:first-child)').remove();
		$('#issue-switch-col').show();
		$.each(jsonData, function setJsonDataToAdminContentEach(key, value) {
			$('#dropdown-issue-list').append($('<li>').addClass('enabled').append($('<a>').text(key).attr('href', '#')));
			var tableElement, trElement, tdElement, tbody, thead, spanElement, i, img;

			tdElement = ['', '', '', '', '', ''];
			spanElement = ['', '', '', '', '', ''];
			tableElement = $('<table>').attr('id', 'table_' + key.replace(/\ /g, '_'));
			tableElement.attr('class', 'table table-condensed tablesorter');
			tableElement.attr('border', '0');
			tableElement.attr('style', 'border-collapse: separate; border-spacing: 0px; display: none;');
			tbody = $('<tbody>');
			thead = $('<thead>');

			trElement = $('<tr>');

			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i] = $('<td>');
				spanElement[i] = $('<spand>');
				spanElement[i].attr('class', 'font-semi-bold');
			}

			// add header row
			spanElement[0].text('#');
			spanElement[1].text(_t(text));
			spanElement[2].text('#Votes');
			spanElement[3].text('#Upvotes');
			spanElement[4].text('#Valid Upotes');
			spanElement[5].text('');

			for (i = 0; i < tdElement.length; i += 1) {
				tdElement[i].append(spanElement[i]);
				trElement.append(tdElement[i]);
				thead.append(trElement);
			}
			tableElement.append(thead);

			// add each attack element
			$.each(value, function setJsonArgumentkDataToAdminContentEach(v_key, v_value) {
				trElement = $('<tr>');
				for (i = 0; i < tdElement.length; i += 1) {
					tdElement[i] = $('<td>');
				}

				img = $('<img>').addClass('glyphicon-local center info-glyphicon');
				img.attr('id', 'info_' + v_value.uid).attr('src', mainpage + "static/images/transparent.gif");
				img.click(function () {
					alert('todo infos about argument ' + v_value.uid);
				});

				tdElement[0].text(v_key).attr('argument_' + v_value.uid);
				tdElement[1].text(v_value.text);
				tdElement[2].text(v_value.votes);
				tdElement[3].text(v_value.valid_votes);
				tdElement[4].text(v_value.valid_upvotes);
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

			space.append(tableElement);
		});

		space.find('table:first-child').show();
		list.find('li:nth-child(2)').removeClass('enabled').addClass('disabled');
		list.find('li:not(:first-child)').each(function(){
			$(this).click(function(){
				var current = $('#dropdown-issue-list').find('li.disabled'),
					currentIssue = current.find('a').text();
				current.addClass('enabled').removeClass('disabled');
				$(this).removeClass('enabled').addClass('disabled');
				$('#table_' + currentIssue.replace(/\ /g, '_')).hide();
				$('#table_' + $(this).find('a').text().replace(/\ /g, '_')).show();
			})
		});
	};

}

$(function () {
	var ai = new AdminInterface();
	$('#issue-switch-col').hide();

	// admin list all users button
	$('#' + listAllUsersButtonId).click(function listAllUsersButtonId() {
		if ($(this).val() === _t(showAllUsers)) {
			$('#admins-space-users').fadeIn();
			$(this).val(_t(hideAllUsers));
		} else {
			$('#admins-space-users').fadeOut();
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
