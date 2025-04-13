// Import required modules
const express = require('express');
const cartService = require('../services/cartService');
const validator = require('../utils/validator');
const { ApiError } = require('../utils/apiError');

// Define controller functions
async function addToCart(req, res, next) {
  try {
    // Validate input
    if (!validator.isValidId(req.user.id) ||!validator.isValidId(req.body.bookId) ||!validator.isValidQuantity(req.body.quantity)) {
      throw new ApiError(400, 'Invalid input');
    }

    // Call cart service to add to cart
    const cart = await cartService.addToCart(req.user.id, req.body.bookId, req.body.quantity);

    // Send JSON response
    res.status(200).json(cart);
  } catch (error) {
    // Pass error to error handling middleware
    next(error);
  }
}

async function viewCart(req, res, next) {
  try {
    // Validate input
    if (!validator.isValidId(req.user.id)) {
      throw new ApiError(400, 'Invalid input');
    }

    // Call cart service to view cart
    const cart = await cartService.viewCart(req.user.id);

    // Send JSON response
    res.status(200).json(cart);
  } catch (error) {
    // Pass error to error handling middleware
    next(error);
  }
}

async function updateCartQuantity(req, res, next) {
  try {
    // Validate input
    if (!validator.isValidId(req.user.id) ||!validator.isValidId(req.params.bookId) ||!validator.isValidQuantity(req.body.quantity)) {
      throw new ApiError(400, 'Invalid input');
    }

    // Call cart service to update cart quantity
    const cart = await cartService.updateCartQuantity(req.user.id, req.params.bookId, req.body.quantity);

    // Send JSON response
    res.status(200).json(cart);
  } catch (error) {
    // Pass error to error handling middleware
    next(error);
  }
}

async function removeFromCart(req, res, next) {
  try {
    // Validate input
    if (!validator.isValidId(req.user.id) ||!validator.isValidId(req.params.bookId)) {
      throw new ApiError(400, 'Invalid input');
    }

    // Call cart service to remove from cart
    const cart = await cartService.removeFromCart(req.user.id, req.params.bookId);

    // Send JSON response
    res.status(200).json(cart);
  } catch (error) {
    // Pass error to error handling middleware
    next(error);
  }
}

// Export controller functions
module.exports = {
  addToCart,
  viewCart,
  updateCartQuantity,
  removeFromCart,
};
