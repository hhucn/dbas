const url = Cypress.env('WEB_PROTOCOL') + "://" + Cypress.env("WEB_HOST") + ":" + Cypress.env("WEB_PORT");
const valid_user = 'Bob';
const valid_pw = 'iamatestuser2016';
const invalid_position = 'coconut';
const invalid_reason = 'cocofruit';
const valid_position = 'coconuts are awesome';
const valid_reason = 'they have hairs';

function login(user, pw) {
    cy.get('#login-user')
        .type(user);
    cy.get('#login-pw')
        .type(pw);
    cy.get('#popup-login-button-login')
        .click();
}

function randomString(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < length; i++)
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function lowercaseFirstLetter(string) {
    return string.charAt(0).toLowerCase() + string.slice(1);
}

function diff(should, str) {
    return should - str.length;
}

function input_not_enough_msg(str) {
    return diff(10, str) + ' more to go';
}

function remaining_input_msg(str) {
    return diff(180, str) + ' characters left';
}

function no_input_msg() {
    return 'Enter at least 10 characters';
}


describe('Test if not logged in user can not contribute', function () {
    it('checks if cat-or-dog denies contribution', function () {
        cy.visit(url + '/discuss');
        cy.get('tbody:first > :nth-child(1) > :nth-child(1) > a')
            .click();
        cy.get('#confirm-dialog-refuse-btn')
            .click();
        cy.get('#item_login')
            .should('exist');
    });
    it('checks if the contribution is really disabled', function () {
        cy.get('#item_2')
            .click();
        cy.get('#confirm-dialog-refuse-btn')
            .click();
        cy.get('#item_disagree')
            .click();
        cy.get('#item_login')
            .should('exist');
    });
});

describe('Test if user can login and can contribute', function () {
    var position = randomString(10);
    var reason = randomString(10);
    var disagreement = randomString(10);
    var premise = randomString(10);

    beforeEach('checks if a user can login and contribute', function () {
        cy.visit(url + '/discuss');
        cy.get('tbody:first > :nth-child(1) > :nth-child(1) > a')
            .click();
        cy.get('#confirm-dialog-refuse-btn')
            .click();
        cy.get('#item_login')
            .should('exist')
            .click();
        login(valid_user, valid_pw);
        cy.get('#item_login')
            .should('not.exist');
        cy.get('#item_start_statement')
            .should('exist');
    });
    it('checks if new position can be contributed', function () {
        cy.get('#item_start_statement').click();
        cy.get('#add-statement-container-main-input-position').type(position);
        cy.get('#add-statement-container-main-input-reason').type(reason);
        cy.get('#send-new-statement').click({force: true});
        cy.contains(capitalizeFirstLetter(position));
        cy.contains(lowercaseFirstLetter(reason));
    });
    it('checks if an user can disagree to new position', function () {
        cy.contains(position).click();
        cy.get('#item_disagree').click();
        cy.get('#add-position-container-main-input').type(disagreement);
        cy.get('#send-new-position').click();
        cy.contains(capitalizeFirstLetter(position));
        cy.contains(lowercaseFirstLetter(disagreement));
    });
    it('checks if an user can agree to new position and adds premise', function () {
        cy.contains(position).click();
        cy.get('#item_agree').click();
        cy.contains(reason);
        cy.get('#item_start_premise').click();
        cy.get('#add-position-container-main-input').type(premise);
        cy.get('#send-new-position').click();
        cy.contains(capitalizeFirstLetter(position));
        cy.contains(lowercaseFirstLetter(premise));
    });

});

