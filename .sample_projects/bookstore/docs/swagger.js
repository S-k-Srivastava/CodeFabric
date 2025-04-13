// Import required modules
const express = require('express');
const swaggerJsdoc = require('swagger-jsdoc');
const swaggerUi = require('swagger-ui-express');
const config = require('../config/config');

// Define Swagger options
const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'Book Manager API',
      version: '1.0.0',
      description: 'API documentation for the Book Manager application',
    },
    servers: [
      {
        url: `http://localhost:${config.port}/api`,
        description: 'Development server',
      },
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'JWT',
        },
      },
    },
    tags: [
      {
        name: 'User Management',
        description: 'Endpoints for user registration, login, and profile management',
      },
      {
        name: 'Book Catalog',
        description: 'Endpoints for browsing and searching books',
      },
      {
        name: 'Shopping Cart',
        description: 'Endpoints for managing shopping cart',
      },
      {
        name: 'Order Processing',
        description: 'Endpoints for placing and managing orders',
      },
      {
        name: 'Admin Dashboard',
        description: 'Endpoints for admin dashboard',
      },
    ],
  },
  apis: ['./routes/*.js'],
};

// Configure Swagger documentation
const specs = swaggerJsdoc(options);

// Create an Express router for Swagger UI
const swaggerRouter = express.Router();

// Set up Swagger UI endpoint
swaggerRouter.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));

// Export the Swagger router
module.exports = { swaggerRouter };
