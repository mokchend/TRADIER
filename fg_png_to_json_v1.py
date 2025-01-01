import os
import shutil
import pytesseract
from pytesseract import image_to_string
from PIL import Image

import json
import re

# Specify the path to Tesseract executable (Update if installed in a custom location)
# C:/Program Files/Tesseract-OCR/tesseract.exe
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"


##############################################################################################################################################
# This script processes .png files in a directory, performs OCR on them, and moves them to a different directory based on the OCR results.
##############################################################################################################################################
# Define directories
base_dir = r"C:/dev/airtable-zennoposter/apps/fast-graphs-snapshot-current/fastgraphs"
destination_dir = os.path.join(base_dir, "item_do_not_exist")
destination_dir_no_data = os.path.join(base_dir, "item_no_data_available")

# Ensure the destination folder exists
os.makedirs(destination_dir, exist_ok=True)
os.makedirs(destination_dir_no_data, exist_ok=True)

def move_png():

    # Iterate through .png files in the base directory (only 1st level)
    for filename in os.listdir(base_dir):
        if filename.endswith(".png"):
            file_path = os.path.join(base_dir, filename)
            try:
                # Open image and perform OCR
                with Image.open(file_path) as img:
                    text = image_to_string(img)
                    # save text to a file
                    with open(f"{base_dir}/{filename}.txt", "w") as f:
                        f.write(text)  

                # Check if the text exists
                if "This item doesn't exist" in text:
                    # Move the file to the destination folder
                    shutil.move(file_path, os.path.join(destination_dir, filename))
                    print(f"Moved: {filename}")

                # Check if the text exists
                if "There is no data available" in text:
                    # Move the file to the destination folder
                    shutil.move(file_path, os.path.join(destination_dir_no_data, filename))
                    print(f"Moved: {filename}")

            except Exception as e:
                print(f"Error processing {filename}: {e}")

    print("Processing completed.")

##############################################################################################################################################
# This script extracts specific sections from a .png file, performs OCR on them, and saves the extracted data to a JSON file.
##############################################################################################################################################

def extract_json_info_from_png(image_path):
    # Load the image
    # image_path = r"/mnt/data/A.png"  # Replace with the correct image file path
    image = Image.open(image_path)

    # Perform OCR on the image
    # extracted_text = pytesseract.image_to_string(image)
    
    # Perform OCR on the image
    processed_text = pytesseract.image_to_string(image)
    # save to file
    with open(f"{image_path}.txt", "w") as f:
        f.write(processed_text)

    # Extract sections
    sections = extract_sections(processed_text)
    print(sections)

    # Parse each section
    data = {
        "FAST_FACTS": parse_key_value(sections["FAST_FACTS"]),
        "GRAPH_KEY": sections["GRAPH_KEY"].split(". ") if sections["GRAPH_KEY"] else None,
        "COMPANY_INFO": parse_key_value(sections["COMPANY_INFO"]),
        "ANALYST_SCORECARD": parse_analyst_scorecard(sections["ANALYST_SCORECARD"]),
    }

    # Save the JSON to a file
    output_json_path = "extracted_data.json"
    with open(output_json_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    # Print the JSON result
    print(json.dumps(data, indent=4))
    
    
    
# Function to extract sections based on section headers
def extract_sections(text):
    sections = {
        "FAST_FACTS": None,
        "GRAPH_KEY": None,
        "COMPANY_INFO": None,
        "ANALYST_SCORECARD": None,
    }
    
    # Regex patterns for headers
    patterns = {
        "FAST_FACTS": r"FAST Facts(.*?)(GRAPH KEY|COMPANY INFO|ANALYST SCORECARD|$)",
        "GRAPH_KEY": r"GRAPH KEY(.*?)(COMPANY INFO|ANALYST SCORECARD|FAST FACTS|$)",
        "COMPANY_INFO": r"COMPANY INFO(.*?)(ANALYST SCORECARD|FAST FACTS|GRAPH KEY|$)",
        "ANALYST_SCORECARD": r"ANALYST SCORECARD(.*?)(FAST FACTS|GRAPH KEY|COMPANY INFO|$)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[key] = match.group(1).strip()

    return sections

# Function to parse key-value pairs
def parse_key_value(section_text):
    if not section_text:
        return None
    key_value_pairs = {}
    for line in section_text.split(". "):
        if ":" in line:
            key, value = map(str.strip, line.split(":", 1))
            key_value_pairs[key] = value
    return key_value_pairs

# Function to parse numerical lists (e.g., Analyst Scorecard)
def parse_analyst_scorecard(section_text):
    if not section_text:
        return None
    scorecard = {}
    lines = section_text.split(". ")
    for line in lines:
        match = re.search(r"(\d+ year):.*?Beat: (\d+\.?\d*%).*?Hit: (\d+\.?\d*%).*?Miss: (\d+\.?\d*%)", line, re.IGNORECASE)
        if match:
            scorecard[match.group(1)] = {
                "Beat": match.group(2),
                "Hit": match.group(3),
                "Miss": match.group(4)
            }
    return scorecard
    
extract_json_info_from_png("C:/dev/airtable-zennoposter/apps/fast-graphs-snapshot-current/fastgraphs/AAL.png")