const jwt = require('jsonwebtoken');
const config = require('../config/config');
const userRepository = require('../repositories/userRepository');
const { ApiError } = require('../utils/apiError');

const authenticate = async (req, res, next) => {
  try {
    const token = req.header('Authorization').replace('Bearer ', '');
    const decoded = jwt.verify(token, config.jwtSecret);
    const user = await userRepository.getUserById(decoded._id);
    if (!user) {
      throw new ApiError(401, 'Please authenticate');
    }
    req.user = user;
    next();
  } catch (error) {
    next(new ApiError(401, 'Please authenticate'));
  }
};

const authorize = (...roles) => {
  return (req, res, next) => {
    if (!roles.includes(req.user.role)) {
      next(new ApiError(403, 'Forbidden'));
    } else {
      next();
    }
  };
};

module.exports = { authenticate, authorize };
