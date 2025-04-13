// Import required modules
const express = require('express');
const router = express.Router();
const cartController = require('../controllers/cartController');
const authMiddleware = require('../middlewares/auth.middleware');
const requestValidatorMiddleware = require('../middlewares/requestValidator.middleware');

// Define routes for shopping cart endpoints
router.post('/cart', 
  authMiddleware.authenticate, 
  requestValidatorMiddleware.createValidationMiddleware([
    require('express-validator').check('bookId').isString().withMessage('Book ID must be a string'),
    require('express-validator').check('quantity').isInt().withMessage('Quantity must be an integer'),
  ]),
  cartController.addToCart
);

router.get('/cart', 
  authMiddleware.authenticate, 
  cartController.viewCart
);

router.put('/cart/:bookId', 
  authMiddleware.authenticate, 
  requestValidatorMiddleware.createValidationMiddleware([
    require('express-validator').check('quantity').isInt().withMessage('Quantity must be an integer'),
  ]),
  cartController.updateCartQuantity
);

router.delete('/cart/:bookId', 
  authMiddleware.authenticate, 
  cartController.removeFromCart
);

// Export the router
module.exports = router;
