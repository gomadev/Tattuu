import dotenv from 'dotenv';

dotenv.config();

const port = Number(process.env.PORT ?? 3333);

export const env = {
  port,
};
