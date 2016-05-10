from openpyxl import load_workbook
wb = load_workbook(r'D:\abykov\BigProjectFiles\151003 Lethbridge Ecological Inventory\titles_160411\RVMP titles222.xlsx')
print wb.get_sheet_names()
ws = wb.active
for row in ws.iter_rows():
    takePrevVal = 0
    for cell in row:
        if cell.column == 'A':
            if cell.value is not None:
                curr_row = row
            elif cell.value is None:
                takePrevVal = 1
                print '------------None:' + str(cell.row)
        if takePrevVal:
            if cell.value is None:
                print 'Col: ' + str(cell.col_idx)
                print 'Val+: ' + str(curr_row[cell.col_idx-1].value)
                if curr_row[cell.col_idx-1].value is not None:
                    cell.value = curr_row[cell.col_idx-1].value
            else:
                print 'Col: ' + str(cell.col_idx)
                print 'Val: ' + str(cell.value)
            #print curr_row[cell.col_idx-1].value

wb.save(r'D:\abykov\BigProjectFiles\151003 Lethbridge Ecological Inventory\titles_160411\RVMP titles222b.xlsx')