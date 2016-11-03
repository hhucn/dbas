/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxGraphHandler(){
	
	/**
	 * Requests JSON-Object
	 * @param uid: current id in url
	 * @param adress: keyword in url
	 */
	this.getUserGraphData = function(uid, adress){
		var dataString;
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		var attack = '';
		var splitted = window.location.href.split('?')[0].split('/');
		if (splitted.indexOf('reaction') != -1)
			attack = splitted[splitted.indexOf('reaction') + 2];
		
		switch(adress){
			case 'attitude':
				dataString = {is_argument: 'false', is_attitude: 'true', is_reaction: 'false', is_position: 'false', uids: uid};
				break;
			case 'justify':
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', is_position: 'false', uids: JSON.stringify(uid)};
				break;
			case 'argument':
				dataString = {is_argument: 'true', is_attitude: 'false', is_reaction: 'true', is_position: 'false', uids: JSON.stringify(uid)};
				break;
			case 'position':
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', is_position: 'true', uids: JSON.stringify(uid)};
		}
		dataString['lang'] = $('#issue_info').data('discussion-language');
		dataString['attack'] = attack;
		$.ajax({
			url: 'ajax_get_user_with_same_opinion',
			type: 'POST',
			dataType: 'json',
			data: dataString,
			async: true,
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function (data) {
			new DiscussionBarometer().callbackIfDoneForGetDictionary(data, adress);
		}).fail(function () {
			new DiscussionBarometer().callbackIfFailForGetDictionary();
		});
	};

	/**
	 * Displays a graph of current discussion
	 */
	this.getDiscussionGraphData = function (url) {
		// TODO FIX CSRF
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			data: {issue: new Helper().getCurrentIssueId()}
		}).done(function (data) {
			new DiscussionGraph().callbackIfDoneForDiscussionGraph(data);
		}).fail(function () {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 *
	 * @param uid
     */
	this.getJumpDataForGraph = function (uid) {
		$.ajax({
			url: '/ajax_get_arguments_by_statement/' + uid,
			type: 'GET',
			dataType: 'json',
			async: true
		}).done(function (data) {
			new DiscussionGraph().callbackIfDoneForGetJumpDataForGraph(data);
		}).fail(function () {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
}
