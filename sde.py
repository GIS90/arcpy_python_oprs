# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe: all operating method of the sde database,
contains feature, table, dataset all feature class.
SDEOpr needs sourec sde file and target sde file to operation.

use:
target_sdename = "target"
target_db_type = DBType.SQL_SERVER
target_server = "localhost"
target_db_name = "ccsde"
target_db_user = "sa"
target_db_pwd = "123456"

source_sdename = "source"
source_db_type = DBType.SQL_SERVER
source_server = "localhost"
source_db_name = "sde"
source_db_user = "sa"
source_db_pwd = "123456"

sde = SDEOpr()
source_sde = sde.create_sde_conndb(source_sdename, source_db_type, source_server, source_db_user, source_db_pwd, source_db_name)
target_sde = sde.create_sde_conndb(target_sdename, target_db_type, target_server, target_db_user, target_db_pwd, target_db_name)

# test sdefeature_copy_sdefeature
try:
    suclist, failist = sde.sdefeature_copy_sdefeature(source_sde, target_sde)
except Exception as e:
    print e.message
else:
    print suclist
    print failist
------------------------------------------------
"""
import inspect
import os
import sys
from log import *

try:
    import arcpy
except ImportError as e:
    emsg = "arcpy module import error: %s" % e.message
    raise Exception(emsg)

try:
    from dbhandler import *
except ImportError as e:
    msg = "arcpy module import error: %s" % e.message
    raise Exception(msg)

__version__ = "v.10"
__author__ = "PyGo"
__time__ = "2016/11/29"

__SDEOpr_method__ = ["create", "copy_feature", "copy_table", "copy_dataset",
                     "copy_one_feature", "copy_one_table", "copy_one_dataset"]


def get_cur_folder():
    if getattr(sys, "forzen", "not find"):
        return os.path.dirname(os.path.abspath(__file__))
    else:
        cur_folder = os.path.dirname(inspect.getfile(inspect.currentframe()))
        return os.path.abspath(cur_folder)


_CURRENT_FOLDER = get_cur_folder()
_SDE_FOLDER = os.path.abspath(os.path.join(_CURRENT_FOLDER, "../config"))
_SDE_VERSION = "SDE.DEFAULT"
_SDE_AUTH_DEFAULT = "DATABASE_AUTH"
_SDE_SERVICE = "5151"

_RECONN_MAX = 5


# spatial sde database type
class DBType(object):
    SQL_SERVER = 1
    ORACLE = 2
    POSTGRESQL = 3
    OTHER = 4


# the element of spatial sde database
class GEOMETRY_ELEMENT(object):
    ShapeFile = 1
    FeatureClass = 2
    FeatureDataset = 3
    RasterDataset = 4
    RasterCatalog = 5
    MosaicDataset = 6
    RelationshipClass = 7
    Table = 8
    Workspace = 9


# sde database operation
class SDEOpr(object):
    def __init__(self):
        pass

    def __del__(self):
        pass

    def __cmp__(self, other):
        pass

    def is_invaild(self):
        pass

    def compare_feature(self):

        pass

    def compare_table(self):
        pass

    def is_dbconn(self, db_type, server, db_port, db_user, db_pwd, db_name):
        """
        try to connect database
        :param db_type: database type
        :param server: database server
        :param db_port: database port
        :param db_user: database user
        :param db_pwd: database password
        :param db_name: database name
        :return: True or False
        """
        try:
            assert isinstance(db_port, int)
        except AssertionError as e:
            emsg = "SDEOpr connect database parameter type assert is error: %s" % e.message
            raise Exception(emsg)
        except Exception as e:
            emsg = "SDEOpr connect database parameter is error: %s" % e.message
            raise Exception(emsg)

        try:
            dbhandle = DBHandler(db_type, server, db_port, db_user, db_pwd, db_name)
            dbhandle.open()
            if not dbhandle.conn:
                for i in range(_RECONN_MAX):
                    dbhandle.open()
                    if dbhandle.conn:
                        dbhandle.close()
                        return True
                return False
        except Exception as e:
            emsg = "SDEOpr is_dbconn is failure: %s" % e.message
            raise Exception(emsg)
        else:
            dbhandle.close()
            return True


    def create_sde_conndb(self, sdename, db_type, server, db_user, db_pwd, db_name, save_user_pass=True):
        """
        get sde file of database connection
        :param sdename: the sde file name
        :param db_type: the database connection of database type
        :param server: the database connection of database server
        :param db_user: the database connection of database user
        :param db_pwd: the database connection of database password
        :param db_name: the database connection of database name
        :param save_user_pass: is or not save user and password
        :return: the object of sde file
        sush as :
            sdename = "target"
            db_type = DBType.SQL_SERVER
            server = "localhost"
            db_name = "ccsde"
            db_user = "sa"
            db_pwd = "123456"
        """
        try:
            assert isinstance(sdename, basestring)
            assert isinstance(server, basestring)
            assert isinstance(db_user, basestring)
            assert isinstance(db_pwd, basestring)
            assert isinstance(db_name, basestring)
            assert isinstance(save_user_pass, bool)
            assert db_type in range(DBType.SQL_SERVER, DBType.OTHER)
        except AssertionError as e:
            emsg = "SDEOpr create_sde_conndb parameter type assert is error: %s" % e.message
            raise Exception(emsg)
        except Exception as e:
            emsg = "SDEOpr create_sde_conndb parameter is error: %s" % e.message
            raise Exception(emsg)

        if db_type == 1:
            db_platform = "SQL_SERVER"
            db_port = 1433
        elif db_type == 2:
            db_platform = "ORACLE"
            db_port = 1521
        elif db_type == 3:
            db_platform = "POSTGRESQL"
            db_port = 5432
        else:
            msg = "SDEOpr create_sde_conndb please input available database type"
            raise Exception(msg)
        try:
            is_valid_conn = self.is_dbconn(db_platform, server, db_port, db_user, db_pwd, db_name)
            if not is_valid_conn:
                return False
        except Exception as e:
            emsg = "SDEOpr create_sde_conndb connect db is error: %s" % e.message
            raise Exception(emsg)

        sdename = db_platform + "_" + server + "_" + db_name + "_" + sdename + ".sde"
        sde = os.path.abspath(os.path.join(_SDE_FOLDER, sdename))
        if os.path.exists(sde):
            os.unlink(sde)
        try:
            arcpy.CreateDatabaseConnection_management(out_folder_path=_SDE_FOLDER,
                                                      out_name=sdename,
                                                      database_platform=db_platform,
                                                      instance=server,
                                                      account_authentication=_SDE_AUTH_DEFAULT,
                                                      username=db_user,
                                                      password=db_pwd,
                                                      save_user_pass=save_user_pass,
                                                      database=db_name,
                                                      version=_SDE_VERSION)
        except Exception as e:
            msg = "SDEOpr create_sde_conndb sde file is failure: %s" % e.message
            raise Exception(msg)
        else:
            return sde

    def get_sde_describe(self, sdefile):
        """
        get the sde describe reference informations
        :param sdefile: the sde file
        :return: sde file map, contains:sde server, sde instance, sde database,
                    sde user, sde version
        sush as :
            sde = "D:\config\SQL_SERVER_localhost_sde_source.sde"
        It is usually sde file root in SDEOpr create_conndb returevalue
        """
        self.isexist_sde(sdefile)
        try:
            sdeinfos = []
            if getattr(arcpy, "Describe", "not find Describe"):
                sdedesc = arcpy.Describe(sdefile)
                sdecp = sdedesc.connectionProperties
                sdeinfos = {"server": sdecp.server,
                            "instance": sdecp.instance,
                            "database": sdecp.database,
                            "dbuser": sdecp.user,
                            "sdeversion": sdecp.version}
        except Exception as e:
            emsg = "SDEOpr sde_describe is get failure: %s" % e.message
            raise Exception(msg)
        else:
            return sdeinfos

    def isexist_sde(self, sdefile):
        """
        judge sde file is or not exist
        :param sdefile: sde file
        :return: None
        sush as :
            sde = "D:\config\SQL_SERVER_localhost_sde_source.sde"
        It is usually sde file root in SDEOpr create_conndb returevalue
        """
        if not os.path.exists(sdefile):
            emsg = "SDEOpr sde file is not exist."
            raise Exception(emsg)
        else:
            return True

    def set_workspace(self, ws):
        """
        set arcpy current work space
        :param ws: work space
        :return: True of False
        sush as :
            ws = "D:\config\SQL_SERVER_localhost_sde_source.sde"
            or
            ws = "D:\config"
        It is usually sde file root in SDEOpr create_conndb returevalue
        ws is the folder of contain shapefile
        """
        try:
            arcpy.env.workspace(ws)
        except:
            return False
        else:
            return True

    def get_workspace(self):
        """
        get arcpy current work space
        :return: work space
        """
        pass

    def get_element_type(self, element):
        """
        get a geometry element type
        :param element: a sde database element
        :return: geometry type
        such as :
            element = "D:\config\SQL_SERVER_localhost_ccsde_target.sde\ccsde.DBO.region"
        elemect root in the sde database element
        """
        try:
            desc = arcpy.Describe(element)
            if hasattr(desc, "dataType"):
                return desc.dataType
        except Exception as e:
            emsg = "SDEOpr get_element_type is error: %s" % e.message
            raise Exception(emsg)
        else:
            return None

    def del_element(self, element):
        """
        delete a geometry element
        :param element: geometry elemect
        :return: True or False
        such as :
            element = "D:\config\SQL_SERVER_localhost_ccsde_target.sde\ccsde.DBO.region"
        elemect root in the sde database element
        """
        try:
            element_type = self.get_element_type(element)
            arcpy.Delete_management(in_data=element,
                                    data_type=element_type)
            return True
        except Exception as e:
            return False

    def sdefeature_copy_sdefeature(self, src_sde, tar_sde, over_write_feature=False):
        """
        the feature class if coneained source sde file copy to the target sde file
        :param src_sde: the source sde file
        :param tar_sde: the target sde file
        :param over_write_feature: over write copy feature
        :return: suclist is success copy feature class
                 failist is failure copy feature class
        if over_write_feature is True , feature class is delete and go on copy
        such as:
            src_sde = "D:\config\SQL_SERVER_localhost_sde_source.sde"
            tar_sde = "D:\config\SQL_SERVER_localhost_sde_source.sde"
            over_write_feature = False
        """
        try:
            assert isinstance(over_write_feature, bool)
        except Exception as e:
            emsg = "SDEOpr sdefeature_copy_sdefeature parameter type is error: %s" % e.message
            raise Exception(msg)
        if src_sde is tar_sde:
            emsg = "SDEOpr sdefeature_copy_sdefeature source sde and target sde is equal"
            raise Exception(emsg)

        self.isexist_sde(src_sde)
        self.isexist_sde(tar_sde)
        suclist = []
        failist = []
        arcpy.env.workspace = src_sde
        for fc in arcpy.ListFeatureClasses():
            srcfc = os.path.abspath(src_sde + "\\" + fc)
            tarfc = os.path.abspath(tar_sde + "\\" + fc)
            tarfc_name = fc.split(".")[-1]
            fc_desc = arcpy.Describe(srcfc)
            if fc_desc.dataType == "FeatureClass":
                try:
                    print srcfc, tar_sde, tarfc_name
                    arcpy.FeatureClassToFeatureClass_conversion(in_features=srcfc,
                                                                out_path=tar_sde,
                                                                out_name=tarfc_name,
                                                                where_clause=None,
                                                                field_mapping=None,
                                                                config_keyword=Non)
                    suclist.append(tarfc_name)
                except Exception as e:
                    emsg = "SDEOpr sdefeature_copy_sdefeature is error: %s" % e.message
                    log.error(emsg)
                    failist.append(tarfc_name)

        return suclist, failist

    def create_dataset(self, ds_name, ds_sde, ds_sf=""):
        """
        create feature dataset of the sde database
        :param ds_name: feature dataset name
        :param ds_sde: the feature dataset sde file
        :param ds_sf: feature dataset spatial reference
        :return: Ture
        such as:
            ds_name = "test"
            ds_sde = "D:\config\SQL_SERVER_localhost_sde_source.sde"
            ds_sf = "C:\data\studyarea.prj" or ""
        sd_sf is defalut null
        """
        try:
            assert isinstance(ds_name, basestring)
            assert isinstance(ds_sf, basestring)
        except Exception as e:
            emsg = "SDEOpr create_dataset parameter type is error: %s" % e.message
            raise Exception(emsg)

        self.isexist_sde(ds_sde)
        try:
            sf = arcpy.SpatialReference(ds_sf) if os.path.exists(ds_sf) else None
            arcpy.CreateFeatureDataset_management(out_dataset_path=ds_sde,
                                                  out_name=ds_name,
                                                  spatial_reference=sf)
        except Exception as e:
            emsg = "SDEOpr create_dataset is failure: %s" % e.message
            raise Exception(emsg)
        else:
            ds = ds_sde + "\\" + ds_name
            return arcpy.Exists(ds)

    def ftdataset_copy_ftdataset(self, src_sde, src_dataset, tar_sde, tar_dataset, create_database=True):
        """
        the dataset of source sde copy to the dataser of target sde
        if create_database is true, the target sde dataset is created if not exist to the target sde
        :param src_sde: the source sde
        :param src_dataset: the dataset name of source sde
        :param tar_sde: the target file
        :param tar_dataset: the dataset name of target sde
        :param create_database: is or not create database
        :return: suclist is success copy the feature class of source dataset
                 failist is failure copy feature class of target dataset
        such as:
            src_sde = "D:\config\SQL_SERVER_localhost_ccsde_source.sde"
            src_dataset = "sde.DBO.basicdata"
            tar_sde = "D:\config\SQL_SERVER_localhost_ccsde_target.sde"
            tar_dataset = "ccsde.DBO.ds"
            create_database = True
        """
        try:
            assert isinstance(src_dataset, basestring)
            assert isinstance(tar_dataset, basestring)
        except AssertionError as e:
            emsg = "SDEOpr ftdataset_copy_ftdataset parameter type assert is error: %s" % e.message
            raise Exception(emsg)
        except Exception as e:
            emsg = "SDEOpr ftdataset_copy_ftdataset parameter is error: %s" % e.message
            raise Exception(emsg)

        self.isexist_sde(src_sde)
        self.isexist_sde(tar_sde)

        src_ds = os.path.abspath(src_sde + "\\" + src_dataset)
        tar_ds = os.path.abspath(tar_sde + "\\" + tar_dataset)
        if src_ds == tar_ds:
            emsg = "SDEOpr ftdataset_copy_ftdataset source dataset and target dataset is equal"
            raise Exception(emsg)
        src_ds_desc = arcpy.Describe(src_ds)
        if arcpy.Exists(src_ds) and src_ds_desc.dataType == "FeatureDataset":
            arcpy.env.workspace = src_ds
            tar_dsname = tar_dataset.split(".")[-1]
            suclist = []
            failist = []
            if not arcpy.Exists(tar_ds):
                self.create_dataset(tar_dsname, tar_sde)

            for fc in arcpy.ListFeatureClasses():
                srcfc = os.path.abspath(src_ds + "\\" + fc)
                tarfc = os.path.abspath(tar_ds + "\\" + fc)
                tar_fcname = fc.split(".")[-1]
                try:
                    arcpy.FeatureClassToFeatureClass_conversion(in_features=srcfc,
                                                                out_path=tar_ds,
                                                                out_name=tar_fcname,
                                                                where_clause=None,
                                                                field_mapping=None,
                                                                config_keyword=None)
                    suclist.append(fc)
                except Exception as e:
                    emsg = "SDEOpr ftdataset_copy_ftdataset is error: %s" % e.message
                    log.error(emsg)
                    failist.append(fc)
            return suclist, failist
        else:
            emsg = "source dataset is not exist"
            raise Exception(emsg)

    def feature_copy_dataset(self, src_sde, src_fc, tar_sde, tar_ds, create_database=True):
        """
        the feature class of source sde copy to the feature class of target sde
        souece sde and target sde can equal
        if create_database is true, the target sde dataset is created if not exist to the target sde
        :param src_sde: the source sde file
        :param src_fc: the feature of source sde file
        :param tar_sde: the target sde file
        :param tar_ds: the feature of target sde file
        :param create_database: is or not create database
        :return: True
        such as:
            src_sde = "D:\config\SQL_SERVER_localhost_ccsde_source.sde"
            src_fc = "sde.DBO.detail"
            tar_sde = "D:\config\SQL_SERVER_localhost_ccsde_target.sde"
            tar_ds = "testds"
        """
        try:
            assert isinstance(src_fc, basestring)
            assert isinstance(tar_ds, basestring)
            assert isinstance(create_database, bool)
        except AssertionError as e:
            emsg = "SDEOpr feature_copy_dataset parameter type assert is error: %s" % e.message
            raise Exception(emsg)
        except Exception as e:
            emsg = "SDEOpr feature_copy_dataset parameter is error: %s" % e.message
            raise Exception(emsg)

        self.isexist_sde(src_sde)
        self.isexist_sde(tar_sde)

        src_fc = os.path.abspath(src_sde + "\\" + src_fc)
        tar_sde_ds = os.path.abspath(tar_sde + "\\" + tar_ds)
        if create_database is True and not arcpy.Exists(tar_sde_ds):
            self.create_dataset(tar_ds, tar_sde)
        tar_fcname = src_fc.split(".")[-1]
        tar_fc = os.path.abspath(tar_sde + "\\" + tar_ds + "\\" + tar_fcname)
        try:
            arcpy.FeatureClassToFeatureClass_conversion(in_features=src_fc,
                                                        out_path=tar_sde_ds,
                                                        out_name=tar_fcname,
                                                        where_clause=None,
                                                        field_mapping=None,
                                                        config_keyword=None)
        except Exception as e:
            emsg = "SDEOpr feature_copy_dataset is failure: %s" % e.message
            raise Exception(emsg)
        else:
            return True

    def shape_import_sde(self):
        pass

    def sde_export_shape(self):
        pass

    def copy_sde_table(self, src_sde, tar_sde, over_write=False):
        """
        the tables of source sde database copy to the tables of target sde database
        remark: sde database table not exist the dataset of sde database
        if over_write is true, the source sde database table over write the target sde database table
        :param src_sde: the source sde file
        :param tar_sde: the target sde file
        :param over_write: is or not over write copy table
        :return: suclist is success copy table
                 failist is failure copy table
        such as:
            src_sde = "D:\config\SQL_SERVER_localhost_sde_source.sde"
            tar_sde = "D:\config\SQL_SERVER_localhost_sde_source.sde"
            over_write_feature = False
        """
        try:
            assert isinstance(over_write, bool)
        except Exception as e:
            emsg = "SDEOpr copy_table parameter type is error: %s" % e.message
            raise Exception(emsg)
        if src_sde == tar_sde:
            emsg = "SDEOpr copy_table source sde and target sde is equal"
            raise Exception(emsg)
        self.isexist_sde(src_sde)
        self.isexist_sde(tar_sde)

        suclist = []
        failist = []
        arcpy.env.workspace = tar_sde
        tar_tables = list(arcpy.ListTables())
        arcpy.env.workspace = src_sde
        for src_table in arcpy.ListTables():
            src_sde_table = os.path.abspath(src_sde + "\\" + src_table)
            tar_sde_table = os.path.abspath(tar_sde + "\\" + src_table)
            src_table_name = src_table.split(".")[-1]
            for tar_table in tar_tables:
                tar_table_name = tar_table.split(".")[-1]
                if (str(src_table_name) == str(tar_table_name)) and (over_write is True):
                    del_tar_sde_table = os.path.abspath(tar_sde + "\\" + tar_table)
                    self.del_element(del_tar_sde_table)
            try:
                arcpy.Copy_management(in_data=src_sde_table,
                                      out_data=tar_sde_table,
                                      data_type="Table")
                suclist.append(src_table_name)
            except:
                failist.append(src_table_name)
        return suclist, failist

    def copy_table_one(self, src_table, src_table_sde, tar_table, tar_table_sde, over_write=False):
        """
        the one table of source sde database copy to the table of target sde database
        remark: one table copy
        if over_write is true, the source sde database table over write the target sde database table
        :param src_table: the cpoyed source table
        :param src_table_sde: the table of source sde database
        :param tar_table: the target table
        :param tar_table_sde: the table of target sde database
        :param over_write: is or not over write table
        :return: True or False
        such as:
            src_table = "sde.DBO.test"
            src_table_sde = "D:\config\SQL_SERVER_localhost_sde_source.sde"
            tar_table = "ccsde.DBO.test"
            tar_table_sde = "D:\config\SQL_SERVER_localhost_sde_source.sde"
            over_write = True
        """
        try:
            assert isinstance(src_table, basestring)
            assert isinstance(tar_table, basestring)
        except AssertionError as e:
            emsg = "SDEOpr copy_table_one parameter type is error: %s" % e.message
            raise Exception(emsg)
        if src_table_sde == tar_table_sde:  # table only exist database, not exist dataset
            emsg = "SDEOpr copy_table_one source sde and target sde is equal"
            raise Exception(emsg)
        self.isexist_sde(src_table_sde)
        self.isexist_sde(tar_table_sde)

        src_sde_table = os.path.abspath(src_table_sde + "\\" + src_table)
        tar_sde_table = os.path.abspath(tar_table_sde + "\\" + tar_table)
        if over_write is True:
            try:
                self.del_element(tar_sde_table)
            except Exception as e:
                emsg = "SDEOpr copy_table_one del_element is failure: %s" % e.message
        try:
            arcpy.Copy_management(in_data=src_sde_table,
                                  out_data=tar_sde_table,
                                  data_type="Table")
        except Exception as e:
            return False
        else:
            return True

