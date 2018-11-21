import xlwt
import xlsxwriter
from django.http import HttpResponse

def export_list_xls(request , list, filename):
    #response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    filename = "python_excel_test.xls"

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=python_excel_test.xls'+filename


    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Damage')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Email', 'Thl', 'Com', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = list.values_list('name', 'email', 'thl', 'com')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)


    #wb.save(filename)
    wb.save(response)

    return response



#  excel export xlsxwriter
def testxlsxwriter(query):

    workbook = xlsxwriter.Workbook('/temp/hello.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'name')
    worksheet.write('B1', 'email')
    worksheet.write('C1', 'thl')
    worksheet.write('D1', 'com')

    row = 1
    for item in query:
        worksheet.write(row, 0, item.name)
        worksheet.write(row, 1, item.email)
        worksheet.write(row, 2, item.thl)
        worksheet.write(row, 3, item.com)
        row = row + 1

    workbook.close()
