import csv
import re

def parse_results_to_rows(text):
    """
    Parse the results text where each record is separated by double newlines.
    Returns a list of dictionaries, one per record.
    """
    if not text or not isinstance(text, str):
        return []

    # Split by double newlines to get individual records
    records = text.strip().split('\n')

    parsed_records = []

    for record in records:
        if not record.strip():
            continue

        # Parse key-value pairs: [key]:value;
        # Pattern matches [anything except brackets]:anything until ;
        pattern = r'\[([^\]]+)\]:([^;]+);'
        matches = re.findall(pattern, record)

        if matches:
            record_dict = dict(matches)
            parsed_records.append(record_dict)

    return parsed_records

def flatten_author_columns(input_file, output_file):
    """
    Alternative: Flatten author columns so each record has Author1, Author2, etc.
    and corresponding Uni1, Uni2, etc. as separate columns.
    This is useful if you want to keep the structure in wide format.
    """
    all_rows = []
    all_keys = set()

    with open(input_file, 'r', newline='', encoding='utf-8-sig') as infile:
        reader = csv.DictReader(infile)

        if 'results' not in reader.fieldnames:
            raise ValueError("Column 'results' not found in CSV file")

        for row in reader:
            results_text = row['results']
            parsed_records = parse_results_to_rows(results_text)

            for record in parsed_records:
                all_rows.append(record)
                all_keys.update(record.keys())

    if not all_rows:
        print("No data extracted")
        return

    # Identify author and uni columns to determine max number
    author_cols = [k for k in all_keys if k.startswith('Author_')]
    uni_cols = [k for k in all_keys if k.startswith('Uni_')]

    # Get max author number
    max_author = 0
    for col in author_cols:
        try:
            num = int(col.split('_')[1])
            max_author = max(max_author, num)
        except:
            pass

    # Define fieldnames in order
    base_fields = ['Category', 'Name']
    author_fields = [f'Author_{i}' for i in range(1, max_author + 1)]
    uni_fields = [f'Uni_{i}' for i in range(1, max_author + 1)]

    fieldnames = base_fields + author_fields + uni_fields

    # Write to output CSV
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for record in all_rows:
            # Create a row with default empty values
            row = {field: '' for field in fieldnames}

            # Fill in the values
            for key, value in record.items():
                if key in fieldnames:
                    row[key] = value

            writer.writerow(row)

    print(f"Processing complete (flattened format)!")
    print(f"Output saved to: {output_file}")
    print(f"Extracted {len(all_rows)} records")
    print(f"Found up to {max_author} authors per paper")

# Change these to your actual file paths
input_csv = "data/scientific_programmes/results_2025.csv"  # Your original CSV with 'results' column

try:
    flatten_author_columns(input_csv, "data/extracted_data/extracted_papers_flattened_2025.csv")

except FileNotFoundError:
    print(f"Error: File '{input_csv}' not found")
    print("Please update the 'input_csv' variable with your actual file path")
except Exception as e:
    print(f"Error: {e}")