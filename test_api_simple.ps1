# Simple PowerShell script to test API - Alternative method
# Usage: .\test_api_simple.ps1 "path\to\file.pdf"

param(
    [Parameter(Mandatory=$true)]
    [string]$FilePath
)

$apiUrl = "https://studygenie-ai.onrender.com/api/upload-pdf"

if (-not (Test-Path $FilePath)) {
    Write-Host "Error: File not found: $FilePath" -ForegroundColor Red
    exit 1
}

Write-Host "Uploading $FilePath..." -ForegroundColor Yellow
Write-Host "Note: First request may take 30-60 seconds (Render free tier wake-up)" -ForegroundColor Cyan

try {
    # Simple method using curl.exe if available
    if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
        Write-Host "Using curl.exe..." -ForegroundColor Green
        $fullPath = (Resolve-Path $FilePath).Path
        curl.exe -X POST $apiUrl `
            -F "file=@$fullPath" `
            -F "quiz_questions=10" `
            -F "interview_questions=10"
    } else {
        # Fallback: Manual multipart form
        Write-Host "Using PowerShell method..." -ForegroundColor Green
        
        $fileBytes = [System.IO.File]::ReadAllBytes($FilePath)
        $fileName = [System.IO.Path]::GetFileName($FilePath)
        $boundary = [System.Guid]::NewGuid().ToString()
        
        $body = @"
--$boundary
Content-Disposition: form-data; name="file"; filename="$fileName"
Content-Type: application/pdf

$([System.Text.Encoding]::GetEncoding("iso-8859-1").GetString($fileBytes))
--$boundary
Content-Disposition: form-data; name="quiz_questions"

10
--$boundary
Content-Disposition: form-data; name="interview_questions"

10
--$boundary--
"@
        
        $bodyBytes = [System.Text.Encoding]::GetEncoding("iso-8859-1").GetBytes($body)
        
        $response = Invoke-RestMethod -Uri $apiUrl -Method POST -Body $bodyBytes `
            -ContentType "multipart/form-data; boundary=$boundary"
        
        Write-Host "`n✅ Success!" -ForegroundColor Green
        $response | ConvertTo-Json -Depth 10
    }
} catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode.value__
        Write-Host "Status Code: $statusCode" -ForegroundColor Red
        if ($statusCode -eq 502) {
            Write-Host "`n💡 Tip: Render free tier services sleep after inactivity." -ForegroundColor Yellow
            Write-Host "   Wait 30-60 seconds and try again, or upgrade to keep service always on." -ForegroundColor Yellow
        }
    }
}

