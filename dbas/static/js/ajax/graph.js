function AjaxGraphHandler() {
    'use strict';

    /**
     * Requests JSON-Object
     * @param uid_array: current id in url
     * @param address: keyword in url
     */
    this.getUserGraphData = function (uid_array, address) {
        var data = {
            is_argument: false,
            is_attitude: false,
            is_reaction: false,
            is_position: false,
            uids: uid_array,
            lang: getDiscussionLanguage()
        };

        switch (address) {
            case 'attitude':
                data.is_attitude = true;
                break;
            case 'justify':
                break;
            case 'argument':
            case 'dont_know':
                data.is_argument = true;
                data.is_reaction = true;
                break;
            case 'position':
                data.is_position = true;
                break;
            default:
                setGlobalErrorHandler(_t_discussion(ohsnap), _t_discussion(requestFailed));
                return;
        }

        var url = 'get_user_with_same_opinion';

        var done = function getUserGraphDataDone(data) {
            new DiscussionBarometer().callbackIfDoneForGetDictionary(data, address);
        };
        var fail = function getUserGraphDataFail(data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', data, done, fail);
    };

    /**
     *
     * Displays a graph of current discussion
     *
     * @param context
     * @param uid
     * @param is_argument
     * @param show_partial_graph
     */
    this.getDiscussionGraphData = function (context, uid, is_argument, show_partial_graph) {
        var inputdata = {
            'path': window.location.href,
            'issue': $('#issue_info').data('issue')
        };
        var request_for_complete = uid === null || !show_partial_graph;
        var url;

        if (request_for_complete) {
            url = '/graph/complete';
        } else {
            url = '/graph/partial';
            inputdata.uid = parseInt(uid);
            inputdata.is_argument = is_argument;
        }

        var done = function (d) {
            context.callbackIfDoneForDiscussionGraph(d);
            new GuiHandler().setDisplayStyleAsGraphView();
        };
        var fail = function (data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', inputdata, done, fail);
    };

    /**
     *
     * @param uid
     */
    this.getJumpDataForGraph = function (uid) {
        var url = '/get_arguments_by_statement/' + uid;
        var issue_uid = $('#issue_info').data('issue');
        var done = function (data) {
            new DiscussionGraph({}, false).callbackIfDoneForGetJumpDataForGraph(data);
        };
        var fail = function (data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', {'issue': issue_uid}, done, fail);
    };
}
