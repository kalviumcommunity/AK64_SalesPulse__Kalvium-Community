import express from 'express';
import * as recommendationController from '../controllers/recommendationController.js';
import { validateRecommendationCreate } from '../validators/recommendationValidator.js';

const router = express.Router();

router.post('/', validateRecommendationCreate, recommendationController.create);
router.get('/', recommendationController.getAll);

export default router;
