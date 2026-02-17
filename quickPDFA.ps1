# Full path to Ghostscript executable
$gsPath = "C:\Program Files\gs\gs10.06.0\bin\gswin64c.exe"

# Folder containing original PDFs
$sourceFolder = "C:\Users\cwhistler\Desktop\testyfol"

# Folder for PDF/A outputs
$outputFolder = "C:\Users\cwhistler\Desktop\testyfol"

# Make sure the output folder exists
New-Item -ItemType Directory -Force -Path $outputFolder

# Convert each PDF
Get-ChildItem $sourceFolder -Filter "*.pdf" | ForEach-Object {
    $input = $_.FullName
    $base = $_.BaseName
    $output = Join-Path $outputFolder ($_.BaseName +".pdf")
    $tempOutput = Join-Path $outputFolder ($base + "_PDFA.pdf")

    Write-Host "Converting:" $_.Name "→" ($_.BaseName + ".pdf")

    & "$gsPath" -dPDFA=2 -dBATCH -dNOPAUSE `
        -sDEVICE=pdfwrite `
        -sColorConversionStrategy=RGB `
        -dPDFACompatibilityPolicy=1 `
        -sOutputFile="$tempOutput" "$input"


    if ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath $tempOutput)) {
        # Overwrite original with the converted file
        Move-Item -LiteralPath $tempOutput -Destination $input -Force}


&python quickADA2.py $input
}