import morgan from 'morgan';
import { config } from '../config/env.js';

// Custom format or standard formats depending on the environment
const logFormat = config.isProduction ? 'combined' : 'dev';

export const requestLogger = morgan(logFormat);
export default requestLogger;
