const path = require('path')

module.exports = {
  // Optimize build performance
  parallel: require('os').cpus().length > 1,
  
  // Faster source maps for development
  configureWebpack: config => {
    if (process.env.NODE_ENV === 'development') {
      config.devtool = 'eval-cheap-module-source-map'
      
      // Optimize resolve
      config.resolve.symlinks = false
      config.resolve.cacheWithContext = false
      
      // Cache configuration
      config.cache = {
        type: 'filesystem',
        buildDependencies: {
          config: [__filename]
        }
      }
    }
  },
  
  devServer: {
    port: 8080,
    hot: true,
    compress: true,
    
    // Disable host checking for faster startup
    allowedHosts: 'all',
    
    // Reduce file watching overhead
    watchFiles: {
      paths: ['src/**/*'],
      options: {
        usePolling: false,
      }
    },
    
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true
      }
    }
  },
  
  // Faster CSS processing
  css: {
    sourceMap: false,
    extract: false
  },
  
  // Optimize chunk splitting
  chainWebpack: config => {
    if (process.env.NODE_ENV === 'development') {
      // Disable prefetch and preload for faster initial load
      config.plugins.delete('prefetch')
      config.plugins.delete('preload')
      
      // Optimize module resolution
      config.resolve.modules
        .clear()
        .add('node_modules')
        .add(path.resolve(__dirname, 'src'))
    }
  }
}