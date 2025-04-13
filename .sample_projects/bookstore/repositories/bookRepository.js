const { Book } = require('../models/book.model');

const createBook = async (bookData) => {
  try {
    const newBook = new Book(bookData);
    await newBook.save();
    return newBook;
  } catch (error) {
    throw new Error('Error creating book');
  }
};

const getBookById = async (bookId) => {
  try {
    const book = await Book.findById(bookId);
    return book;
  } catch (error) {
    throw new Error('Error fetching book by ID');
  }
};

const getAllBooks = async (page = 1, limit = 10, filter = {}, sort = {}) => {
  try {
    const skip = (page - 1) * limit;
    const books = await Book.find(filter).sort(sort).skip(skip).limit(limit);
    const totalBooks = await Book.countDocuments(filter);
    const totalPages = Math.ceil(totalBooks / limit);
    return {
      books,
      totalPages,
      currentPage: page,
    };
  } catch (error) {
    throw new Error('Error fetching all books');
  }
};

const updateBook = async (bookId, updateData) => {
  try {
    const updatedBook = await Book.findByIdAndUpdate(bookId, updateData, { new: true });
    return updatedBook;
  } catch (error) {    throw new Error('Error updating book');
  }
};

const deleteBook = async (bookId) => {
  try {
    await Book.findByIdAndDelete(bookId);
    return { message: 'Book deleted successfully' };
  } catch (error) {
    throw new Error('Error deleting book');
  }
};

const searchBooks = async (query, page = 1, limit = 10) => {
  try {
    const skip = (page - 1) * limit;
    const filter = {
      $or: [
        { title: { $regex: query, $options: 'i' } },
        { author: { $regex: query, $options: 'i' } },
        { ISBN: { $regex: query, $options: 'i' } },
      ],
    };
    const books = await Book.find(filter).skip(skip).limit(limit);
    const totalBooks = await Book.countDocuments(filter);
    const totalPages = Math.ceil(totalBooks / limit);
    return {
      books,
      totalPages,
      currentPage: page,
    };
  } catch (error) {
    throw new Error('Error searching books');  }
};

const getBooksByGenre = async (genre, page = 1, limit = 10) => {
  try {
    const skip = (page - 1) * limit;
    const filter = { genre: genre };
    const books = await Book.find(filter).skip(skip).limit(limit);
    const totalBooks = await Book.countDocuments(filter);
    const totalPages = Math.ceil(totalBooks / limit);
    return {
      books,
      totalPages,
      currentPage: page,
    };
  } catch (error) {
    throw new Error('Error fetching books by genre');
  }
};

const bulkCreateBooks = async (bookList) => {  try {
    const result = await Book.insertMany(bookList);
    return result;
  } catch (error) {
    throw new Error('Error bulk creating books');
  }
};

module.exports = {
  createBook,
  getBookById,
  getAllBooks,
  updateBook,
  deleteBook,
  searchBooks,
  getBooksByGenre,
  bulkCreateBooks,};
