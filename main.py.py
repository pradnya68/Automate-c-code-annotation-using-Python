import pandas as pd
import os

def extract_all_tables_from_html(html_path):
    """Extract all tables from an HTML file."""
    try:
        if not os.path.exists(html_path):
            raise FileNotFoundError(f"The file {html_path} does not exist.")
        
        tables = pd.read_html(html_path)
        print(f"Extracted {len(tables)} tables from the HTML file.")
        return tables
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return []

def filter_tables_with_status_column(tables):
    """Filter tables based on the presence of a 'Status' column."""
    filtered_tables = [table for table in tables if isinstance(table, pd.DataFrame) and "Status" in table.columns]
    return filtered_tables

def extract_justified_rows(tables):
    """Extract rows where the 'Status' column is 'Justified' with specific columns."""
    justified_rows = []
    required_columns = ["Guideline", "Line", "Severity", "Status", "Comment"]
    
    for table in tables:
        if isinstance(table, pd.DataFrame):
            matching_rows = table[table["Status"].astype(str).str.contains("Justified", case=False, na=False)]
            if not matching_rows.empty:
                existing_columns = [col for col in required_columns if col in matching_rows.columns]
                if existing_columns:
                    selected_rows = matching_rows[existing_columns].copy()
                    justified_rows.append(selected_rows)
    return justified_rows

def generate_c_code_snippet(row):
    """Generate the C code snippet for a single row as a comment."""
    return (
        '/* polyspace<MISRA-C3: %s: %s: justified> %s */\n' % (
            str(row.get("Guideline", "")),
            str(row.get("Severity", "")),
            str(row.get("Comment", ""))
        )
    )

def insert_c_code_into_file(c_paths, justified_rows):
    """Insert the C code snippet into the existing C source files at specified lines."""
    try:
        for c_path in c_paths:
            with open(c_path, 'r') as file:
                lines = file.readlines()
            
            # Flatten all justified rows into a list of tuples (line_number, comment)
            comments = []
            for table in justified_rows:
                for index, row in table.iterrows():
                    line_number = int(row.get("Line", -1))
                    if line_number != -1:
                        comments.append((line_number, generate_c_code_snippet(row)))
            
            # Sort comments by line number
            comments.sort(key=lambda x: x[0])
            
            # Dictionary to accumulate comments by line number
            comments_dict = {}
            for line_number, comment in comments:
                if line_number in comments_dict:
                    comments_dict[line_number].append(comment)
                else:
                    comments_dict[line_number] = [comment]

            # Insert accumulated comments into the file
            line_offset = 0
            for line_number in sorted(comments_dict.keys()):
                insert_position = line_number + line_offset - 1
                if insert_position < len(lines):
                    for comment in comments_dict[line_number]:
                        print(f"Inserting at line {line_number}: {comment.strip()}")
                        lines.insert(insert_position, comment)
                        insert_position += 1
                        line_offset += 1
            
            with open(c_path, 'w') as file:
                file.writelines(lines)
            
            print(f"Data successfully inserted into {c_path}.")
    except Exception as e:
        print(f"Error inserting data into C source files: {e}")

def main(html_path, c_paths):
    """Main function to extract tables from HTML and insert justified comments into C files."""
    print(f"Extracting tables from {html_path}...")
    tables = extract_all_tables_from_html(html_path)
    
    if tables:
        print(f"{len(tables)} tables extracted. Filtering tables with a 'Status' column...")
        filtered_tables = filter_tables_with_status_column(tables)
        
        if filtered_tables:
            print(f"{len(filtered_tables)} tables found with a 'Status' column. Extracting rows where status is 'Justified'...")
            justified_rows = extract_justified_rows(filtered_tables)
            
            if justified_rows:
                print(f"Rows with 'Justified' status found. Inserting data into {len(c_paths)} C files...")
                insert_c_code_into_file(c_paths, justified_rows)
            else:
                print(f"No rows with 'Justified' status were found.")
        else:
            print(f"No tables with a 'Status' column were found.")
    else:
        print("No tables were extracted from the HTML file.")

# Example usage with multiple C files
html_path = r"C:\Users\Admin\Desktop\Polyspace\Polyspace_Developer_report.html"
c_paths = [
    r"C:\Users\Admin\Desktop\Polyspace\MqCddDcfOtp.c",
    
]

main(html_path, c_paths)
