const express = require('express');
const bookService = require('../services/bookService');
const validator = require('../utils/validator');
const { ApiError } = require('../utils/apiError');
const csv = require('csv-parser');
const fs = require('fs');

const browseBooks = async (req, res, next) => {
  try {
    const query = req.query;
    const result = await bookService.browseBooks(query);
    res.status(200).json(result);
  } catch (error) {
    next(error);
  }
};

const searchBooks = async (req, res, next) => {
  try {
    const query = req.query;
    const result = await bookService.searchBooks(query.query, query.page, query.limit);
    res.status(200).json(result);
  } catch (error) {
    next(error);
  }
};

const addBook = async (req, res, next) => {
  try {
    const bookData = req.body;
    const validatedData = validator.validateBookData(bookData);
    const result = await bookService.addBook(validatedData);
    res.status(201).json(result);
  } catch (error) {
    next(error);
  }
};

const updateBook = async (req, res, next) => {
  try {
    const bookId = req.params.bookId;
    const updateData = req.body;
    const validatedData = validator.validateBookData(updateData);
    const result = await bookService.updateBook(bookId, validatedData);
    res.status(200).json(result);
  } catch (error) {
    next(error);
  }
};

const deleteBook = async (req, res, next) => {
  try {
    const bookId = req.params.bookId;
    const result = await bookService.deleteBook(bookId);
    res.status(200).json({ message: 'Book deleted successfully' });
  } catch (error) {
    next(error);
  }
};

const bulkUploadBooks = async (req, res, next) => {
  try {
    const csvFile = req.file.path;
    const result = await bookService.bulkUploadBooks(csvFile);
    res.status(200).json({ message: 'Books uploaded successfully', count: result });
  } catch (error) {
    next(error);
  }
};

module.exports = {
  browseBooks,
  searchBooks,
  addBook,
  updateBook,
  deleteBook,
  bulkUploadBooks,
};
