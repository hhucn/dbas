/**
 * @author Tobias Krauthoff
 * @email krauthoff@cs.uni-duesseldorf.de
 */

function AjaxGraphHandler(){
	
	/**
	 * Requests JSON-Object
	 * @param uid: current id in url
	 * @param address: keyword in url
	 */
	this.getUserGraphData = function(uid, address){
		var dataString;
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		
		switch(address){
			case 'attitude':
				dataString = {is_argument: 'false', is_attitude: 'true', is_reaction: 'false', is_position: 'false', uids: uid};
				break;
			case 'justify':
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', is_position: 'false', uids: JSON.stringify(uid)};
				break;
			case 'argument':
			case 'dont_know':
				dataString = {is_argument: 'true', is_attitude: 'false', is_reaction: 'true', is_position: 'false', uids: JSON.stringify(uid)};
				break;
			case 'position':
				dataString = {is_argument: 'false', is_attitude: 'false', is_reaction: 'false', is_position: 'true', uids: JSON.stringify(uid)};
				break;
			default:
				setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
				return;
		}
		
		dataString['lang'] = $('#issue_info').data('discussion-language');
		$.ajax({
			url: 'ajax_get_user_with_same_opinion',
			type: 'POST',
			dataType: 'json',
			data: dataString,
			async: true,
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function (data) {
			new DiscussionBarometer().callbackIfDoneForGetDictionary(data, address);
		}).fail(function () {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};

	/**
	 * Displays a graph of current discussion
	 */
	this.getDiscussionGraphData = function (url) {
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: url,
			type: 'GET',
			dataType: 'json',
			data: {issue: getCurrentIssueId(), path: window.location.href},
			headers: {'X-CSRF-Token': csrf_token}
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
		var csrf_token = $('#' + hiddenCSRFTokenId).val();
		$.ajax({
			url: '/ajax_get_arguments_by_statement/' + uid,
			type: 'GET',
			dataType: 'json',
			async: true,
			headers: {'X-CSRF-Token': csrf_token}
		}).done(function (data) {
			new DiscussionGraph().callbackIfDoneForGetJumpDataForGraph(data);
		}).fail(function () {
			setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
		});
	};
}
