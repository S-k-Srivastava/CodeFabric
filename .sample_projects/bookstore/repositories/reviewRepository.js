const { Review } = require('../models/review.model');

const createReview = async (reviewData) => {
  try {
    const review = new Review(reviewData);
    await review.save();
    return review;
  } catch (error) {
    throw new Error('Failed to create review');
  }
};

const getReviewById = async (reviewId) => {
  try {
    const review = await Review.findById(reviewId);
    return review;
  } catch (error) {
    throw new Error('Failed to get review by ID');
  }
};

const getBookReviews = async (bookId) => {  try {
    const reviews = await Review.find({ bookId }).populate('userId', 'firstName lastName');
    return reviews;
  } catch (error) {
    throw new Error('Failed to get book reviews');  }
};

const getUserReviews = async (userId) => {  try {
    const reviews = await Review.find({ userId }).populate('bookId', 'title');
    return reviews;
  } catch (error) {
    throw new Error('Failed to get user reviews');
  }
};

module.exports = {
  createReview,
  getReviewById,
  getBookReviews,
  getUserReviews
};