'use strict'
process.env.NODE_ENV = 'development'

const webpack = require('webpack')
const base = require('./webpack.base')
const _ = require('./utils')
const FriendlyErrors = require('friendly-errors-webpack-plugin')

var proxy;
try {
  proxy = require('./proxy');
} catch (e) {
  console.info('ATTN: You might be missing a proxy.js file. Your API request might not work \n\n');
}


base.devtool = 'eval-source-map'
base.plugins.push(
  new webpack.DefinePlugin({
    'process.env.NODE_ENV': JSON.stringify('development')
  }),
  new webpack.HotModuleReplacementPlugin(),
  new webpack.NoEmitOnErrorsPlugin(),
  new FriendlyErrors()
)

// push loader for css files
_.cssProcessors.forEach(processor => {
  let loaders
  if (processor.loader === '') {
    loaders = ['postcss-loader']
  } else {
    loaders = ['postcss-loader', processor.loader]
  }
  base.module.loaders.push({
    test: processor.test,
    loaders: ['style-loader', _.cssLoader].concat(loaders)
  })
});

//setup proxy
base.devServer = {
  proxy: {
    '**': proxy ? proxy.url : ''
  }
};

module.exports = base