# coding:utf-8

import os
import arcpy
import codecs
import sys

reload(sys)
sys.setdefaultencoding('utf8')

filePath = r'E:\region'
arcpy.env.workspace = filePath
for shp in arcpy.ListFiles('*.shp'):
    fc = os.path.join(filePath, shp)
    desc = arcpy.Describe(fc)
    jsonFile = os.path.join(filePath, (os.path.splitext(shp)[0] + '_Echart.json'))
    if os.path.exists(jsonFile):
        print 'Json File Exist , Delete . . . . . .'
        os.unlink(jsonFile)
    f_w = codecs.open(jsonFile, 'w', 'utf-8')
    if desc.shapeType == 'Polyline':
        fields = ['NAME', 'SP', 'EP']
        with arcpy.da.SearchCursor(fc, fields) as cursor:
            for row in cursor:
                name = row[0]
                sp = row[1]
                ep = row[2]
                f_w.write('%s : [' % name)
                f_w.write("{'name':'%s'},{'name':'%s','value':'0'}" % (sp, ep))
                f_w.write(']')
                f_w.write('\r\n')
    f_w.close()
    print 'OK !'
