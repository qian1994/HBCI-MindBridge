'use strict'
const path = require('path');
function resolve(dir) {
    return path.join(__dirname, dir)
}

module.exports = {
    outputDir: '../web-app/app',
    publicPath: process.env.NODE_ENV === 'production' ? './' : './',
    devServer: {
        port: 8082
    },
    productionSourceMap:process.env.NODE_ENV === 'production'? true:true, // 设置上线后是否加载webpack文件
    configureWebpack: {
        devtool: 'source-map',
        performance: {
            hints: 'warning',
            maxEntrypointSize: 50000000,
            maxAssetSize: 30000000,
            assetFilter: function (assetFilename) {
                return assetFilename.endsWith('.js');
            }
        },
        resolve: {
            alias: {
                "%": resolve('src')
            },
        },
    }
}