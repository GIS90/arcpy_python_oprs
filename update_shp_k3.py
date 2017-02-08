# -*- coding:utf-8 -*-


import datetime
import random

import arcpy
# import execeptionLogging


def updateShpK3(filePath):
    print 'Start Update LinkGeo K3 ........'
    field = 'k3'
    arcpy.env.workspace = filePath
    # 遍历数据
    for shp in arcpy.ListFiles('*.shp'):
        # 更新区域K3
        if shp == 'region.shp':
            cursor = arcpy.UpdateCursor(shp)
            fields = arcpy.ListFields(shp)
            for row in cursor:
                try:
                    k3 = random.uniform(0, 8)
                    row.setValue(field, k3)
                    cursor.updateRow(row)
                    print 'FID = %s %s ShpFile Is Update Success !' % (row.getValue(fields[0].name), row.getValue(fields[3].name))
                except Exception as e:
                    print '-----Occur Exception Info :-----'
                    logType = 'error'
                    logInfo = e.message
                    execeptionLogging.log(logType, logInfo)
        print 'Area Update All OK----------------------------'
        # 更新路网K3
        if shp == 'Linkgeo.shp':
            cursor = arcpy.UpdateCursor(shp)
            fields = arcpy.ListFields(shp)
            for row in cursor:
                try:
                    k3 = random.uniform(0, 8.5)
                    row.setValue(field, k3)
                    cursor.updateRow(row)
                    print 'FID = %s ShpFile Is Update Success !' % row.getValue(fields[0].name)
                except Exception as e:
                    print '-----Occur Exception Info :-----'
                    logType = 'error'
                    logInfo = e.message
                    execeptionLogging.log(logType, logInfo)
        print 'LinkGeo Update All OK----------------------------'


if __name__ == '__main__':

    n = 0
    while True:
        print 'Execute %s ' % n
        n += 1
        filePath = r'E:\data\jn\02ChinaVector13Q3_clip'

        # 获取当前时间
        now = datetime.datetime.now()
        timeFormat = '%Y-%m-%d-%H:%m:%S'
        startTime = now.strftime(timeFormat)
        print '********************************************'
        print 'Start Time Is : %s' % startTime

        # 对数据进行update操作
        updateShpK3(filePath)
        # time.sleep(1)
        # 获取更新后时间，计算脚本运行时间
        endTime = datetime.datetime.now()
        costTime = (endTime - now).seconds
        print 'PyScript Cost Time Is : %s' % costTime
        print '********************************************'
