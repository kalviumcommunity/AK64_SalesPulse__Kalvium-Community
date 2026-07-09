import dotenv from 'dotenv';
import path from 'path';

// Load environment variables
dotenv.config();

const requiredEnv = ['DATABASE_URL', 'JWT_SECRET'];

for (const envVar of requiredEnv) {
  if (!process.env[envVar]) {
    throw new Error(`CRITICAL: Environment variable ${envVar} is missing.`);
  }
}

export const config = {
  port: parseInt(process.env.PORT || '5000', 10),
  databaseUrl: process.env.DATABASE_URL,
  jwtSecret: process.env.JWT_SECRET,
  nodeEnv: process.env.NODE_ENV || 'development',
  isProduction: process.env.NODE_ENV === 'production',
  isDevelopment: process.env.NODE_ENV === 'development' || !process.env.NODE_ENV,
};
