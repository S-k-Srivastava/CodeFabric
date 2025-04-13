// Import required modules
const express = require('express');
const orderController = require('../controllers/orderController');
const authMiddleware = require('../middlewares/auth.middleware');
const requestValidatorMiddleware = require('../middlewares/requestValidator.middleware');

// Create a router for order processing API endpoints
const orderRoutes = express.Router();

// Define routes for order processing endpoints
orderRoutes.post('/order', 
  authMiddleware.authenticate, 
  requestValidatorMiddleware.orderValidationMiddleware, 
  orderController.placeOrder);

orderRoutes.get('/orders', 
  authMiddleware.authenticate, 
  orderController.getOrderHistory);

orderRoutes.get('/admin/orders', 
  authMiddleware.authenticate, 
  authMiddleware.authorize('admin'), 
  orderController.getAdminOrders);

orderRoutes.get('/admin/order/:orderId', 
  authMiddleware.authenticate, 
  authMiddleware.authorize('admin'), 
  orderController.getAdminOrderById);

orderRoutes.put('/admin/order/:orderId', 
  authMiddleware.authenticate, 
  authMiddleware.authorize('admin'), 
  requestValidatorMiddleware.orderValidationMiddleware, 
  orderController.updateAdminOrder);

// Export the order routes
module.exports = {
  orderRoutes,
};
