import pdfplumber
import pandas as pd

def read_table(path):
    count = 0
    headers_written = False  # Flag to check if headers have been written
    rows = []  # List to store rows from all pages

    with pdfplumber.open(path) as pdf:
        print(len(pdf.pages))
        
        for page in pdf.pages:
            table_data = pdf.pages[count].extract_table()

            try:
                for row in table_data:
                    # Append each row to the list
                    rows.append(row)

                print(f'Data from page {count + 1} has been collected')
            except TypeError:
                pass
            
            count += 1

    # Create a DataFrame from the list of rows
    df = pd.DataFrame(rows)
    return df
    # # Specify the CSV file path
    # csv_file_path = csvname

    # # Write DataFrame to CSV without including headers, append if file exists
    # df.to_csv(csv_file_path, mode='a', index=False, header=headers_written)

    # print(f'Data has been written to {csv_file_path}')

