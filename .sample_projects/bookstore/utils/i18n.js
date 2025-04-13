// Import required modules
const i18n = require('i18n-node');

// Initialize and configure i18n-node for internationalization
i18n.configure({
  locales: ['en', 'es'],
  directory: './locales',
  defaultLocale: 'en',
  fallbacks: { 'es': 'en' },
  indent: '  ',
  objectNotation: true,
  register: global,
});

// Function to detect locale based on user settings or request headers
function detectLocale(req) {
  try {
    // Check if locale is set in request headers
    const locale = req.headers['accept-language'];
    if (locale) {
      // Extract the first two characters (language code) from the locale string
      const langCode = locale.substring(0, 2);
      // Check if the language code is supported
      if (i18n.getLocales().includes(langCode)) {
        return langCode;
      }
    }
    // If locale is not set in request headers, use the default locale
    return i18n.getDefaultLocale();
  } catch (error) {
    // Log any errors that occur during locale detection
    console.error('Error detecting locale:', error);
    return i18n.getDefaultLocale();
  }
}

// Function to get a translated string
function getTranslation(locale, key) {
  try {
    // Set the locale for the current request
    i18n.setLocale(locale);
    // Get the translated string
    return i18n.__({ phrase: key });
  } catch (error) {
    // Log any errors that occur during translation
    console.error('Error getting translation:', error);
    return key;
  }
}

// Function to get a translated string with placeholders
function getTranslationWithPlaceholders(locale, key, placeholders) {
  try {
    // Set the locale for the current request
    i18n.setLocale(locale);
    // Get the translated string with placeholders
    return i18n.__({ phrase: key, locale: locale }, placeholders);
  } catch (error) {
    // Log any errors that occur during translation
    console.error('Error getting translation with placeholders:', error);
    return key;
  }
}

// Export functions explicitly as named functions
module.exports = {
  detectLocale,
  getTranslation,
  getTranslationWithPlaceholders,
};
