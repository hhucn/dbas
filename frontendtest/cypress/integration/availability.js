const url = Cypress.env('WEB_PROTOCOL') + '://' + Cypress.env('WEB_HOST') + ':' + Cypress.env('WEB_PORT');

function get_every_element_at(element, at) {
    cy.visit(at);
    cy.get(element)
        .each(($el) => {
            cy.wrap($el).click();
            cy.url().should('contains', at);
        });
}

describe('Click every element at /', function () {

    it('clicks every navigation item', function () {
        get_every_element_at('.nav-link', url + '/');
    });
    it('checks if every buttons has access to a active site', function () {
        cy.visit(url);
        cy.get('a.btn:visible')
            .each(($el) => {
                cy.wrap($el)
                    .should('have.attr', 'href')
                    .then((href) => {
                        if (href.indexOf('https') === -1) {
                            cy.request({
                                url: url + href,
                                baseUrl: url
                            })
                                .then((resp) => {
                                    expect(resp.status).to.eq(200);
                                });
                        }
                    });
            });
    });
});

describe('Click every button at /discuss', function () {
    it('checks if every discussion is active', function () {
        cy.visit(url + '/discuss');
        cy.get('td > a:visible')
            .each(($el) => {
                cy.wrap($el)
                    .should('have.attr', 'href')
                    .then((href) => {
                        console.log('href ' + href);
                        cy.request({
                            url: url + href,
                            baseUrl: url
                        })
                            .then((resp) => {
                                expect(resp.status).to.eq(200);
                            });
                    });
            });
    });
});