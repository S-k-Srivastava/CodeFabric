const express = require('express');
const reviewService = require('../services/reviewService');
const { ApiError } = require('../utils/apiError');
const validator = require('../utils/validator');
const requestValidator = require('../middlewares/requestValidator.middleware');

const createReview = async (req, res, next) => {
  try {
    const { bookId, rating, reviewText } = req.body;
    const userId = req.user.id;

    // Input validation
    if (!validator.isValidRating(rating)) {
      return res.status(400).json({ message: 'Invalid rating. Rating must be between 1 and 5.' });
    }

    if (!validator.isValidReviewText(reviewText)) {
      return res.status(400).json({ message: 'Invalid review text. Review text must be between 1 and 500 characters.' });
    }

    const review = await reviewService.createReview(userId, bookId, rating, reviewText);
    return res.status(201).json(review);
  } catch (error) {
    next(error);
  }
};

const getReviews = async (req, res, next) => {
  try {
    const bookId = req.params.bookId;

    // Input validation
    if (!validator.isValidObjectId(bookId)) {
      return res.status(400).json({ message: 'Invalid book ID.' });
    }

    const reviews = await reviewService.getBookReviews(bookId);
    return res.status(200).json(reviews);
  } catch (error) {
    next(error);
  }
};

module.exports = {
  createReview,
  getReviews,
};
