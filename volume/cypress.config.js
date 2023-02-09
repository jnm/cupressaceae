const { defineConfig } = require('cypress')

module.exports = defineConfig({
  defaultCommandTimeout: 45000,
  video: false,
  e2e: {
    supportFile: false,
    setupNodeEvents(on, config) {},
  },
})
