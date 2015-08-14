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
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut]
	 */
	this.createRelationsText = function(premisse, conclusion){
		var undermine	= 'Wrong, it is not true that ' + premisse + '. [undermine]',
		support		= 'Right, it is true that ' + premisse + '. [support]',
		undercut	= 'Right, ' + premisse + ', but I do not believe that this is a good argument for ' + conclusion + '. [undercut]',
		overbid		= 'Right, ' + premisse + ', and I do believe that this is a good argument for ' + conclusion + '. [overbid]',
		rebut		= 'Right, ' + premisse + ' and I do accept that this is an argument for ' + conclusion
					+ '. However, I have a much stronger argument for rejecting that ' + conclusion + '. [rebut]';
		return [undermine, support, undercut, overbid, rebut];
	}
}