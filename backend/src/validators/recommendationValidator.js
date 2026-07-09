import { body } from 'express-validator';
import { handleValidationErrors } from '../middlewares/validationHandler.js';

export const validateRecommendationCreate = [
  body('userId').isUUID().withMessage('User ID must be a valid UUID'),
  body('dealId').optional().isUUID().withMessage('Deal ID must be a valid UUID'),
  body('content').trim().notEmpty().withMessage('Recommendation content is required'),
  body('score').optional().isFloat({ min: 0, max: 1 }).withMessage('Score must be between 0 and 1'),
  handleValidationErrors,
];
