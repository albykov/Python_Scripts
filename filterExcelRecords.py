#author: albykov@gmail.com
#non standard includes: openpyxl
#usage: scans excel spreadsheet and fills the gaps using previous rows

#load library
from openpyxl import load_workbook
import myhelpers
import fileLocations

def getShortTitleNameNoSpaces(tn):
    if len(tn.split('+')) > 1:
        return tn.split('+')[0].replace(' ', '') + tn.split('+')[1].zfill(3)
    else:
        return tn.replace(' ', '')

#load workbook to memory
wbPath = fileLocations.lethbridge_TitleExcel
wb = load_workbook(wbPath)
#print wb.get_sheet_names()

#get active worksheet
ws = wb.active

#go through all rows
isFirstRow = True
for row in ws.iter_rows():
    if not isFirstRow:
        takePrevVal = 0
        #go through all cell of current row
        for cell in row:
            #if this is a first column
            if cell.column == 'A':
                #if this column is non None
                if cell.value is not None:
                    #save it to variable curr_row
                    curr_row = row
                    print cell.row
                    cell.value = getShortTitleNameNoSpaces(cell.value)
                    #if this cell is None
                elif cell.value is None:
                    #switch to fix it
                    takePrevVal = 1
                    print '------------None:' + str(cell.row)
                    #if fix switcher is on
            if takePrevVal:
                #if current cell value is None
                if cell.value is None:
                    print 'Col: ' + str(cell.col_idx)
                    print 'Val+: ' + str(curr_row[cell.col_idx-1].value)
                    #if saved prev row cell value is non None
                    if curr_row[cell.col_idx-1].value is not None:
                        cell.value = curr_row[cell.col_idx-1].value
                else:
                    print 'Col: ' + str(cell.col_idx)
                    print 'Val: ' + str(cell.value)
    else:
        isFirstRow = False
#save workbook
print myhelpers.getNewFilePathWithDateNoSpaces(wbPath)
wb.save(myhelpers.getNewFilePathWithDateNoSpaces(wbPath))