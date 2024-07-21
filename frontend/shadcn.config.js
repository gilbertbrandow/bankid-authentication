const { createShadcnConfig } = require('@shadcn/ui')

module.exports = createShadcnConfig({
  outputPath: './src/components',
  components: ['button', 'card', 'modal'],
  theme: './src/theme.js',
})
