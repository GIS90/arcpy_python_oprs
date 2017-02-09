# coding:gbk

import xlrd
import codecs
import os
import datetime


def ExcelToEchartMapJson(Xls, Json, SheetNum):
    if os.path.exists(Json):
        os.unlink(Json)
    JsonData = []
    f_w = codecs.open(Json, 'w', 'utf-8')
    excelObj = xlrd.open_workbook(Xls)
    sheetObj = excelObj.sheet_by_index(SheetNum)
    nRow = sheetObj.nrows
    nCol = sheetObj.ncols
    sName = sheetObj.name
    print 'sName = %s , nRows = %d , nCols = %d' % (sName, nRow, nCol)
    for i in range(0, 4):
        print 'colNum = %d , colName = %s' % (i + 1, sheetObj.cell_value(0, i))
    JsonData.append('var peopleNum={"peopleD":{')
    try:
        for num in range(0, 24):
            JsonData.append('"%s":[' % (num))
            for row in range(1, nRow):
                cellHour = int(sheetObj.cell_value(row, 0))
                cellName = sheetObj.cell_value(row, 2)
                cellValue = sheetObj.cell_value(row, 3)
                if (cellHour == num and num < 23):
                    JsonData.append('{"name":"%s","value":%d}' % (cellName, cellValue))
                    if row < (nRow - 24):
                        JsonData.append(',')
                    else:
                        JsonData.append('],')
                elif (cellHour == num == 23):
                    JsonData.append('{"name":"%s","value":%d}' % (cellName, cellValue))
                    if row < (nRow - 24):
                        JsonData.append(',')
                    else:
                        JsonData.append(']}}')
    except Exception as e:
        print e.message
    finally:
        f_w.writelines(JsonData)
        f_w.close()


if __name__ == '__main__':
    print '***************************************'
    print 'Ihe Python Tool Start Working !'
    startTime = datetime.datetime.now()
    print '*****Start Time : %s' % startTime
    '''
    传入之指定的参数：
        FilePath:文件的存放路径
        XlsName：Excel文件的名称
        SheetNum:转成Json文件的sheet表位置角标
    '''
    FilePath = r'E:\2015Project\青岛项目\EchartJsonData'
    XlsName = 'QDXQRS20151005.xls'
    Xls = os.path.join(FilePath, XlsName)
    Json = os.path.join(FilePath, (XlsName.split('.')[0] + '.json'))
    SheetNum = 0
    ExcelToEchartMapJson(Xls, Json, SheetNum)

    print 'Ihe Python Tool Worked OK !'
    endTime = datetime.datetime.now()
    costTime = (endTime - startTime).seconds
    print '*****Cost Time : %s' % costTime
    print '***************************************'
