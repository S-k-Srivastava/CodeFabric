const mongoose = require('mongoose');

const discountSchema = new mongoose.Schema({
  bookId: {
    type: mongoose.Schema.Types.ObjectId,    ref: 'Book',
    required: true,
    index: true,  },
  discountPercentage: {
    type: Number,
    required: true,
    min: 1,
    max: 50,
  },
  expirationDate: {
    type: Date,
  },
}, {
  timestamps: true,
});

const Discount = mongoose.model('Discount', discountSchema);

module.exports = {
  Discount,
};
