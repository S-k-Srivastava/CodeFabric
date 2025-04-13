// Import required modules
const bookRepository = require('../repositories/bookRepository');
const { ApiError } = require('../utils/apiError');
const validator = require('../utils/validator');

// In-memory cart storage (can be extended to Redis or database)
const cartStorage = {};

// Function to add a book to the cart
async function addToCart(userId, bookId, quantity) {
  try {
    // Validate input
    if (!validator.isValidId(userId) ||!validator.isValidId(bookId) ||!validator.isValidQuantity(quantity)) {
      throw new ApiError(400, 'Invalid input');
    }

    // Fetch book details
    const book = await bookRepository.getBookById(bookId);
    if (!book) {
      throw new ApiError(404, 'Book not found');
    }

    // Check if book is already in cart
    if (cartStorage[userId] && cartStorage[userId][bookId]) {
      // Update quantity if book is already in cart
      cartStorage[userId][bookId].quantity += quantity;
    } else {
      // Add book to cart if it's not already there
      if (!cartStorage[userId]) {
        cartStorage[userId] = {};
      }
      cartStorage[userId][bookId] = {
        bookId,
        title: book.title,
        price: book.price,
        quantity,
      };
    }

    // Calculate cart total
    const cartTotal = calculateCartTotal(cartStorage[userId]);

    // Return updated cart
    return {
      items: Object.values(cartStorage[userId]),
      total: cartTotal,
    };
  } catch (error) {
    throw new ApiError(500, 'Error adding to cart', false, error.stack);
  }
}

// Function to view the cart
async function viewCart(userId) {
  try {
    // Check if cart exists for user
    if (!cartStorage[userId]) {
      throw new ApiError(404, 'Cart not found');
    }

    // Calculate cart total
    const cartTotal = calculateCartTotal(cartStorage[userId]);

    // Return cart
    return {
      items: Object.values(cartStorage[userId]),
      total: cartTotal,
    };
  } catch (error) {
    throw new ApiError(500, 'Error viewing cart', false, error.stack);
  }
}

// Function to update cart quantity
async function updateCartQuantity(userId, bookId, quantity) {
  try {
    // Validate input
    if (!validator.isValidId(userId) ||!validator.isValidId(bookId) ||!validator.isValidQuantity(quantity)) {
      throw new ApiError(400, 'Invalid input');
    }

    // Check if cart exists for user
    if (!cartStorage[userId]) {
      throw new ApiError(404, 'Cart not found');
    }

    // Check if book is in cart
    if (!cartStorage[userId][bookId]) {
      throw new ApiError(404, 'Book not found in cart');
    }

    // Update quantity
    cartStorage[userId][bookId].quantity = quantity;

    // Calculate cart total
    const cartTotal = calculateCartTotal(cartStorage[userId]);

    // Return updated cart
    return {
      items: Object.values(cartStorage[userId]),
      total: cartTotal,
    };
  } catch (error) {
    throw new ApiError(500, 'Error updating cart quantity', false, error.stack);
  }
}

// Function to remove a book from the cart
async function removeFromCart(userId, bookId) {
  try {
    // Validate input
    if (!validator.isValidId(userId) ||!validator.isValidId(bookId)) {
      throw new ApiError(400, 'Invalid input');
    }

    // Check if cart exists for user
    if (!cartStorage[userId]) {
      throw new ApiError(404, 'Cart not found');
    }

    // Check if book is in cart
    if (!cartStorage[userId][bookId]) {
      throw new ApiError(404, 'Book not found in cart');
    }

    // Remove book from cart
    delete cartStorage[userId][bookId];

    // Calculate cart total
    const cartTotal = calculateCartTotal(cartStorage[userId]);

    // Return updated cart
    return {
      items: Object.values(cartStorage[userId]),
      total: cartTotal,
    };
  } catch (error) {
    throw new ApiError(500, 'Error removing from cart', false, error.stack);
  }
}

// Function to calculate cart total
function calculateCartTotal(cartItems) {
  let total = 0;
  Object.values(cartItems).forEach((item) => {
    total += item.price * item.quantity;
  });
  return total;
}

// Export functions
module.exports = {
  addToCart,
  viewCart,
  updateCartQuantity,
  removeFromCart,
};
