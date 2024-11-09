import pandas as pd
import pyreadstat

# Load the Excel file
excel_data = pd.read_excel('/Users/zheer/Desktop/s.xlsx')

# Clean column names by removing spaces, slashes, and special characters
excel_data.columns = (
    excel_data.columns
    .str.replace(r'\W', '', regex=True)  # Remove non-alphanumeric characters
    .str.replace(' ', '_')               # Replace spaces with underscores
)

# Convert to SPSS format
pyreadstat.write_sav(excel_data, 'survey.sav')
