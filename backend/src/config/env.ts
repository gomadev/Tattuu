import dotenv from 'dotenv';

dotenv.config();

const port = Number(process.env.PORT ?? 3333);
const corsOrigin = process.env.CORS_ORIGIN ?? 'http://localhost:8080';
const nodeEnv = process.env.NODE_ENV ?? 'development';

export const env = {
  port,
  corsOrigin,
  nodeEnv,
};
