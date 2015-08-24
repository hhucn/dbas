/*global $, jQuery, alert*/

/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 * @copyright Krauthoff 2015
 */

function Helper() {

	/**
	 *
	 * @param id
	 * @param title
	 * @param text
	 * @returns {jQuery|HTMLElement}
	 */
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
	 * Return the full HTML text of an given element
	 * @param element which should be translated
	 */
	this.getFullHtmlTextOf = function (element) {
		return $('<div>').append(element).html();
	};

	/**
	 *
	 * @param text
	 * @returns {string}
	 */
	this.startWithLowerCase = function (text){
		return text.substr(0, 1).toLowerCase() + text.substr(1);
	};

	/**
	 * Returns all kinds of attacks for the given premisse and conclusion
	 * @param premisse current premisses
	 * @param conclusion current conclusion
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @param endWithDot, true, when each sentences should end with a dot
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut]
	 */
	this.createRelationsText = function(premisse, conclusion, startLowerCase, endWithDot){
		if (premisse.substr(premisse.length-1) == ".")
			premisse = premisse.substr(0, premisse.length-1);

		if (conclusion.substr(conclusion.length-1) == ".")
			conclusion = conclusion.substr(0, conclusion.length-1);

		var w = startLowerCase ? 'w' : 'W', r = startLowerCase ? 'r' : 'R', enddot = endWithDot ? '.' : '',
			undermine = '<b>' + w + 'rong, it is not true that \'' + premisse + '\'</b>' + enddot,
			support	  = '<b>' + r + 'ight, it is true that \'' + premisse + '\'</b>' + enddot,
			undercut  = '<b>' + r + 'ight, \'' + premisse + '\'</b>, but I do not believe that this is a good counter-argument for my justification.',
				// <b>\'' + conclusion + '\'</b>' + enddot,
			overbid	  = '<b>' + r + 'ight, \'' + premisse + '\'</b>, and I do believe that this is a good counter-argument for my justification.',
				// <b>\'' + conclusion + '\'</b>' + enddot,
			rebut	  = '<b>' + r + 'ight, \'' + premisse + '\'</b> and I do accept that this is an counter-argument for <b>\'' + conclusion
				+ '\'</b>. However, I have a much stronger argument for accepting that <b>\'' + conclusion + '\'</b>' + enddot;
		return [undermine, support, undercut, overbid, rebut];
	};

	/**
	 *
	 * @param confrontation
	 * @param premisse
	 * @param conclusion
	 * @param startLowerCase
	 * @param endWithDot
	 * @returns {*[]}
	 */
	this.createConfrontationsRelationsText = function(confrontation, premisse, conclusion, startLowerCase, endWithDot){
		if (premisse.substr(premisse.length-1) == ".")
			premisse = premisse.substr(0, premisse.length-1);

		if (conclusion.substr(conclusion.length-1) == ".")
			conclusion = conclusion.substr(0, conclusion.length-1);

		if (premisse.substr(premisse.length-1) == ".")
			premisse = premisse.substr(0, premisse.length-1);

		var w = startLowerCase ? 'w' : 'W', r = startLowerCase ? 'r' : 'R', enddot = endWithDot ? '.' : '',
			undermine = w + 'rong, it is not true that <b>\'' + confrontation + '\'</b>' + enddot,
			support	  = r + 'ight, it is true that <b>\'' + confrontation + '\'</b>' + enddot,
			undercut  = r + 'ight, <b>\'' + confrontation + '\'</b>, but I do not believe that this is a good counter-argument for my justification.',
				// <b>\'' + conclusion + '\'</b>' + enddot,
			overbid	  = r + 'ight, <b>\'' + confrontation + '\'</b>, and I do believe that this is a good counter-argument for my justification.',
				// <b>\'' + conclusion + '\'</b>' + enddot,
			rebut	  = r + 'ight, <b>\'' + confrontation + '\'</b> and I do accept that this is an counter-argument for <b>\'' + conclusion
				+ '\'</b>. However, I have a much stronger argument for accepting that <b>\'' + conclusion + '\'</b>' + enddot;
		return [undermine, support, undercut, overbid, rebut];
	};
}