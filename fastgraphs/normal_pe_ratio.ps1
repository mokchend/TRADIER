# Set the path to the folder containing the JSON files
$folderPath = "C:/dev/airtable-zennoposter/apps/fast-graphs-snapshot-current/fastgraphs"


# Get all JSON files in the folder
$jsonFiles = Get-ChildItem -Path $folderPath -Filter *.json

# Loop through each JSON file
foreach ($file in $jsonFiles) {
    try {
        # Read the JSON content
        $jsonContent = Get-Content -Path $file.FullName -Raw | ConvertFrom-Json

        # Check if the key "Normal P/E Ratio" or "Normal P/OCF Ratio" exists and extract its value
        if ($jsonContent.'Normal P/E Ratio' -ne $null -or $jsonContent.'Normal P/OCF Ratio' -ne $null  -or $jsonContent.'Normal P/AFFO Ratio' -ne $null -or $jsonContent.'Normal P/FFO Ratio' -ne $null) {
            # Check for Normal P/E Ratio first
            if ($jsonContent.'Normal P/E Ratio' -ne $null) {
                $peRatio = [double]($jsonContent.'Normal P/E Ratio' -replace '[^\d\.]', '')

                # Check if the Normal P/E Ratio is greater than 110
                if ($peRatio -gt 250) {
                    Write-Host "File: $($file.FullName) - Normal P/E Ratio: $peRatio"
                }
            }

            # Check for Normal P/OCF Ratio
            if ($jsonContent.'Normal P/OCF Ratio' -ne $null) {
                $pocfRatio = [double]($jsonContent.'Normal P/OCF Ratio' -replace '[^\d\.]', '')

                # Check if the Normal P/OCF Ratio is greater than 110
                if ($pocfRatio -gt 250) {
                    Write-Host "File: $($file.FullName) - Normal P/OCF Ratio: $pocfRatio"
                }
            }

            # check for Normal P/AFFO Ratio
            if ($jsonContent.'Normal P/AFFO Ratio' -ne $null) {
                $paffoRatio = [double]($jsonContent.'Normal P/AFFO Ratio' -replace '[^\d\.]', '')

                # Check if the Normal P/AFFO Ratio is greater than 110
                if ($paffoRatio -gt 250) {
                    Write-Host "File: $($file.FullName) - Normal P/AFFO Ratio: $paffoRatio"
                }
            }

            # check for Normal P/FFO Ratio
            if ($jsonContent.'Normal P/FFO Ratio' -ne $null) {
                $pffoRatio = [double]($jsonContent.'Normal P/FFO Ratio' -replace '[^\d\.]', '')

                # Check if the Normal P/FFO Ratio is greater than 110
                if ($pffoRatio -gt 250) {
                    Write-Host "File: $($file.FullName) - Normal P/FFO Ratio: $pffoRatio"
                }
            }

        } else {
            # If the key doesn't exist, log it (optional)
            Write-Host ">>> File: $($file.FullName) - Key 'Normal P/E Ratio' not found" -ForegroundColor Yellow
        }
    } catch {
        # Log any errors encountered during processing
        Write-Host "Error processing file: $($file.FullName) - $($_.Exception.Message)" -ForegroundColor Red
    }
}