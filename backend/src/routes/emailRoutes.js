import express from 'express';
import * as emailController from '../controllers/emailController.js';
import { validateEmailCreate } from '../validators/emailValidator.js';

const router = express.Router();

router.post('/', validateEmailCreate, emailController.create);
router.get('/', emailController.getAll);

export default router;
