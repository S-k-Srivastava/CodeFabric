// Import required modules
const request = require('supertest');
const app = require('../server');
const bookService = require('../services/bookService');
const bookRepository = require('../repositories/bookRepository');
const validator = require('../utils/validator');
const { ApiError } = require('../utils/apiError');
const csv = require('csv-parser');
const fs = require('fs');
const jest = require('jest');

// Mock dependencies
jest.mock('../repositories/bookRepository');
jest.mock('../services/bookService');

// Test suite for book functionalities
describe('Book Functionalities', () => {
  // Test case for browsing books
  it('should browse books successfully', async () => {
    // Mock book repository to return a list of books
    bookRepository.getAllBooks.mockResolvedValue({
      books: [
        { title: 'Book 1', author: 'Author 1' },
        { title: 'Book 2', author: 'Author 2' },
      ],
      totalPages: 1,
      currentPage: 1,
    });

    // Send GET request to /api/books endpoint
    const response = await request(app).get('/api/books');

    // Assert expected response
    expect(response.status).toBe(200);
    expect(response.body).toEqual({
      books: [
        { title: 'Book 1', author: 'Author 1' },
        { title: 'Book 2', author: 'Author 2' },
      ],
      totalPages: 1,
      currentPage: 1,
    });
  });

  // Test case for searching books
  it('should search books successfully', async () => {
    // Mock book repository to return a list of books
    bookRepository.searchBooks.mockResolvedValue({
      books: [
        { title: 'Book 1', author: 'Author 1' },
        { title: 'Book 2', author: 'Author 2' },
      ],
      totalPages: 1,
      currentPage: 1,
    });

    // Send GET request to /api/search endpoint
    const response = await request(app).get('/api/search').query({ query: 'book' });

    // Assert expected response
    expect(response.status).toBe(200);
    expect(response.body).toEqual({
      books: [
        { title: 'Book 1', author: 'Author 1' },
        { title: 'Book 2', author: 'Author 2' },
      ],
      totalPages: 1,
      currentPage: 1,
    });
  });

  // Test case for adding a book
  it('should add a book successfully', async () => {
    // Mock book service to return a new book
    bookService.addBook.mockResolvedValue({ title: 'New Book', author: 'New Author' });

    // Send POST request to /api/admin/book endpoint
    const response = await request(app).post('/api/admin/book').send({ title: 'New Book', author: 'New Author' });

    // Assert expected response
    expect(response.status).toBe(201);
    expect(response.body).toEqual({ title: 'New Book', author: 'New Author' });
  });

  // Test case for updating a book
  it('should update a book successfully', async () => {
    // Mock book service to return an updated book
    bookService.updateBook.mockResolvedValue({ title: 'Updated Book', author: 'Updated Author' });

    // Send PUT request to /api/admin/book/:bookId endpoint
    const response = await request(app).put('/api/admin/book/1').send({ title: 'Updated Book', author: 'Updated Author' });

    // Assert expected response
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ title: 'Updated Book', author: 'Updated Author' });
  });

  // Test case for deleting a book
  it('should delete a book successfully', async () => {
    // Mock book service to return a success message
    bookService.deleteBook.mockResolvedValue({ message: 'Book deleted successfully' });

    // Send DELETE request to /api/admin/book/:bookId endpoint
    const response = await request(app).delete('/api/admin/book/1');

    // Assert expected response
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ message: 'Book deleted successfully' });
  });

  // Test case for bulk uploading books
  it('should bulk upload books successfully', async () => {
    // Mock book service to return a success message
    bookService.bulkUploadBooks.mockResolvedValue({ message: 'Books uploaded successfully', count: 2 });

    // Send POST request to /api/admin/books/bulk endpoint
    const response = await request(app).post('/api/admin/books/bulk').attach('file', 'books.csv');

    // Assert expected response
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ message: 'Books uploaded successfully', count: 2 });
  });

  // Test case for error scenario: invalid book data
  it('should return an error for invalid book data', async () => {
    // Mock book service to throw an error
    bookService.addBook.mockRejectedValue(new ApiError(400, 'Invalid book data'));

    // Send POST request to /api/admin/book endpoint
    const response = await request(app).post('/api/admin/book').send({});

    // Assert expected response
    expect(response.status).toBe(400);
    expect(response.body).toEqual({ message: 'Invalid book data' });
  });

  // Test case for error scenario: book not found
  it('should return an error for book not found', async () => {
    // Mock book service to throw an error
    bookService.updateBook.mockRejectedValue(new ApiError(404, 'Book not found'));

    // Send PUT request to /api/admin/book/:bookId endpoint
    const response = await request(app).put('/api/admin/book/1').send({});

    // Assert expected response
    expect(response.status).toBe(404);
    expect(response.body).toEqual({ message: 'Book not found' });
  });
});

// Export all functions explicitly as named functions
module.exports = {
  browseBooks,
  searchBooks,
  addBook,
  updateBook,
  deleteBook,
  bulkUploadBooks,
};
