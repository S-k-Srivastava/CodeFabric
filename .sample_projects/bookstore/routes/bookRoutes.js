// Import required modules
const express = require('express');
const router = express.Router();
const bookController = require('../controllers/bookController');
const authMiddleware = require('../middlewares/auth.middleware');
const requestValidatorMiddleware = require('../middlewares/requestValidator.middleware');

// Define routes for book catalog endpoints
router.get('/books', bookController.browseBooks);
router.get('/search', bookController.searchBooks);

// Apply authentication middleware for admin routes
router.use('/admin', authMiddleware.authenticate, authMiddleware.authorize('admin'));

// Define admin routes for book management
router.post('/admin/book', requestValidatorMiddleware.bookValidationMiddleware, bookController.addBook);
router.put('/admin/book/:bookId', requestValidatorMiddleware.bookValidationMiddleware, bookController.updateBook);
router.delete('/admin/book/:bookId', bookController.deleteBook);
router.post('/admin/books/bulk', bookController.bulkUploadBooks);

// Export the router
module.exports = router;
