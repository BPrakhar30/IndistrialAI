import pandas as pd
from fuzzywuzzy import fuzz, process
import re
from utils import get_best_match

def fuzzy_match(query, choices, threshold=70):
    """
    Perform fuzzy matching to find the best matches for a query in a list of choices.
    :param query: The query string to match.
    :param choices: A list of strings to match against.
    :param threshold: The minimum score to consider a match.
    :return: A list of matching choices with their scores.
    """
    results = process.extract(query, choices, scorer=fuzz.token_sort_ratio)
    return [(match, score) for match, score in results if score >= threshold]


def regex_match(query, choices):
    """
    Perform regex matching to find matches for a query in a list of choices.
    :param query: The query string to match.
    :param choices: A list of strings to match against.
    :return: A list of matching choices.
    """
    pattern = re.compile(query, re.IGNORECASE)
    return [choice for choice in choices if pattern.search(choice)]


def process_matching(config):
    query_file_path = config['updated_excel_path']
    query_df = pd.read_excel(query_file_path)

    database_path = config['database_path']
    product_df = pd.read_csv(database_path, header=None)  

    database_column_index = config['database_column_index']
    fuzzy_match_threshold = config['fuzzy_match_threshold']

    query_df['Best Match'] = ""

    # Performing fuzzy matching for each row in the query_df
    for index, row in query_df.iterrows():
        item_description = row['Item Name and Description']
        dimension = row['Dimension']
        category = row['Category']
        
    # Trying matching using the item description
        matches = fuzzy_match(item_description, product_df[database_column_index].tolist())
    
        if matches: # when exact name exists in db
            best_match = matches[0]  # Assuming the first match is the best one
            query_df.at[index, 'Best Match'] = best_match[0]  
            continue  

        else: # when exact name does not exists in db
            # If no matches at item description level, try matching using the category
            if pd.notna(category) and str(category).strip(): # when category exists 
                matched_categories = regex_match(category, product_df[database_column_index].tolist())
            
                if matched_categories: # when there are matches based on category              
                    # Further filter matches by dimension
                    if pd.notna(dimension) and str(dimension).strip():  # when dimension matching is possible
                        matched_dimensions = regex_match(str(dimension), matched_categories)
                        if matched_dimensions:
                            best_matches = get_best_match(item_description, matched_dimensions) 
                            query_df.at[index, 'Best Match'] = ", ".join(best_matches)
                            continue  
                        else:  # when no dimension matches 
                            best_matches = get_best_match(item_description, matched_categories) 
                            query_df.at[index, 'Best Match'] = ", ".join(best_matches)
                            continue
                    else: # When dimension matching is not possible
                        best_matches = get_best_match(item_description, matched_categories)  
                        query_df.at[index, 'Best Match'] = ", ".join(best_matches)
                        continue 
              
                # Try matching using the dimension directly
                elif pd.notna(dimension) and str(dimension).strip():
                    matches = regex_match(str(dimension), product_df[database_column_index].tolist())
                    if matches:
                        best_matches = get_best_match(item_description, matches) 
                        query_df.at[index, 'Best Match'] = ", ".join(best_matches)
                    else:
                        query_df.at[index, 'Best Match'] = "not matched"
                else:
                    query_df.at[index, 'Best Match'] = "not matched"
            else:
                query_df.at[index, 'Best Match'] = "not matched"


    # Saving the updated DataFrame to a new Excel file
    output_excel_path = config['final_output_excel_path']
    query_df.to_excel(output_excel_path, index=False, header=True)

    print("Mapping done, excel file saved to {output_excel_path}")
        

