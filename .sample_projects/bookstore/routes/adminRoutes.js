// Import required modules
const express = require('express');
const bookRoutes = require('./bookRoutes');
const orderRoutes = require('./orderRoutes');
const discountRoutes = require('./discountRoutes');
const authMiddleware = require('../middlewares/auth.middleware');

// Create a router for admin API endpoints
const adminRouter = express.Router();

// Apply admin role authorization middleware to all admin routes
adminRouter.use(authMiddleware.authenticate, authMiddleware.authorize('admin'));

// Mount book routes under /admin path
adminRouter.use('/book', bookRoutes);

// Mount order routes under /admin path
adminRouter.use('/order', orderRoutes.orderRoutes);

// Mount discount routes under /admin path
adminRouter.use('/discount', discountRoutes);

// Export the admin router
module.exports = adminRouter;
