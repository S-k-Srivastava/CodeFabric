const mongoose = require('mongoose');
const config = require('../config/config');
const logger = require('../utils/logger');

const connectDB = async () => {
  try {
    await mongoose.connect(config.databaseUri, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    logger.info('MongoDB connected');
  } catch (error) {
    logger.error('MongoDB connection error:', error);
    process.exit(1);
  }
};mongoose.connection.on('connected', () => {
  logger.info('Mongoose connected to DB');
});

mongoose.connection.on('error', (err) => {
  logger.error('Mongoose connection error:', err);
});

mongoose.connection.on('disconnected', () => {
  logger.info('Mongoose disconnected from DB');
});

mongoose.connection.on('reconnected', () => {
  logger.info('Mongoose reconnected to DB');
});

const initDB = async () => {
  await connectDB();
};

module.exports = {
  initDB,
};
