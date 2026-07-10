import userService from '../services/userService.js';
import { catchAsync } from '../utils/catchAsync.js';
import { successResponse } from '../utils/apiResponse.js';

export const register = catchAsync(async (req, res, next) => {
  const result = await userService.registerUser(req.body);
  return successResponse(res, 'User registered successfully (placeholder)', result, 201);
});

export const login = catchAsync(async (req, res, next) => {
  const result = await userService.loginUser(req.body);
  return successResponse(res, 'User logged in successfully (placeholder)', result);
});

export const getProfile = catchAsync(async (req, res, next) => {
  // Normally would get id from req.user (JWT)
  const result = await userService.getUserById(req.params.id);
  return successResponse(res, 'User profile fetched successfully (placeholder)', result);
});
