import client from 'prom-client';

const collectDefaultMetrics = client.collectDefaultMetrics;
const registry = new client.Registry();

collectDefaultMetrics({ registry });
registry.setDefaultLabels({ service: 'tatt-oo-backend' });

const httpRequestDurationSeconds = new client.Histogram({
  name: 'http_request_duration_seconds',
  help: 'Tempo de resposta das requisicoes HTTP em segundos',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.05, 0.1, 0.25, 0.5, 1, 2, 5],
  registers: [registry],
});

const httpRequestsTotal = new client.Counter({
  name: 'http_requests_total',
  help: 'Total de requisicoes HTTP recebidas',
  labelNames: ['method', 'route', 'status_code'],
  registers: [registry],
});

export { httpRequestDurationSeconds, httpRequestsTotal, registry };
