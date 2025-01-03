# Define the path to your Python script
$scriptPath = "C:\dev\TRADIER\stream_stock_price_to_db.py"

# Loop to continuously restart the script if it fails
while ($true) {
    try {
        # Run the Python script
        python $scriptPath
    } catch {
        # Log the exception (optional)
        Write-Host "Script failed with an error: $($_.Exception.Message)"
    }

    # Wait for a few seconds before restarting (optional)
    Start-Sleep -Seconds 5

    Write-Host "Restarting the script..."
}
