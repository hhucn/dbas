/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function Helper() {

	this.getATagForDropDown = function (id, title, text) {
		var a = $('<a>');
		a.attr('id', id);
		a.attr('role', 'menuitem');
		a.attr('tabindex', '-1');
		a.attr('data-toggle', 'modal');
		a.attr('title', title);
		a.attr('href', '#');
		a.text(text);
		return a
	};

	/**
	 *
	 * @param premisse
	 * @param conclusion
	 * @param startLowerCase
	 * @param endWithDot
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut]
	 */
	this.createRelationsText = function(premisse, conclusion, startLowerCase, endWithDot){
		if (premisse.substr(premisse.length-1) == ".")
			premisse = premisse.substr(0, premisse.length-1);

		if (conclusion.substr(conclusion.length-1) == ".")
			conclusion = conclusion.substr(0, conclusion.length-1);

		var undermine = (startLowerCase ? 'w' : 'W') + 'rong, it is not true that ' + premisse + (endWithDot ? '.' : '') + ' [undermine]',
		support	= (startLowerCase ? 'r' : 'R') + 'ight, it is true that ' + premisse + (endWithDot ? '.' : '') + ' [support]',
		undercut= (startLowerCase ? 'r' : 'R') + 'ight, ' + premisse + ', but I do not believe that this is a good argument for '
			+ conclusion + (endWithDot ? '.' : '') + ' [undercut]',
		overbid	= (startLowerCase ? 'r' : 'R') + 'ight, ' + premisse + ', and I do believe that this is a good argument for '
			+ conclusion + (endWithDot ? '.' : '') + ' [overbid]',
		rebut	= (startLowerCase ? 'r' : 'R') + 'ight, ' + premisse + ' and I do accept that this is an argument for '
			+ conclusion + '. However, I have a much stronger argument for rejecting that ' + conclusion + (endWithDot ? '.' : '') + ' [rebut]';
		return [undermine, support, undercut, overbid, rebut];
	}
}