const fs = require('fs');
const path = require('path');

const srcDir = path.resolve(__dirname, '..', 'src');
const distDir = path.resolve(__dirname, '..', 'dist');

console.log('Building frontend to dist/...');

// Clean dist
if (fs.existsSync(distDir)) {
  fs.rmSync(distDir, { recursive: true, force: true });
}

// Ensure dist exists
fs.mkdirSync(distDir, { recursive: true });

// Copy all files from src to dist
fs.cpSync(srcDir, distDir, { recursive: true });

console.log('Frontend build completed successfully!');

