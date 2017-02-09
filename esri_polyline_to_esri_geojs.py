# coding:utf-8

import codecs
import datetime
import os
import sys

import arcpy

"""
    用来把shp数据(polline类型)转为相对应的ESRI Service Json格式数据
"""


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


def shpGeoJsonToJson(fields, path):
    """
    将shp类型数据转为Json数据
    :param fields: shp数据进行写入Json的标识字段
    :param path: 存放shp数据的文件夹路径
    :return:执行错误，退出脚本
    """
    assert isinstance(path, basestring)
    assert isinstance(fields, list)
    arcpy.env.workspace = path

    for shp in arcpy.ListFiles("*.shp"):
        try:
            shape = os.path.join(path, shp)
            json_file = os.path.join(path, (os.path.splitext(shp)[0] + '_New.js'))
            if os.path.exists(json_file):
                print "%s is exist,delete it." % str(os.path.split(json_file)[1])
                os.unlink(json_file)
            f_w = codecs.open(json_file, 'w', 'utf-8')
            f_w.write('{')
            f_w.write('"displayFieldName": "NAME",')
            f_w.write(' "fieldAliases": {"%s": "%s"},' % (fields[0], fields[0]))
            f_w.write('"geometryType": "esriGeometryPolyline",')
            f_w.write('"spatialReference": {"wkid": 4326,"latestWkid": 4326},')
            f_w.write('"fields": [{"name": "%s","type": "esriFieldTypeOID","alias": "%s"}],'
                      % (fields[0], fields[0]))
            f_w.write('"features": [')
            rowNum = GetShpRowNums(shape)
            n = 1
            with arcpy.da.SearchCursor(shape, fields) as cursor:
                for row in cursor:
                    try:
                        objectid = int(row[0])
                        print objectid
                        geo = str(row[1]).split(':')[1].split(',"')[0]
                        geo_spl = geo.split('[[[')[1].split(']]]')[0].split('],[')
                        geo_new = '[[['
                        for i in range(0, len(geo_spl)):
                            i_new = geo_spl[i].split(',')
                            for ii in range(0, len(i_new)):
                                value = str(float(i_new[ii]))
                                geo_new += value
                                if ii == 0:
                                    geo_new += ','
                            if i < len(geo_spl) - 1:
                                geo_new += '],['
                        geo_new += ']]]'
                        f_w.write('{')
                        f_w.write('"attributes": {"%s": %d},' % (fields[0], objectid))
                        f_w.write('"geometry": {"paths":%s}' % geo_new)
                        if n != rowNum:
                            f_w.write('},')
                            n += 1
                        else:
                            f_w.write('}]}')
                    except Exception as e:
                        print 'shpGeoJsonToJson %d occur exception: %s' % (objectid, e.message)

                print '%s is tranfter success ！' % str(json_file)
                f_w.close()
        except Exception as e:
            pass


# 主函数入口
if __name__ == '__main__':

    print 'Ihe Python Tool Start Working !'
    start_time = datetime.datetime.now()
    print '*****Start Time : %s*****' % start_time
    shape_dir = r'E:\data\ty\ty_test'
    shape_fields = ["OBJECTID", "SHAPE@JSON"]
    if not os.path.exists(shape_dir):
        print 'Path is not exist, please input availiable path.'
        sys.exit(0)
    shpGeoJsonToJson(shape_fields, shape_dir)
    print 'Tools Is Execute Success !'
    end_time = datetime.datetime.now()
    cost_time = (end_time - start_time).seconds
    print '*****Cost Time : %s s.*****' % cost_time
