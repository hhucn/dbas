const url = Cypress.env('WEB_PROTOCOL') + '://' + Cypress.env('WEB_HOST') + ':' + Cypress.env('WEB_PORT');
const valid_user = 'Bob';
const valid_pw = 'iamatestuser2016';
const invalid_user = 'August Engelhardt';
const invalid_pw = 'Kokosnuss';

function login(user, pw) {
    cy.get('#link_popup_login')
        .click();
    cy.get('#login-user')
        .type(user);
    cy.get('#login-pw')
        .type(pw);
    cy.get('#popup-login-button-login')
        .click();
}

beforeEach('Visit /discuss', function () {
    cy.visit(url + '/discuss');
});

describe('Test if login activates user menu', function () {
    it('checks if user menu is visible', function () {
        cy.get('#user-menu-dropdown')
            .should('not.exist');
        login(valid_user, valid_pw);
        cy.get('#user-menu-dropdown')
            .should('exist');
        cy.get('#user-menu-dropdown')
            .should('contain', valid_user);
    });
});

describe('Test if user can logout', function () {
    it('checks if the user menu is disables if the user is logged out', function () {
        cy.get('#user-menu-dropdown')
            .should('not.exist');
        login(valid_user, valid_pw);
        cy.get('#user-menu-dropdown')
            .should('exist');
        cy.get('#user-menu-dropdown')
            .should('contain', valid_user);
        cy.get('#user-menu-dropdown')
            .click();
        cy.get('#logout-link')
            .click();
        cy.get('#user-menu-dropdown')
            .should('not.exist');
    });
});

describe('Test if invalid user cant login', function () {
    it('checks if a invalid user can not login', function () {
        cy.get('#user-menu-dropdown')
            .should('not.exist');
        login(invalid_user, invalid_pw);
        cy.get('#popup-login-failed')
            .should('exist');
    });
});

describe('Test if invalid user can not use user menu', function () {
    it('checks if a invalid user has no user menu', function () {
        cy.get('#user-menu-dropdown')
            .should('not.exist');
        login(invalid_user, invalid_pw);
        cy.get('#popup-login-failed')
            .should('exist');
        cy.get('#popup-login-close-button2')
            .click();
        cy.get('#user-menu-dropdown')
            .should('not.exist');
    });
});
