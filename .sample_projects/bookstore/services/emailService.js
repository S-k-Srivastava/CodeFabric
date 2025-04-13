const nodemailer = require('nodemailer');
const config = require('../config/config');
const logger = require('../utils/logger');

// Configure email transport
const transport = nodemailer.createTransport({
  service: config.emailConfig.service,
  auth: {
    user: config.emailConfig.user,
    pass: config.emailConfig.pass,
  },
});

// Email templates
const orderConfirmationTemplate = (order) => {
  return `
    <h2>Order Confirmation</h2>
    <p>Dear ${order.customerName},</p>
    <p>Your order has been successfully placed. Order details are as follows:</p>
    <ul>
      <li>Order ID: ${order.orderId}</li>
      <li>Order Date: ${order.orderDate}</li>
      <li>Total: ${order.total}</li>
    </ul>
    <p>Thank you for shopping with us.</p>
  `;
};

const orderStatusUpdateTemplate = (order) => {
  return `
    <h2>Order Status Update</h2>
    <p>Dear ${order.customerName},</p>
    <p>The status of your order has been updated to ${order.status}.</p>
    <ul>
      <li>Order ID: ${order.orderId}</li>
      <li>Order Date: ${order.orderDate}</li>
      <li>Status: ${order.status}</li>
    </ul>
    <p>Thank you for shopping with us.</p>
  `;
};

const forgotPasswordTemplate = (user) => {
  return `
    <h2>Forgot Password</h2>
    <p>Dear ${user.name},</p>
    <p>To reset your password, please click on the following link: <a href="${user.resetLink}">${user.resetLink}</a></p>
    <p>Thank you for using our service.</p>
  `;
};

const lowStockAlertTemplate = (book) => {
  return `
    <h2>Low Stock Alert</h2>
    <p>Dear Admin,</p>
    <p>The stock of ${book.title} has fallen below 10. Please consider restocking.</p>
    <ul>
      <li>Book Title: ${book.title}</li>
      <li>Current Stock: ${book.quantity}</li>
    </ul>
    <p>Thank you for using our service.</p>
  `;
};

// Email sending functions
const sendOrderConfirmationEmail = async (order) => {
  try {
    const mailOptions = {
      from: config.emailConfig.from,
      to: order.customerEmail,
      subject: 'Order Confirmation',
      html: orderConfirmationTemplate(order),
    };
    await transport.sendMail(mailOptions);
    logger.info('Order confirmation email sent successfully');
  } catch (error) {
    logger.error('Error sending order confirmation email: ', error);
  }
};

const sendOrderStatusUpdateEmail = async (order) => {
  try {
    const mailOptions = {
      from: config.emailConfig.from,
      to: order.customerEmail,
      subject: 'Order Status Update',
      html: orderStatusUpdateTemplate(order),
    };
    await transport.sendMail(mailOptions);
    logger.info('Order status update email sent successfully');
  } catch (error) {
    logger.error('Error sending order status update email: ', error);
  }
};

const sendForgotPasswordEmail = async (user) => {
  try {
    const mailOptions = {
      from: config.emailConfig.from,
      to: user.email,
      subject: 'Forgot Password',
      html: forgotPasswordTemplate(user),
    };
    await transport.sendMail(mailOptions);
    logger.info('Forgot password email sent successfully');
  } catch (error) {
    logger.error('Error sending forgot password email: ', error);
  }
};

const sendLowStockAlertEmail = async (book) => {
  try {
    const mailOptions = {
      from: config.emailConfig.from,
      to: 'admin@example.com',
      subject: 'Low Stock Alert',
      html: lowStockAlertTemplate(book),
    };
    await transport.sendMail(mailOptions);
    logger.info('Low stock alert email sent successfully');
  } catch (error) {
    logger.error('Error sending low stock alert email: ', error);
  }
};

// Export email sending functions
module.exports = {
  sendOrderConfirmationEmail,
  sendOrderStatusUpdateEmail,
  sendForgotPasswordEmail,
  sendLowStockAlertEmail,
};
