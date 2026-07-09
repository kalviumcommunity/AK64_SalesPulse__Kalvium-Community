import { AppError } from '../utils/appError.js';

export const notFoundHandler = (req, res, next) => {
  next(new AppError(`Cannot find ${req.originalUrl} on this server.`, 404));
};
