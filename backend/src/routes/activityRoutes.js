import express from 'express';
import * as activityController from '../controllers/activityController.js';
import { validateActivityCreate } from '../validators/activityValidator.js';

const router = express.Router();

router.post('/', validateActivityCreate, activityController.create);
router.get('/', activityController.getAll);

export default router;
