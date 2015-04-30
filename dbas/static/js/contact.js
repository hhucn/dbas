/*global $ */
$(document).ready(function () {
	'use strict';

	// Change text inside send button on submit
	$('#alert-message').hide();
	$('#warning-message').hide();
	var send = document.getElementById('contact-submit');
	if (send) {
		send.onclick = function () {
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
				
				$('#warning-message-text').text('Better check your e-mail!');
				
			// check message
			} else if (!message || /^\s*$/.test(message) || message.length < 50) {
				$('#alert-message').hide();
				$('#warning-message').show();
				$('#warning-message-text').text('Better check your message, because the input is too short!');
				
			} else {
				$('#warning-message').hide();
				if (spam !== 4) {
					$('#alert-message').show();
				} else {
					$('#alert-message').hide();
					this.innerHTML = '...opening mail client...';
					window.location.href = "mailto:krauthoff@cs.uni-duesseldorf.de?subject=Contact%20D-BAS&body=Name:%20" + name + "&#13;&#10;Phone:%20" + phone + "&#13;&#10;Message:&#13;&#10;&#13;&#10;" + message;
				}
			}
		};
	}

})();