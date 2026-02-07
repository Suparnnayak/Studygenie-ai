# Simple test script for the upload endpoint
# Usage: .\test_upload_simple.ps1 "path\to\file.pdf"

param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

$apiUrl = "https://studygenie-ai.onrender.com/api/upload-pdf"

if (-not (Test-Path $FilePath)) {
    Write-Host "❌ File not found: $FilePath" -ForegroundColor Red
    exit 1
}

$resolvedPath = (Resolve-Path $FilePath).Path
Write-Host "📤 Uploading: $resolvedPath" -ForegroundColor Cyan
Write-Host "🌐 URL: $apiUrl" -ForegroundColor Cyan
Write-Host "⏳ This may take 30-60 seconds (first request wakes up free tier service)..." -ForegroundColor Yellow

try {
    # Create multipart form data
    $boundary = [System.Guid]::NewGuid().ToString()
    $fileBytes = [System.IO.File]::ReadAllBytes($resolvedPath)
    $fileName = [System.IO.Path]::GetFileName($resolvedPath)
    
    $bodyLines = @(
        "--$boundary",
        "Content-Disposition: form-data; name=`"file`"; filename=`"$fileName`"",
        "Content-Type: application/pdf",
        "",
        [System.Text.Encoding]::GetEncoding("iso-8859-1").GetString($fileBytes),
        "--$boundary",
        "Content-Disposition: form-data; name=`"quiz_questions`"",
        "",
        "10",
        "--$boundary",
        "Content-Disposition: form-data; name=`"interview_questions`"",
        "",
        "10",
        "--$boundary--"
    )
    
    $body = $bodyLines -join "`r`n"
    $bodyBytes = [System.Text.Encoding]::GetEncoding("iso-8859-1").GetBytes($body)
    
    $headers = @{
        "Content-Type" = "multipart/form-data; boundary=$boundary"
    }
    
    Write-Host "`n🚀 Sending POST request..." -ForegroundColor Green
    
    $response = Invoke-RestMethod -Uri $apiUrl -Method POST -Body $bodyBytes -Headers $headers -TimeoutSec 180
    
    Write-Host "`n✅ SUCCESS!" -ForegroundColor Green
    Write-Host "`n📊 Results:" -ForegroundColor Cyan
    Write-Host "  Skill Map Topics: $($response.skill_map.total_topics)" -ForegroundColor White
    Write-Host "  Quiz Questions: $($response.quiz.total_questions)" -ForegroundColor White
    Write-Host "  Interview Questions: $($response.interview_qa.total_questions)" -ForegroundColor White
    
    Write-Host "`n💾 Saving full response to response.json..." -ForegroundColor Yellow
    $response | ConvertTo-Json -Depth 10 | Out-File -FilePath "response.json" -Encoding UTF8
    Write-Host "✅ Saved!" -ForegroundColor Green
    
} catch {
    Write-Host "`n❌ ERROR:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "Status Code: $statusCode" -ForegroundColor Red
        
        if ($statusCode -eq 405) {
            Write-Host "`n💡 This endpoint requires POST method, not GET" -ForegroundColor Yellow
        } elseif ($statusCode -eq 502) {
            Write-Host "`n💡 Service is waking up. Wait 30-60 seconds and try again." -ForegroundColor Yellow
        }
        
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            Write-Host "Response: $responseBody" -ForegroundColor Red
        } catch {}
    }
}

