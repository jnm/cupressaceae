// USERNAME, PASSWORD, and URL can be set in the OS environment as
// CYPRESS_USERNAME, CYPRESS_PASSWORD, and CYPRESS_URL

describe('Log in to production servers', () => {
  const server = Cypress.env('URL')
  it('Logs into ' + server, () => {
    cy.visit(server)

    cy.get('#id_username').type(Cypress.env('USERNAME'))
    cy.get('#id_password').type(Cypress.env('PASSWORD'))
    cy.get('button[type=submit]').click()

    cy.get('.account-username').should('contain', Cypress.env('USERNAME'))
  })
})
