import express from 'express';
import userRoutes from './userRoutes.js';
import customerRoutes from './customerRoutes.js';
import dealRoutes from './dealRoutes.js';
import activityRoutes from './activityRoutes.js';
import emailRoutes from './emailRoutes.js';
import analyticsRoutes from './analyticsRoutes.js';
import recommendationRoutes from './recommendationRoutes.js';

const router = express.Router();

// Mount modules
router.use('/users', userRoutes);
router.use('/customers', customerRoutes);
router.use('/deals', dealRoutes);
router.use('/activities', activityRoutes);
router.use('/emails', emailRoutes);
router.use('/analytics', analyticsRoutes);
router.use('/recommendations', recommendationRoutes);

export default router;
