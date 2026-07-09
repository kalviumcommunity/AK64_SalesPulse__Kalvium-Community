import dealService from '../services/dealService.js';
import { catchAsync } from '../utils/catchAsync.js';
import { successResponse } from '../utils/apiResponse.js';

export const create = catchAsync(async (req, res, next) => {
  const result = await dealService.createDeal(req.body);
  return successResponse(res, 'Deal created successfully (placeholder)', result, 201);
});

export const getAll = catchAsync(async (req, res, next) => {
  const result = await dealService.getDeals();
  return successResponse(res, 'Deals fetched successfully (placeholder)', result);
});
