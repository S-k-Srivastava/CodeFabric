const helmet = require('helmet');

const securityHeadersMiddleware = () => {
  return helmet({
    hsts: {
      maxAge: 31536000,
      includeSubDomains: true,
      preload: true
    },
    frameguard: {
      action: 'sameorigin'
    },
    xssFilter: {},
    noSniff: {},
    contentSecurityPolicy: {
      directives: {
        defaultSrc: ["'self'"],
        scriptSrc: ["'self'", "'unsafe-inline'"],
        styleSrc: ["'self'", "'unsafe-inline'"],
        imgSrc: ["'self'", 'data:'],
        fontSrc: ["'self'"],
        connectSrc: ["'self'"],
      }
    }
  });
};

module.exports = {
  securityHeadersMiddleware
};
