const url = Cypress.env('WEB_PROTOCOL') + '://' + Cypress.env('WEB_HOST') + ':' + Cypress.env('WEB_PORT');
const valid_user = 'Bob';
const valid_pw = 'iamatestuser2016';
const invalid_position = 'coconut';
const invalid_reason = 'cocofruit';
const valid_position = 'coconuts are awesome';
const valid_reason = 'they have hairs';
const discussions = ['Cat or Dog', 'Make the world better',
    'Elektroautos', 'Unterstützung der Sekretariate', 'Read only Issue'];

function login(user, pw) {
    cy.get('#login-user')
        .type(user);
    cy.get('#login-pw')
        .type(pw);
    cy.get('#popup-login-button-login')
        .click({force: true});
}

function randomString(length) {
    var text = '';
    var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

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

function slugify(str) {
    return str.replace(/ /g, '-').toLowerCase();
}

describe('Test the functions while discussing', function () {

    const options = ['#labels', '#positions', '#statements', '#my-statements', '#supports-on-my-statements'];

    function visit_graph() {
        cy.get('#display-style-icon-graph-img')
            .should('exist')
            .click({force: true});
        cy.get('#confirm-dialog-refuse-btn')
            .click({force: true});
        cy.get('#circle-issue')
            .should('exist');
    }

    beforeEach(function () {
        cy.visit(url + '/discuss');
        cy.contains(discussions[0])
            .click({force: true});
        cy.get('#item_login')
            .should('exist')
            .should('have.property', 'onClick')
            .click({force: true});
        login(valid_user, valid_pw);
        cy.get('#item_start_statement')
            .should('exist')
            .click({force: true});
    });
    it('choose position and restart discussion', function () {
        cy.url()
            .should('eq', url + '/discuss/' + slugify(discussions[0]));
        cy.get('#discussion-restart-btn')
            .click({force: true});
        cy.url()
            .should('eq', url + '/discuss/' + slugify(discussions[0]));
    });

    it('add more then one reason', function () {
        cy.get('#item_2')
            .click({force: true});
        cy.get('#item_disagree')
            .click({force: true});
        cy.get('.icon-add-premise')
            .click({force: true});
        cy.get(':nth-child(2) > .flex-div')
            .should('exist');
        cy.get(':nth-child(2) > :nth-child(2) > .icon-add-premise')
            .click({force: true});
        cy.get(':nth-child(3) > .flex-div')
            .should('exist');
        cy.get(':nth-child(3) > :nth-child(2) > .icon-rem-premise')
            .click({force: true});
        cy.get(':nth-child(3) > .flex-div')
            .should('not.exist');
        cy.get(':nth-child(2) > :nth-child(2) > .icon-add-premise')
            .should('exist');
        cy.get(':nth-child(2) > :nth-child(2) > .icon-rem-premise')
            .click({force: true});
        cy.get('.icon-add-premise')
            .should('exist');
    });

    it('tests if the discussion can be shared', function () {
        cy.get('#share-url')
            .should('exist')
            .click({force: true});
        cy.get('#popup-url-sharing')
            .should('exist');
    });
    it('tests if the barometer can be used', function () {
        cy.get('#opinion-barometer-img')
            .should('exist')
            .click({force: true});
        cy.get('#barometer-popup')
            .should('exist');
    });
    it('tests if the graph can be used', function () {
        visit_graph();
    });
    it('tests all options of the graph', function () {
        visit_graph();
        for (var i = 0; i < options.length; i++) {
            cy.get(options[i])
                .click({force: true});
            if ('#labels' === options[i]) {
                cy.contains('we should get a cat');
            }
        }
    });
    it('tests if new statement is added to the graph', function () {
        const position = randomString(10);
        const reason = randomString(10);
        cy.get('#add-statement-container-main-input-position').type(position, {force: true});
        cy.get('#add-statement-container-main-input-reason').type(reason, {force: true});
        cy.get('#send-new-statement')
            .click({force: true});
        cy.visit(url + '/discuss');
        cy.contains(discussions[0])
            .click({force: true});
        visit_graph();
        cy.get(options[0])
            .click({force: true});
        cy.contains(position);
        cy.contains(reason);
    });
});

describe('Test if not logged in user can not contribute', function () {
    it('checks if every discussion denies contribution', function () {
        for (var i = 0; i < discussions.length; i++) {
            cy.visit(url + '/discuss');
            cy.contains(discussions[i])
                .click({force: true});
            cy.get('#item_login')
                .should('exist');
        }
    });

});

describe('Test if user can login and can contribute at ' + discussions[0], function () {
    var position = randomString(10);
    var reason = randomString(10);
    var disagreement = randomString(10);
    var premise = randomString(10);
    beforeEach('checks if a user can login and contribute', function () {
            cy.visit(url + '/discuss');
            cy.contains(discussions[0])
                .click({force: true});
            cy.get('#item_login')
                .should('exist')
                .click({force: true});
            login(valid_user, valid_pw);
            cy.get('#item_login')
                .should('not.exist');
            cy.get('#item_start_statement')
                .should('exist');
            cy.get('#confirm-dialog-refuse-btn')
                .then(($btn) => {
                    if ($btn) {
                        $btn.click({force: true});
                    }
                });
        }
    );

    it('checks if new position can be contributed', function () {
        cy.get('#item_start_statement').click({force: true});
        cy.get('#add-statement-container-main-input-position').type(position, {force: true});
        cy.get('#add-statement-container-main-input-reason').type(reason, {force: true});
        cy.get('#send-new-statement').click({force: true});

        cy.contains(capitalizeFirstLetter(position));
        cy.contains(lowercaseFirstLetter(reason));
    });
    it('checks if an user can disagree to new position', function () {
        cy.contains(position).click({force: true});
        cy.get('#item_disagree').click({force: true});
        cy.get('#add-position-container-main-input').type(disagreement, {force: true});
        cy.get('#send-new-position').click({force: true});

        cy.contains(capitalizeFirstLetter(position));
        cy.contains(lowercaseFirstLetter(disagreement));
    });
    it('checks if an user can agree to new position and adds premise', function () {
        cy.contains(position).click({force: true});
        cy.get('#item_agree').click({force: true});
        cy.contains(reason);
        cy.get('#item_start_premise').click({force: true});
        cy.get('#add-position-container-main-input').type(premise, {force: true});
        cy.get('#send-new-position').click({force: true});

        cy.contains(capitalizeFirstLetter(position));
        cy.contains(lowercaseFirstLetter(premise));
    });
});

describe('Test for leaks while adding new statements at ' + discussions[0], function () {
    beforeEach(function () {
        cy.visit(url + '/discuss');
        cy.contains(discussions[0])
            .click({force: true});
        cy.get('#item_login')
            .should('exist')
            .click({force: true});
        login(valid_user, valid_pw);
        cy.get('#item_login')
            .should('not.exist');
        cy.get('#item_start_statement')
            .should('exist')
            .click({force: true});
    });

    afterEach(function () {
        cy.get('#send-new-position').click({force: true});
        cy.get('#add-statement-error-container')
            .should('exist');
        cy.get('#add-statement-container-main-input-position')
            .clear({force: true});
        cy.get('#add-statement-container-main-input-reason')
            .clear({force: true});
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
            .type(valid_position, {force: true});
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
            .type(invalid_position, {force: true});
        cy.get('#add-statement-container-main-input-reason')
            .type(valid_reason, {force: true});
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
            .type(invalid_position, {force: true});
        cy.get('#add-statement-container-main-input-reason')
            .type(invalid_reason, {force: true});
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
            .type(valid_reason, {force: true});
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
            .type(invalid_reason, {force: true});
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
            .type(invalid_position, {force: true});
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
            .type(valid_position, {force: true});
        cy.get('#add-statement-container-main-input-reason')
            .type(invalid_reason, {force: true});
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

