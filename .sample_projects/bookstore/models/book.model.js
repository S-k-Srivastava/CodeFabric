const mongoose = require('mongoose');

const bookSchema = new mongoose.Schema({
  title: {
    type: String,    required: true,
  },
  author: {
    type: String,
    required: true,
  },
  ISBN: {
    type: String,
    required: true,
    unique: true,
  },
  genre: {
    type: String,
    enum: ['fiction', 'non-fiction', 'sci-fi', 'mystery', 'biography'],
  },
  publicationYear: {    type: Number,
  },
  price: {
    type: Number,
    required: true,
  },
  quantity: {
    type: Number,
    required: true,
  },
  coverImageURL: {
    type: String,
  },
  description: {
    type: String,
  },
  format: {
    type: String,
    enum: ['hardcover', 'paperback', 'e-book'],
  },
}, {
  timestamps: true,
});

bookSchema.index({ ISBN: 1 });
bookSchema.index({ genre: 1 });

const Book = mongoose.model('Book', bookSchema);

module.exports = {
  Book,
};
