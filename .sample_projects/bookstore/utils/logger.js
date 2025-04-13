const winston = require('winston');const config = require('../config/config');

const logLevel = process.env.LOG_LEVEL || 'info';

const logger = winston.createLogger({
  level: logLevel,
  format: winston.format.combine(
    winston.format.timestamp({
      format: 'YYYY-MM-DD HH:mm:ss'
    }),
    winston.format.errors({ stack: true }),
    winston.format.splat(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console({
      format: winston.format.combine(
        winston.format.colorize(),
        winston.format.simple()
      )
    }),
    new winston.transports.File({ filename: 'logs/error.log', level: 'error' }),
    new winston.transports.File({ filename: 'logs/combined.log' })
  ],
});

function info(message, ...args) {
  logger.info(message, ...args);
}

function error(message, ...args) {
  logger.error(message, ...args);
}

function warn(message, ...args) {  logger.warn(message, ...args);
}

function debug(message, ...args) {
  logger.debug(message, ...args);
}

module.exports = {
  info,
  error,
  warn,
  debug,
};
