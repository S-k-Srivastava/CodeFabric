const discountRepository = require('../repositories/discountRepository');
const bookRepository = require('../repositories/bookRepository');
const { ApiError } = require('../utils/apiError');
const validator = require('../utils/validator');

const createDiscount = async (discountData) => {
  try {
    const { bookId, discountPercentage, expirationDate } = discountData;
    const book = await bookRepository.getBookById(bookId);
    if (!book) {
      throw new ApiError(404, 'Book not found');
    }
    const validatedData = validator.validateDiscountData(discountData);
    const discount = await discountRepository.createDiscount(validatedData);
    return discount;
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(500, 'Failed to create discount');
  }
};

const getDiscounts = async () => {
  try {
    const discounts = await discountRepository.getAllDiscounts();
    return discounts;
  } catch (error) {
    throw new ApiError(500, 'Failed to get discounts');
  }
};

const getActiveDiscounts = async () => {
  try {
    const discounts = await discountRepository.getActiveDiscounts();
    return discounts;
  } catch (error) {
    throw new ApiError(500, 'Failed to get active discounts');
  }
};

module.exports = { createDiscount, getDiscounts, getActiveDiscounts };
