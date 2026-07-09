import { body } from 'express-validator';
import { handleValidationErrors } from '../middlewares/validationHandler.js';

export const validateEmailCreate = [
  body('body').notEmpty().withMessage('Email body is required'),
  body('subject').optional().trim(),
  body('sentiment')
    .optional()
    .isIn(['POSITIVE', 'NEUTRAL', 'NEGATIVE'])
    .withMessage('Invalid sentiment value'),
  body('sentimentScore')
    .optional()
    .isFloat({ min: -1, max: 1 })
    .withMessage('Sentiment score must be a number between -1 and 1'),
  body('userId').isUUID().withMessage('User ID must be a valid UUID'),
  body('customerId').isUUID().withMessage('Customer ID must be a valid UUID'),
  body('dealId').optional().isUUID().withMessage('Deal ID must be a valid UUID'),
  handleValidationErrors,
];
