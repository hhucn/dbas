/*global $, upperCase, set_total, check_strength, generate_password*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

// check password strength
// based on http://git.aaronlumsden.com/strength.js/
var upperCase = new RegExp('[A-Z]'),
	lowerCase = new RegExp('[a-z]'),
	numbers = new RegExp('[0-9]'),
	specialchars = new RegExp('([!,%,&,@,#,$,^,*,?,_,~])');

function set_total(total, pwextras, pwstrength, pwmeter) {
	'use strict';
	pwmeter.removeClass();
	pwstrength.text('Strength: very weak');
	pwextras.fadeIn("slow");
	if (total === 1) {
		pwmeter.addClass('veryweak');
		pwstrength.text('Strength: very weak');
	} else if (total === 2) {
		pwmeter.addClass('weak');
		pwstrength.text('Strength: weak');
	} else if (total === 3) {
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
	'use strict';
	var total = 0,
		pw = pwinput.val();
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

// password generator
function generate_password(output) {
	'use strict';
	var keylist = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!%&@#$^*?_~',
		password = '',
		i = 0;
	while (!(upperCase.test(password) && lowerCase.test(password) && numbers.test(password) && specialchars.test(password))) {
		i = 0;
		password = '';
		for (i; i < 8; i = i + 1) {
			password += keylist.charAt(Math.floor(Math.random() * keylist.length));
		}
	}
	output.val(password);
}

$(document).ready(function () {
	'use strict';

	var pwd_extras = $('#password-extras'),
		pwd_input = $('#password-input'),
		pwd_strength = $('#password-strength'),
		pwd_meter = $('#password-meter'),
		pwd_output = $('#password-generator-output'),
		pwd_gen = $('#password-generator-button');

	if (pwd_extras) {
		pwd_extras.fadeOut('slow');
	}

	if (pwd_input) {
		pwd_input.bind("change paste keyup", function () {
			check_strength(pwd_extras, pwd_input, pwd_strength, pwd_meter);
		});
	}

	if (pwd_gen) {
		pwd_gen.click(function () {
			generate_password(pwd_output);
		});
	}

});