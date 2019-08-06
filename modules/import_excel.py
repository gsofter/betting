#import the xlrd module

import xlrd

#open the spreadsheet file(or workbook)
workbook = xlrd.open_workbook("input.xlsx")


#open the sheet
#if you know the name of the sheet, you can open it by running the following
worksheet = workbook.sheet_by_index(0)

#Once you haev selected the worksheet,
#you can extract the value of a particular data cell as follows


print("the value at row 4 column 2 is : {0}".format(worksheet.cell(4,2).value))