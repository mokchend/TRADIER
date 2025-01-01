import os
import json
import re
from PIL import Image
import pytesseract

# Set up paths
input_dir = r"C:/dev/airtable-zennoposter/apps/fast-graphs-snapshot-current/fastgraphs"
output_dir = os.path.join(input_dir, "processed_jsons")
ocr_logs_dir = os.path.join(input_dir, "ocr_logs")

# Ensure output directories exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(ocr_logs_dir, exist_ok=True)

# Function to perform OCR and extract JSON data
def process_image_to_json(image_path):
    # Load the image
    image = Image.open(image_path)

    # Perform OCR on the image
    processed_text = pytesseract.image_to_string(image)

    # Save OCR text for debugging
    ocr_output_file = os.path.join(ocr_logs_dir, os.path.basename(image_path) + "_ocr.txt")
    with open(ocr_output_file, "w") as f:
        f.write(processed_text)

    # Extract sections
    sections = extract_sections(processed_text)

    # Parse each section
    data = {
        "FAST_FACTS": parse_key_value(sections.get("FAST_FACTS", "")),
        "GRAPH_KEY": sections.get("GRAPH_KEY", "").split(". ") if sections.get("GRAPH_KEY") else None,
        "COMPANY_INFO": parse_key_value(sections.get("COMPANY_INFO", "")),
        "ANALYST_SCORECARD": parse_analyst_scorecard(sections.get("ANALYST_SCORECARD", "")),
    }

    return data

# Function to extract sections based on patterns
def extract_sections(text):
    sections = {
        "FAST_FACTS": "",
        "GRAPH_KEY": "",
        "COMPANY_INFO": "",
        "ANALYST_SCORECARD": "",
    }

    # Regex patterns to capture sections
    patterns = {
        "FAST_FACTS": r"(FAST Facts[\s\S]*?)(GRAPH KEY|COMPANY INFO|ANALYST SCORECARD|$)",
        "GRAPH_KEY": r"(GRAPH KEY[\s\S]*?)(COMPANY INFO|ANALYST SCORECARD|FAST FACTS|$)",
        "COMPANY_INFO": r"(COMPANY INFO[\s\S]*?)(ANALYST SCORECARD|FAST FACTS|GRAPH KEY|$)",
        "ANALYST_SCORECARD": r"(ANALYST SCORECARD[\s\S]*?)(FAST FACTS|GRAPH KEY|COMPANY INFO|$)"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            sections[key] = match.group(1).strip()

    return sections

# Function to parse key-value pairs
def parse_key_value(section_text):
    if not section_text:
        return {}
    key_value_pairs = {}
    for line in section_text.split("\n"):
        if ":" in line:
            key, value = map(str.strip, line.split(":", 1))
            key_value_pairs[key] = value
    return key_value_pairs

# Function to parse the Analyst Scorecard section
def parse_analyst_scorecard(section_text):
    if not section_text:
        return {}
    scorecard = {}
    lines = section_text.split("\n")
    for line in lines:
        match = re.search(r"(\d+ year):.*?Beat: (\d+\.?\d*%).*?Hit: (\d+\.?\d*%).*?Miss: (\d+\.?\d*%)", line, re.IGNORECASE)
        if match:
            scorecard[match.group(1)] = {
                "Beat": match.group(2),
                "Hit": match.group(3),
                "Miss": match.group(4)
            }
    return scorecard

# Batch process all PNG files in the directory
def process_all_images(input_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            image_path = os.path.join(input_dir, filename)
            try:
                # Process image and generate JSON
                json_data = process_image_to_json(image_path)

                # Save JSON output to file
                json_output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + ".json")
                with open(json_output_path, "w") as json_file:
                    json.dump(json_data, json_file, indent=4)

                print(f"Processed {filename} -> {json_output_path}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

# Run the batch processing
process_all_images(input_dir)
