import emailService from '../services/emailService.js';
import { catchAsync } from '../utils/catchAsync.js';
import { successResponse } from '../utils/apiResponse.js';

export const create = catchAsync(async (req, res, next) => {
  const result = await emailService.analyzeEmail(req.body);
  return successResponse(res, 'Email logged and analyzed successfully (placeholder)', result, 201);
});

export const getAll = catchAsync(async (req, res, next) => {
  const result = await emailService.getEmails();
  return successResponse(res, 'Emails fetched successfully (placeholder)', result);
});
