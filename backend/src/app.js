import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import cookieParser from 'cookie-parser';

import requestLogger from './middlewares/requestLogger.js';
import { notFoundHandler } from './middlewares/notFoundHandler.js';
import { errorHandler } from './middlewares/errorHandler.js';
import apiRouter from './routes/index.js';

const app = express();

// Security Middlewares
app.use(helmet());
app.use(cors({
  origin: true, // Allow all origins for development; customize as needed
  credentials: true,
}));

// Utility Middlewares
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(requestLogger);

// Health Check API
app.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    message: 'SalesPulse Backend Running',
  });
});

// Versioned Routes
app.use('/api/v1', apiRouter);

// Error Handling Middlewares
app.use(notFoundHandler);
app.use(errorHandler);

export default app;
export { app };
