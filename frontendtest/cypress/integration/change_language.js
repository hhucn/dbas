const url = Cypress.env('WEB_PROTOCOL') + "://" + Cypress.env("WEB_HOST") + ":" + Cypress.env("WEB_PORT");

function switch_language(from, to) {
    cy.reload()
        .getCookie('_LOCALE_')
        .should('have.property', 'value', from);
    cy.get('#link-trans-' + to + ' > .language_selector_img')
        .click();
    cy.reload()
        .getCookie('_LOCALE_')
        .should('have.property', 'value', to);
}


describe('Test language at /', function () {
    beforeEach('Visit /', function () {
        cy.visit(url);
        cy.setCookie('_LOCALE_', 'de')
            .reload();
        cy.getCookies()
            .reload()
            .should('have.length', 2);
    });
    it('Switch from german to english', function () {
        switch_language('de', 'en');
    });
    it('Switch from german to english to german', function () {
        switch_language('de', 'en');
        switch_language('en', 'de');
    });
});

describe('Switch language at /discussion', function () {
    it('Switch from german to english', function () {
        cy.get('.btn-group > .btn-default')
            .click();
        cy.getCookie('_LOCALE_')
            .should('have.property', 'value', 'en');
        cy.get('#link-trans-de')
            .click();
        cy.get('#confirm-dialog-accept-btn')
            .click();
        cy.getCookie('_LOCALE_')
            .should('have.property', 'value', 'de');
    });
});
