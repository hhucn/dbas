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
	
	$('#warning-message').hide();
	var send = document.getElementById('login-register-submit');
	if (send) {
		send.onclick = function () {
			var userfirstname = $('#userfirstname-input').val(),
				userlastname = $('#userlastname-input').val(),
				email = $('#email-input').val(),
				password = $('#password-input').val(),
				passwordconfirm = $('#passwordconfirm-input').val();

			if (!userfirstname || /^\s*$/.test(userfirstname) || 0 === userfirstname.length) {
				$('#warning-message').show();
				$('#warning-message-text').text('Better check your first name, because the input is empty!');

			} else if (!userlastname || /^\s*$/.test(userlastname) || 0 === userlastname.length) {
				$('#warning-message').show();
				$('#warning-message-text').text('Better check your last name, because the input is empty!');

			} else if (!email || /^\s*$/.test(email) || 0 === email.length) {
				$('#warning-message').show();
				$('#warning-message-text').text('Better check email, because the input is empty!');

			} else if (!password || /^\s*$/.test(password) || 0 === password.length) {
				$('#warning-message').show();
				$('#warning-message-text').text('Better check password, because the input is empty!');

			} else if (!passwordconfirm || /^\s*$/.test(passwordconfirm) || 0 === passwordconfirm.length) {
				$('#warning-message').show();
				$('#warning-message-text').text('Better check the confirmation of your password, because the input is empty!');
			} else if (password !== passwordconfirm) {
				$('#warning-message').show();
				$('#warning-message-text').text('Better check your passwords, because they are not equal!');

			} else {
				$('#warning-message').hide();
				this.innerHTML = '...Sending Registration';
			}
		}
	}

	// Change text inside send button on submit
	var send = document.getElementById('submit-login');
	if (send) {
		send.onclick = function () {
			this.innerHTML = '...Sending Login';
		}
	}

})();