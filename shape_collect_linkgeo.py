# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe: 
------------------------------------------------
"""
import os
import sys
import Queue
from threading import Thread

import arcpy

reload(sys)
sys.setdefaultencoding('utf-8')

__version__ = "v.10"
__author__ = "PyGo"
__time__ = "2017/1/23"

IS_THREADS = True
SHAPE_DEFAULT_FIELDS = ['name', 'kind', 'type', 'class', 'k3']

GDAL_PATH_CODE = "GDAL_FILENAME_IS_UTF8"
GDAL_ATTR_CODE = "SHAPE_ENCODING"
GDAL_DRIVER = "ESRI Shapefile"

COSUMER_MAX = 3

try:
    import ogr
    import gdal
except ImportError as e:
    from osgeo import ogr
    from osgeo import gdal
else:
    gdal.SetConfigOption(GDAL_PATH_CODE, "NO")
    gdal.SetConfigOption(GDAL_ATTR_CODE, "")
    ogr.RegisterAll()
    driver = ogr.GetDriverByName(GDAL_DRIVER)
    queue = Queue.Queue()


class Consumer(Thread):
    def __init__(self, name, shape):
        Thread.__init__(self)
        self.name = name
        self.is_stop = False
        self.src_ft = shape

    def run(self):
        while not self.is_stop:
            try:
                tar_ft = queue.get(block=True, timeout=20)
                print "Thread %s is run %s" % (self.name, os.path.splitext(tar_ft)[1])

            except Exception as e:
                pass




class Shape(object):
    def __init__(self, workspace):
        self.__workspace = workspace

    def create(self):

        shpgcs = """GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],
                    PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;
                    -100000 10000;-100000 10000;8.98315284119522E-09;.001;.001;IsHighPrecision
                 """
        shpname = "LinkGeo.shp"
        shptype = "POLYLINE"
        template = ""
        has_m = "DISABLED"
        has_z = "DISABLED"
        arcpy.env.workspace = self.__workspace
        ft = os.path.abspath(os.path.join(self.__workspace, shpname))
        workspace = os.path.dirname(ft)

        if os.path.exists(ft):
            return ft

        try:
            arcpy.CreateFeatureclass_management(out_path=workspace,
                                                out_name=shpname,
                                                geometry_type=shptype,
                                                template=template,
                                                has_m=has_m,
                                                has_z=has_z,
                                                spatial_reference=shpgcs,
                                                config_keyword=None,
                                                spatial_grid_1=None,
                                                spatial_grid_2=None,
                                                spatial_grid_3=None)
        except Exception as e:
            emsg = "Shape create cccur exception: " + e.message
            raise Exception(emsg)
        else:
            print "Shape create %s is finish" % shpname
            return ft

    def defattr(self, shape):

        ds = driver.Open(shape, 1)
        layer = ds.GetLayerByIndex(0)
        for fn in SHAPE_DEFAULT_FIELDS:
            try:
                if fn == 'name':
                    field = ogr.FieldDefn(fn, ogr.OFTString)
                    field.SetWidth(20)
                    layer.CreateField(field)
                elif fn == 'kind':
                    field = ogr.FieldDefn(fn, ogr.OFTString)
                    field.SetWidth(20)
                    layer.CreateField(field)
                elif fn == 'type':
                    field = ogr.FieldDefn(fn, ogr.OFTString)
                    field.SetWidth(20)
                    layer.CreateField(field)
                elif fn == 'class':
                    field = ogr.FieldDefn(fn, ogr.OFTInteger)
                    field.SetWidth(8)
                    layer.CreateField(field)
                elif fn == 'k3':
                    field = ogr.FieldDefn(fn, ogr.OFTReal)
                    field.SetWidth(8)
                    field.SetPrecision(4)
                    layer.CreateField(field)
                else:
                    break
            except Exception as e:
                emsg = "Shape defattr is error: %s" % e.message
                raise Exception(emsg)
        print 'Shape defattr %s is finish' % SHAPE_DEFAULT_FIELDS

    def appattr(self, fname, ftype):
        pass

    def parattr(self):
        pass

    def delattr(self):
        pass

    def collect(self, shape):
        assert isinstance(shape, basestring)
        for c in range(0, COSUMER_MAX):
            cname = 'consumer_' + str(c)
            cons = Consumer(consume_name, shape)
            cons.start()
            cons.join()
        print 'Shape LinkGeo.shp collect is finish'


def main(shape_folder):

    assert isinstance(shape_folder, basestring)

    if not os.path.isdir(path):
        print '%s is not folder, please reinput' % path
        sys.exit(1)
    if not os.path.exists(path):
        print '%s is not exist, please reinput' % path
        sys.exit(1)
    try:
        arcpy.env.workspace = shape_folder
        for f in arcpy.ListFiles('*.shp'):
            ft = os.path.join(shape_folder, f)
            ft = os.path.abspath(ft)
            desc = arcpy.Describe(ft)
            if hasattr(desc, "shapeType"):
                shape_type = desc.shapeType
                if shape_type == 'Polyline':
                    ft_name = os.path.splitext(f)[0].split("_")[0]
                    if ft_name == "铁路" or ft_name == "轮渡":
                        continue
                    else:
                        queue.put(ft)
                        field = "type"
                        expression = ft_name
                        arcpy.AddField_management(f, field, "TEXT", "", "", "20")
                        arcpy.CalculateField_management(f, field, expression, "PYTHON_9.3")

        shape = Shape(shape_folder)
        linkgeo = shape.create()
        shape.defattr(linkgeo)
        shape.collect(linkgeo)

    except Exception as e:
        print 'main occur error: %s' % e.message
    else:
        print 'finish'



if __name__ == '__main__':
    path = 'E:\\data\\jn\\Map2013City_clip'
    main(path)



