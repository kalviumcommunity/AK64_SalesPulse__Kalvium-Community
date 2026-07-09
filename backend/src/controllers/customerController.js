import customerService from '../services/customerService.js';
import { catchAsync } from '../utils/catchAsync.js';
import { successResponse } from '../utils/apiResponse.js';

export const create = catchAsync(async (req, res, next) => {
  const result = await customerService.createCustomer(req.body);
  return successResponse(res, 'Customer created successfully (placeholder)', result, 201);
});

export const getAll = catchAsync(async (req, res, next) => {
  const result = await customerService.getCustomers();
  return successResponse(res, 'Customers fetched successfully (placeholder)', result);
});
