const validateEmail = (email) => {
  if (!email) {
    return false;
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

const validatePassword = (password) => {
  if (!password) {
    return false;
  }  if (password.length < 8) {
    return false;
  }
  const passwordRegex = /^(?=.*[a-zA-Z])(?=.*[0-9])/;
  return passwordRegex.test(password);};

const sanitizeInput = (input) => {
  if (!input) {
    return '';
  }
  let sanitizedInput = input.trim();
  sanitizedInput = sanitizedInput.replace(/</g, '&lt;').replace(/>/g, '&gt;');
  return sanitizedInput;};

module.exports = {
  validateEmail,
  validatePassword,
  sanitizeInput,
};
