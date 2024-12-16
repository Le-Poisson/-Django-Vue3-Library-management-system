const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '0.0.0.0', // 允许来自所有IP的访问
    port: 8080, // 使用的端口
    client: {
      overlay: false
    },
  }
})
