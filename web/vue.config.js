const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    historyApiFallback: true,
    allowedHosts: "all",
    port: 9901,
  }
}