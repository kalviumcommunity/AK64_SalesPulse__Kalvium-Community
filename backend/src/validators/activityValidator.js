import { body } from 'express-validator';
import { handleValidationErrors } from '../middlewares/validationHandler.js';

export const validateActivityCreate = [
  body('type')
    .isIn(['CALL', 'MEETING', 'TASK', 'NOTE', 'EMAIL'])
    .withMessage('Invalid activity type'),
  body('description').optional().trim(),
  body('userId').isUUID().withMessage('User ID must be a valid UUID'),
  body('customerId').optional().isUUID().withMessage('Customer ID must be a valid UUID'),
  body('dealId').optional().isUUID().withMessage('Deal ID must be a valid UUID'),
  handleValidationErrors,
];
