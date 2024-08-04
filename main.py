import yaml
from pdf_processing import process_pdf
from query_preprocessing import process_dimension_and_category
from mapping import process_matching

# Loading configuration from config.yaml
with open("config.yaml", 'r') as stream:
    config = yaml.safe_load(stream)

def main():
    # Extracting text from pdf
    process_pdf(config)
    
    # Preprocessing the extracted content into desired form for querying 
    process_dimension_and_category(config)

    # Mapping requests to the productdb
    process_matching(config)

if __name__ == "__main__":
    main()