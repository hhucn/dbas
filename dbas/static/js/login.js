/*global $, jQuery, alert*/
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
	var register = document.getElementById('login-register-submit');
	if (register) {
		register.onclick = function () {
			var userfirstname = $('#userfirstname-input').val(),
				userlastname = $('#userlastname-input').val(),
				nick = $('#nick-input').val(),
				email = $('#email-input').val(),
				password = $('#password-input').val(),
				passwordconfirm = $('#passwordconfirm-input').val();

			if (!userfirstname || /^\s*$/.test(userfirstname) || 0 === userfirstname.length) {
				$('#warning-message').fadeIn("slow")
				$('#warning-message-text').text('Better check your first name, because the input is empty!');

			} else if (!userlastname || /^\s*$/.test(userlastname) || 0 === userlastname.length) {
				$('#warning-message').fadeIn("slow")
				$('#warning-message-text').text('Better check your last name, because the input is empty!');

			} else if (!nick || /^\s*$/.test(nick) || 0 === nick.length) {
				$('#warning-message').fadeIn("slow")
				$('#warning-message-text').text('Better check your nickname, because the input is empty!');

			} else if (!email || /^\s*$/.test(email) || 0 === email.length) {
				$('#warning-message').fadeIn("slow")
				$('#warning-message-text').text('Better check email, because the input is empty!');

			} else if (!password || /^\s*$/.test(password) || 0 === password.length) {
				$('#warning-message').fadeIn("slow")
				$('#warning-message-text').text('Better check password, because the input is empty!');

			} else if (!passwordconfirm || /^\s*$/.test(passwordconfirm) || 0 === passwordconfirm.length) {
				$('#warning-message').fadeIn("slow")
				$('#warning-message-text').text('Better check the confirmation of your password, because the input is empty!');
			} else if (password !== passwordconfirm) {
				$('#warning-message').fadeIn("slow")
				$('#warning-message-text').text('Better check your passwords, because they are not equal!');

			} else {
				$('#warning-message').hide();
				this.val = '...Sending Registration';
			}
		};
	}

	// check password strength
	// based on http://git.aaronlumsden.com/strength.js/
	var upperCase = new RegExp('[A-Z]'),
		lowerCase = new RegExp('[a-z]'),
		numbers = new RegExp('[0-9]'),
		specialchars = new RegExp('([!,%,&,@,#,$,^,*,?,_,~])');

	function set_total(total, pwextras, pwstrength, pwmeter) {
		pwmeter.removeClass();
		pwstrength.text('Strength: very weak');
		pwextras.fadeIn("slow");
		if (total == 1) {
			pwmeter.addClass('veryweak');
			pwstrength.text('Strength: very weak');
		} else if (total == 2) {
			pwmeter.addClass('weak');
			pwstrength.text('Strength: weak');
		} else if (total == 3) {
			pwmeter.addClass('medium');
			pwstrength.text('Strength: medium');
		} else if (total > 3) {
			pwmeter.addClass('strong');
			pwstrength.text('Strength: strong');
		} else {
			pwextras.fadeOut('slow');
		}
	}

	function check_strength(pwextras, pwinput, pwstrength, pwmeter) {
		var total = 0;
		var pw = pwinput.val();
		if (pw.length > 8) {
			total = total + 1;
		}
		if (upperCase.test(pw)) {
			total = total + 1;
		}
		if (lowerCase.test(pw)) {
			total = total + 1;
		}
		if (numbers.test(pw)) {
			total = total + 1;
		}
		if (specialchars.test(pw)) {
			total = total + 1;
		}
		set_total(total, pwextras, pwstrength, pwmeter);
	}

	var pwextras = $('#password-extras');
	var pwinput = $('#password-input');
	var pwstrength = $('#password-strength');
	var pwmeter = $('#password-meter');

	pwextras.fadeOut('slow');
	pwinput.bind("change paste keyup", function () {
		check_strength(pwextras, pwinput, pwstrength, pwmeter)
	});
	
	
	// password generator
	function generate_password() {
		var keylist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!%&@#$^*?_~';
		var password = '';
		while (!(upperCase.test(password) && lowerCase.test(password) && numbers.test(password) && specialchars.test(password))) {
			var i = 0;
			password = '';
			for (i; i < 8; i = i + 1) {
				password += keylist.charAt(Math.floor(Math.random() * keylist.length));
			}
		}
		var output = document.getElementById('password-generator-output');
		output.value = password;
	}

	var pwd_gen = $('#password-generator-button');
	if (pwd_gen) {
		pwd_gen.click(function () {
			generate_password();
		});
	}


})();