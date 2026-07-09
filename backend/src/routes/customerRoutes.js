import express from 'express';
import * as customerController from '../controllers/customerController.js';
import { validateCustomerCreate } from '../validators/customerValidator.js';

const router = express.Router();

router.post('/', validateCustomerCreate, customerController.create);
router.get('/', customerController.getAll);

export default router;
