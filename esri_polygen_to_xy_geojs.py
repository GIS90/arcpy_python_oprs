# coding:utf-8

import codecs
import datetime
import os
import sys

import arcpy


def GetShpRowNums(shpData):
    rowNums = 0
    with arcpy.da.SearchCursor(shpData, ["SHAPE@"]) as cursor:
        for row in cursor:
            rowNums = rowNums + 1
    print rowNums
    return rowNums


def ShpXYToJson(filePath):
    fields = ["ID", "SHAPE@XY"]
    arcpy.env.workspace = filePath
    try:
        for shp in arcpy.ListFiles("*.shp"):
            shpData = os.path.join(filePath, shp)
            jsonFile = os.path.join(filePath, (os.path.splitext(shp)[0] + '_XY_Echart.js'))
            if os.path.exists(jsonFile):
                print 'Json File Is Exists , Delete'
                os.unlink(jsonFile)
            f_w = codecs.open(jsonFile, 'w', 'utf-8')
            f_w.write('var coords={')
            rowNums = GetShpRowNums(shpData)
            num = 0
            with arcpy.da.SearchCursor(shpData, fields) as cursor1:
                for row in cursor1:
                    num = num + 1
                    if isinstance(row[0], unicode):
                        name = row[0].encode('utf-8')
                    else:
                        name = str(row[0]).decode('utf-8')
                    XY = list(row[1])
                    # res = float(name.decode('utf-8'))
                    f_w.write('\r\n')
                    f_w.write('\t')
                    para = float(name)
                    name = int(para)
                    info = '"' + str(name) + '"' + ":" + str(XY)
                    print info
                    cmd = info.decode("utf-8")
                    print XY
                    f_w.write(cmd)
                    if (num == rowNums):
                        f_w.write('\r\n')
                        f_w.write('}')
                    else:
                        f_w.write(',')
                print '%s XY Is Transfer To Json Success ！' % str(shp)
        return 1
    except Exception as e:
        print 'Occur Exception : %s' % e.message
        return -1


# 主函数入口
if __name__ == '__main__':
    print '*************************************************'
    print 'Ihe Python Tool Start Working !'
    startTime = datetime.datetime.now()
    print '*****Start Time : %s*****' % startTime
    path = r'E:\data\nj_js\zq_shp'
    if not os.path.exists(path):
        print 'Path is not exist .'
        sys.exit(0)
    ShpXYToJson(path)
    print 'Tools Is Execute Success !'
    endTime = datetime.datetime.now()
    costTime = (endTime - startTime).seconds
    print '*****Cost Time : %s s.*****' % costTime
    print '*************************************************'
