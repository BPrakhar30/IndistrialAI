import pandas as pd
import openai
import os
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to identify dimension and category using LLM
def identify_dimension_and_category(item_details, model, system_message, temperature):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": item_details}
        ],
        temperature = temperature,
    )

    more_details = response.choices[0].message.content
    return more_details

def process_dimension_and_category(config):
    excel_file_path = config['output_excel_path']
    df = pd.read_excel(excel_file_path, header=0)  

    # Replace all occurrences of '°' with "'"
    df = df.replace('°', "'", regex=True)

    # Initializing new columns for dimension and category
    df['Dimension'] = ""
    df['Category'] = ""

    # Processing each item in the first column
    for index, row in df.iterrows():
        item_description = row[0]  
        result = identify_dimension_and_category(item_description, config['openai_model'], config['system_message_category_dimension'], config['temperature_category_dimension'])
        
        # Extracting dimension and category from the result
        try:
            dimension = result.split(",")[0].split(":")[1].strip()
            category = result.split(",")[1].split(":")[1].strip()
        except IndexError:
            dimension = ""
            category = ""
        
        # Updating the dataframe
        df.at[index, 'Dimension'] = dimension
        df.at[index, 'Category'] = category

    # Removing all double quotes from the "Dimension" column
    def remove_special_chars(text):
        cleaned_text = text.replace('"', '').replace('”', '').replace("'", '').replace("unknown","")
        return cleaned_text

    df['Dimension'] = df['Dimension'].apply(remove_special_chars)

    # Saving the updated dataframe to a new excel file
    output_excel_path = config['updated_excel_path']
    df.to_excel(output_excel_path, index=False, header=True)

    print(f"Excel file saved to {output_excel_path}")