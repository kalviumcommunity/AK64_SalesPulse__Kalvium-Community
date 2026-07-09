import express from 'express';
import * as userController from '../controllers/userController.js';
import { validateUserRegistration, validateUserLogin } from '../validators/userValidator.js';

const router = express.Router();

router.post('/register', validateUserRegistration, userController.register);
router.post('/login', validateUserLogin, userController.login);
router.get('/:id', userController.getProfile);

export default router;