describe('Test for leaks while adding new statements', function () {
    before(function () {
        cy.visit(url + '/discuss');
        cy.get('tbody:first > :nth-child(1) > :nth-child(1) > a')
            .click();
        cy.get('#confirm-dialog-refuse-btn')
            .click();
        cy.get('#item_login')
            .should('exist')
            .click();
        login(valid_user, valid_pw);

        cy.get('#item_login')
            .should('not.exist');
        cy.get('#item_start_statement')
            .should('exist')
            .click();
    });
    afterEach(function () {
        cy.get('#add-statement-container-main-input-position')
            .clear();
        cy.get('#add-statement-container-main-input-reason')
            .clear();
    });
    it('writes no position and no reason ', function () {
        cy.get('#add-statement-container-main-input-position-text-counter')
            .should('be.visible')
            .contains(no_input_msg());
        cy.get('#add-statement-container-main-input-reason-text-counter')
            .should('be.visible')
            .contains(no_input_msg());
    });
    it('writes an valid position and no reason', function () {

        cy.get('#add-statement-container-main-input-position')
            .type(valid_position);
        var remaining = remaining_input_msg(valid_position);
        cy.get('#add-statement-container-main-input-position-text-counter')
            .should('be.visible')
            .contains(remaining);
        cy.get('#add-statement-container-main-input-reason-text-counter')
            .should('be.visible')
            .contains(no_input_msg());
    });
    it('writes an invalid position and an valid reason', function () {
        cy.get('#add-statement-container-main-input-position')
            .type(invalid_position);
        cy.get('#add-statement-container-main-input-reason')
            .type(valid_reason);
        var remaining = remaining_input_msg(valid_reason);
        var not_enough = input_not_enough_msg(invalid_position);
        cy.get('#add-statement-container-main-input-position-text-counter')
            .should('be.visible')
            .contains(not_enough);
        cy.get('#add-statement-container-main-input-reason-text-counter')
            .should('be.visible')
            .contains(remaining);
    });
    it('writes an invalid position and an invalid reason', function () {
        cy.get('#add-statement-container-main-input-position')
            .type(invalid_position);
        cy.get('#add-statement-container-main-input-reason')
            .type(invalid_reason);
        var not_enough_p = input_not_enough_msg(invalid_position);
        var not_enough_r = input_not_enough_msg(invalid_reason);
        cy.get('#add-statement-container-main-input-position-text-counter')
            .should('be.visible')
            .contains(not_enough_p);
        cy.get('#add-statement-container-main-input-reason-text-counter')
            .should('be.visible')
            .contains(not_enough_r);
    });
    it('writes no position and an valid reason', function () {
        cy.get('#add-statement-container-main-input-reason')
            .type(valid_reason);
        var remaining = remaining_input_msg(valid_reason);
        cy.get('#add-statement-container-main-input-reason-text-counter')
            .should('be.visible')
            .contains(remaining);
        cy.get('#add-statement-container-main-input-position-text-counter')
            .should('be.visible')
            .contains(no_input_msg());
    });
    it('writes no position and an invalid reason', function () {
        cy.get('#add-statement-container-main-input-reason')
            .type(invalid_reason);
        var not_enough = input_not_enough_msg(invalid_reason);
        cy.get('#add-statement-container-main-input-reason-text-counter')
            .should('be.visible')
            .contains(not_enough);
        cy.get('#add-statement-container-main-input-position-text-counter')
            .should('be.visible')
            .contains(no_input_msg());
    });
    it('writes an invalid position and no reason ', function () {
        cy.get('#add-statement-container-main-input-position')
            .type(invalid_position);
        var remaining = diff(10, invalid_position) + ' more to go ...';
        cy.get('#add-statement-container-main-input-position-text-counter')
            .should('be.visible')
            .contains(remaining);
        cy.get('#add-statement-container-main-input-reason-text-counter')
            .should('be.visible')
            .contains(no_input_msg());
    });
    it('writes an valid position and an invalid reason', function () {
        cy.get('#add-statement-container-main-input-position')
            .type(valid_position);
        cy.get('#add-statement-container-main-input-reason')
            .type(invalid_reason);
        var remaining = remaining_input_msg(valid_position);
        var not_enough = input_not_enough_msg(invalid_reason);
        cy.get('#add-statement-container-main-input-position-text-counter')
            .should('be.visible')
            .contains(remaining);
        cy.get('#add-statement-container-main-input-reason-text-counter')
            .should('be.visible')
            .contains(not_enough);
    });
});
