param(
    [string]$BackendUrl = "http://localhost:8000"
)

Write-Host "Starting Flashoot website crawl..." -ForegroundColor Green
Write-Host "Backend URL: $BackendUrl" -ForegroundColor Gray

try {
    $response = Invoke-RestMethod -Uri "$BackendUrl/ingest" -Method Post -ContentType "application/json" -Body '{}'
    Write-Host "Crawl complete!" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json) -ForegroundColor Cyan
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
    exit 1
}
