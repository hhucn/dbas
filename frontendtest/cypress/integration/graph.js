const url = Cypress.env('WEB_PROTOCOL') + '://' + Cypress.env('WEB_HOST') + ':' + Cypress.env('WEB_PORT');
const discussions = ['Cat or Dog', 'Make the world better',
    'Elektroautos', 'Unterstützung der Sekretariate', 'Read only Issue'];
const valid_user = 'Bob';
const valid_pw = 'iamatestuser2016';

function slugify(str) {
    return str.replace(/ /g, '-').toLowerCase();
}

describe('Test grap functions', function () {
    function login(user, pw) {
        cy.get('#link_popup_login')
            .should('exist')
            .click({force: true});
        cy.get('#login-user')
            .type(user, {force: true});
        cy.get('#login-pw')
            .type(pw, {force: true});
        cy.get('#popup-login-button-login')
            .click({force: true});
        cy.wait(1000);
    }

    function visit_graph() {
        cy.get('#display-style-icon-graph-img')
            .should('exist')
            .click({force: true});
        cy.get('#confirm-dialog-refuse-btn')
            .click({force: true});
        cy.get('#circle-issue')
            .should('exist');
    }


    it('checks if every option is active', function () {

        cy.visit(url + "/discuss/cat-or-dog#graph");
        login(valid_user, valid_pw);
        cy.wait(1000);
        cy.get('ul#graph-sidebar > li:visible')
            .each(($el) => {
                cy.wrap($el)
                    .should('have.attr', 'id')
                    .then((id) => {
                        console.log('id ' + id);
                        cy.get('#' + id)
                            .should('exist')
                            .click({force: true});
                    });
            });
    });

});