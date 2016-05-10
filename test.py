import openpyxl

f_xlsx = r'C:\abykov\shared\projects\15_PythonTest\data\RVMPtitles.xlsx'
wb = openpyxl.load_workbook(f_xlsx, use_iterators=True)
wbfs = wb.get_sheet_names()[0]
wsh = wb.get_sheet_by_name(wbfs)

i = 1
for row in wsh.iter_rows():
    #print row
    print i
    for cell in row:
        print cell.value
    i = i + 1

#from openpyxl import Workbook
