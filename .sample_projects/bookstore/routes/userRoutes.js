// Import required modules
const express = require('express');
const router = express.Router();
const userController = require('../controllers/userController');
const authMiddleware = require('../middlewares/auth.middleware');
const requestValidatorMiddleware = require('../middlewares/requestValidator.middleware');

// Define routes for user-related endpoints
router.post('/register', 
  requestValidatorMiddleware.registerValidationMiddleware, 
  userController.registerUser
);

router.post('/login', 
  requestValidatorMiddleware.loginValidationMiddleware, 
  userController.loginUser
);

router.put('/user', 
  authMiddleware.authenticate, 
  requestValidatorMiddleware.registerValidationMiddleware, 
  userController.updateUserProfile
);

router.post('/forgotpassword', 
  requestValidatorMiddleware.loginValidationMiddleware, 
  userController.forgotPassword
);

router.post('/resetpassword', 
  requestValidatorMiddleware.loginValidationMiddleware, 
  userController.resetPassword
);

// Export the router
module.exports = router;
