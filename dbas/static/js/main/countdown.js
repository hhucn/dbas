/**
 * Little simple countdown-timer with 1000ms steps
 *
 * @param options dictionary with seconds, onUpdateStatus and onCounterEnd as functions
 * @constructor
 */
function Countdown(options) {
    'use strict';

    var timer;
    var instance = this;
    var seconds = options.seconds;
    var updateStatus = options.onUpdateStatus;
    var counterEnd = options.onCounterEnd;

    function decrementCounter() {
        updateStatus(seconds);
        if (seconds === 0) {
            counterEnd();
            instance.stop();
        }
        seconds--;
    }

    /**
     * Start timer
     */
    this.start = function () {
        clearInterval(timer);
        seconds = options.seconds;
        timer = setInterval(decrementCounter, 1000);
    };

    /**
     * Stop timer
     */
    this.stop = function () {
        clearInterval(timer);
    };
}
