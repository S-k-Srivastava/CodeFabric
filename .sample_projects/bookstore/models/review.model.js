const mongoose = require('mongoose');

const reviewSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  bookId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Book',
    required: true
  },
  rating: {
    type: Number,
    required: true,
    min: 1,
    max: 5
  },
  reviewText: {
    type: String
  },
  createdAt: {
    type: Date,    default: Date.now
  }
});

reviewSchema.index({ bookId: 1 });

const Review = mongoose.model('Review', reviewSchema);

module.exports = {
  Review
};
