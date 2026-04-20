docker compose up -d --build
Write-Host 'Frontend: http://localhost:8080'
Write-Host 'Backend health: http://localhost:3333/api/health'
Write-Host 'Metrics: http://localhost:3333/api/metrics'
Write-Host 'Prometheus: http://localhost:9090'
Write-Host 'Grafana: http://localhost:3000 (admin/admin)'
Write-Host 'Adminer: http://localhost:8081'
