// Import required modules
const request = require('supertest');
const app = require('../server');
const jest = require('jest');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');
const mongoose = require('mongoose');
const User = require('../models/user.model');
const userRepository = require('../repositories/userRepository');
const userService = require('../services/userService');
const userController = require('../controllers/userController');

// Mock dependencies
jest.mock('../repositories/userRepository');
jest.mock('../services/userService');

// Test suite for user functionalities
describe('User Functionalities', () => {
  // Test registration
  it('should register a new user', async () => {
    const userData = {
      email: 'test@example.com',
      password: 'password123',
      firstName: 'John',
      lastName: 'Doe',
      phoneNumber: '1234567890',
      address: '123 Main St',
    };

    // Mock user repository to return a new user
    userRepository.createUser.mockResolvedValue({
      _id: '1234567890',
      email: userData.email,
      password: await bcrypt.hash(userData.password, 10),
      firstName: userData.firstName,
      lastName: userData.lastName,
      phoneNumber: userData.phoneNumber,
      address: userData.address,
    });

    // Send a POST request to the registration endpoint
    const response = await request(app)
     .post('/api/register')
     .send(userData)
     .expect(201);

    // Assert the response contains the expected data
    expect(response.body).toHaveProperty('token');
    expect(response.body).toHaveProperty('user');
    expect(response.body.user).toHaveProperty('id');
    expect(response.body.user).toHaveProperty('email');
    expect(response.body.user).toHaveProperty('firstName');
    expect(response.body.user).toHaveProperty('lastName');
  });

  // Test login
  it('should login an existing user', async () => {
    const loginData = {
      email: 'test@example.com',
      password: 'password123',
    };

    // Mock user repository to return an existing user
    userRepository.getUserByEmail.mockResolvedValue({
      _id: '1234567890',
      email: loginData.email,
      password: await bcrypt.hash('password123', 10),
      firstName: 'John',
      lastName: 'Doe',
      phoneNumber: '1234567890',
      address: '123 Main St',
    });

    // Send a POST request to the login endpoint
    const response = await request(app)
     .post('/api/login')
     .send(loginData)
     .expect(200);

    // Assert the response contains the expected data
    expect(response.body).toHaveProperty('token');
    expect(response.body).toHaveProperty('user');
    expect(response.body.user).toHaveProperty('id');
    expect(response.body.user).toHaveProperty('email');
    expect(response.body.user).toHaveProperty('firstName');
    expect(response.body.user).toHaveProperty('lastName');
  });

  // Test profile update
  it('should update an existing user\'s profile', async () => {
    const updateData = {
      firstName: 'Jane',
      lastName: 'Doe',
      phoneNumber: '0987654321',
      address: '456 Elm St',
    };

    // Mock user repository to return an existing user
    userRepository.getUserById.mockResolvedValue({
      _id: '1234567890',
      email: 'test@example.com',
      password: await bcrypt.hash('password123', 10),
      firstName: 'John',
      lastName: 'Doe',
      phoneNumber: '1234567890',
      address: '123 Main St',
    });

    // Mock user repository to return an updated user
    userRepository.updateUser.mockResolvedValue({
      _id: '1234567890',
      email: 'test@example.com',
      password: await bcrypt.hash('password123', 10),
      firstName: updateData.firstName,
      lastName: updateData.lastName,
      phoneNumber: updateData.phoneNumber,
      address: updateData.address,
    });

    // Send a PUT request to the profile update endpoint
    const response = await request(app)
     .put('/api/user')
     .send(updateData)
     .set("Authorization", `Bearer ${jwt.sign({ userId: '1234567890' }, process.env.JWT_SECRET, { expiresIn: '24h' })}`)
     .expect(200);

    // Assert the response contains the expected data
    expect(response.body).toHaveProperty('firstName');
    expect(response.body).toHaveProperty('lastName');
    expect(response.body).toHaveProperty('phoneNumber');
    expect(response.body).toHaveProperty('address');
  });

  // Test error scenarios
  it('should return an error for invalid registration data', async () => {
    const userData = {
      email: 'invalid-email',
      password: 'password123',
      firstName: 'John',
      lastName: 'Doe',
      phoneNumber: '1234567890',
      address: '123 Main St',
    };

    // Send a POST request to the registration endpoint
    const response = await request(app)
     .post('/api/register')
     .send(userData)
     .expect(400);

    // Assert the response contains an error message
    expect(response.body).toHaveProperty('errors');
  });

  it('should return an error for invalid login credentials', async () => {
    const loginData = {
      email: 'test@example.com',
      password: 'invalid-password',
    };

    // Send a POST request to the login endpoint
    const response = await request(app)
     .post('/api/login')
     .send(loginData)
     .expect(401);

    // Assert the response contains an error message
    expect(response.body).toHaveProperty('error');
  });

  it('should return an error for unauthorized profile update', async () => {
    const updateData = {
      firstName: 'Jane',
      lastName: 'Doe',
      phoneNumber: '0987654321',
      address: '456 Elm St',
    };

    // Send a PUT request to the profile update endpoint without authentication
    const response = await request(app)
     .put('/api/user')
     .send(updateData)
     .expect(401);

    // Assert the response contains an error message
    expect(response.body).toHaveProperty('error');
  });
});

// Export the test suite
module.exports = {
  testUserFunctionalities: () => {
    describe('User Functionalities', () => {
      // Test suite for user functionalities
    });
  },
};
