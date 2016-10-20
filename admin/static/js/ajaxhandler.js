/**
 * Created by tobias on 20.10.16.
 */

function AdminAjaxHandler(){
	
	/**
	 *
	 * @param uid
	 */
	this.deleteSomething = function(uid){
		console.log('ajax delete ' + uid);
		new AdminCallbackHandler().doSomething();
	};
	
	/**
	 *
	 * @param uid
	 */
	this.saveSomething = function(uid){
		console.log('ajax save ' + uid);
		new AdminCallbackHandler().doSomething(uid);
	}
}

function AdminCallbackHandler(){
	
	/**
	 *
	 */
	this.doSomething = function(uid){
		console.log('callback ' + uid);
	}
}