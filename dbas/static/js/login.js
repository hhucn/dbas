/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

$('.tab a').on('click', function (e) {
	'use strict';
	e.preventDefault();

	$(this).parent().addClass('active');
	$(this).parent().siblings().removeClass('active');

	var target = $(this).attr('href');

	$('.tab-content > div').not(target).hide();

	$(target).fadeIn(600);

});

$(document).ready(function () {
	'use strict';

	$('#warning-message').fadeOut('slow');

	$('#login-register-submit').onclick = function () {
		var userfirstname = $('#userfirstname-input').val(),
			userlastname = $('#userlastname-input').val(),
			nick = $('#nick-input').val(),
			email = $('#email-input').val(),
			password = $('#password-input').val(),
			passwordconfirm = $('#passwordconfirm-input').val();

		if (!userfirstname || /^\s*$/.test(userfirstname) || 0 === userfirstname.length) {
			$('#warning-message').fadeIn("slow");
			$('#warning-message-text').text('Better check your first name, because the input is empty!');

		} else if (!userlastname || /^\s*$/.test(userlastname) || 0 === userlastname.length) {
			$('#warning-message').fadeIn("slow");
			$('#warning-message-text').text('Better check your last name, because the input is empty!');

		} else if (!nick || /^\s*$/.test(nick) || 0 === nick.length) {
			$('#warning-message').fadeIn("slow");
			$('#warning-message-text').text('Better check your nickname, because the input is empty!');

		} else if (!email || /^\s*$/.test(email) || 0 === email.length) {
			$('#warning-message').fadeIn("slow");
			$('#warning-message-text').text('Better check email, because the input is empty!');

		} else if (!password || /^\s*$/.test(password) || 0 === password.length) {
			$('#warning-message').fadeIn("slow");
			$('#warning-message-text').text('Better check password, because the input is empty!');

		} else if (!passwordconfirm || /^\s*$/.test(passwordconfirm) || 0 === passwordconfirm.length) {
			$('#warning-message').fadeIn("slow");
			$('#warning-message-text').text('Better check the confirmation of your password, because the input is empty!');

		} else if (password !== passwordconfirm) {
			$('#warning-message').fadeIn("slow");
			$('#warning-message-text').text('Better check your passwords, because they are not equal!');

		} else {
			$('#warning-message').hide();
			this.val = '...Sending Registration';
		}
	};

});