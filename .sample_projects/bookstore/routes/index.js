// Import required modules
const express = require('express');
const userRoutes = require('./userRoutes');
const bookRoutes = require('./bookRoutes');
const cartRoutes = require('./cartRoutes');
const orderRoutes = require('./orderRoutes');
const reviewRoutes = require('./reviewRoutes');
const wishlistRoutes = require('./wishlistRoutes');
const adminRoutes = require('./adminRoutes');

// Create a main router for the application
const mainRouter = express.Router();

// Mount user routes under /api path
mainRouter.use('/api', userRoutes);

// Mount book routes under /api path
mainRouter.use('/api', bookRoutes);

// Mount cart routes under /api path
mainRouter.use('/api', cartRoutes);

// Mount order routes under /api path
mainRouter.use('/api', orderRoutes.orderRoutes);

// Mount review routes under /api path
mainRouter.use('/api', reviewRoutes);

// Mount wishlist routes under /api path
mainRouter.use('/api', wishlistRoutes);

// Mount admin routes under /api path
mainRouter.use('/api', adminRoutes);

// Export the main router
module.exports = { mainRouter };
