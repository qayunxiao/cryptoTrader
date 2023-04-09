# -*- coding: utf-8 -*-
# @Time    : 2019/9/18 15:45
# @Author  : alvin
# @File    : qatest_excel.py
# @Software: PyCharm

from openpyxl import Workbook
from openpyxl.reader.excel import load_workbook

import os
import time



def writeExcel():
    # 获取文件路径
    excelPath = os.path.join(os.getcwd(), 'ExcelData')
    print (excelPath)
    # 定义文件名称
    #  invalid mode ('wb') or filename: 'Excel2017-09-21_20:15:57.xlsx'   这种方式明明文件，会提示保存失败，无效的文件名。
    # nameTime = time.strftime('%Y-%m-%d_%H:%M:%S')
    nameTime = time.strftime('%Y-%m-%d_%H-%M-%S')
    excelName = 'Excel' + nameTime + '.xlsx'
    ExcelFullName= os.path.join(excelPath,excelName)
    print (ExcelFullName)
    wb = Workbook()
    ws = wb.active
    tableTitle = ['userName', 'Phone', 'age', 'Remark']
    # 维护表头
    #        if row < 1 or column < 1:
    #          raise ValueError("Row or column values must be at least 1")
    # 如上，openpyxl 的首行、首列 是 （1,1）而不是（0,0），如果坐标输入含有小于1的值，提示 ：Row or column values must be at least 1，即最小值为1.
    for col in range(len(tableTitle)):
        c = col + 1
        ws.cell(row=1, column=c).value = tableTitle[col]

    # 数据表基本信息
    tableValues = [['张学友', 15201062100, 18, '测试数据！'], ['李雷', 15201062598, 19, '测试数据！'],['Marry', 15201062191, 28, '测试数据！']]

    for row in range(len(tableValues)):
        ws.append(tableValues[row])
    #wb.save(ExcelFullName)
    wb.save(filename=ExcelFullName)
    return ExcelFullName

def readExcel(ExcelFullName):
    wb = load_workbook(ExcelFullName)
    #wb = load_workbook(filename=ExcelFullName)

    # 获取当前活跃的worksheet,默认就是第一个worksheet
    #ws = wb.active
    # 当然也可以使用下面的方法
    # 获取所有表格(worksheet)的名字
    sheets = wb.get_sheet_names()
    print (sheets)
    # # 第一个表格的名称
    sheet_first = sheets[0]
    # # 获取特定的worksheet
    #
    ws = wb.get_sheet_by_name(sheet_first)
    print (sheet_first)
    print (ws.title)
    print ("^^^")
    # 获取表格所有行和列，两者都是可迭代的
    rows = ws.rows
    print (rows)
    columns = ws.columns
    # 迭代所有的行
    for row in rows:
        line = [col.value for col in row]
        print (line)
    # 通过坐标读取值
    print (ws['A1'].value)  # A表示列,1表示行
    print (ws.cell(row=1, column=1).value)

if __name__ == '__main__':
    ExcelFullName = writeExcel()
    # readExcel(ExcelFullName)
