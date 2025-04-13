class ApiError extends Error {
  constructor(statusCode, message, isOperational = true, stack = '') {
    super(message);    this.statusCode = statusCode;
    this.isOperational = isOperational;
    if (stack) {
      this.stack = stack;
    } else {
      Error.captureStackTrace(this, this.constructor);
    }
  }

  static handleMongooseError(error) {
    return new ApiError(400, 'Database Error', false, error.stack);
  }

  static handleValidationError(error) {
    return new ApiError(400, 'Validation Error', false, error.stack);
  }

  static handleCastError(error) {    return new ApiError(400, 'Cast Error', false, error.stack);
  }
}

module.exports = {  ApiError
};
