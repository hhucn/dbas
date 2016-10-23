/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AdminGui() {
	
	/**
	 *
	 * @param _this
	 * @param elements_class
	 * @param text_class
	 */
	this.activateElement = function(_this, elements_class, text_class) {
		var element = $(_this).parents('td:first').find('.' + elements_class);
		element.removeClass('text-muted').addClass(text_class);
		element.parent().css('pointer-events', '');
	};
	
	/**
	 *
	 * @param _this
	 * @param elements_class
	 * @param text_class
	 */
	this.deactivateElement = function(_this, elements_class, text_class) {
		var element = $(_this).parents('td:first').find('.' + elements_class);
		element.addClass('text-muted').removeClass(text_class);
		element.parent().css('pointer-events', 'none');
	};
	
	/**
	 *
	 */
	this.setAddClickEvent = function() {
		$('body').find('.add').each(function () {
			$(this).click(function () {
				var dialog = $('#' + popupConfirmRowDialogId);
				var body = dialog.find('.modal-body');
				body.children().remove();
				dialog.modal('show');
				dialog.children().eq(0).removeClass('modal-lg');
				dialog.find('.modal-title').text('Add Data');
				$('#data').find('th:not(:last-child)').each(function (){
					if ($(this).text() != 'uid') {
						var form = $('<div>').addClass('form-group');
						var label = $('<label>').addClass('col-sm-5').addClass('control-label').attr('for', $(this).text()).text($(this).text());
						var div = $('<div>').addClass('col-sm-7').append($('<input>').attr({
							'class': 'form-control',
							'data-for': $(this).text()
						}));
						body.append(form.append(label).append(div));
					}
				});
				dialog.find('.btn-danger').off('click').click(function (){
					dialog.modal('hide');
				});
				dialog.find('.btn-success').off('click').click(function (){
					var data = {};
					body.find('input').each(function (){
						data[$(this).data('for')] = $(this).val();
					});
					new AdminAjaxHandler().addSomething(data);
				});
			})
		});
	};
	
	/**
	 *
	 * @param parent
	 */
	this.setEditClickEvent = function(parent) {
		var _this = this;
		parent.find('.pencil').each(function () {
			$(this).click(function () {
				var parent = $(this).parents('tr:first');
				// var uid = parent.find('td:first').text();
				_this.activateElement(this, 'floppy', 'text-success');
				_this.activateElement(this, 'square', 'text-danger');
				_this.deactivateElement(this, 'pencil', 'text-danger');
				parent.find('td:not(:last)').each(function(){
					$(this).append($('<input>').attr({'class': 'form-control', 'placeholder': $(this).text().trim()}).val($(this).text().trim()));
					$(this).find('span').hide();
				});
			})
		});
	};
	
	/**
	 *
	 * @param parent
	 */
	this.setDeleteClickEvent = function(parent) {
		var _this = this;
		parent.find('.trash').each(function () {
			$(this).click(function () {
				var uids = _this.getUids($(this).parents('tr:first'));
				new AdminAjaxHandler().deleteSomething(uids, $(this).parents('tr:first'));
			})
		});
	};
	
	/**
	 *
	 * @param parent
	 */
	this.setSaveClickEvent = function(parent) {
		var _this = this;
		parent.find('.floppy').each(function () {
			$(this).click(function () {
				var tmp = $(this).parents('tr:first');
				var uids = _this.getUids(tmp);
				var keys = [];
				var values = [];
				tmp.find('input').each(function (){
					values.push($(this).val());
				});
				$('#data').find('thead').find('th:not(:last-child)').each(function () {
					keys.push($(this).text());
				});
				new AdminAjaxHandler().updateSomething(this, uids, keys, values);
				tmp.find('input').remove();
				tmp.find('span').show();
			})
		});
	};
	
	/**
	 *
	 * @param parent
	 */
	this.setCancelClickEvent = function(parent) {
		var _this = this;
		parent.find('.square').each(function () {
			$(this).click(function () {
				var tmp = $(this).parents('tr:first');
				// var uid = tmp.find('td:first').text();
				_this.deactivateElement(this, 'floppy', 'text-success');
				_this.deactivateElement(this, 'square', 'text-danger');
				_this.activateElement(this, 'pencil', '');
				tmp.find('input').remove();
				tmp.find('span').show();
			})
		});
	};
	
	/**
	 * Searches the PK of the table and returns an array
	 *
	 * @param element is the tr element of the table
	 * @returns {Array}
	 */
	this.getUids = function(element){
		var uids = [];
		// Premise has two columns as PK
		$.inArray( 'Premise', [ "8", "9", "10", 10 + "" ] );
		if ($('#table_name').text().toLowerCase() === 'premise'){
			uids.push(element.find('td:nth-child(1)').text().trim());
			uids.push(element.find('td:nth-child(2)').text().trim());
		} else {
			uids.push(element.find('td:first').text().trim());
		}
		return uids;
	}
}

// main function
$(document).ready(function () {
	$('#admin-login-button').click(function(){
		new AdminIndex().login();
	});
	
	var data = $('#data');
	var gui = new AdminGui();
	var helper = new Helper();
	
	// events for edit
	gui.setEditClickEvent(data);
	
	// events for delete
	gui.setDeleteClickEvent(data);
	
	// events for save
	gui.setSaveClickEvent(data);
	
	// events for cancel
	gui.setCancelClickEvent(data);
	
	// events for add
	gui.setAddClickEvent();
	
	if (!helper.isCookieSet('hide-admin-caution-warning')) {
		$('#close-warning').fadeIn();
		$('#close-warning-btn').click(function(){
			$('#close-warning').fadeOut();
			helper.setCookieForDays('hide-admin-caution-warning', 7, 'true')
		});
	}
	
	$('#admin-overview').find('tr').each(function() {
		$(this).css('cursor', 'pointer');
		$(this).click(function (){
			window.location.href = $(this).data('href');
		});
	})
	
});
