/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */


/**
 * Little simple coutdowntimer with 1000ms steps
 *
 * @param options dictionary with seconds, onUpdateStatus and onCounterEnd as functions
 * @constructor
 */
function Countdown(options) {
	let timer;
	const instance = this;
	let seconds = options.seconds;
	const updateStatus = options.onUpdateStatus;
	const counterEnd = options.onCounterEnd;
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