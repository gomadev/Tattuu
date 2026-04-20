import cors from 'cors';
import express from 'express';

import { env } from './config/env';
import { httpRequestDurationSeconds, httpRequestsTotal } from './monitoring/metrics';
import { router } from './routes';

const app = express();

app.disable('x-powered-by');

app.use(cors({ origin: env.corsOrigin }));
app.use(express.json());

app.use((req, res, next) => {
	const start = process.hrtime.bigint();

	res.on('finish', () => {
		const durationSeconds = Number(process.hrtime.bigint() - start) / 1_000_000_000;
		const route = req.route?.path ?? req.path;
		const statusCode = String(res.statusCode);

		httpRequestDurationSeconds.observe(
			{ method: req.method, route, status_code: statusCode },
			durationSeconds,
		);
		httpRequestsTotal.inc({ method: req.method, route, status_code: statusCode });
	});

	next();
});

app.use('/api', router);

export { app };
