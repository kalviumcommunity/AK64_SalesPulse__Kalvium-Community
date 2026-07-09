import { body } from 'express-validator';
import { handleValidationErrors } from '../middlewares/validationHandler.js';

export const validateUserRegistration = [
  body('email').isEmail().withMessage('Please provide a valid email address').normalizeEmail(),
  body('password').isLength({ min: 6 }).withMessage('Password must be at least 6 characters long'),
  body('name').trim().notEmpty().withMessage('Name is required'),
  body('role')
    .optional()
    .isIn(['ADMIN', 'MANAGER', 'REPRESENTATIVE'])
    .withMessage('Role must be one of: ADMIN, MANAGER, REPRESENTATIVE'),
  handleValidationErrors,
];

export const validateUserLogin = [
  body('email').isEmail().withMessage('Please provide a valid email address').normalizeEmail(),
  body('password').notEmpty().withMessage('Password is required'),
  handleValidationErrors,
];
