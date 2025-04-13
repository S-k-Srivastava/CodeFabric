const express = require('express');
const { check, validationResult } = require('express-validator');
const userService = require('../services/userService');
const { ApiError } = require('../utils/apiError');
const validator = require('../utils/validator');

const registerUser = async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    const { email, password, firstName, lastName, phoneNumber, address } = req.body;
    const userData = { email, password, firstName, lastName, phoneNumber, address };
    const result = await userService.registerUser(userData);
    res.status(201).json(result);
  } catch (error) {
    next(error);
  }
};

const loginUser = async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    const { email, password } = req.body;
    const loginData = { email, password };
    const result = await userService.loginUser(loginData);
    res.status(200).json(result);
  } catch (error) {
    next(error);
  }
};

const updateUserProfile = async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    const userId = req.user.id;
    const updateData = req.body;
    const result = await userService.updateUserProfile(userId, updateData);
    res.status(200).json(result);
  } catch (error) {
    next(error);
  }
};

const forgotPassword = async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    const { email } = req.body;
    const result = await userService.forgotPassword(email);
    res.status(200).json(result);
  } catch (error) {
    next(error);
  }
};

const resetPassword = async (req, res, next) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ errors: errors.array() });
    }
    const { token, password, confirmPassword } = req.body;
    const result = await userService.resetPassword(token, password, confirmPassword);
    res.status(200).json(result);
  } catch (error) {
    next(error);
  }
};

module.exports = {
  registerUser,
  loginUser,
  updateUserProfile,
  forgotPassword,
  resetPassword,
};
