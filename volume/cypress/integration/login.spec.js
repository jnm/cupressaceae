function logInAsJnmDemo(server) {
  cy.visit(server)

  cy.get('#id_username').type('HEY_USERNAME')
  cy.get('#id_password').type('make something up')
  cy.get('input[type=submit]').click()

  cy.get('.account-username').should('contain', 'HEY_USERNAME')
}

describe('Log in to production servers', () => {
  it('Logs into HHI', () => {
    logInAsJnmDemo('https://kf.kobotoolbox.org/')
  })
  it('Logs into OCHA', () => {
    logInAsJnmDemo('https://kobo.humanitarianresponse.info/')
  })
})
