# Automate-c-code-annotation-using-Python

## Overview
This Python script automates the annotation of C source code using **Polyspace MISRA guideline reports**. It extracts justified findings from HTML reports and inserts formatted comments directly into the corresponding C source files, reducing manual review time and effort.

## Key Features
- Extracts tables from HTML Polyspace reports
- Filters rows with 'Justified' status
- Generates formatted C code comments
- Inserts comments automatically into C source files
- Orchestrated via a main function for seamless execution

## Technologies Used
- Python
- Pandas (for HTML table extraction and filtering)

## Function Details

### 1. `extract_all_tables_from_html(html_path)`
- **Purpose:** Extract all tables from an HTML file using Pandas.  
- **Parameters:** `html_path` (str) – Path to the HTML file.  
- **Returns:** List of tables as Pandas DataFrames.  
- **Comments:** Checks file existence, reads HTML tables, handles exceptions.

### 2. `filter_tables_with_status_column(tables)`
- **Purpose:** Keeps only tables containing a 'Status' column.  
- **Parameters:** `tables` (list of DataFrames)  
- **Returns:** Filtered list of tables  
- **Comments:** Uses list comprehension to filter tables.

### 3. `extract_justified_rows(tables)`
- **Purpose:** Extracts rows where 'Status' is 'Justified'.  
- **Returns:** List of DataFrames containing justified rows.

### 4. `generate_c_code_snippet(row)`
- **Purpose:** Generates formatted C code comment from a data row.  
- **Returns:** Comment as a string.

### 5. `insert_c_code_into_file(c_paths, justified_rows)`
- **Purpose:** Inserts generated comments into C source files.  
- **Parameters:** 
  - `c_paths` (list) – C file paths  
  - `justified_rows` (list of DataFrames)  
- **Returns:** None

### 6. `main(html_path, c_paths)`
- **Purpose:** Orchestrates extraction and insertion workflow.  
- **Parameters:** 
  - `html_path` – Path to HTML report  
  - `c_paths` – List of C files  
- **Returns:** None

## Usage
```bash
python automate_c_annotation.py <polyspace_report.html> <c_file1.c> <c_file2.c> ...

