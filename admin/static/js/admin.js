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
	 * @param parent
	 */
	this.setAddClickEvent = function(parent) {
		parent.find('.add').each(function () {
			$(this).click(function () {
				console.log('todo create');
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
					$(this).append($('<input>').attr({'class': 'form-control', 'placeholder': $(this).text()}).val($(this).text()));
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
		parent.find('.trash').each(function () {
			$(this).click(function () {
				var uid = $(this).parents('tr:first').find('td:first').text();
				new AdminAjaxHandler().deleteSomething(uid, $(this).parents('tr:first'));
			})
		});
	};
	
	/**
	 *
	 * @param parent
	 */
	this.setSaveClickEvent = function(parent) {
		parent.find('.floppy').each(function () {
			$(this).click(function () {
				var tmp = $(this).parents('tr:first');
				var uid = $(this).parents('tr:first').find('td:first').text();
				var keys = [];
				var values = [];
				$(this).parents('tr:first').find('input').each(function (){
					values.push($(this).val());
				});
				$('#data').find('thead').find('th:not(:last-child)').each(function () {
					keys.push($(this).text());
				});
				new AdminAjaxHandler().updateSomething(this, uid, keys, values);
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
	}
}

// main function
$(document).ready(function () {
	$('#admin-login-button').click(function(){
		new AdminIndex().login();
	});
	
	var data = $('#data');
	var gui = new AdminGui();
	
	// events for edit
	gui.setEditClickEvent(data);
	
	// events for delete
	gui.setDeleteClickEvent(data);
	
	// events for save
	gui.setSaveClickEvent(data);
	
	// events for cancel
	gui.setCancelClickEvent(data);
	
	// events for add
	gui.setAddClickEvent(data);
});
