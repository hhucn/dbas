'use strict';

var assert = require('assert');
var expect = require('chai').expect;
var should = require('chai').should();


describe('Array', function(){
	describe('#indexOf()', function(){
		it('should return -1 when the value is not present', function(){
			assert.equal(-1, [1,2,3].indexOf(5));
			assert.equal(-1, [1,2,3].indexOf(0));
		})
	})
});

describe('addition', function () {
	it('should add 1+1 correctly', function (done) {
		var onePlusOne = 1 + 1;
		assert.equal(2, onePlusOne);
		done();
	});
	it('should add 1+2 correctly', function (done) {
		var onePlusOne = 1 + 2;
		expect(4+5).equal(9);
		done();
	});
});


describe('MyAPI', function() {
    beforeEach(function() {
        this.xhr = sinon.useFakeXMLHttpRequest();

        this.requests = [];
        this.xhr.onCreate = function(xhr) {
            this.requests.push(xhr);
        }.bind(this);
    });

    afterEach(function() {
        this.xhr.restore();
    });


    //Tests etc. go here
});