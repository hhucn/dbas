// main function
$(document).ready(function () {
    'use strict';

    $('#admin-login-button').click(function () {
        var user = $('#admin-login-user').val();
        var pw = $('#admin-login-pw').val();
        new AjaxLoginHandler().login(user, pw, true);
    });

    // gui modification for the caution row
    if (!Cookies.get(ADMIN_WARNING)) {
        $('#close-warning').fadeIn();
        $('#close-warning-btn').click(function () {
            $('#close-warning').fadeOut();
            Cookies.set(ADMIN_WARNING, true, {expires: 7});
        });
    }

    // set pointer and click event for every row
    $('#admin-entities').find('tr').each(function () {
        $(this).css('cursor', 'pointer');
        $(this).click(function () {
            window.location.href = $(this).data('href');
        });
    });

    // reset modal if it hides.
    $("#api-token-generate-dialog").on("hidden.bs.modal", function () {
        $('#api-token').hide().empty();
        $('#api-token-footer').hide();
        $('#api-token-generate-form').show();
    });
});
