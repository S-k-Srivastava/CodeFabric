const wishlistRepository = require('../repositories/wishlistRepository');
const bookRepository = require('../repositories/bookRepository');
const { ApiError } = require('../utils/apiError');
const validator = require('../utils/validator');

const addToWishlist = async (userId, bookId) => {
  try {
    // Validate input
    if (!validator.isValidObjectId(userId) ||!validator.isValidObjectId(bookId)) {
      throw new ApiError(400, 'Invalid user or book ID');
    }

    // Check if book exists
    const book = await bookRepository.getBookById(bookId);
    if (!book) {
      throw new ApiError(404, 'Book not found');
    }

    // Check if book is already in wishlist
    const isBookInWishlist = await wishlistRepository.isBookInWishlist(userId, bookId);
    if (isBookInWishlist) {
      throw new ApiError(400, 'Book is already in your wishlist');
    }

    // Check if wishlist has reached the limit
    const wishlistCount = await wishlistRepository.getWishlistByUserId(userId).then((wishlist) => wishlist.length);
    if (wishlistCount >= 50) {
      throw new ApiError(400, 'Wishlist is full. You can add up to 50 books.');
    }

    // Add book to wishlist
    const wishlistItem = await wishlistRepository.addToWishlist(userId, bookId);
    return wishlistItem;
  } catch (error) {
    throw error;
  }
};

const getWishlist = async (userId) => {
  try {
    // Validate input
    if (!validator.isValidObjectId(userId)) {
      throw new ApiError(400, 'Invalid user ID');
    }

    // Get wishlist
    const wishlist = await wishlistRepository.getWishlistByUserId(userId);
    return wishlist;
  } catch (error) {
    throw error;
  }
};

const removeFromWishlist = async (userId, bookId) => {
  try {
    // Validate input
    if (!validator.isValidObjectId(userId) ||!validator.isValidObjectId(bookId)) {
      throw new ApiError(400, 'Invalid user or book ID');
    }

    // Check if book is in wishlist
    const isBookInWishlist = await wishlistRepository.isBookInWishlist(userId, bookId);
    if (!isBookInWishlist) {
      throw new ApiError(404, 'Book is not in your wishlist');
    }

    // Remove book from wishlist
    const result = await wishlistRepository.removeFromWishlist(userId, bookId);
    return result;
  } catch (error) {
    throw error;
  }
};

module.exports = { addToWishlist, getWishlist, removeFromWishlist };
