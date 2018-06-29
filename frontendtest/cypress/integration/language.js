const url = Cypress.env('WEB_PROTOCOL') + '://' + Cypress.env('WEB_HOST') + ':' + Cypress.env('WEB_PORT');

function switch_language(from, to) {
    cy.reload()
        .getCookie('_LOCALE_')
        .should('have.property', 'value', from);
    cy.get('#link-trans-' + to + ' > .language_selector_img')
        .click();
    cy.get('#confirm-dialog-accept-btn')
        .then(($btn) => {
            if ($btn) {
                $btn.click();
            }
        });
    cy.reload()
        .getCookie('_LOCALE_')
        .should('have.property', 'value', to);
}

describe('Test language at /', function () {
    beforeEach('Visit /', function () {
        cy.visit(url);
        cy.setCookie('_LOCALE_', 'de')
            .reload();
    });
    it('switches from german to english', function () {
        switch_language('de', 'en');
    });
    it('switch from german to english to german', function () {
        switch_language('de', 'en');
        switch_language('en', 'de');
    });
});

describe('Test language at /discussion', function () {
    beforeEach('Visit /', function () {
        cy.visit(url + '/discuss');
        cy.setCookie('_LOCALE_', 'de')
            .reload();
    });
    it('switches from german to english', function () {
        switch_language('de', 'en');
    });
    it('switches from german to english to german', function () {
        switch_language('de', 'en');
        switch_language('en', 'de');
    });
});
