function Sharing() {
    'use strict';

    /**
     *
     * @param url
     * @param title
     * @param descr
     * @param image
     */
    this.facebookShare = function (url, title, descr, image) {
        var winTop, winLeft, winWidth, winHeight;
        winWidth = 520;
        winHeight = 350;
        winTop = (screen.height / 2) - (winHeight / 2);
        winLeft = (screen.width / 2) - (winWidth / 2);
        window.open('http://www.facebook.com/sharer.php?s=100&p[title]=' + title + '&p[summary]=' + descr + '&p[url]=' + url + '&p[images][0]=' + image, 'sharer',
            ',top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
    };

    /**
     *
     * @param text
     * @param link
     */
    this.twitterShare = function (text, link) {
        var winWidth = 550,
            winHeight = 420,
            winTop = (screen.height / 2) - (winHeight / 2),
            winLeft = (screen.width / 2) - (winWidth / 2);
        text = link.length > 0 ? text + ' on ' + link : text;
        window.open('https://twitter.com/intent/tweet?text=' + text + '&hashtags=DBAS,nrwfkop', 'sharer',
            ',top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
    };

    /**
     *
     * @param to
     * @param subject
     * @param body
     */
    this.emailShare = function (to, subject, body) {
        window.location.href = "mailto:" + to + "?subject=" + subject + "&body=" + body;
    };

    /**
     *
     * @param url
     */
    this.googlePlusShare = function (url) {
        var winTop, winLeft, winWidth, winHeight;
        winWidth = 600;
        winHeight = 400;
        winTop = (screen.height / 2) - (winHeight / 2);
        winLeft = (screen.width / 2) - (winWidth / 2);
        window.open('https://plus.google.com/share?url=' + url, 'sharer',
            ',top=' + winTop + ',left=' + winLeft + ',toolbar=0,status=0,width=' + winWidth + ',height=' + winHeight);
    };
}
