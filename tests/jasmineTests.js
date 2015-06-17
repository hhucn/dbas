describe("A suite", function() {
	it("contains spec with an expectation", function() {
		expect(true).toBe(true);
	});
});

describe("A suite is just a function", function() {
	var a;
	it("and so is a spec", function() {
		a = true;
		expect(a).toBe(true);

	});
});


describe("The 'toBe' matcher compares with ===", function() {
	it("and has a positive case", function() {
		expect(true).toBe(true);
	});
	it("and can have a negative case", function() {
		expect(false).not.toBe(true);
	});
});


describe('Array', function(){
	describe('#indexOf()', function(){
		it('should return -1 when the value is not present', function(){
			expect(-1).toBe([1,2,3].indexOf(5));
			expect(-1).toBe([1,2,3].indexOf(0));
		})
	})
});


describe("mocking ajax", function() {
	describe("suite wide usage", function() {
		beforeEach(function() {
			jasmine.Ajax.install();
		});
		afterEach(function() {
			jasmine.Ajax.uninstall();
		});

		it("specifying response when you need it", function() {
			var doneFn = jasmine.createSpy("success");
			var xhr = new XMLHttpRequest();
			xhr.onreadystatechange = function(args) {
				if (this.readyState == this.DONE) {
					doneFn(this.responseText);
				}
			};

			xhr.open("GET", "/some/cool/url");
			xhr.send();
			expect(jasmine.Ajax.requests.mostRecent().url).toBe('/some/cool/url');
			expect(doneFn).not.toHaveBeenCalled();
			jasmine.Ajax.requests.mostRecent().respondWith({
				"status": 200,
				"contentType": 'text/plain',
				"responseText": 'awesome response'
			});
			expect(doneFn).toHaveBeenCalledWith('awesome response');
		});
		it("allows responses to be setup ahead of time", function () {
			var doneFn = jasmine.createSpy("success");
			jasmine.Ajax.stubRequest('/another/url').andReturn({
				"responseText": 'immediate response'
			});
			var xhr = new XMLHttpRequest();
			xhr.onreadystatechange = function(args) {
				if (this.readyState == this.DONE) {
					doneFn(this.responseText);
				}
			};

			xhr.open("GET", "/another/url");
			xhr.send();

			expect(doneFn).toHaveBeenCalledWith('immediate response');
		});
  });

	it("allows use in a single spec", function() {
		var doneFn = jasmine.createSpy('success');
		jasmine.Ajax.withMock(function() {
			var xhr = new XMLHttpRequest();
			xhr.onreadystatechange = function(args) {
				if (this.readyState == this.DONE) {
					doneFn(this.responseText);
				}
			};

			xhr.open("GET", "/some/cool/url");
			xhr.send();

			expect(doneFn).not.toHaveBeenCalled();

			jasmine.Ajax.requests.mostRecent().respondWith({
				"status": 200,
				"responseText": 'in spec response'
			});

			expect(doneFn).toHaveBeenCalledWith('in spec response');
		});
	});
});