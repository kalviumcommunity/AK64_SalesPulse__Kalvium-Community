import activityService from '../services/activityService.js';
import { catchAsync } from '../utils/catchAsync.js';
import { successResponse } from '../utils/apiResponse.js';

export const create = catchAsync(async (req, res, next) => {
  const result = await activityService.logActivity(req.body);
  return successResponse(res, 'Activity logged successfully (placeholder)', result, 201);
});

export const getAll = catchAsync(async (req, res, next) => {
  const result = await activityService.getActivities();
  return successResponse(res, 'Activities fetched successfully (placeholder)', result);
});
