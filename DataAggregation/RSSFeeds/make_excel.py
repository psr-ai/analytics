from openpyxl import Workbook, load_workbook
wb = load_workbook('news.xlsx')
# grab the active worksheet
ws = wb.active
# Data can be assigned directly to cells
# Rows can also be appended
ws.append([4, 5, 6])
# Save the file
wb.save("news.xlsx")

