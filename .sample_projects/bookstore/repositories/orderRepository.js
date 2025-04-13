const { Order } = require('../models/order.model');
const { OrderItem } = require('../models/orderItem.model');
const mongoose = require('mongoose');

const createOrder = async (userId, shippingAddress, paymentMethod, cartItems) => {
  const session = await mongoose.startSession();
  session.startTransaction();  try {
    const order = new Order({
      userId,
      shippingAddress,
      paymentMethod,
      totalCost: cartItems.reduce((total, item) => total + item.quantity * item.price, 0),    });

    await order.save({ session });

    const orderItems = cartItems.map(item => ({
      orderId: order._id,
      bookId: item.bookId,
      quantity: item.quantity,
      unitPrice: item.price,
    }));

    await OrderItem.insertMany(orderItems, { session });

    await session.commitTransaction();
    session.endSession();

    return order;
  } catch (error) {
    await session.abortTransaction();
    session.endSession();
    throw error;
  }
};

const getOrderById = async (orderId) => {
  try {
    const order = await Order.findById(orderId);
    return order;
  } catch (error) {
    throw error;
  }
};

const getUserOrders = async (userId) => {
  try {
    const orders = await Order.find({ userId });
    return orders;
  } catch (error) {
    throw error;
  }
};

const getAllOrders = async () => {
  try {
    const orders = await Order.find();
    return orders;
  } catch (error) {
    throw error;
  }
};

const updateOrderStatus = async (orderId, status) => {
  try {
    const order = await Order.findByIdAndUpdate(orderId, { status }, { new: true });
    return order;
  } catch (error) {
    throw error;
  }
};

module.exports = {
  createOrder,
  getOrderById,
  getUserOrders,
  getAllOrders,
  updateOrderStatus,
};
