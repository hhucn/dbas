const url = Cypress.env('WEB_PROTOCOL') + "://" + Cypress.env("WEB_HOST") + ":" + Cypress.env("WEB_PORT");
var pages = ['', 'news', 'imprint', 'discuss', 'settings', 'notifications', 'admin/'];

describe('Test if test are active', function () {
    it('checks if all pages return 200 response if user is not logged in', function () {
        for (var i = 0; i < pages.length; i++) {
            cy.request({
                url: url + '/' + pages[i],
            })
                .then((resp) => {
                    expect(resp.status).to.eq(200);
                });
        }
    });
    it('visits every page', function () {
        for (var i = 0; i < pages.length; i++) {
            cy.visit(url + '/' + pages[i]);
            cy.url().should('contain', pages[i]);
        }
    });
});