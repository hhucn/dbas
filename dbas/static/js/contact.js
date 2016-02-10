/*global $ */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

$(document).ready(function () {
	'use strict';

	// Change text inside send button on submit
	$('#alert-message').hide();
	$('#warning-message').hide();
	$('#contact-submit').onclick = function () {
		// getting input
		var name = $('#name-input').val(),
				phone = $('#phone-input').val(),
				email = $('#email-input').val(),
				message = $('#message-input').val(),
				spam = $('#spam-input').val();

		var mail_regex = /^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$/i,
				valid_mail = mail_regex.test(email);

		// check name
		if (!name || /^\s*$/.test(name) || 0 === name.length) {
			$('#alert-message').hide();
			$('#warning-message').show();
			$('#warning-message-text').text('Better check your name, because the input is empty!');

		// check mail mail
		} else if (!valid_mail) {
			$('#alert-message').hide();
			$('#warning-message').show();

			$('#warning-message-text').text('Better check your e-mail, because it is not valid!');

		// check message
		} else if (!message || /^\s*$/.test(message) || message.length < 5) {
			$('#alert-message').hide();
			$('#warning-message').show();
			$('#warning-message-text').text('Better check your message, because the input is too short!');

		} else {
			$('#warning-message').hide();
			if (spam !== 4) {
				$('#alert-message').show();
			} else {
				$('#alert-message').hide();
			}
		}
	};
});
