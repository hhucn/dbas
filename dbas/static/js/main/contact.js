/**
 * @author Tobias Krauthoff <krauthoff@cs.uni-duesseldorf.de>
 */

function setContactLoading(){
    'use strict';
	$('#' + contactSubmitButtonId).click(function(){
		$('.ajaxloader').show();
	});
}

$(document).ready(function () {
    'use strict';
    setContactLoading();
});
