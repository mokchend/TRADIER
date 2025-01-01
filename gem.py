import json

def extract_data_from_image(image_path):
  """
  Extracts data from an image of a FAST Graphs report and returns a JSON string.

  Args:
    image_path: Path to the image file.

  Returns:
    A JSON string containing the extracted data.
  """

  try:
    import pytesseract
    from PIL import Image
  except ImportError:
    raise ImportError("Please install pytesseract and Pillow to use this function.")

  # Load the image
  img = Image.open(image_path)

  # Extract text from the image using pytesseract
  text = pytesseract.image_to_string(img)

  # Split the text into lines
  lines = text.splitlines()

  # Initialize dictionaries to store the extracted data
  fast_facts = {}
  graph_key = {}
  company_info = {}
  analyst_scorecard = {}

  # Extract FAST Facts
  for line in lines:
    if "Previous close:" in line:
      fast_facts["Previous close"] = line.split(":")[1].strip()
    elif "Blended P/E:" in line:
      fast_facts["Blended P/E"] = line.split(":")[1].strip()
    elif "EPS Yid" in line:
      fast_facts["EPS Yid"] = line.split(":")[1].strip()
    elif "Div Yld:" in line:
      fast_facts["Div Yld"] = line.split(":")[1].strip()
    elif "TYPE:" in line:
      fast_facts["TYPE"] = line.split(":")[1].strip()

  # Extract GRAPH KEY
  for line in lines:
    if "Adjusted (Operating) Earnings Growth" in line:
      graph_key["Adjusted (Operating) Earnings Growth"] = line.split(":")[1].strip()
    elif "Fair Value Ratio" in line:
      graph_key["Fair Value Ratio"] = line.split(":")[1].strip()
    elif "Normal P/E Ratio:" in line:
      graph_key["Normal P/E Ratio"] = line.split(":")[1].strip()
    elif "Dividends Declared" in line:
        if len(line.split(":")) > 1:
            graph_key["Dividends Declared"] = line.split(":")[1].strip()
        else:
        # Handle the case where there's no colon or value
            print(f"Warning: No value found for 'Dividends Declared' in line: {line}")
        # graph_key["Dividends Declared"] = line.split(":")[1].strip()
    elif "Dividend yield and payout" in line:
        if len(line.split(":")) > 1:
            graph_key["Dividend yield and payout"] = line.split(":")[1].strip()
        else:
        # Handle the case where there's no colon or value
            print(f"Warning: No value found for 'vidend yield and payout' in line: {line}")

  # Extract COMPANY INFO
  for line in lines:
    if "GICS Sub-industry:" in line:
      company_info["GICS Sub-industry"] = line.split(":")[1].strip()
    elif "Country:" in line:
      company_info["Country"] = line.split(":")[1].strip()
    elif "Markat Cap" in line:
      company_info["Markat Cap"] = line.split(":")[1].strip()
    elif "S&P Credit Rating:" in line:
      company_info["S&P Credit Rating"] = line.split(":")[1].strip()
    elif "LT Debt/Capital:" in line:
      company_info["LT Debt/Capital"] = line.split(":")[1].strip()
    elif "TEV" in line:
      company_info["TEV"] = line.split(":")[1].strip()
    elif "Splits:" in line:
      company_info["Splits"] = line.split(":")[1].strip()
    elif "Spinoffs:" in line:
      company_info["Spinoffs"] = line.split(":")[1].strip()

  # Extract ANALYST SCORECARD
  for i, line in enumerate(lines):
    if "Analyst scorecard" in line:
      # Assuming the scorecard data is in the next 3 lines
      for j in range(i + 1, i + 4):
        if "Beat:" in lines[j]:
          analyst_scorecard["Beat"] = lines[j].split(":")[1].strip()
        elif "Hit" in lines[j]:
          analyst_scorecard["Hit"] = lines[j].split(":")[1].strip()
        elif "Miss:" in lines[j]:
          analyst_scorecard["Miss"] = lines[j].split(":")[1].strip()

  # Create a dictionary to store all the extracted data
  data = {
      "FAST_FACTS": fast_facts,
      "GRAPH_KEY": graph_key,
      "COMPANY_INFO": company_info,
      "ANALYST_SCORECARD": analyst_scorecard,
  }

  # Convert the data to JSON
  json_data = json.dumps(data, indent=2)

  return json_data

# Example usage
image_path = "C:/dev/airtable-zennoposter/apps/fast-graphs-snapshot-current/fastgraphs/AA.png"  # Replace with the actual path to your image
json_data = extract_data_from_image(image_path)
print(json_data)