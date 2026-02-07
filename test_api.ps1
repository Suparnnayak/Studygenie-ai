# PowerShell script to test the API upload endpoint
# Usage: .\test_api.ps1 [path-to-pdf-file]

param(
    [string]$FilePath = ""
)

$apiUrl = "https://studygenie-ai.onrender.com/api/upload-pdf"

# If no file path provided, try to find a PDF in current directory
if ([string]::IsNullOrEmpty($FilePath)) {
    $pdfFiles = Get-ChildItem -Path . -Filter "*.pdf" -File | Select-Object -First 1
    if ($pdfFiles) {
        $FilePath = $pdfFiles.FullName
        Write-Host "Using PDF file: $FilePath" -ForegroundColor Cyan
    } else {
        Write-Host "Error: No PDF file specified and none found in current directory." -ForegroundColor Red
        Write-Host "Usage: .\test_api.ps1 [path-to-pdf-file]" -ForegroundColor Yellow
        Write-Host "Example: .\test_api.ps1 'C:\Users\YourName\Documents\syllabus.pdf'" -ForegroundColor Yellow
        exit 1
    }
}

# Check if file exists
if (-not (Test-Path $FilePath)) {
    Write-Host "Error: File not found: $FilePath" -ForegroundColor Red
    Write-Host "`nPlease provide a valid PDF file path." -ForegroundColor Yellow
    Write-Host "Usage: .\test_api.ps1 [path-to-pdf-file]" -ForegroundColor Yellow
    exit 1
}

Write-Host "`nUploading $FilePath to $apiUrl..." -ForegroundColor Yellow

# Method: Using multipart/form-data (compatible with all PowerShell versions)
try {
    # Resolve the full path to avoid path issues
    $resolvedPath = (Resolve-Path $FilePath -ErrorAction Stop).Path
    Write-Host "Resolved file path: $resolvedPath" -ForegroundColor Gray
    
    $boundary = [System.Guid]::NewGuid().ToString()
    $LF = "`r`n"
    
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
    
    $body = $bodyLines -join $LF
    $bodyBytes = [System.Text.Encoding]::GetEncoding("iso-8859-1").GetBytes($body)
    
    $headers = @{
        "Content-Type" = "multipart/form-data; boundary=$boundary"
    }
    
    $response = Invoke-WebRequest -Uri $apiUrl -Method POST -Body $bodyBytes -Headers $headers
    
    Write-Host "`n✅ Success! Status Code: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Cyan
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
} catch {
    Write-Host "`n❌ Error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "Response: $responseBody" -ForegroundColor Red
    }
}

