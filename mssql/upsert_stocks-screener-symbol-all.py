import csv
import pyodbc
import os
import glob

#############################################################################################################################################################
# The provided PowerShell script performs the following actions:

# Defines the folder containing CSV files.
# Iterates through all CSV files in the specified folder.
# Checks if the last line of each file contains the text "Downloaded from Barchart.com".
# If the text is found, removes the last line and saves the updated content back to the same file.
#############################################################################################################################################################

# Define the folder containing the CSV files
folder_path = r"C:/dev/airtable-zennoposter/apps/barchart-symbol-extract/barchart"
import datetime

# format current date using this format 12-28-2024
now = datetime.datetime.now()
dateStr = now.strftime("%m-%d-%Y")
print(dateStr)

# move all csv from this folder to a new folder with the current date
# Define the folder containing the CSV files
folder_path = r"C:/dev/airtable-zennoposter/apps/barchart-symbol-extract/barchart"
new_folder_path = f"C:/dev/airtable-zennoposter/apps/barchart-symbol-extract/barchart/{dateStr}"
os.makedirs(new_folder_path, exist_ok=True)
# move all csv files to the new folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(folder_path, file_name)
        new_file_path = os.path.join(new_folder_path, file_name)
        os.rename(file_path, new_file_path)
        print(f"Moved file: {file_path} to {new_file_path}")
        



# Iterate through all CSV files in the folder
for file_name in os.listdir(new_folder_path):
    if file_name.endswith(".csv"):
        file_path = os.path.join(new_folder_path, file_name)
        
        # Read all lines of the file
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Check if the last line contains the target text
        if lines and "Downloaded from Barchart.com" in lines[-1]:
            # Remove the last line
            lines = lines[:-1]
            
            # Save the modified content back to the same file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)
            
            print(f"Modified file: {file_path}")
        else:
            print(f"No modification needed: {file_path}")


#############################################################################################################################################################
# The PowerShell script (01-mergeStockScreenFiles.ps1) performs the following actions:

# Input Files: Defines a file pattern to locate CSV files to merge.
# Output File: Specifies the output file path.
# Header: Defines an expected header and writes it to the output file.
# File Processing: Iterates over matching CSV files:
# Skips the header in each input file.
# Appends the remaining content to the output file.
# Here’s the equivalent functionality implemented in Python:
#############################################################################################################################################################


# Define the input file pattern and output file path
input_pattern = fr"{new_folder_path}/*-viewV1.csv"
output_file = fr"{new_folder_path}/stocks-screener-symbol-all-{dateStr}.csv"

# Define the expected header
expected_header = (
    "Symbol,Name,Signal,Last,Pivot,Trend,\"Trend Str\",\"Trend Dir\",Opinion,Strength,"
    "Direction,\"Short Term Signal\",\"Med Term Signal\",\"Long Term Signal\",Exchange,"
    "Industry,\"SIC Description\",\"1st Res\",\"2nd Res\",\"3rd Res\",\"1st Sup\",\"2nd Sup\",\"3rd Sup\""
)

# Initialize the output file by writing the header
with open(output_file, 'w', encoding='utf-8') as file:
    file.write(expected_header + '\n')

# Get all matching CSV files
csv_files = glob.glob(input_pattern)

# Iterate over each file and append its content to the output file
for file_path in csv_files:
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Skip the header (first line) and append the remaining content
    if len(lines) > 1:  # Ensure there are lines beyond the header
        with open(output_file, 'a', encoding='utf-8') as output:
            output.writelines(lines[1:])  # Append everything except the first line

    print(f"Processed and merged file: {file_path}")

print(f"All files merged into: {output_file}")


# Define the new header
new_header = (
    "symbol, name, bc_signal, bc_last, bc_pivot, bc_trend, bc_trend_str, bc_trend_dir, bc_opinion, "
    "bc_strength, bc_direction, bc_short_term_signal, bc_med_term_signal, bc_long_term_signal, "
    "bc_exchange, bc_industry, bc_sic_description, bc_first_res, bc_second_res, bc_third_res, "
    "bc_first_sup, bc_second_sup, bc_third_sup\n"
)

# Path to the uploaded CSV file
csv_file_path = f"{output_file}"

# Replace the first line in the file with the new header
with open(csv_file_path, 'r', encoding='utf-8') as file:
    lines = file.readlines()

# Replace the first line
lines[0] = new_header

# Write the updated content back to the same file
updated_csv_file_path = f"{output_file}-updated.csv"
with open(updated_csv_file_path, 'w', encoding='utf-8') as file:
    file.writelines(lines)
    


