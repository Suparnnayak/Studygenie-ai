# Quick test - Copy and paste this entire block into PowerShell

$filePath = "Samples\syllabus.pdf"
$apiUrl = "https://studygenie-ai.onrender.com/api/upload-pdf"

Write-Host "📤 Uploading $filePath..." -ForegroundColor Cyan

$resolvedPath = (Resolve-Path $filePath).Path
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

try {
    Write-Host "⏳ Sending request (may take 30-60s on first request)..." -ForegroundColor Yellow
    $response = Invoke-RestMethod -Uri $apiUrl -Method POST -Body $bodyBytes -Headers $headers -TimeoutSec 180
    
    Write-Host "`n✅ SUCCESS!" -ForegroundColor Green
    Write-Host "Topics: $($response.skill_map.total_topics)" -ForegroundColor Cyan
    Write-Host "Quiz Questions: $($response.quiz.total_questions)" -ForegroundColor Cyan
    Write-Host "Interview Questions: $($response.interview_qa.total_questions)" -ForegroundColor Cyan
    
    $response | ConvertTo-Json -Depth 10 | Out-File "response.json" -Encoding UTF8
    Write-Host "`n💾 Full response saved to response.json" -ForegroundColor Green
} catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "Status: $statusCode" -ForegroundColor Red
    }
}

