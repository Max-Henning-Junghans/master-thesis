const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/measurements',
    createProxyMiddleware({
      target: 'http://127.0.0.1:5000/measurements',
      changeOrigin: true,
    })
  );
  app.use(
      '/definitions',
      createProxyMiddleware({target: 'http://127.0.0.1:5000/definitions', changeOrigin: true,
      })
  );
};
