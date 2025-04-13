// Import required modules
const express = require('express');
const router = express.Router();
const discountController = require('../controllers/discountController');
const authMiddleware = require('../middlewares/auth.middleware');
const requestValidatorMiddleware = require('../middlewares/requestValidator.middleware');

// Define routes for discount endpoints
router.post('/admin/discount', 
  authMiddleware.authenticate, 
  authMiddleware.authorize('admin'), 
  requestValidatorMiddleware.bookValidationMiddleware, 
  discountController.createDiscount
);

router.get('/admin/discounts', 
  authMiddleware.authenticate, 
  authMiddleware.authorize('admin'), 
  discountController.getDiscounts
);

// Export the router
module.exports = router;
