import recommendationService from '../services/recommendationService.js';
import { catchAsync } from '../utils/catchAsync.js';
import { successResponse } from '../utils/apiResponse.js';

export const create = catchAsync(async (req, res, next) => {
  const result = await recommendationService.generateRecommendation(req.body);
  return successResponse(res, 'Recommendation created successfully (placeholder)', result, 201);
});

export const getAll = catchAsync(async (req, res, next) => {
  const result = await recommendationService.getRecommendations();
  return successResponse(res, 'Recommendations fetched successfully (placeholder)', result);
});
