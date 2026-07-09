import { body } from 'express-validator';
import { handleValidationErrors } from '../middlewares/validationHandler.js';

export const validateCustomerCreate = [
  body('name').trim().notEmpty().withMessage('Customer name is required'),
  body('email').isEmail().withMessage('A valid email address is required').normalizeEmail(),
  body('company').optional().trim(),
  body('phone').optional().trim(),
  handleValidationErrors,
];
