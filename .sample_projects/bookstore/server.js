// Import required modules
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const mongoose = require('mongoose');
const config = require('./config/config');
const logger = require('./utils/logger');
const db = require('./db/mongoose');
const securityMiddlewares = require('./middlewares/security');
const rateLimiter = require('./middlewares/rateLimiter');
const apiRoutes = require('./routes/index');
const swaggerRouter = require('./docs/swagger');
const errorHandler = require('./utils/errorHandler');

// Set up Express app
const app = express();

// Load configurations
const port = config.port;

// Initialize logger
logger.info('Server starting...');

// Connect to MongoDB
db.initDB();

// Apply middlewares
app.use(cors());
app.use(morgan('dev'));
app.use(securityMiddlewares.securityHeadersMiddleware());
app.use(rateLimiter.loginLimiter);
app.use(rateLimiter.resetPasswordLimiter);
app.use(express.json());

// Mount API routes
app.use('/api', apiRoutes.mainRouter);

// Set up Swagger documentation endpoint
app.use('/api-docs', swaggerRouter.swaggerRouter);

// Apply global error handling middleware
app.use(errorHandler.errorHandler);

// Start the server and listen on port
const server = app.listen(port, () => {
  logger.info(`Server listening on port ${port}`);
});

// Handle server startup errors
server.on('error', (error) => {
  logger.error('Server startup error:', error);
  process.exit(1);
});

// Export the server
module.exports = {
  server,
  app,
};
