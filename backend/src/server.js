import app from './app.js';
import { config } from './config/env.js';

// Handle Uncaught Exceptions globally
process.on('uncaughtException', (err) => {
  console.error('UNCAUGHT EXCEPTION! Shutting down server...');
  console.error(err.name, err.message, err.stack);
  process.exit(1);
});

const server = app.listen(config.port, () => {
  console.log(`==================================================`);
  console.log(` SalesPulse AI Backend running on port ${config.port}`);
  console.log(` Environment: ${config.nodeEnv}`);
  console.log(` API Base URL: http://localhost:${config.port}/api/v1`);
  console.log(`==================================================`);
});

// Handle Unhandled Rejections globally
process.on('unhandledRejection', (err) => {
  console.error('UNHANDLED REJECTION! Shutting down server...');
  console.error(err);
  server.close(() => {
    process.exit(1);
  });
});
