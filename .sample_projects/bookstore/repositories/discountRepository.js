const { Discount } = require('../models/discount.model');

const createDiscount = async (discountData) => {
  try {
    const discount = new Discount(discountData);
    await discount.save();
    return discount;
  } catch (error) {
    throw new Error('Failed to create discount');
  }
};

const getDiscountById = async (id) => {  try {
    const discount = await Discount.findById(id);    return discount;
  } catch (error) {
    throw new Error('Failed to get discount by ID');
  }
};

const getDiscountsByBookId = async (bookId) => {
  try {
    const discounts = await Discount.find({ bookId });    return discounts;
  } catch (error) {
    throw new Error('Failed to get discounts by book ID');
  }
};const getAllDiscounts = async () => {
  try {
    const discounts = await Discount.find();
    return discounts;
  } catch (error) {
    throw new Error('Failed to get all discounts');
  }
};

const updateDiscount = async (id, updateData) => {
  try {
    const discount = await Discount.findByIdAndUpdate(id, updateData, { new: true });
    return discount;
  } catch (error) {
    throw new Error('Failed to update discount');
  }
};

const deleteDiscount = async (id) => {
  try {
    const discount = await Discount.findByIdAndDelete(id);
    return discount;
  } catch (error) {
    throw new Error('Failed to delete discount');
  }
};

const getActiveDiscounts = async () => {
  try {
    const currentDate = new Date();
    const discounts = await Discount.find({
      $or: [
        { expirationDate: { $gte: currentDate } },
        { expirationDate: { $exists: false } },
        { expirationDate: null }
      ]
    });
    return discounts;
  } catch (error) {
    throw new Error('Failed to get active discounts');
  }
};

module.exports = {
  createDiscount,
  getDiscountById,
  getDiscountsByBookId,  getAllDiscounts,
  updateDiscount,
  deleteDiscount,  getActiveDiscounts,
};
