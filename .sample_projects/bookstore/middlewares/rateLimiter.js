const rateLimit = require('express-rate-limit');

const loginLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 10, // 10 attempts per minute
  message: 'Too many login attempts from this IP, please try again after a minute',
  headers: true,
  standardHeaders: true,
  legacyHeaders: false,
});

const resetPasswordLimiter = rateLimit({
  windowMs: 60 * 60 * 1000, // 1 hour
  max: 5, // 5 requests per hour
  message: 'Too many password reset requests from this IP, please try again after an hour',
  headers: true,
  standardHeaders: true,
  legacyHeaders: false,
});

module.exports = {
  loginLimiter,
  resetPasswordLimiter,};
