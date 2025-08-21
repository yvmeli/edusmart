// e2e/playwright.config.js
const { defineConfig } = require('@playwright/test');

module.exports = defineConfig({
  testDir: '.',                       // los specs están en esta misma carpeta
  testMatch: /.*\.spec\.js/,
  reporter: [['list'], ['html', { outputFolder: '../frontend/test-results' }]],
  use: {
    baseURL: 'http://127.0.0.1:8000',
    headless: true,
  },
  webServer: {
    // En Windows suele funcionar mejor 'py -3' que 'python'
    command: 'py -3 ../backend/app.py',
    url: 'http://127.0.0.1:8000',
    reuseExistingServer: true,
    timeout: 120000,
  },
});
