import analyticsService from '../services/analyticsService.js';
import { catchAsync } from '../utils/catchAsync.js';
import { successResponse } from '../utils/apiResponse.js';

export const getSummary = catchAsync(async (req, res, next) => {
  const result = await analyticsService.getDashboardSummary();
  return successResponse(res, 'Analytics dashboard summary fetched successfully (placeholder)', result);
});

export const getPerformance = catchAsync(async (req, res, next) => {
  const result = await analyticsService.getPerformanceMetrics();
  return successResponse(res, 'Analytics team performance metrics fetched successfully (placeholder)', result);
});
