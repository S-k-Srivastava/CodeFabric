const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const nodemailer = require('nodemailer');
const { ApiError } = require('../utils/apiError');
const { validateEmail, validatePassword, sanitizeInput } = require('../utils/validator');
const { createUser, getUserByEmail, getUserById, updateUser } = require('../repositories/userRepository');
const { emailConfig } = require('../config/config');
const transporter = nodemailer.createTransport({
  service: emailConfig.service,
  auth: {
    user: emailConfig.user,
    pass: emailConfig.pass,
  },
});

const registerUser = async (userData) => {
  try {
    const { email, password, firstName, lastName, phoneNumber, address } = userData;
    if (!validateEmail(email)) {
      throw new ApiError(400, 'Invalid email');
    }
    if (!validatePassword(password)) {
      throw new ApiError(400, 'Invalid password');
    }
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = await createUser({
      email,
      password: hashedPassword,
      firstName,
      lastName,
      phoneNumber,
      address,
    });
    const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '24h' });
    return { token, user: { id: user._id, email: user.email, firstName: user.firstName, lastName: user.lastName } };
  } catch (error) {
    throw new ApiError(500, 'Failed to register user');
  }
};

const loginUser = async (loginData) => {
  try {
    const { email, password } = loginData;
    if (!validateEmail(email)) {
      throw new ApiError(400, 'Invalid email');
    }
    const user = await getUserByEmail(email);
    if (!user) {
      throw new ApiError(404, 'User not found');
    }
    const isValidPassword = await bcrypt.compare(password, user.password);
    if (!isValidPassword) {
      throw new ApiError(401, 'Invalid password');
    }
    const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '24h' });
    return { token, user: { id: user._id, email: user.email, firstName: user.firstName, lastName: user.lastName } };
  } catch (error) {
    throw new ApiError(500, 'Failed to login user');
  }
};

const updateUserProfile = async (userId, updateData) => {
  try {
    const user = await getUserById(userId);
    if (!user) {
      throw new ApiError(404, 'User not found');
    }
    const updatedUser = await updateUser(userId, updateData);
    return updatedUser;
  } catch (error) {
    throw new ApiError(500, 'Failed to update user profile');
  }
};

const forgotPassword = async (email) => {
  try {
    const user = await getUserByEmail(email);
    if (!user) {
      throw new ApiError(404, 'User not found');
    }
    const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });
    const mailOptions = {
      from: emailConfig.from,
      to: email,
      subject: 'Password Reset',
      text: `Click on the link to reset your password: http://localhost:3000/api/resetpassword?token=${token}`,
    };
    await transporter.sendMail(mailOptions);
    return { message: 'Password reset link sent' };
  } catch (error) {
    throw new ApiError(500, 'Failed to send password reset link');
  }
};

const resetPassword = async (token, password, confirmPassword) => {
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    const user = await getUserById(decoded.userId);
    if (!user) {
      throw new ApiError(404, 'User not found');
    }
    if (password!== confirmPassword) {
      throw new ApiError(400, 'Passwords do not match');
    }
    const hashedPassword = await bcrypt.hash(password, 10);
    await updateUser(user._id, { password: hashedPassword });
    return { message: 'Password reset successful' };
  } catch (error) {
    throw new ApiError(500, 'Failed to reset password');
  }
};

module.exports = {
  registerUser,
  loginUser,
  updateUserProfile,
  forgotPassword,
  resetPassword,
};
