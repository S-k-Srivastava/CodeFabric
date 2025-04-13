const bookRepository = require('../repositories/bookRepository');
const { ApiError } = require('../utils/apiError');
const csv = require('csv-parser');
const fs = require('fs');
const validator = require('../utils/validator');

const browseBooks = async (query) => {
  try {
    const { genre, author, priceRange, sort } = query;
    const filter = {};
    if (genre) filter.genre = genre;
    if (author) filter.author = author;
    if (priceRange) {
      const [min, max] = priceRange.split(',');
      filter.price = { $gte: min, $lte: max };
    }
    const sortOptions = {};
    if (sort) {
      const [field, order] = sort.split('-');
      sortOptions[field] = order === 'asc'? 1 : -1;
    }
    const result = await bookRepository.getAllBooks(1, 50, filter, sortOptions);
    return result;
  } catch (error) {
    throw new ApiError(500, 'Error browsing books', false, error.stack);
  }
};

const searchBooks = async (query, page = 1, limit = 10) => {
  try {
    const result = await bookRepository.searchBooks(query, page, limit);
    return result;
  } catch (error) {
    throw new ApiError(500, 'Error searching books', false, error.stack);
  }
};

const addBook = async (bookData) => {
  try {
    const validatedData = validator.validateBookData(bookData);
    const result = await bookRepository.createBook(validatedData);
    return result;
  } catch (error) {
    throw new ApiError(500, 'Error adding book', false, error.stack);
  }
};

const updateBook = async (bookId, updateData) => {
  try {
    const validatedData = validator.validateBookData(updateData);
    const result = await bookRepository.updateBook(bookId, validatedData);
    return result;
  } catch (error) {
    throw new ApiError(500, 'Error updating book', false, error.stack);
  }
};

const deleteBook = async (bookId) => {
  try {
    const result = await bookRepository.deleteBook(bookId);
    return result;
  } catch (error) {
    throw new ApiError(500, 'Error deleting book', false, error.stack);
  }
};

const bulkUploadBooks = async (csvFile) => {
  try {
    const bookList = [];
    fs.createReadStream(csvFile)
     .pipe(csv())
     .on('data', (row) => {
        const bookData = {
          title: row.title,
          author: row.author,
          ISBN: row.ISBN,
          genre: row.genre,
          publicationYear: row.publicationYear,
          price: row.price,
          quantity: row.quantity,
          description: row.description,
          format: row.format,
        };
        bookList.push(bookData);
      })
     .on('end', async () => {
        const result = await bookRepository.bulkCreateBooks(bookList);
        return result;
      });
  } catch (error) {
    throw new ApiError(500, 'Error bulk uploading books', false, error.stack);
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
