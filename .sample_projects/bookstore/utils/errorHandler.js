const { ApiError } = require('./apiError');
const logger = require('./logger');const errorHandler = (err, req, res, next) => {
  let error = err;

  if (!(error instanceof ApiError)) {
    let statusCode = 500;
    let message = 'Internal Server Error';

    if (error.name === 'ValidationError') {
      error = ApiError.handleValidationError(error);
    } else if (error.name === 'CastError') {
      error = ApiError.handleCastError(error);
    } else if (error.name === 'MongoError' || error.name === 'MongooseError') {
      error = ApiError.handleMongooseError(error);
    } else {
      error = new ApiError(statusCode, message, false, err.stack);
    }
  }

  logger.error(
    `Error: ${error.message} - ${req.method} ${req.originalUrl} - ${req.ip}`,
    error
  );

  const statusCode = error.statusCode || 500;

  if (process.env.NODE_ENV === 'development') {
    res.status(statusCode).json({
      status: 'error',
      statusCode,
      message: error.message,
      stack: error.stack,
    });
  } else {
    res.status(statusCode).json({
      status: 'error',
      statusCode,
      message: error.isOperational ? error.message : 'Something went wrong!',
    });
  }
};

const handleUnhandledRejections = () => {
  process.on('unhandledRejection', (reason, promise) => {
    logger.error('Unhandled Rejection at:', promise, 'reason:', reason);
    process.exit(1);
  });
};

const handleUncaughtExceptions = () => {
  process.on('uncaughtException', (err) => {
    logger.error('Uncaught Exception:', err);
    process.exit(1);
  });
};module.exports = {
  errorHandler,
  handleUnhandledRejections,
  handleUncaughtExceptions,
};
