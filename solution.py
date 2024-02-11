import pandas as pd
import PyPDF2

pdf_path = "JAN - MAR. 2024.pdf"

with open(pdf_path, 'rb') as pdf:
    pdf = PyPDF2.PdfReader(pdf)
    first_page = pdf.pages[1]
    headers = first_page.extract_text().split("\n")[0].split()[2:]
    sheet = pd.DataFrame(columns=headers)

    for page in pdf.pages[1:]:
        lines = page.extract_text().split("\n")
        if lines[0].lower().startswith("hmo summary"):
            lines = lines[2:]

        for line in lines[1:]:
            if line.split() == headers:
                continue

            data = [d.strip() for d in line.split("+ + + =")]
            if len(data) < 2:
                break

            hcp_id = data[1].split()[0]
            hcp_name = " ".join(data[1].split()[1:])
            principal = data[0].split()[0] + " +"
            dependant = data[0].split()[1] + " +"
            extra_dep = data[0].split()[2] + " +"
            voluntary = data[0].split()[3] + " ="
            beneficiaries = data[0].split()[4]
            sheet = pd.concat([sheet, pd.DataFrame([{
                "HCP_ID": hcp_id,
                "hcpname": hcp_name,
                "Principal": principal,
                "Dependant": dependant,
                "ExtraDep": extra_dep,
                "Voluntary": voluntary,
                "beneficiaries": beneficiaries
            }])], ignore_index=True)
        else:
            continue
        break

    sheet.to_csv(pdf_path.replace(".pdf", ".csv"), index=False)




#  # Import the pandas library for data manipulation and analysis
# import pandas as pd

# # Import PyPDF2 library for working with PDF files
# import PyPDF2

# # Specify the path to the PDF file
# pdf_path = "JAN - MAR. 2024.pdf"

# # Open the PDF file in binary mode
# with open(pdf_path, 'rb') as pdf:
#     # Use PyPDF2 to read the PDF file
#     pdf = PyPDF2.PdfReader(pdf)

#     # Extract the first page of the PDF
#     first_page = pdf.pages[1]

#     # Extract headers from the first page's text
#     headers = first_page.extract_text().split("\n")[0].split()[2:]

#     # Create an empty DataFrame with extracted headers
#     sheet = pd.DataFrame(columns=headers)

#     # Loop through pages starting from the second page
#     for page in pdf.pages[1:]:
#         # Split the text of the page into lines
#         lines = page.extract_text().split("\n")

#         # Check if the page starts with "HMO Summary" and skip relevant lines
#         if lines[0].lower().startswith("hmo summary"):
#             lines = lines[2:]

#         # Loop through each line of the page
#         for line in lines[1:]:
#             # Skip lines that match the headers
#             if line.split() == headers:
#                 continue

#             # Split the line using "+ + + =" as a separator
#             data = [d.strip() for d in line.split("+ + + =")]

#             # Break if the line does not contain enough data
#             if len(data) < 2:
#                 break

#             # Extract values from the data list
#             hcp_id = data[1].split()[0]
#             hcp_name = " ".join(data[1].split()[1:])
#             principal = data[0].split()[0] + " +"
#             dependant = data[0].split()[1] + " +"
#             extra_dep = data[0].split()[2] + " +"
#             voluntary = data[0].split()[3] + " ="
#             beneficiaries = data[0].split()[4]

#             # Concatenate the extracted values into the DataFrame
#             sheet = pd.concat([sheet, pd.DataFrame([{
#                 "HCP_ID": hcp_id,
#                 "hcpname": hcp_name,
#                 "Principal": principal,
#                 "Dependant": dependant,
#                 "ExtraDep": extra_dep,
#                 "Voluntary": voluntary,
#                 "beneficiaries": beneficiaries
#             }])], ignore_index=True)
#         else:
#             continue
#         break

#     # Save the DataFrame to a CSV file with the same name as the PDF file
#     sheet.to_csv(pdf_path.replace(".pdf", ".csv"), index=False)
