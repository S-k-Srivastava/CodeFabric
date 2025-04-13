// Import required modules
const express = require('express');
const router = express.Router();
const authMiddleware = require('../middlewares/auth.middleware');
const requestValidatorMiddleware = require('../middlewares/requestValidator.middleware');
const wishlistController = require('../controllers/wishlistController');

// Define routes for wishlist endpoints
router.post('/wishlist', 
  authMiddleware.authenticate, 
  requestValidatorMiddleware.bookValidationMiddleware, 
  wishlistController.addToWishlist
);

router.get('/wishlist', 
  authMiddleware.authenticate, 
  wishlistController.getWishlist
);

router.delete('/wishlist/:bookId', 
  authMiddleware.authenticate, 
  requestValidatorMiddleware.bookValidationMiddleware, 
  wishlistController.removeFromWishlist
);

// Export the router
module.exports = router;
