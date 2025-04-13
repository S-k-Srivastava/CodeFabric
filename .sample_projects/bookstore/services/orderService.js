// Import required modules
const orderRepository = require('../repositories/orderRepository');
const cartService = require('../services/cartService');
const emailService = require('../services/emailService');
const stripe = require('stripe')(require('../config/config').stripeApiKey);
const { ApiError } = require('../utils/apiError');
const validator = require('../utils/validator');

// Function to place an order
async function placeOrder(userId, shippingAddress, paymentMethod) {
  try {
    // Validate input
    if (!validator.isValidId(userId) ||!validator.isValidAddress(shippingAddress) ||!validator.isValidPaymentMethod(paymentMethod)) {
      throw new ApiError(400, 'Invalid input');
    }

    // Get user's cart
    const cart = await cartService.viewCart(userId);
    if (!cart || cart.items.length === 0) {
      throw new ApiError(404, 'Cart is empty');
    }

    // Calculate order total
    const orderTotal = cart.items.reduce((total, item) => total + item.quantity * item.price, 0);

    // Create order and order items in database
    const order = await orderRepository.createOrder(userId, shippingAddress, paymentMethod, cart.items);

    // Process payment using Stripe
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(orderTotal * 100),
      currency: 'usd',
      payment_method_types: [paymentMethod],
    });

    // Update order status to 'processing'
    await orderRepository.updateOrderStatus(order._id, 'processing');

    // Clear user's cart
    await cartService.clearCart(userId);

    // Send order confirmation email
    await emailService.sendOrderConfirmationEmail(userId, order);

    // Return order details
    return {
      orderId: order._id,
      status: order.status,
      total: order.totalCost,
      items: order.items,
    };
  } catch (error) {
    throw new ApiError(500, 'Error placing order', false, error.stack);
  }
}

// Function to get order history
async function getOrderHistory(userId) {
  try {
    // Validate input
    if (!validator.isValidId(userId)) {
      throw new ApiError(400, 'Invalid input');
    }

    // Get user's orders
    const orders = await orderRepository.getUserOrders(userId);

    // Return order history
    return orders;
  } catch (error) {
    throw new ApiError(500, 'Error getting order history', false, error.stack);
  }
}

// Export functions
module.exports = {
  placeOrder,
  getOrderHistory,
};
