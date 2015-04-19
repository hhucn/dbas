$('.form').find('input, textarea').on('keyup blur focus', function (e) {

	var $this = $(this),
		label = $this.prev('label');

	if (e.type === 'keyup') {
		if ($this.val() === '') {
			label.removeClass('active highlight');
		} else {
			label.addClass('active highlight');
		}
	} else if (e.type === 'blur') {
		if ($this.val() === '') {
			label.removeClass('active highlight');
		} else {
			label.removeClass('highlight');
		}
	} else if (e.type === 'focus') {

		if ($this.val() === '') {
			label.removeClass('highlight');
		} else if ($this.val() !== '') {
			label.addClass('highlight');
		}
	}
});

$('.tab a').on('click', function (e) {

	e.preventDefault();

	$(this).parent().addClass('active');
	$(this).parent().siblings().removeClass('active');

	target = $(this).attr('href');

	$('.tab-content > div').not(target).hide();

	$(target).fadeIn(600);

});

$(document).ready(function () {
	'use strict';

	// Create input element for testing
	var inputs = document.createElement('input');

	// Create the supports object
	var supports = {};

	supports.autofocus = 'autofocus' in inputs;
	supports.required = 'required' in inputs;
	supports.placeholder = 'placeholder' in inputs;

	// Fallback for autofocus attribute
	if (!supports.autofocus) {

	}

	// Fallback for required attribute
	if (!supports.required) {

	}

	// Fallback for placeholder attribute
	if (!supports.placeholder) {

	}

	// Change text inside send button on submit
	var send = document.getElementById('submit-register');
	if (send) {
		send.onclick = function () {
			this.innerHTML = '...Sending Registration';
		}
	}
	var send = document.getElementById('submit-login');
	if (send) {
		send.onclick = function () {
			this.innerHTML = '...Sending Login';
		}
	}

})();