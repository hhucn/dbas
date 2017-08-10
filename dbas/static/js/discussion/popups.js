/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function PopupHandler() {
	'use strict';
	
	/**
	 * Opens the edit statements popup
	 * @param statements_uids
	 */
	this.showEditStatementsPopup = function (statements_uids) {
		var input_space = $('#' + popupEditStatementInputSpaceId);
		var ajaxHandler = new AjaxDiscussionHandler();
		$('#' + popupEditStatementId).modal('show');
		input_space.empty();
		$('#' + popupEditStatementLogfileSpaceId).empty();
		$('#' + proposalEditListGroupId).empty();
		$('#' + popupEditStatementErrorDescriptionId).text('');
		$('#' + popupEditStatementSuccessDescriptionId).text('');
		$('#' + popupEditStatementInfoDescriptionId).text('');
		$('#' + popupEditStatementSubmitButtonId).addClass('disabled').off('click');
		
		// Get logfile
		ajaxHandler.getLogfileForStatements(statements_uids);
		
		// Add inputs
		$.each(statements_uids, function (index, value) {
			var statement = $('#' + value).text().trim().replace(/\s+/g, ' ');
			
			var group = $('<div>').addClass('form-group');
			var outerInputGroup = $('<div>').addClass('col-md-12').addClass('input-group');
			var innerInputGroup = $('<div>').addClass('input-group-addon');
			var group_icon = $('<i>').addClass('fa').addClass('fa-2x').addClass('fa-pencil-square-o').attr('aria-hidden', '"true"');
			var input = $('<input>')
				.addClass('form-control')
				.attr('id', 'popup-edit-statement-input-' + index)
				.attr('name', 'popup-edit-statement-input-' + index)
				.attr('type', text)
				.attr('placeholder', statement)
				.attr('data-statement-uid', value)
				.val(statement);
			
			innerInputGroup.append(group_icon);
			outerInputGroup.append(innerInputGroup).append(input);
			group.append(outerInputGroup);
			input_space.append(group);
		});

		// GUI for editing statements
		var _l = function(s1, s2){
			return levensthein(s1, s2);
		};
		input_space.find('input').each(function () {
			$(this).keyup(function () {
				var oem = $(this).attr('placeholder');
				var now = $(this).val();
				var id = $(this).attr('id');
				var statement_uid = $(this).data('statement-uid');
				
				// reduce noise
				var levensthein = _l(oem, now);
				var tmp = _t_discussion(pleaseEditAtLeast).replace('X', 5 - levensthein);
				$('#' + popupEditStatementInfoDescriptionId).text(levensthein < 5 ? tmp : '');
				
				var btn = $('#' + popupEditStatementSubmitButtonId);
				if (now && oem && now.toLowerCase() === oem.toLowerCase()) {
					btn.addClass('disabled');
					btn.off('click');
					
				} else {
					btn.removeClass('disabled');
					btn.off('click').click(function popupEditStatementSubmitButton() {
						var elements = [];
						$('#' + popupEditStatementInputSpaceId).find('input').each(function(){
							elements.push({'text': $(this).val(), 'uid': $(this).data('statement-uid')});
						});
						new AjaxDiscussionHandler().sendCorrectionOfStatement(elements, statements_uids);
					});
				}
				
				
				setTimeout(function () {
					ajaxHandler.fuzzySearch(now, id, fuzzy_statement_popup, statement_uid);
				}, 200);
			});
		});
	};
	
	/**
	 * Clears the edit statement popup
	 */
	this.hideAndClearEditStatementsPopup = function () {
		$('#' + popupEditStatementId).modal('hide');
		$('#' + popupEditStatementLogfileSpaceId).empty();
		$('#' + popupEditStatementInputSpaceId).empty();
	};
	
	/**
	 * Display url sharing popup
	 */
	this.showUrlSharingPopup = function () {
		var popup = $('#' + popupUrlSharingId);
		popup.modal('show');
		popup.on('hidden.bs.modal', function (e) {
			clearAnchor();
		});
		setAnchor('sharing');
		new AjaxDiscussionHandler().getShortenUrl(window.location);
		//$('#' + popupUrlSharingInputId).val(window.location);
	};
	
	/**
	 * Display url sharing popup
	 */
	this.showGeneratePasswordPopup = function () {
		$('#' + popupGeneratePasswordId).modal('show');
		$('#' + popupGeneratePasswordCloseButtonId).click(function () {
			$('#' + popupGeneratePasswordId).modal('hide');
		});
		$('#' + popupLoginCloseButton).click(function () {
			$('#' + popupGeneratePasswordId).modal('hide');
		});
	};
	
	/**
	 * Displays add topic plugin
	 *
	 */
	this.showAddTopicPopup = function () {
		$('#popup-add-topic').modal('show');
		$('#popup-add-topic-accept-btn').click(function () {
			var info = $('#popup-add-topic-info-input').val();
			var long_info = $('#popup-add-topic-long-info-input').val();
			var title = $('#popup-add-topic-title-input').val();
			var lang = $('#popup-add-topic-lang-input').find('input[type="radio"]:checked').attr('id');
			new AjaxDiscussionHandler().sendNewIssue(info, long_info, title, lang);
		});
		$('#popup-add-topic-refuse-btn').click(function () {
			$('#popup-add-topic').modal('hide');
		});
	};
	
	/**
	 * Display popup for flagging statements
	 *
	 * @param uid of the argument
	 * @param is_argument is true if the statement is a complete argument
	 * @param text of the statement
	 */
	this.showFlagStatementPopup = function (uid, is_argument, text) {
		var popup = $('#' + popupFlagStatement);
		$('#' + popupFlagStatementTextField).text(text);
		if (is_argument) {
			popup.find('.statement_text').hide();
			popup.find('.argument_text').show();
			// arguments are never duplicates nor can they be merged or splitted
			this._hideFlagElement(popup, 'dupl');
			this._hideFlagElement(popup, 'merge');
			this._hideFlagElement(popup, 'split');
			
			// do not mark arguments for optimizations
			popup.find('fieldset').children().eq(0).hide();
			popup.find('fieldset').children().eq(1).hide();
			popup.find('fieldset').children().eq(2).hide();
		} else {
			popup.find('.statement_text').show();
			popup.find('.argument_text').hide();
			// only statements are duplicates
			this._showFlagElement(popup, 'dupl');
			this._showFlagElement(popup, 'merge');
			this._showFlagElement(popup, 'split');
		}
		
		popup.modal('show');
		popup.on('hide.bs.modal', function () {
			popup.find('input').off('click').unbind('click');
		});
		
		popup.on('hidden.bs.modal', function () {
			popup.find('fieldset').children().eq(0).show();
			popup.find('fieldset').children().eq(1).show();
			popup.find('fieldset').children().eq(2).show();
		});
		
		popup.find('input').not('#dupl').not('#split').not('#merge').click(function () {
			var reason = $(this).attr('value');
			if (reason === 'optimization' && is_argument){
				// do not mark arguments for optimizations
				return false;
			}
			new AjaxMainHandler().ajaxFlagArgumentOrStatement(uid, reason, is_argument, null);
			popup.find('input').prop('checked', false);
			popup.modal('hide');
		});
		
		popup.find('#dupl').click(function () {
			popup.find('input').prop('checked', false);
			popup.modal('hide');
			var text = $('#' + popupFlagStatementTextField).text();
			var reason = $(this).attr('value');
			// check for premisegroup
			if ($('#item_' + uid).parent().find('label').length > 1){
				new PopupHandler().showPopupForSelectingDuplicateFromPrgroup(uid, reason);
			} else {
				// correct uid
				var is_premisegroup = window.location.href.split('?')[0].indexOf('justify') !== -1;
				if (is_premisegroup) {
					uid = $('label[for="item_' + uid + '"]').attr('id');
				}
				new PopupHandler().showStatementDuplicatePopup(uid, text, reason);
			}
		});
		
		popup.find('#split').click(function () {
			popup.find('input').prop('checked', false);
			popup.modal('hide');
			var text = $('#' + popupFlagStatementTextField).text();
			var reason = $(this).attr('value');
			alert('todo split for "' + text + '" because ' + reason);
		});
		
		popup.find('#merge').click(function () {
			popup.find('input').prop('checked', false);
			popup.modal('hide');
			var text = $('#' + popupFlagStatementTextField).text();
			var reason = $(this).attr('value');
			alert('todo merge for "' + text + '" because ' + reason);
		});
	};
	
	/**
	 *
	 * @param popup
	 * @param id
	 * @private
	 */
	this._hideFlagElement = function(popup, id){
		popup.find('#' + id).prev().show(); // input element
		popup.find('#' + id).next().show(); // br tag
		popup.find('#' + id).show();
	};
	
	/**
	 *
	 * @param popup
	 * @param id
	 * @private
	 */
	this._showFlagElement = function(popup, id){
		popup.find('#' + id).prev().show(); // input element
		popup.find('#' + id).next().show(); // br tag
		popup.find('#' + id).show();
	};
	
	/**
	 * Display popup for flagging arguments
	 *
	 * @param uid of the argument
	 */
	this.showFlagArgumentPopup = function (uid) {
		var popup = $('#popup-flag-argument');
		var bubble = $('#question-bubble-' + uid);
		if (bubble.length === 0){
			bubble = $('#' + uid.replace('.', '\\.'));
		}
		
		// clean text
		// cut the part after <br><br>
		var text = bubble.find('.triangle-content').html();
		text = text.substr(0, text.indexOf('<br>'));
		
		// cut the author
		var tmp = text.indexOf('</a>');
		if (tmp !== -1) {
			var a = bubble.find('.triangle-content a').attr('title');
			text = a + ' ' + text.substr(tmp + '</a>'.length);
		}
			
		// cut all spans
		while (text.indexOf('</span>') !== -1) {
			text = text.replace('</span>', '');
		}
		while (text.indexOf('<span') !== -1) {
			text = text.substr(0, text.indexOf('<span')) + text.substr(text.indexOf('>') + 1);
		}
		
		$('#popup-flag-argument-text').text(text);
		popup.modal('show');
		popup.on('hide.bs.modal', function () {
			popup.find('input').off('click').unbind('click');
		});
		popup.find('input,label').off('click').click(function () {
			var special = $(this).data('special');
			var id = $(this).attr('id');
			var next = $(this).next();
			if ($(this).is('label')){  // gettin the <input>
				special = $(this).prev().data('special');
				id = $(this).prev().attr('id');
				next = $(this);
			}
			if (special === 'undercut') {
				$('#item_undercut').click();
				
			} else if (special === 'argument') {
				new PopupHandler().showFlagStatementPopup(uid, true, text);
				
			} else {
				var tmp = next.find('em').text();
				new PopupHandler().showFlagStatementPopup(id, false, tmp);
			}
			popup.find('input').prop('checked', false);
			popup.modal('hide');
		});
		
		// pretty stuff on hovering
		popup.find('input').each(function () {
			if ($(this).data('special') === '') {
				var current = $(this).next().find('em').text().trim();
				$(this).hover(function () {
					var modded_text = text.replace(new RegExp("(" + (current + '').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1") + ")", 'gi'), "<span class='text-primary'>$1</span>");
					$('#popup-flag-argument-text').html(modded_text);
					$(this).next().find('em').html("<span class='text-primary'>" + current + "</span>");
				}, function () {
					$('#popup-flag-argument-text').text(text);
					$(this).next().find('em').html(current);
				});
			}
		});
		popup.find('label').each(function () {
			if ($(this).prev().data('special') === '') {
				var current = $(this).find('em').text().trim();
				$(this).hover(function () {
					var modded_text = text.replace(new RegExp("(" + (current + '').replace(/([\\\.\+\*\?\[\^\]\$\(\)\{\}\=\!\<\>\|\:])/g, "\\$1") + ")", 'gi'), "<span class='text-primary'>$1</span>");
					$('#popup-flag-argument-text').html(modded_text);
					$(this).find('em').html("<span class='text-primary'>" + current + "</span>");
				}, function () {
					$('#popup-flag-argument-text').text(text);
					$(this).find('em').text(current);
				});
			}
		});
	};
	
	/**
	 *
	 */
	this.showSearchStatementPop = function(){
		var titleText = _t(searchStatementPopupTitleText);
		var bodyText =
			'<p>' + _t(searchStatementPopupBodyText) + '</p>' +
			'<div class="form-group">' +
			'<div class="input-group">' +
			'<span class="input-group-addon"><i class="fa fa-search" aria-hidden="true" style="padding: 6px 7px;"></i></span>' +
			'<input id="search-statement-input" type="text" class="form-control" placeholder="' + _t(pleaseEnterYourTextForSearchHere) + '">' +
			'</div>' +
			'</div>' +
			'<div id="' + proposalStatementSearchGroupId + '"></div>';
		
		displayConfirmationDialog(titleText, bodyText, null, null, false);
		$('#' + popupConfirmDialogId).find('#confirm-dialog-accept-btn').hide();
		
		$("#search-statement-input").keyup(function () {
			var val = $('#search-statement-input').val();
			setTimeout(function () {
				new AjaxDiscussionHandler().fuzzySearch(escapeHtml(val), 'search-statement-input', fuzzy_find_statement, '');
			}, 200);
		});
	};
	
	/**
	 *
	 * @param uid
	 * @param reason
	 */
	this.showPopupForSelectingDuplicateFromPrgroup = function(uid, reason){
		var popup = $('#popup-choose-statement');
		var body = $('#popup-choose-statement-radios');
		body.empty();
		popup.modal('show');
		
		$.each($('#item_' + uid).parent().find('label:even'), function(){
			var div = $('<div>').addClass('radio');
			var label = $('<label>').attr({'data-uid': $(this).attr('id')});
			var input = $('<input>').attr({'type': 'radio', 'name': 'selectStatementDupl'});
			var span = $('<span>').text($(this).text());
			body.append(div.append(label.append(input).append(span)));
			label.click(function(){
				new PopupHandler().showStatementDuplicatePopup($(this).data('uid'), $(this).text(), reason);
				popup.modal('hide');
			});
			label.hover(function () {
					$(this).find('input').prop('checked', true);
			}, function () {
					$(this).find('input').prop('checked', false);
			});
		});
	};
	
	/**
	 * Displays popup for marking a duplicate
	 *
	 * @param uid of the statement
	 * @param text of the statement
	 * @param reason
	 */
	this.showStatementDuplicatePopup = function(uid, text, reason){
		var popup = $('#' + popupDuplicateStatementId);
		popup.modal('show');
		popup.on('hide.bs.modal', function () {
			popup.find('input').off('click').unbind('click');
		});
		
		$('#' + popupDuplicateStatementTextId).text(text).attr('data-statement-uid', uid);
		
		// fuzzy search
		var input = $('#' + popupDuplicateStatementTextSearchId);
		input.on('keyup', function(){
			var escapedText = escapeHtml($(this).val());
			setTimeout(function () {
				new AjaxDiscussionHandler().fuzzySearch(escapedText, popupDuplicateStatementTextSearchId, fuzzy_duplicate, uid, reason);
			}, 200);
		});
	};
	
	/**
	 *
	 * @param reason
	 * @param uid
	 */
	this.duplicateValueSelected = function(reason, uid){
		var btn = $('#popup-flag-statement-accept-btn');
		btn.off('click').removeClass('disabled');
		btn.click(function(){
			var oem_uid = $('#' + popupDuplicateStatementTextId).data('statement-uid');
			new AjaxMainHandler().ajaxFlagArgumentOrStatement(uid, reason, false, oem_uid);
		});
	};
	
	/**
	 * Popup for revoking content
	 *
	 * @param uid of the element
	 * @param is_argument boolean
	 */
	this.showDeleteContentPopup = function (uid, is_argument) {
		var popup = $('#popup-delete-content');
		popup.modal('show');
		
		$('#popup-delete-content-submit').click(function () {
			new AjaxDiscussionHandler().revokeContent(uid, is_argument);
			popup.modal('hide');
		});
		
		$('#popup-delete-content-close').click(function () {
			popup.modal('hide');
		});
	};
	
	/**
	 * Popup for managing the references
	 *
	 * @param data in json-format
	 */
	this.showReferencesPopup = function (data) {
		var popup = $('#' + popupReferences);
		var references_body = $('#popup-references-body');
		var references_body_add = $('#popup-references-body-add').hide();
		var add_button = $('#popup-reference-add-btn');
		var send_button = $('#popup-reference-send-btn');
		var dropdown = $('#popup-references-cite-dropdown');
		var dropdown_list = $('#popup-references-cite-dropdown-list');
		var reference_text = $('#popup-references-add-text');
		var reference_source = $('#popup-references-add-source');
		var info_text = $('#choose_reference_text');
		
		dropdown.hide();
		info_text.hide();
		popup.modal('show');
		dropdown_list.empty();
		references_body.empty();
		add_button.show();
		send_button.prop('disabled', true);
		reference_text.val('');
		reference_source.val('');
		
		add_button.off('click').click(function () {
			add_button.hide();
			references_body_add.fadeIn();
			//send_button.prop('disabled', false);
			if (dropdown_list.find('li').length < 2) {
				dropdown.hide();
				info_text.hide();
			} else {
				dropdown.show();
				info_text.show();
			}
			if (dropdown_list.find('li').length < 2) {
				send_button.prop('disabled', false);
			}
		});
		
		send_button.off('click').click(function () {
			var uid = $(this).data('id');
			var reference = reference_text.val();
			var ref_source = reference_source.val();
			new AjaxReferenceHandler().setReference(uid, reference, ref_source);
		});
		
		this.createReferencesPopupBody(data);
		
		if (references_body.children().length === 0) {
			references_body.append($('<p>').addClass('lead').text(_t_discussion(noReferencesButYouCanAdd)));
			add_button.hide();
			send_button.prop('disabled', false);
			references_body_add.fadeIn();
			if (dropdown_list.find('li').length < 2) {
				dropdown.hide();
				info_text.hide();
			} else {
				dropdown.show();
				info_text.show();
				send_button.prop('disabled', true);
			}
		}
		
		dropdown_list.find('li').each(function() {
			$(this).off('click').click(function(){
				send_button.attr('data-id', $(this).data('id'));
				send_button.prop('disabled', false);
			});
		});
	};
	
	/**
	 * Creates the body of the reference popup
	 *
	 * @param data in json-format
	 */
	this.createReferencesPopupBody = function (data) {
		var references_body = $('#popup-references-body');
		var send_button = $('#popup-reference-send-btn');
		var dropdown = $('#popup-references-cite-dropdown');
		var dropdown_list = $('#popup-references-cite-dropdown-list');
		var dropdown_title = $('#popup-references-cite-dropdown-title');
		
		// data is an dictionary with all statement uid's as key
		// the value of every key is an array with dictionaries for every reference
		$.each(data.data, function (statement_uid, array) {
			var statements_div = $('<div>');
			var text = '';
			// build a callout for every reference
			array.forEach(function (dict) {
				text = dict.statement_text;
				var author = $('<a>').attr({'href': dict.author.link, 'target': '_blank'}).addClass('pull-right')
					.append($('<span>').text(dict.author.name).css('padding-right', '0.5em'))
					.append($('<img>').addClass('img-circle').attr('src', dict.author.img));
				
				var link = $('<a>').attr({
					'href': dict.host + dict.path,
					'target': '_blank'
				}).text('(' + dict.host + dict.path + ')');
				var span = $('<span>').text(dict.reference + ' ');
				
				var label = $('<label>').addClass('bs-callout').addClass('bs-callout-primary');
				var body = $('<p>').append(span).append(link).append(author);
				label.append(body);
				
				statements_div.append(label);
			});
			// Add the statement itself
			var glqq = $.parseHTML('<i class="fa fa-quote-left" aria-hidden="true" style="padding: 0.5em; font-size: 12px;"></i>');
			var grqq = $.parseHTML('<i class="fa fa-quote-right" aria-hidden="true" style="padding: 0.5em; font-size: 12px;"></i>');
			var statement = $('<span>').addClass('lead').text(text);
			var wrapper = $('<p>').append(glqq).append(statement).append(grqq);
			
			// Add elements for the drop-down
			if (text.length > 0) {
				references_body.append(wrapper.append(statements_div));
			} else {
				text = data.text[statement_uid];
			}
			var tmp = $('<a>').attr('href', '#').attr('data-id', statement_uid).text(text).click(function () {
				// set text, remove popup
				dropdown_title.text($(this).text()).parent().attr('aria-expanded', false);
				dropdown.removeClass('open');
				send_button.attr('data-id', statement_uid);
			});
			dropdown_list.append($('<li>').append(tmp));
			
			// Default id
			send_button.attr('data-id', statement_uid);
		});
	};
	
	/**
	 * Closes the popup and deletes all of its contents
	 */
	this.hideAndClearUrlSharingPopup = function () {
		$('#' + popupUrlSharingId).modal('hide');
		$('#' + popupUrlSharingInputId).val('');
	};
}