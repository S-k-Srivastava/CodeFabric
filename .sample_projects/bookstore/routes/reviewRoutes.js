// Import required modules
const express = require('express');
const reviewController = require('../controllers/reviewController');
const authMiddleware = require('../middlewares/auth.middleware');
const requestValidatorMiddleware = require('../middlewares/requestValidator.middleware');

// Create a router instance
const reviewRouter = express.Router();

// Define routes for review endpoints
reviewRouter.post('/review', 
  authMiddleware.authenticate, 
  requestValidatorMiddleware.createValidationMiddleware([
    require('express-validator').check('bookId').isString().withMessage('Book ID must be a string'),
    require('express-validator').check('rating').isInt({ min: 1, max: 5 }).withMessage('Rating must be between 1 and 5'),
    require('express-validator').check('reviewText').isString().isLength({ min: 1, max: 500 }).withMessage('Review text must be between 1 and 500 characters'),
  ]),
  reviewController.createReview
);

reviewRouter.get('/reviews/:bookId', 
  requestValidatorMiddleware.createValidationMiddleware([
    require('express-validator').check('bookId').isString().withMessage('Book ID must be a string'),
  ]),
  reviewController.getReviews
);

// Export the review router
module.exports = reviewRouter;
