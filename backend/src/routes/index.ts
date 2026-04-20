import { Router } from 'express';

import { registry } from '../monitoring/metrics';

const router = Router();

router.get('/health', (_req, res) => {
  res.status(200).json({
    status: 'ok',
    service: 'tatt-oo-backend',
    timestamp: new Date().toISOString(),
  });
});

router.get('/metrics', async (_req, res) => {
  res.setHeader('Content-Type', registry.contentType);
  res.status(200).send(await registry.metrics());
});

export { router };
