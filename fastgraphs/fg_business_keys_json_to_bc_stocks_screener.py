import pyodbc
import json
import os
from loguru import logger

# Database connection configuration
def connect_to_database():
    try:
        connection = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=localhost;"
            "Database=stockscreener;"
            "Trusted_Connection=yes;"
        )

        logger.info("Successfully connected to the database.")
        return connection
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        raise

# Update data in the table
# Update data in the table
def update_data(cursor, symbol, data):
    try:
        query = """UPDATE bc_stocks_screener SET
            fg_fastfacts_previous_close = ?,
            fg_fastfacts_blended_pe = ?,
            fg_fastfacts_eps_yield = ?,
            fg_fastfacts_dividend_yield = ?,
            fg_fastfacts_type = ?,
            fg_graphkey_adjusted_operating_earnings_growth_rate = ?,
            fg_graphkey_fair_value_ratio = ?,
            fg_graphkey_normal_pe_ratio = ?,
            fg_graphkey_normal_p_affo = ?,
            fg_companyinfo_gics_sub_industry = ?,
            fg_companyinfo_country = ?,
            fg_companyinfo_marketcap = ?,
            fg_companyinfo_sp_credit_rating = ?,
            fg_companyinfo_tev = ?,
            fg_analystscorecard_beat_zero_year = ?,
            fg_analystscorecard_hit_zero_year = ?,
            fg_analystscorecard_miss_zero_year = ?,
            fg_analystscorecard_beat_one_year = ?,
            fg_analystscorecard_hit_one_year = ?,
            fg_analystscorecard_miss_one_year = ?,
            last_update_date = SYSDATETIME()
            WHERE symbol = ?"""

        # Prepare the values in order
        values = (
            data.get("fg_fastfacts_previous_close"),
            data.get("fg_fastfacts_blended_pe"),
            data.get("fg_fastfacts_eps_yield"),
            data.get("fg_fastfacts_dividend_yield"),
            data.get("fg_fastfacts_type"),
            data.get("fg_graphkey_adjusted_operating_earnings_growth_rate"),
            data.get("fg_graphkey_fair_value_ratio"),
            data.get("fg_graphkey_normal_pe_ratio"),
            data.get("fg_graphkey_normal_p_affo"),
            data.get("fg_companyinfo_gics_sub_industry"),
            data.get("fg_companyinfo_country"),
            data.get("fg_companyinfo_marketcap"),
            data.get("fg_companyinfo_sp_credit_rating"),
            data.get("fg_companyinfo_tev"),
            data.get("fg_analystscorecard_beat_zero_year"),
            data.get("fg_analystscorecard_hit_zero_year"),
            data.get("fg_analystscorecard_miss_zero_year"),
            data.get("fg_analystscorecard_beat_one_year"),
            data.get("fg_analystscorecard_hit_one_year"),
            data.get("fg_analystscorecard_miss_one_year"),
            symbol,
        )

        # Log the SQL query with values
        # logger.debug(f"Executing SQL: {query} with values: {values}")

        # Execute the query
        cursor.execute(query, values)
        logger.info(f"Data updated for symbol: {symbol}")
    except Exception as e:
        logger.error(f"Error updating data for symbol {symbol}: {e}")
        raise

# Process JSON files
def process_json_files(folder_path):
    connection = connect_to_database()
    cursor = connection.cursor()
    
    field_mapping = {
        "fg_fastfacts_previous_close": "Previous close",
        "fg_fastfacts_blended_pe": "Blended P/E",
        "fg_fastfacts_eps_yield": "EPS Yld",
        "fg_fastfacts_dividend_yield": "Div Yld",
        "fg_fastfacts_type": "TYPE",
        "fg_graphkey_adjusted_operating_earnings_growth_rate": "Adjusted (Operating) Earnings Growth Rate",
        "fg_graphkey_fair_value_ratio": "Fair Value Ratio",
        "fg_graphkey_normal_pe_ratio": "Normal P/E Ratio",
        "fg_graphkey_normal_p_affo" : "Normal P/AFFO Ratio",
        "fg_companyinfo_gics_sub_industry": "GICS Sub-industry",
        "fg_companyinfo_country": "Country",
        "fg_companyinfo_marketcap": "Market Cap",
        "fg_companyinfo_sp_credit_rating": "S&P Credit Rating",
        "fg_companyinfo_tev": "TEV",
        "fg_analystscorecard_beat_zero_year": "Beat",
        "fg_analystscorecard_hit_zero_year": "Hit",
        "fg_analystscorecard_miss_zero_year": "Miss",
        "fg_analystscorecard_beat_one_year": "Beat_1",
        "fg_analystscorecard_hit_one_year": "Hit_1",
        "fg_analystscorecard_miss_one_year": "Miss_1"
    }

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):
            symbol = os.path.splitext(file_name)[0]
            file_path = os.path.join(folder_path, file_name)

            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    raw_data = json.load(file)
                    # logger.debug(f"Raw JSON data for symbol {symbol}: {raw_data}")

                    # Normalize data
                    data = {
                        field: (
                            raw_data.get(attribute, None)
                            .strip() if raw_data.get(attribute) and isinstance(raw_data.get(attribute), str) else None
                        )
                        for field, attribute in field_mapping.items()
                    }

                    # Handle special characters
                    for key, value in data.items():
                        if value in {"â€”", "--"}:
                            data[key] = None
                    
                    # logger.debug(f"Normalized data for symbol {symbol}: {data}")
                    update_data(cursor, symbol, data)
            except Exception as e:
                logger.error(f"Error processing file {file_name}: {e}")

    connection.commit()
    logger.info("Changes committed to the database.")
    cursor.close()
    connection.close()
    logger.info("All files processed.")

# Folder containing JSON files
json_folder_path = r"C:\dev\airtable-zennoposter\apps\fast-graphs-snapshot-current\fastgraphs"  # Update this path as necessary

if __name__ == "__main__":
    process_json_files(json_folder_path)
