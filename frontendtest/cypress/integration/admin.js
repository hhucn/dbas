const url = Cypress.env('WEB_PROTOCOL') + "://" + Cypress.env("WEB_HOST") + ":" + Cypress.env("WEB_PORT");
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

describe('Test admin rights', function () {
    var elements = ['General', 'Users', 'Content', 'Voting', 'Reviews', 'Reviewer', 'Reputation'];
    var contents = ['Issue', 'Language', 'RSS', 'History', 'Group', 'User', 'Settings', 'Message', 'Statement',
        'StatementOrigins', 'StatementToIssue', 'TextVersion', 'StatementReferences', 'PremiseGroup', 'Premise',
        'Argument', 'ClickedArgument', 'ClickedStatement', 'MarkedArgument', 'MarkedStatement', 'SeenArgument',
        'SeenStatement', 'ReviewDelete', 'ReviewEdit', 'ReviewEditValue', 'ReviewOptimization', 'ReviewDeleteReason',
        'ReviewDuplicate', 'LastReviewerDelete', 'LastReviewerEdit', 'LastReviewerOptimization', 'LastReviewerDuplicate',
        'ReputationHistory', 'ReputationReason', 'OptimizationReviewLocks', 'ReviewCanceled', 'RevokedContent',
        'RevokedContentHistory', 'RevokedDuplicate'];

    it('visits /admin and logs in as admin', function () {
        cy.visit(url + '/admin/');
        login_via_popup(valid_user, valid_pw);
        for (var i = 0; i < elements.length; i++) {
            cy.contains(elements[i])
                .should('exist')
                .should('be.visible');
        }
    });
    it('visits /admin and tests if every element is visitable', function () {
        cy.visit(url + '/admin/');
        login_via_popup(valid_user, valid_pw);
        for (var i = 0; i < contents.length; i++) {
            cy.get('#' + contents[i])
                .should('exist')
                .should('be.visible');
        }
    });
    it('checks if each element in /admin return 200 response', function () {
        for (var i = 0; i < contents.length; i++) {
            cy.request({
                url: url + '/admin/' + contents[i],
            })
                .then((resp) => {
                    expect(resp.status).to.eq(200);
                });
        }
    });
});
