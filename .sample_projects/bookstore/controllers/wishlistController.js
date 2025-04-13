const express = require('express');
const wishlistService = require('../services/wishlistService');
const validator = require('../utils/validator');
const { ApiError } = require('../utils/apiError');

const addToWishlist = async (req, res, next) => {
  try {
    const { bookId } = req.body;
    const userId = req.user.id;

    // Validate input
    if (!validator.isValidObjectId(userId) ||!validator.isValidObjectId(bookId)) {
      throw new ApiError(400, 'Invalid user or book ID');
    }

    // Call wishlistService method to handle business logic
    const wishlistItem = await wishlistService.addToWishlist(userId, bookId);

    // Send JSON response with appropriate status code and data
    res.status(201).json(wishlistItem);
  } catch (error) {
    // Handle errors and pass them to error handling middleware
    next(error);
  }
};

const getWishlist = async (req, res, next) => {
  try {
    const userId = req.user.id;

    // Validate input
    if (!validator.isValidObjectId(userId)) {
      throw new ApiError(400, 'Invalid user ID');
    }

    // Call wishlistService method to handle business logic
    const wishlist = await wishlistService.getWishlist(userId);

    // Send JSON response with appropriate status code and data
    res.status(200).json(wishlist);
  } catch (error) {
    // Handle errors and pass them to error handling middleware
    next(error);
  }
};

const removeFromWishlist = async (req, res, next) => {
  try {
    const { bookId } = req.params;
    const userId = req.user.id;

    // Validate input
    if (!validator.isValidObjectId(userId) ||!validator.isValidObjectId(bookId)) {
      throw new ApiError(400, 'Invalid user or book ID');
    }

    // Call wishlistService method to handle business logic
    const result = await wishlistService.removeFromWishlist(userId, bookId);

    // Send JSON response with appropriate status code and data
    res.status(200).json(result);
  } catch (error) {
    // Handle errors and pass them to error handling middleware
    next(error);
  }
};

module.exports = { addToWishlist, getWishlist, removeFromWishlist };
