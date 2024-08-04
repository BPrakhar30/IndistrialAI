from pdf2image import convert_from_path
from pytesseract import image_to_string
from PIL import Image
import os
import openai
from dotenv import load_dotenv
import pandas as pd
from io import StringIO
import yaml

# Loading configuration from config.yaml
with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

def convert_pdf_to_img(pdf_file):
    return convert_from_path(pdf_file)

def convert_image_to_text(file):
    text = image_to_string(file)
    return text

def get_text_from_any_pdf(pdf_file):
    images = convert_pdf_to_img(pdf_file)
    final_text = ""
    for pg, img in enumerate(images):
        final_text += convert_image_to_text(img)  
    return final_text

def process_pdf(config):
    path_to_pdf = config['pdf_path'] 
    extracted_text = get_text_from_any_pdf(path_to_pdf)

    # Using LLM to extract only the item details from all the content inside pdf
    extracted_text = f"Extracted text from pdf: {extracted_text}"
    useful_text = openai.chat.completions.create(
                model = config['openai_model'],
                messages=[
                    {"role": "system", "content": config['system_message_pdf_2_text']},
                    {"role": "user", "content": extracted_text}
                ],
                temperature = config['temperature_pdf_2_text']
            )
    useful_text = useful_text.choices[0].message.content

    # Parsing the markdown table to create a DataFrame
    lines = useful_text.split("\n")
    header = lines[0].split("|")[1:-1]
    header = [h.strip() for h in header]

    data = []
    for line in lines[2:]:
        if line.strip():
            row = line.split("|")[1:-1]
            row = [r.strip() for r in row]
            data.append(row)

    df = pd.DataFrame(data, columns=header)

    # Saving dataframe to an excel file
    output_path = config['output_excel_path']
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_excel(output_path, index=False)

    print(f"Excel file saved to {output_path}")
