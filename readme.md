## Project Overview

Thank you for giving me the opportunity to work on this challenging problem. I enjoyed working on it and implemented the best possible approach within the limited time frame. Below is the workflow for my pipeline:

### Workflow

#### Step 1: Extracting PDF Content
1. Extract the content from the PDF using Tesseract OCR.
2. Use an LLM to further extract item details in a specified structure.
3. Save the details in an Excel sheet.

**Considerations:**
- Other methods like VLMs can be tried, but they are more suited for image descriptions rather than content extraction.
- The extracted data can be saved in various formats (CSV, JSON, etc.), but here Excel was used.

**Flow:**
Input ['request.pdf'] --> ['pdf_processing.py'] --> Output ['query1.xlsx']

**Output File Structure:**
- `query1.xlsx` has 2 columns: `name_details` and `quantity` (although quantity is not required for this case study).

#### Step 2: Processing the Query File
1. Process the `query1.xlsx` file.
2. Add more structure to the dataset - item names, categories (like "track", "stud", etc.), and dimensions (like 4IN).

**Considerations:**
- Adding more structure improves results since a basic RAG system and cosine similarity match didn't work well due to similar products.
- Creating a custom vector search method with metadata filtering is needed but requires more time.

**Flow:**
Input ['query1.xlsx'] --> ['query_preprocessing.py'] --> Output ['updated_query1.xlsx']

**Output File Structure:**
- `updated_query1.xlsx` has 4 columns: `name_details`, `quantity`, `dimension`, and `category`.

#### Step 3: Mapping Items
1. Find the best match of the item name with column 3 of the `productdb` using fuzzy matching (threshold: 70).
2. If no match, use regex matching on the category.
3. Perform dimension matching on the retrieved items using regex in the previous step.
4. Retrieve items from step 3 and perform vector search to get the top 10 items.

**Flow:**
Input [query1.xlsx and productdb.csv (column 3)] --> [mapping.py] --> Output [after_mapping.xlsx]

**Output File Structure:**
- `after_mapping.xlsx` has 5 columns: `name_details`, `quantity`, `dimension`, `category`, and `mapped items`.

### Notes

1. Apologies for not retrieving all the top 10 matches for each entry in `request.pdf`. This was done only for categories where mapping was based on category or dimension. For name-based mapping, only the best match was used.
2. An end-to-end pipeline for generating the final quotation is not completed; converting the mapped items to PDF is pending.
3. My first method used ChromaDB as vectordb (also tried FAISS, which performed better with vector search on the query) and Text Embedding 3 Large as the embedding model.
4. The first method had very low latency (almost real-time) but poor results, making it unsuitable for calculating top-k accuracy.
5. The second method, detailed above, takes around 15 minutes for `request1.pdf` and about 20 minutes for `request2.pdf`. This is slow because most matches are based on category and dimension rather than item name.
6. The second method could be optimized using a more sophisticated RAG system as in method 1, but the cost of creating embeddings would remain high. A cost comparison could be made: embedding the entire data (10k items) versus embedding 20 items each with 200 items, resulting in a cost comparison of 10k vs 4k.
