$frontend = Invoke-WebRequest -Uri 'http://localhost:8080/' -UseBasicParsing
$health = Invoke-WebRequest -Uri 'http://localhost:3333/api/health' -UseBasicParsing
$metrics = Invoke-WebRequest -Uri 'http://localhost:3333/api/metrics' -UseBasicParsing

if ($frontend.StatusCode -ne 200) { throw 'Frontend indisponivel' }
if ($health.StatusCode -ne 200) { throw 'Backend indisponivel' }
if ($metrics.StatusCode -ne 200) { throw 'Metrics indisponivel' }

Write-Host 'Smoke test concluido com sucesso.'
