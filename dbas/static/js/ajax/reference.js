/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function AjaxReferenceHandler() {
    'use strict';

    /**
     *
     * @param uid
     * @param reference
     * @param ref_source
     * @param issue
     */
    this.setReference = function (uid, reference, ref_source, issue) {
        var url = 'set_references';
        var d = {
            statement_id: uid,
            ref_source: ref_source,
            text: reference,
            issue: issue,
        };
        var done = function () {
            setGlobalSuccessHandler('Yeah!', _t_discussion(dataAdded));
            $('#' + popupReferences).modal('hide');
        };
        var fail = function (data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };

    /**
     *
     * @param uids
     * @param is_argument
     */
    this.getReferences = function (uids, is_argument) {
        var url = 'get_references';
        var d = {
            'uids': uids,
            'is_argument': is_argument
        };
        var done = function (data) {
            new PopupHandler().showReferencesPopup(data);
        };
        var fail = function (data) {
            setGlobalErrorHandler(_t_discussion(ohsnap), data.responseJSON.errors[0].description);
        };
        ajaxSkeleton(url, 'POST', d, done, fail);
    };
}
