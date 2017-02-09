# coding:utf-8
"""
    用来把shp数据(polygon类型)转为相对应的EChart后台的Json格式数据
"""
import codecs
import datetime
import os
import sys

import arcpy


def GetShpRowNums(shpData):
    """
    获取shp数据包含的数量
    :param shpData: shp数据的文件路径
    :return: 返回shp数据的包含的数据个数
    """
    rowNums = 0
    with arcpy.da.SearchCursor(shpData, ["SHAPE@"]) as cursor:
        for row in cursor:
            rowNums += 1
    print '%s num is %d' % (shpData, rowNums)
    return rowNums


def ShpGeoJsonToJson(shpField, shpPath):
    """
    将shp类型数据转为Json数据
    :param shpField: shp数据进行写入Json的标识字段
    :param shpPath: 存放shp数据的文件夹路径
    :return:
    """
    assert isinstance(shpPath, basestring)
    assert isinstance(shpField, list)
    arcpy.env.workspace = shpPath
    for shp in arcpy.ListFiles("*.shp"):
        shpData = os.path.join(shpPath, shp)
        jsonFile = os.path.join(shpPath, (os.path.splitext(shp)[0] + '_EChart.js'))
        if os.path.exists(jsonFile):
            print '%s File Is Exists , Delete' % jsonFile
            os.unlink(jsonFile)
        f_w = codecs.open(jsonFile, 'w', 'utf-8')
        data = []
        num = 0
        rowNums = GetShpRowNums(shpData)
        try:
            with arcpy.da.SearchCursor(shpData, fields) as cursor:
                data.append('{"type": "FeatureCollection" ,')
                data.append('"features": [')
                for row in cursor:
                    num += 1
                    if isinstance(row[0], unicode):
                        name = row[0].encode('utf-8')
                    else:
                        name = str(row[0]).decode('utf-8')
                    geoName = row[0]
                    info = row[1]
                    geoInfo = str(info).split(':')[1].split(',"')[0].split('}')[0]
                    data.append('{"type":"Feature",')
                    data.append('"properties":{"name":"%s"},' % geoName)
                    data.append('"geometry":{')
                    data.append('"type":"MultiPolygon",')
                    data.append('"coordinates":[%s' % geoInfo)
                    if num < rowNums:
                        data.append(']}},')
                    else:
                        data.append(']}}]}')
                f_w.writelines(data)
                f_w.close()
                print '%s is transfer to json success ！' % str(jsonFile)
        except Exception as e:
            print 'Occur exception : %s' % e.message
            print 'Tool execute failure .'
            sys.exit(0)


# 主函数入口
if __name__ == '__main__':
    print '*************************************************'
    print 'The python tool start working !'
    startTime = datetime.datetime.now()
    print '*****Start time : %s*****' % startTime
    path = r'E:\data\hn'
    fields = ["NAME", "SHAPE@JSON"]
    if not os.path.exists(path):
        print 'Path is not exist .'
        sys.exit(0)
    ShpGeoJsonToJson(fields, path)
    print 'Tools is execute success !'
    endTime = datetime.datetime.now()
    costTime = (endTime - startTime).seconds
    print '*****Cost time : %s s.*****' % costTime
    print '*************************************************'
