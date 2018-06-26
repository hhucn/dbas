const url = Cypress.env('WEB_PROTOCOL') + "://" + Cypress.env("WEB_HOST") + ":" + Cypress.env("WEB_PORT");
var buttons = ['about', 'requirements', 'services', 'github', 'partners', 'news', 'contact'];

function set_cookie_to(language) {
    cy.setCookie('_LOCALE_', 'en');
    cy.getCookie('_LOCALE_').should('have.property', 'value', 'en');
}

function test_for_element_to_be_clickable(arr) {
    for (var i = 0; i < arr.length; i++) {
        cy.get('#' + arr[i])
            .should('exist')
            .should('be.visible')
            .click();
    }
}

describe('Test if content is visible with english language', function () {
    beforeEach('Set language to english', function () {
        cy.visit(url);
        set_cookie_to('en');
    });
    it('checks for present buttons at /', function () {
        test_for_element_to_be_clickable(buttons);
    });
});
describe('Test if content is visible with german language', function () {
    beforeEach('Set language to german', function () {
        cy.visit(url);
        set_cookie_to('de');
    });
    it('checks for present buttons at /', function () {
        test_for_element_to_be_clickable(buttons);
    });
});