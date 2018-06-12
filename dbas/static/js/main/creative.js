(function ($) {
    "use strict"; // Start of use strict

    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').click(function () {
        $('.navbar-collapse').collapse('hide');
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $('body').scrollspy({
        target: '#mainNav',
        offset: 48
    });

    // Collapse the navbar when page is scrolled
    $(window).scroll(function () {
        var nav = $("#mainNav");
        if (nav.length !== 0) {
            if (nav !== null && $(document).scrollTop() > 100) {
                nav.addClass("navbar-shrink");
            } else {
                nav.removeClass("navbar-shrink");
            }
        }
    });

})(jQuery); // End of use strict
