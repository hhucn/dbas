(function ($) {
    "use strict"; // Start of use strict
    
    // Smooth scrolling using jQuery easing by https://css-tricks.com/snippets/jquery/smooth-scrolling/
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (location.pathname.replace(/^\//, '') === this.pathname.replace(/^\//, '') && location.hostname === this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) { // Does a scroll target exist?
                event.preventDefault(); // Only prevent default if animation is actually gonna happen
                $('html, body').animate({
                    scrollTop: target.offset().top - 50
                }, 1000, function () {
                    $(target).focus();
                    if ($(target).is(":focus")) { // Checking if the target was focused
                        return false;
                    }
                    $(target).attr('tabindex', '-1'); // Adding tabindex for elements not focusable
                    $(target).focus(); // Set focus again
                });
            }
        }
    });
    
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
            if (typeof nav !== 'undefined' && $(document).scrollTop() > 100) {
                nav.addClass("navbar-shrink");
            } else {
                nav.removeClass("navbar-shrink");
            }
        }
    });
    
})(jQuery); // End of use strict
