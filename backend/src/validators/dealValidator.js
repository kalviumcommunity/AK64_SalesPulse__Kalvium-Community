import { body } from 'express-validator';
import { handleValidationErrors } from '../middlewares/validationHandler.js';

export const validateDealCreate = [
  body('title').trim().notEmpty().withMessage('Deal title is required'),
  body('amount').isNumeric().withMessage('Deal amount must be a number'),
  body('stage')
    .optional()
    .isIn(['PROSPECT', 'QUALIFICATION', 'PROPOSAL', 'NEGOTIATION', 'CLOSED_WON', 'CLOSED_LOST'])
    .withMessage('Invalid deal stage'),
  body('userId').isUUID().withMessage('Assigned User ID must be a valid UUID'),
  body('customerId').isUUID().withMessage('Customer ID must be a valid UUID'),
  handleValidationErrors,
];
