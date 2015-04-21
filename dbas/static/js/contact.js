/*global $ */
$(document).ready(function () {
	'use strict';

	// Change text inside send button on submit
	$('#alert-message').hide();
	$('#warning-message').hide();
	var send = document.getElementById('contact-submit');
	if (send) {
		send.onclick = function () {
			var name = $('#name-input').val(),
					phone = $('#phone-input').val(),
					message = $('#message-input').val(),
					spam = $('#spam-input').val();

			if (!name || /^\s*$/.test(name) || 0 === name.length) {
				$('#alert-message').hide();
				$('#warning-message').show();
				$('#warning-message-text').text('Better check your name, because the input is empty!');
				
			} else if (!message || /^\s*$/.test(message) || 0 === message.length) {
				$('#alert-message').hide();
				$('#warning-message').show();
				$('#warning-message-text').text('Better check your message, because the input is empty!');
				
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