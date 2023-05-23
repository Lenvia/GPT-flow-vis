const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  devServer: {
    historyApiFallback: true,
    allowedHosts: "all",
    port: 9901,
  },

  pluginOptions: {
    electronBuilder: {
      // Use this to set the development server URL
      // in development mode
      builderOptions: {
        // Set the development server URL
        // in development mode
        extraMetadata: {
          WEBPACK_DEV_SERVER_URL: 'http://localhost:9901/main',
        },
      },
    },
  },

})
