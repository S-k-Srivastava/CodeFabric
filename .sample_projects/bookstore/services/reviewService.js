const reviewRepository = require('../repositories/reviewRepository');
const bookRepository = require('../repositories/bookRepository');
const { ApiError } = require('../utils/apiError');
const validator = require('../utils/validator');

const createReview = async (userId, bookId, rating, reviewText) => {
  try {
    // Input validation
    if (!validator.isValidRating(rating)) {
      throw new ApiError(400, 'Invalid rating. Rating must be between 1 and 5.');
    }

    if (!validator.isValidReviewText(reviewText)) {
      throw new ApiError(400, 'Invalid review text. Review text must be between 1 and 500 characters.');
    }

    // Check if user has already reviewed the book
    const existingReview = await reviewRepository.getReviewById(userId, bookId);
    if (existingReview) {
      throw new ApiError(400, 'You have already reviewed this book.');
    }

    // Fetch book details
    const book = await bookRepository.getBookById(bookId);
    if (!book) {
      throw new ApiError(404, 'Book not found.');
    }

    // Create review
    const reviewData = {
      userId,
      bookId,
      rating,
      reviewText,
    };
    const review = await reviewRepository.createReview(reviewData);
    return review;
  } catch (error) {
    throw new ApiError(500, 'Failed to create review.', false, error.stack);
  }
};

const getBookReviews = async (bookId) => {
  try {
    // Fetch book details
    const book = await bookRepository.getBookById(bookId);
    if (!book) {
      throw new ApiError(404, 'Book not found.');
    }

    // Get reviews
    const reviews = await reviewRepository.getBookReviews(bookId);
    return reviews;
  } catch (error) {
    throw new ApiError(500, 'Failed to get book reviews.', false, error.stack);
  }
};

module.exports = {
  createReview,
  getBookReviews,
};
