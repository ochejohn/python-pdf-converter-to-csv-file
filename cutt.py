import pdfplumber
import re
import pandas as pd

pdf_path = "JAN - MAR. 2024.pdf"
output_xlsx_path = "outpu_data.xlsx"

try:
    with pdfplumber.open(pdf_path) as pdf_document:
        # Get the total number of pages in the PDF
        total_pages = len(pdf_document.pages)

        # Initialize an empty list to store processed data
        all_data = []

        # Loop through pages 28, 29, and 30
        for target_page_number in range(28, min(total_pages, 39)):
            # Get the specified page
            target_page = pdf_document.pages[target_page_number - 1]

            # Extract text from the page
            page_text = target_page.extract_text()

            # Split the text into lines
            lines = page_text.split('\n')

            # Start reading from line 3 and exclude the last two lines
            processed_lines = lines[2:-2]

            # Find the position of "SANCTA MARIA 22 CONSTITUTION" using regular expressions
            regex_pattern = re.compile(r'SANCTA MARIA 22 CONSTITUTION')
            match = regex_pattern.search(page_text)

            # Add space before reading line 4
            processed_lines[0] += " "

            # Adjust line 4 to start from the position of "SANCTA MARIA 22 CONSTITUTION"
            if match:
                start_position = match.start()
                processed_lines[1] = processed_lines[1][:start_position] + "SPECIALIST AND MAT.- CRESCENT ABA"

            # Concatenate "child" and the corresponding number into a single column
            for i in range(len(processed_lines)):
                if "child" in processed_lines[i].lower():
                    processed_lines[i] = processed_lines[i].replace("child", f"child {processed_lines[i + 1]}")
                    processed_lines.pop(i + 1)

            # Split the modified text into columns
            data = [line.split() for line in processed_lines]

            # Append the data to the list
            all_data.extend(data)

        # Create a DataFrame with the appropriate number of columns
        num_columns = max(len(row) for row in all_data)
        column_names = [f"Col{i}" for i in range(1, num_columns + 1)]
        df = pd.DataFrame(all_data, columns=column_names)

        # Save the DataFrame to an Excel file
        df.to_excel(output_xlsx_path, index=False)

        # Display the DataFrame
        print("DataFrame:")
        print(df)

        print(f"\nData saved to {output_xlsx_path}")

except Exception as e:
    print(f"Error reading PDF: {e}")




