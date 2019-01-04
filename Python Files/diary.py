from time import *
import os
import ez
from docx import Document
from docx.shared import Pt
leapYear = lambda year:((year % 4 == 0 and year % 100 != 0) or year % 400 == 0)
os.chdir('C:\\Users\\Seaky\\Desktop\\Docs\\日记')
def main(startYear = 0, endYear = 0):
    d = ['Mon','一','Tue','二','Wed','三','Thu','四','Fri','五','Sat','六','Sun','天','年0','年','月0','月']
    startYear = startYear or thisYear
    endYear = endYear or startYear
    t = 28800 + 86400 * (365 * (startYear - 1970) + sum(leapYear(y) for y in range(1970, startYear + 1)))
    for year in range(startYear, endYear + 1):
        days = 365 + leapYear(year)
        t += 86400 * days * (year - startYear)
        s = ''.join([strftime('%Y年%m月%d日   星期%a   天气：\n1、\n2、\n\n',localtime(t + 86400 * day)) for day in range(days)])
        s = ez.sub(s, *d)
        document = Document()
        paragraph = document.add_paragraph(s)
        document.styles['Normal'].paragraph_format.line_spacing = 1.15
        document.styles['Normal'].paragraph_format.space_after = Pt(0)
        document.styles['Normal'].font.size = Pt(10.5)
        document.styles['Normal'].font.name = u'宋体'
        document.save(f'{year}.docx')
        
if __name__ == '__main__':
    main(2010, 2014)

