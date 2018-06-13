$(document).ready(function () {
    'use strict';
    $('#' + popupLoginPasswordInputId).keyup(function () {
        if ($('#popup-login-password-input').is(':visible')) {
            checkStrength($(this).val());
        }
    });

    function checkStrength(password) {
        var r = $('#' + popupLoginPasswordMeterId);
        var t = $('#' + popupLoginPasswordStrengthId);
        var strength = 0;
        if (password.length < 6) {
            r.removeClass();
            r.addClass('col-md-9 veryweak');
            t.text(_t(veryweak));
        }
        if (password.length > 7) {
            strength += 1;
        }
        // If password contains both lower and uppercase characters, increase strength value.
        if (password.match(/([a-z].*[A-Z])|([A-Z].*[a-z])/)) {
            strength += 1;
        }
        // If it has numbers and characters, increase strength value.
        if (password.match(/([a-zA-Z])/) && password.match(/([0-9])/)) {
            strength += 1;
        }
        // If it has one special character, increase strength value.
        if (password.match(/([!,%,&,@,#,$,^,*,?,_,~])/)) {
            strength += 1;
        }
        // If it has two special characters, increase strength value.
        if (password.match(/(.*[!,%,&,@,#,$,^,*,?,_,~].*[!,%,&,@,#,$,^,*,?,_,~])/)) {
            strength += 1;
        }
        // Calculated strength value, we can return messages
        // If value is less than 2
        if (strength < 3) {
            r.removeClass();
            r.addClass('col-md-9 veryweak');
            t.text(_t(veryweak));
        } else if (strength < 4) {
            r.removeClass();
            r.addClass('col-md-9 weak');
            t.text(_t(weak));
        } else if (strength < 5) {
            r.removeClass();
            r.addClass('col-md-9 medium');
            t.text(_t(medium));
        } else {
            r.removeClass();
            r.addClass('col-md-9 strong');
            t.text(_t(strong));
        }
    }
});
