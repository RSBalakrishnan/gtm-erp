import openpyxl

def debug_excel(excel_path):
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    sheet = wb.active
    
    for i, row in enumerate(sheet.iter_rows(max_row=15, values_only=True)):
        print(f"Row {i+1}: {row}")

if __name__ == "__main__":
    debug_excel("/Users/apple/Desktop/gtm/forscrapling.xlsx")
