const { User } = require('../models/user.model');

const createUser = async (userData) => {
  try {
    const user = new User(userData);
    await user.save();
    return user;
  } catch (error) {
    throw new Error('Failed to create user');
  }};

const getUserByEmail = async (email) => {
  try {
    const user = await User.findOne({ email });
    return user;
  } catch (error) {
    throw new Error('Failed to get user by email');
  }
};

const getUserById = async (id) => {  try {
    const user = await User.findById(id);    return user;
  } catch (error) {
    throw new Error('Failed to get user by ID');
  }
};

const updateUser = async (id, updateData) => {
  try {
    const user = await User.findByIdAndUpdate(id, updateData, { new: true });
    return user;
  } catch (error) {
    throw new Error('Failed to update user');
  }
};

const deleteUser = async (id) => {
  try {
    const user = await User.findByIdAndDelete(id);
    return user;
  } catch (error) {
    throw new Error('Failed to delete user');
  }
};

module.exports = {
  createUser,  getUserByEmail,
  getUserById,
  updateUser,  deleteUser
};
