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

		var w = startLowerCase ? 'wrong' : 'Wrong',
			r = startLowerCase ? 'right' : 'Right',
			enddot = endWithDot ? '.' : '',
			belCounterJusti = 'believe that this is a good counter-argument for my justification',
			undermine = '<b>' + w + ', it is not true that ' + premisse + '</b>' + enddot,
			support	  = '<b>' + r + ', it is true that ' + premisse + '</b>' + enddot,
			undercut  = '<b>' + r + ', ' + premisse + '</b>, and I do not ' + belCounterJusti + enddot, // <b>' + conclusion + '</b>' + enddot,
			overbid	  = '<b>' + r + ', ' + premisse + '</b>, and I do ' + belCounterJusti + enddot, // <b>' + conclusion + '</b>' + enddot,
			rebut	  = '<b>' + r + ', ' + premisse + '</b> and I do accept that this is an counter-argument for <b>' + conclusion
				+ '</b>. However, I have a much stronger argument for accepting that <b>' + conclusion + '</b>' + enddot;
		return [undermine, support, undercut, overbid, rebut];
	};

	/**
	 * Returns all kinds of attacks for the given confrontation and conclusion
	 * @param confrontation current confrontation
	 * @param conclusion current conclusion
	 * @param startLowerCase, true, when each sentences should start as lowercase
	 * @param endWithDot, true, when each sentences should end with a dot
	 * @returns {*[]} with [undermine, support, undercut, overbid, rebut]
	 */
	this.createConfrontationsRelationsText = function(confrontation, conclusion, startLowerCase, endWithDot){

		if (conclusion.substr(conclusion.length-1) == ".")
			conclusion = conclusion.substr(0, conclusion.length-1);

		var w = startLowerCase ? 'wrong' : 'Wrong',
			r = startLowerCase ? 'right' : 'Right',
			enddot = endWithDot ? '.' : '',
			belCounterJusti = 'believe that this is a good counter-argument for my justification',
			undermine = w + ', it is not true that <b>' + confrontation + '</b>' + enddot,
			support	  = r + ', it is true that <b>' + confrontation + '</b>' + enddot,
			undercut  = r + ', <b>' + confrontation + '</b>, and I do not ' + belCounterJusti + enddot, // <b>' + conclusion + '</b>' + enddot,
			overbid	  = r + ', <b>' + confrontation + '</b>, and I do ' + belCounterJusti + enddot, // <b>' + conclusion + '</b>' + enddot,
			rebut	  = r + ', <b>' + confrontation + '</b> and I do accept that this is an counter-argument for <b>' + conclusion
				+ '</b>. However, I have a much stronger argument for accepting that <b>' + conclusion + '</b>' + enddot;
		return [undermine, support, undercut, overbid, rebut];
	};

	/**
	 * Creates an input element tih key as id and val as value. This is embedded in an li element
	 * @param key will be used as id
	 * @param val will be used as value
	 * @param isStartStatement if true, argumentButtonWasClicked is used, otherwise
	 * @param isPremisse
	 * @param isRelation
	 * @param mouseover
	 * @returns {Element|*} a type-input element in a li tag
	 */
	this.getKeyValAsInputInLiWithType = function (key, val, isStartStatement, isPremisse, isRelation, mouseover) {
		var liElement, inputElement, labelElement;
		liElement = $('<li>');
		liElement.attr({id: 'li_' + key});

		inputElement = $('<input>');
		inputElement.attr({id: key, type: 'radio', value: val});
		//inputElement.attr({data-dismiss: 'modal'});

		inputElement.attr({name: radioButtonGroup});
		// adding label for the value
		labelElement = '<label title="' + mouseover + '" for="' + key + '">' + val + '</label>';

		inputElement.attr({onclick: "new InteractionHandler().radioButtonChanged(this.id);"});
		if (isStartStatement){ inputElement.addClass('start'); }
		if (isPremisse){ inputElement.addClass('premisse'); }
		if (isRelation){ inputElement.addClass('relation'); }
		if (!isStartStatement && !isPremisse && !isRelation){ inputElement.addClass('add'); }

		liElement.html(new Helper().getFullHtmlTextOf(inputElement) + labelElement);

		return liElement;
	};
}