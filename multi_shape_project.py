# -*- coding: utf-8 -*-

"""
------------------------------------------------
@version: 1.0v
@author: PyGoHU
@contact: gaoming971366@163.com
@software: PyCharm Community Edition
@file: multi_shape_project.py
@time: 2016/8/12 11:52
@describe:
@remark: shape is not null interact to chip
------------------------------------------------
"""

import arcpy
import os
import sys
import datetime


def define_pro_wgs84(in_path):
    """
    Define shpfile project to wgs84
    :param in_path: input file path
    :return:
    """
    print "*****************************************"
    print "Bat define project to shapeFile----------"

    assert isinstance(in_path, basestring)
    if not os.path.exists(in_path):
        print 'Input path is incorrect ,please re-input.'
        sys.exit(1)
    arcpy.env.workspace = in_path
    for shp in arcpy.ListFiles('*.shp'):
        wgs84 = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]]," \
                "PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
        in_data_set = shp
        try:
            arcpy.DefineProjection_management(in_data_set, wgs84)
            print '%s Define Project wgs84 Success !' % in_data_set
        except Exception as e:
            print e.message

    print "ALL data define project success ---------"
    print "*****************************************"


def trans_pro_wgs84(in_path, out_path):
    """
    Transform shpfile project to wgs84
    :param in_path: input file path
    :param out_path: output file path
    :return:
    """
    print "*****************************************"
    print "Bat shapeFile transfer project to wgs84----------"

    assert isinstance(in_path, basestring)
    assert isinstance(out_path, basestring)
    if not os.path.exists(in_path):
        print 'Input path is incorrect ,please re-input.'
        sys.exit(1)
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    arcpy.env.workspace = in_path
    for shp in arcpy.ListFiles('*.shp'):
        wgs84 = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]]," \
                "PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
        in_data_set = shp
        template_data_set = ''
        transformation = ''
        outfile = out_path
        try:
            arcpy.BatchProject_management(in_data_set,
                                          outfile,
                                          wgs84,
                                          template_data_set,
                                          transformation)
            print '%s transform project success !' % in_data_set
        except Exception as te:
            print 'transprowgs84 occur exception : %s' % te.message

    print "ALL Data transform Project Success ---------"
    print "*****************************************"


if __name__ == '__main__':

    input_dir = r'E:\data\jn\02ChinaVector13Q3_clip'
    output_dir = r'E:\data\jn\02ChinaVector13Q3_clip(wgs84)'
    start_time = datetime.datetime.now()
    try:
        # define_pro_wgs84(infilePath)
        trans_pro_wgs84(input_dir, output_dir)
    except Exception as e:
        print "do_clip occur exception: %s" % e.message
    end_time = datetime.datetime.now()
    exe_time = (end_time - start_time).seconds
    print "All features finish and cost time is : %s s." % exe_time
