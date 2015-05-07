
$(document).ready(function () {
	'use strict';

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