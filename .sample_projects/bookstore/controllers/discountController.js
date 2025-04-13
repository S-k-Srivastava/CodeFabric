const express = require('express');
const discountService = require('../services/discountService');
const validator = require('../utils/validator');
const { ApiError } = require('../utils/apiError');

const createDiscount = async (req, res, next) => {
  try {
    const { bookId, discountPercentage, expirationDate } = req.body;
    const validatedData = validator.validateDiscountData(req.body);
    const discount = await discountService.createDiscount(validatedData);
    res.status(201).json({ message: 'Discount created successfully', discount });
  } catch (error) {
    if (error instanceof ApiError) {
      next(error);
    } else {
      next(new ApiError(500, 'Failed to create discount'));
    }
  }
};

const getDiscounts = async (req, res, next) => {
  try {
    const discounts = await discountService.getDiscounts();
    res.status(200).json({ message: 'Discounts retrieved successfully', discounts });
  } catch (error) {
    if (error instanceof ApiError) {
      next(error);
    } else {
      next(new ApiError(500, 'Failed to get discounts'));
    }
  }
};

module.exports = { createDiscount, getDiscounts };
