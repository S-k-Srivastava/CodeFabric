// Import required modules
const express = require('express');
const orderService = require('../services/orderService');
const validator = require('../utils/validator');
const { ApiError } = require('../utils/apiError');

// Create a router for order processing API endpoints
const orderController = express.Router();

// Function to handle place order requests
async function placeOrder(req, res, next) {
  try {
    // Validate request inputs
    if (!req.body.shippingAddress ||!req.body.paymentMethod) {
      throw new ApiError(400, 'Invalid input');
    }

    // Call orderService to handle business logic
    const orderDetails = await orderService.placeOrder(req.user._id, req.body.shippingAddress, req.body.paymentMethod);

    // Send JSON response with order details
    res.status(201).json(orderDetails);
  } catch (error) {
    // Handle errors and pass them to error handling middleware
    next(error);
  }
}

// Function to handle get order history requests
async function getOrderHistory(req, res, next) {
  try {
    // Validate request inputs
    if (!req.user) {
      throw new ApiError(401, 'Unauthorized');
    }

    // Call orderService to handle business logic
    const orderHistory = await orderService.getOrderHistory(req.user._id);

    // Send JSON response with order history
    res.status(200).json(orderHistory);
  } catch (error) {
    // Handle errors and pass them to error handling middleware
    next(error);
  }
}

// Define API endpoints
orderController.post('/order', placeOrder);
orderController.get('/orders', getOrderHistory);

// Export the order controller
module.exports = {
  orderController,
  placeOrder,
  getOrderHistory,
};
