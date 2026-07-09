import { PrismaClient } from '@prisma/client';
import { config } from '../config/env.js';

let prisma;

if (config.isProduction) {
  prisma = new PrismaClient();
} else {
  // Prevent multiple instances of Prisma Client in development due to hot reloading
  if (!global.__prisma) {
    global.__prisma = new PrismaClient({
      log: ['query', 'info', 'warn', 'error'],
    });
  }
  prisma = global.__prisma;
}

export { prisma };
export default prisma;
