const url = 'http://' + Cypress.env('WEB_HOST') + ':4284';
const valid_user = 'Bob';
const valid_pw = 'iamatestuser2016';


function login_via_popup(user, pw) {
    cy.get('#link_popup_login')
        .should('exist')
        .click();
    cy.get('#login-user')
        .type(user);
    cy.get('#login-pw')
        .type(pw);
    cy.get('#popup-login-button-login')
        .click();
}

function set_welcome_cookies() {
    cy.setCookie('PASSED_GUIDED_TOUR', 'true');
    cy.setCookie('EU_COOKIE_LAW_CONSENT', 'true');
    cy.setCookie('_LOCALE_', 'de');
}

function set_login_cookie() {
    cy.setCookie('auth_tkt', 'dc7a06e726ffed55229c431e70187195c7bc74421f676342a2d23fa9c8333d11089b61185a3c35a9521c0000b1ceb37cbe70172bee6978d04de793deb575b8385def56dfQm9i!userid_type:b64unicode');
}

describe('Login Test', function () {
    beforeEach(function () {
        set_welcome_cookies();
        cy.visit(url + '/discuss/');
    });
    it('Tries to log in with wrong password and it should fail', function () {
        login_via_popup(valid_user, "FooBarBaz");
        cy.get('#popup-login-failed').should('visible');
    });

    it('Tries to log in with correct password and succeeds', function () {
        login_via_popup(valid_user, valid_pw);
        cy.get('#popup-login-failed').should('not.visible');
    });
});


describe('Add Issue Test', function () {
    beforeEach(function () {
        set_welcome_cookies();
        set_login_cookie();
        cy.visit(url + '/discuss/');
    });
    it('Tries to add an issue with missing input and it should fail.', function () {
        cy.get('#add-topic.icon-badge.blue-btn.bottom-right').should('exist').click();
        cy.get('#popup-add-topic-title-input').should('exist');
        cy.get('#popup-add-topic-title-input').type('frontendtesting');
        cy.get('#popup-add-topic-accept-btn').click();
        cy.get('#popup-add-topic-error').should('visible');
    });
    it('Tries to add and issue with input and succeeds', function () {
        cy.get('#add-topic.icon-badge.blue-btn.bottom-right').should('exist').click();
        cy.get('#popup-add-topic-title-input').should('exist');
        cy.get('#popup-add-topic-title-input').type('frontendtesting');
        cy.get('#popup-add-topic-info-input').type('Should we use frontendtesting?');
        cy.get('#popup-add-topic-long-info-input').type('Should we use frontendtesting?');
        cy.get('#popup-add-topic-accept-btn').click();
        cy.get('#popup-add-topic-error').should('not.visible');
    });
});

describe('Add Position Test', function () {
    beforeEach(function () {
        set_welcome_cookies();
        set_login_cookie();
        cy.visit(url + '/discuss/frontendtesting');
    });
    it('Tries to add a position without input and it should fail', function () {
        cy.get('#send-new-statement').click();
        cy.get('#add-statement-error-container').should('visible');
    });
    it('Tries to add an position with input and succeeds', function () {
        cy.get('#add-statement-container-main-input-position').type('FooBarBaz');
        cy.wait(1000);
        cy.get('#add-statement-container-main-input-reason').type('Very good reason!!!');
        cy.wait(1000);
        cy.get('#send-new-statement').click();
        cy.get('#add-statement-error-container').should('not.visible');
    });
});


describe('Agree and disagree test', function () {
    var position = "FooBarBaz";
    var reason = "Very good reason!";
    var disagreement = "NegativeFooBarBaz";
    var premise = "Very good premise";
    beforeEach(function () {
        set_welcome_cookies();
        set_login_cookie();
        cy.visit(url + '/discuss/frontendtesting');
    });

    it('checks if an user can disagree to new position and tries to send empty reason. It should fail', function () {
        cy.contains(position).click();
        cy.get('#item_disagree').click();
        cy.get('#send-new-position').click();
        cy.get('#add-premise-error-container').should('visible');
    });

    it('checks if an user can disagree to new position and sends reason. It should succeed', function () {
        cy.contains(position).click();
        cy.get('#item_disagree').click();
        cy.get('#add-position-container-main-input').type(disagreement);
        cy.get('#send-new-position').click();
        cy.get('#add-premise-error-container').should('not.visible');
    });
    it('checks if an user can agree to new position and tries to send empty reason. It should fail', function () {
        cy.contains(position).click();
        cy.get('#item_agree').click();
        cy.get('#item_start_premise').click();
        cy.get('#send-new-position').click();
        cy.get('#add-premise-error-container').should('visible');
    });

    it('checks if an user can agree to new position and sends reason. It should succeed', function () {
        cy.contains(position).click();
        cy.get('#item_agree').click();
        cy.get('#item_start_premise').click();
        cy.get('#add-position-container-main-input').type(disagreement);
        cy.get('#send-new-position').click();
        cy.get('#add-premise-error-container').should('not.visible');
    });

    it('checks if an user can agree to new position and selects given reason.', function () {
        cy.contains(position).click();
        cy.get('#item_agree').click();
        cy.get('#item_70').click();
    });

    it('checks if an user can disagree to new position and selects given reason.', function () {
        cy.contains(position).click();
        cy.get('#item_disagree').click();
        cy.get('#item_71').click();
    });
});


describe('Support, undercut and rebut test', function () {
    var position = "FooBarBaz";
    beforeEach(function () {
        set_welcome_cookies();
        set_login_cookie();
        cy.visit(url + '/discuss/frontendtesting');
        cy.contains(position).click();
        cy.get('#item_agree').click();
        cy.get('#item_70').click();
    });

    it('checks if an user can select undermine', function () {
        cy.get('#item_undermine').click();
    });

    it('checks if an user can select support', function () {
        cy.get('#item_support').click();
    });

    it('checks if an user can select support', function () {
        cy.get('#item_undercut').click();
    });

    it('checks if an user can select rebut', function () {
        cy.get('#item_rebut').click();
    });
});

