// Import required modules
const { check, validationResult } = require('express-validator');
const { ApiError } = require('../utils/apiError');

// Function to create validation middleware based on validation schema
const createValidationMiddleware = (schema) => {
  return [
   ...schema,
    (req, res, next) => {
      const errors = validationResult(req);
      if (!errors.isEmpty()) {
        return next(new ApiError(400, 'Validation Error', false, errors.array()));
      }
      next();
    },
  ];
};

// Validation schema for user registration
const registerSchema = [
  check('email').isEmail().withMessage('Invalid email'),
  check('password').isLength({ min: 8 }).withMessage('Password must be at least 8 characters'),
  check('firstName').isString().withMessage('First name must be a string'),
  check('lastName').isString().withMessage('Last name must be a string'),
  check('phoneNumber').isString().withMessage('Phone number must be a string'),
  check('address').isString().withMessage('Address must be a string'),
];

// Validation schema for user login
const loginSchema = [
  check('email').isEmail().withMessage('Invalid email'),
  check('password').isLength({ min: 8 }).withMessage('Password must be at least 8 characters'),
];

// Validation schema for book creation
const bookSchema = [
  check('title').isString().withMessage('Title must be a string'),
  check('author').isString().withMessage('Author must be a string'),
  check('ISBN').isString().withMessage('ISBN must be a string'),
  check('genre').isString().withMessage('Genre must be a string'),
  check('publicationYear').isInt().withMessage('Publication year must be an integer'),
  check('price').isFloat().withMessage('Price must be a float'),
  check('quantity').isInt().withMessage('Quantity must be an integer'),
  check('coverImageURL').isString().withMessage('Cover image URL must be a string'),
  check('description').isString().withMessage('Description must be a string'),
  check('format').isString().withMessage('Format must be a string'),
];

// Validation schema for order creation
const orderSchema = [
  check('shippingAddress').isString().withMessage('Shipping address must be a string'),
  check('paymentMethod').isString().withMessage('Payment method must be a string'),
];

// Export validation middlewares
module.exports = {
  registerValidationMiddleware: createValidationMiddleware(registerSchema),
  loginValidationMiddleware: createValidationMiddleware(loginSchema),
  bookValidationMiddleware: createValidationMiddleware(bookSchema),
  orderValidationMiddleware: createValidationMiddleware(orderSchema),
};