#############################################################################################################################################################
# UPSERT operation in SQL Server
# The following Python script demonstrates how to perform an UPSERT (INSERT or UPDATE) operation in SQL Server using the pyodbc library.
#############################################################################################################################################################


# Path to the uploaded CSV file
csv_file_path = f"{updated_csv_file_path}"


# Establish a connection to the database
try:
    # Establish a connection to the database
    # Database connection configuration (replace with actual connection details)
    connection = pyodbc.connect(
        "Driver={SQL Server};"
        "Server=localhost;"
        "Database=stockscreener;"
        "Trusted_Connection=yes;"
    )
    cursor = connection.cursor()
    print("Database connection established successfully.")
except pyodbc.Error as e:
    print(f"Error connecting to the database: {e}")
    exit()

# Define the UPSERT query
upsert_query = """
MERGE INTO bc_stocks_screener AS target
USING (
    SELECT ? AS symbol, ? AS name, ? AS bc_signal, ? AS bc_last, ? AS bc_pivot,
           ? AS bc_trend, ? AS bc_trend_str, ? AS bc_trend_dir, ? AS bc_opinion,
           ? AS bc_strength, ? AS bc_direction, ? AS bc_short_term_signal, ? AS bc_med_term_signal,
           ? AS bc_long_term_signal, ? AS bc_exchange, ? AS bc_industry, ? AS bc_sic_description,
           ? AS bc_first_res, ? AS bc_second_res, ? AS bc_third_res, ? AS bc_first_sup,
           ? AS bc_second_sup, ? AS bc_third_sup
) AS source
ON target.symbol = source.symbol
WHEN MATCHED THEN 
    UPDATE SET 
        name = source.name,
        bc_signal = source.bc_signal,
        bc_last = source.bc_last,
        bc_pivot = source.bc_pivot,
        bc_trend = source.bc_trend,
        bc_trend_str = source.bc_trend_str,
        bc_trend_dir = source.bc_trend_dir,
        bc_opinion = source.bc_opinion,
        bc_strength = source.bc_strength,
        bc_direction = source.bc_direction,
        bc_short_term_signal = source.bc_short_term_signal,
        bc_med_term_signal = source.bc_med_term_signal,
        bc_long_term_signal = source.bc_long_term_signal,
        bc_exchange = source.bc_exchange,
        bc_industry = source.bc_industry,
        bc_sic_description = source.bc_sic_description,
        bc_first_res = source.bc_first_res,
        bc_second_res = source.bc_second_res,
        bc_third_res = source.bc_third_res,
        bc_first_sup = source.bc_first_sup,
        bc_second_sup = source.bc_second_sup,
        bc_third_sup = source.bc_third_sup
WHEN NOT MATCHED THEN 
    INSERT (symbol, name, bc_signal, bc_last, bc_pivot, bc_trend, bc_trend_str, bc_trend_dir, bc_opinion, 
            bc_strength, bc_direction, bc_short_term_signal, bc_med_term_signal, bc_long_term_signal, 
            bc_exchange, bc_industry, bc_sic_description, bc_first_res, bc_second_res, bc_third_res, 
            bc_first_sup, bc_second_sup, bc_third_sup)
    VALUES (source.symbol, source.name, source.bc_signal, source.bc_last, source.bc_pivot, source.bc_trend, 
            source.bc_trend_str, source.bc_trend_dir, source.bc_opinion, source.bc_strength, source.bc_direction, 
            source.bc_short_term_signal, source.bc_med_term_signal, source.bc_long_term_signal, source.bc_exchange, 
            source.bc_industry, source.bc_sic_description, source.bc_first_res, source.bc_second_res, 
            source.bc_third_res, source.bc_first_sup, source.bc_second_sup, source.bc_third_sup);
"""

# Process the CSV file and execute the UPSERT query
try:
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)  # Skip the header row

        for row in csv_reader:
            # Ensure the row has the correct number of values
            if len(row) != 23:
                print(f"Skipping invalid row: {row}")
                continue

            # Clean up any extra spaces in column names
            clean_row = [value.strip() for value in row]

            # Execute the UPSERT query with the row values
            cursor.execute(upsert_query, *clean_row)
    
    # Commit the transaction
    connection.commit()
    print("Upsert operation completed successfully.")
except Exception as e:
    print(f"Error during UPSERT operation: {e}")
finally:
    # Close the database connection
    cursor.close()
    connection.close()
    print("Database connection closed.")
