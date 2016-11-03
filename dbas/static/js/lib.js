/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */


/**
 * Swaps the element with the parameter
 * @param from element
 * @param to element
 * @returns {*}
 */
function swapElements (from, to) {
    var copy_to = $(to).clone(true),
	    copy_from = $(from).clone(true);
	$(to).replaceWith(copy_from);
	$(from).replaceWith(copy_to);
}

/**
 * Delays a specific function
 */
function delay (){
	var timer = 0;
	return function(callback, ms){
		clearTimeout (timer);
		timer = setTimeout(callback, ms);
	}();
}

