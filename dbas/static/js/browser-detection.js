/**
 * Created by tobias on 03.01.17.
 */

// http://stackoverflow.com/a/5918791/2648872
navigator.sayswho = (function(){
    var ua= navigator.userAgent, tem,
    M= ua.match(/(opera|chrome|safari|firefox|msie|trident(?=\/))\/?\s*(\d+)/i) || [];
    if(/trident/i.test(M[1])){
        tem=  /\brv[ :]+(\d+)/g.exec(ua) || [];
        return 'IE '+(tem[1] || '');
    }
    if(M[1]=== 'Chrome'){
        tem= ua.match(/\b(OPR|Edge)\/(\d+)/);
        if(tem!= null) return tem.slice(1).join(' ').replace('OPR', 'Opera');
    }
    M= M[2]? [M[1], M[2]]: [navigator.appName, navigator.appVersion, '-?'];
    if((tem= ua.match(/version\/(\d+)/i))!= null) M.splice(1, 1, tem[1]);
    return M.join(' ');
})();

/**
 * Sets data for the global sucess field
 */
function setGlobalErrorHandlerWithoutIds(){
    var heading = 'Ohh!';
    if ((navigator.language || navigator.userLanguage).indexOf('de') != -1){
        var body = 'Ihr Browser ist veraltet. D-BAS wird vermutlich nicht korrekt funtkionieren!';
    } else {
        var body = 'Your browser is out of date and D-BAS will not be executed correctly!';
    }
    $('#request_failed_container').fadeIn();
    $('#request_failed_container_close').click(function () {
        $('#request_failed_container').fadeOut();
    });
    $('#request_failed_container_heading').html(heading);
    $('#request_failed_container_message').html(body);
}

$(document).ready(function mainDocumentReady() {
	return;
	var splitted = navigator.sayswho.split(' ');
	var browser = splitted[0];
	var version = splitted[1];
	
	if (browser == 'Chrome' && version < 52
		|| browser == 'Safari' && version < 10
		|| browser == 'Firefox' && version < 47) {
		setTimeout(function () {
			setGlobalErrorHandlerWithoutIds();
		}, 1500);
	}
	
	if (browser == 'Safari' && version < 10) {
		setTimeout(function () {
			setGlobalErrorHandlerWithoutIds();
		}, 1500);
	}
});