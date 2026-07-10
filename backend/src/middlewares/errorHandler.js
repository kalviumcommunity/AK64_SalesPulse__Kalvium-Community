import { config } from '../config/env.js';

export const errorHandler = (err, req, res, next) => {
  err.statusCode = err.statusCode || 500;
  err.status = err.status || 'error';

  // Log the full error internally in development
  if (config.isDevelopment) {
    console.error('Error Details:', err);
  }

  // Handle Prisma unique constraint violation
  if (err.code === 'P2002') {
    const fields = err.meta?.target || [];
    return res.status(400).json({
      success: false,
      message: `Duplicate field value for: ${fields.join(', ')}`,
      errors: err.meta,
    });
  }

  // Handle Prisma record not found
  if (err.code === 'P2025') {
    return res.status(404).json({
      success: false,
      message: err.meta?.cause || 'Record not found',
    });
  }

  // Default Express JSON parser error
  if (err instanceof SyntaxError && err.status === 400 && 'body' in err) {
    return res.status(400).json({
      success: false,
      message: 'Invalid JSON payload format.',
    });
  }

  // Production vs Development error responses
  if (config.isDevelopment) {
    return res.status(err.statusCode).json({
      success: false,
      message: err.message,
      stack: err.stack,
      error: err,
    });
  } else {
    // Production - don't leak database/internal details for non-operational errors
    if (err.isOperational) {
      return res.status(err.statusCode).json({
        success: false,
        message: err.message,
      });
    }

    return res.status(500).json({
      success: false,
      message: 'Something went wrong on our end. Please try again later.',
    });
  }
};
