import express from 'express';
import * as dealController from '../controllers/dealController.js';
import { validateDealCreate } from '../validators/dealValidator.js';

const router = express.Router();

router.post('/', validateDealCreate, dealController.create);
router.get('/', dealController.getAll);

export default router;
