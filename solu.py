import pandas as pd
import PyPDF2

pdf_path = "JAN - MAR. 2024.pdf"
output_xlsx_path = pdf_path.replace(".pdf", "_output.xlsx")

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

    # Save the DataFrame to an Excel file
    sheet.to_excel(output_xlsx_path, index=False)

    # Display the DataFrame
    print("DataFrame:")
    print(sheet)

    print(f"\nData saved to {output_xlsx_path}")
