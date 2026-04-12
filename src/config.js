// Configuration for different environments
const CONFIG = {
  development: {
    API_BASE: 'http://localhost:8000/api',
    DEBUG: true,
  },
  production: {
    API_BASE: 'https://thuvienso-api.herokuapp.com/api', // Change to your backend URL
    DEBUG: false,
  },
  staging: {
    API_BASE: 'https://thuvienso-staging-api.herokuapp.com/api', // Change if needed
    DEBUG: false,
  },
};

// Get current environment from URL or default to production
function getEnvironment() {
  const hostname = window.location.hostname;
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'development';
  }
  // Add your staging domain here if needed
  if (hostname.includes('staging')) {
    return 'staging';
  }
  return 'production';
}

// Get config for current environment
const ENVIRONMENT = getEnvironment();
const API_BASE = CONFIG[ENVIRONMENT].API_BASE;
const DEBUG = CONFIG[ENVIRONMENT].DEBUG;

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { API_BASE, DEBUG, ENVIRONMENT, CONFIG };
}
