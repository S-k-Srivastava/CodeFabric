const { Wishlist } = require('../models/wishlist.model');

const addToWishlist = async (userId, bookId) => {
  try {
    const wishlist = new Wishlist({ userId, bookId });
    await wishlist.save();    return wishlist;
  } catch (error) {
    if (error.code === 11000) {
      throw new Error('Book already in wishlist');
    }
    throw new Error('Could not add to wishlist');
  }
};

const getWishlistByUserId = async (userId) => {
  try {
    const wishlistItems = await Wishlist.find({ userId }).populate('bookId', 'title author price');
    return wishlistItems;
  } catch (error) {
    throw new Error('Could not retrieve wishlist');
  }
};

const removeFromWishlist = async (userId, bookId) => {
  try {
    const result = await Wishlist.deleteOne({ userId, bookId });
    return result;  } catch (error) {
    throw new Error('Could not remove from wishlist');
  }
};

const isBookInWishlist = async (userId, bookId) => {
  try {
    const wishlist = await Wishlist.findOne({ userId, bookId });
    return !!wishlist;
  } catch (error) {
    throw new Error('Could not check wishlist');
  }
};

module.exports = {
  addToWishlist,
  getWishlistByUserId,
  removeFromWishlist,  isBookInWishlist
};
