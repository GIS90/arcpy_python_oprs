# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe: arcgis publish map server tool,
it main contain publish_server, make_tiled method to operating XXXX.mxd map
via __create_server_connfile, __create_mapsddraft, __stage_service_server,
__upload_service_definition_server private method together with the map
release process for thorough automation.

use:
    connect_type = GIS_SERVICES_TYPE.administrator
    server_url = "http://192.168.2.163:6080/arcgis/admin"
    server_type = SERVER_TYPR.arcgis
    isuse_stage_folder = True
    user = "siteadmin"
    pwd = "123456"
    issave_user_pwd = True
    mapserver = MapServer(connect_type,
                          server_url,
                          server_type,
                          isuse_stage_folder,
                          user,
                          pwd,
                          issave_user_pwd)

    service_mxd = r"E:\data\ty\Map2013City_clip_sour\ty_region.mxd"
    service_name = "ty_region"
    service_type = SERVER_TYPR.arcgis
    service_folder = "taiyuan"
    iscopy_data_to_server = False
    summary = "tai yuan server test"
    tags = "tai yuan server test"
    service_rlt = mapserver.publish_server(service_name,
                                           service_mxd,
                                           server_type,
                                           iscopy_data_to_server,
                                           service_folder,
                                           summary,
                                           tags)
------------------------------------------------
"""
import arcpy
from arcpy.mapping import *

from log import *

__version__ = "v.10"
__author__ = "PyGo"
__time__ = "2016/12/5"



class GIS_SERVICES_TYPE(object):
    """
    create a connection represents the connection GIS Services type
    use < publish < administer
    * USE_GIS_SERVICES: Use GIS Services.
    * PUBLISH_GIS_SERVICES: Publish GIS Services.
    * ADMINISTER_GIS_SERVICES: Administer GIS Services.
    """
    user = "USE_GIS_SERVICES"
    publish = "PUBLISH_GIS_SERVICES"
    administrator = "ADMINISTER_GIS_SERVICES"


class SERVER_TYPR(object):
    """
    publish server type, default is ARCGIS_SERVER
    ARCGIS_SERVER —ArcGIS for Server server type
    SPATIAL_DATA_SERVER —A Spatial Data Server server type
    FROM_CONNECTION_FILE —Get the server_type as specified in the connection_file_path parameter
    MY_HOSTED_SERVICES —My Hosted Services server type
    """
    arcgis = "ARCGIS_SERVER"
    spatial_data = "SPATIAL_DATA_SERVER"
    connect_file = "FROM_CONNECTION_FILE"
    my_host_service = "MY_HOSTED_SERVICES"


def get_cur_folder():
    if getattr(sys, "forzen", "not find"):
        return os.path.dirname(os.path.abspath(__file__))
    else:
        cur_folder = os.path.dirname(inspect.getfile(inspect.currentframe()))
        return os.path.abspath(cur_folder)


_CURRENT_FOLDER = get_cur_folder()
_STAGE_FOLDER = _AGS_FOLDER = _SERVICE_FOLDER = os.path.abspath(os.path.join(_CURRENT_FOLDER, "../config"))


# publish map service
class MapServer(object):
    __open_def__ = ["publish_server", "make_tile"]
    __private_def__ = ["__create_server_connfile", "__create_mapsddraft", "__stage_service_server",
                       "__upload_service_definition_server"]

    def __init__(self, connect_type, server_url, server_type, isuse_stage_folder, user, password, issave_user_pwd):
        """
        MapServer class initialization
        :param connect_type: GIS services connection type
                             administartor authority is best
        :param server_url: the URL to the server
        :param server_type: the server type
                            default is ARCGIS_SERVER
        :param isuse_stage_folder: is or not usr stage folder
                                   default is True
        :param user: the GIS services user
                    default is siteadmin
                    used if the connection_type is PUBLISH_GIS_SERVICES or ADMINISTER_GIS_SERVICES.
        :param password: the GIS services password
        :param issave_user_pwd: is or not save user and password
        :return: GIS services connection file
        such as:
            connect_type = GIS_SERVICES_TYPE.administrator
            server_url = "http://192.168.2.163:6080/arcgis/admin"
            server_type = SERVER_TYPR.arcgis
            isuse_stage_folder = True
            user = "siteadmin"
            pwd = "123456"
            issave_user_pwd = True
        use:
            mapserver = MapServer(connect_type,
                                  server_url,
                                  server_type,
                                  isuse_stage_folder,
                                  user,
                                  pwd,
                                  issave_user_pwd)
        """
        try:
            assert isinstance(connect_type, basestring)
            assert isinstance(server_url, basestring)
            assert isinstance(server_type, basestring)
            assert isinstance(isuse_stage_folder, bool)
            assert isinstance(user, basestring)
            assert isinstance(password, basestring)
            assert isinstance(issave_user_pwd, bool)
        except AssertionError as e:
            emsg = "MapServer __init__ parameter type is error: %s" % e.message
            raise Exception(emsg)
        except Exception as e:
            emsg = "MapServer __init__ is error: %s" % e.message
            raise Exception(emsg)

        self.__connect_type = connect_type
        # :param ags_name: the folder of GIS services connection.ags file
        self.__ags_folder = _AGS_FOLDER
        # :param ags_name: GIS services connection.ags file name
        self.__ags_name = "GIS_" + self.__connect_type + "_file.ags"
        self.__server_url = server_url
        self.__server_type = server_type
        self.__isuse_stage_folder = isuse_stage_folder
        self.__stage_folder = _STAGE_FOLDER
        # :param stage_folder: . if you will be using this connection to create and save service definitions,
        # you can choose where the service definition files will be staged .
        # connection file default staged in a folder on local machine.
        # If this parameter is set to None, ArcGIS for Desktop's staging folder will be used.
        # This parameter is only used if the connection_type is PUBLISH_GIS_SERVICES or ADMINISTER_GIS_SERVICES.
        self.__user = user
        self.__pwd = password
        self.__issave_user_pwd = issave_user_pwd

    def publish_server(self, service_name, service_mxd, service_type, iscopy_data_to_server, service_folder=None, summary=None, tags=None):
        """
        publish_server is MapServer class main method.
        :param service_name: the service name
        :param service_mxd: the mapdocument object of map mxd file
        :param service_type: the service type, default is ARCGIS_SERVER
            ARCGIS_SERVER —ArcGIS for Server server type
            FROM_CONNECTION_FILE —Get the server_type as specified in the connection_file_path parameter
            SPATIAL_DATA_SERVER —Spatial Data Server server type
            MY_HOSTED_SERVICES —My Hosted Services server type
        :param service_folder: the service stored folder, default is None
        :param iscopy_data_to_server:  is or not the map document will be copied the server
        :param summary: the service description summary
        :param tags: the service description tags
        :return: True
        such as:
            service_name = "ty_region"
            service_mxd = r"E:\data\ty\Map2013City_clip_sour\ty_region.mxd"
            service_type = SERVER_TYPR.arcgis
            service_folder = "taiyuan"
            iscopy_data_to_server = False
            summary = "tai yuan server test"
            tags = "tai yuan server test"
        use:
            map_service_rlt = mapserver.publish_server(service_name,
                                                       service_mxd,
                                                       server_type,
                                                       iscopy_data_to_server,
                                                       service_folder,
                                                       summary,
                                                       tags)
        """
        try:
            assert isinstance(service_name, basestring)
            assert isinstance(service_mxd, basestring)
            assert isinstance(service_type, basestring)
            assert isinstance(iscopy_data_to_server, bool)
            assert isinstance(service_folder, basestring)
            assert isinstance(summary, basestring)
            assert isinstance(tags, basestring)
        except AssertionError as e:
            emsg = "MapServer publish_server parameter type is error: %s" % e.message
            raise Exception(emsg)
        except Exception as e:
            emsg = "MapServer publish_server is error: %s" % e.message
            raise Exception(emsg)

        service_mxd_layers = []
        mapdoc = arcpy.mapping.MapDocument(service_mxd)
        for ly in arcpy.mapping.ListLayers(mapdoc):
            service_mxd_layers.append(ly.name)
        log.info("%s contains layers: %s" % (service_mxd, service_mxd_layers))
        try:
            ags_file = self.__create_server_connfile()
            sddraft_file, analysis = self.__create_map_sddraft(ags_file=ags_file,
                                                               service_name=service_name,
                                                               service_mxd=service_mxd,
                                                               service_type=service_type,
                                                               iscopy_data_to_server=iscopy_data_to_server,
                                                               service_folder=service_folder,
                                                               summary=summary,
                                                               tags=tags)
            if analysis["errors"]:
                emsg = "MapServer publish_server mxd have error: %s" % str(analysis["errors"])
                raise Exception(emsg)
            sd_file = self.__stage_service_server(sddraft_file,
                                                  service_name)
            service_result = self.__upload_service_definition_server(ags_file,
                                                                     sd_file)
            return service_result
        except Exception as e:
            emsg = "MapServer publish_server is error: %s" % e.message
            raise Exception(emsg)

    def make_tile(self):
        pass

    def close(self):
        pass

    def __create_server_connfile(self):
        """
        create a server connection file of to connect ArcGIS for Server or Spatial Data Server,
        thie file use to release the map services and manager released map servies
        :return: the server connection .ags file
        such as:
            create_server_connfile parameter root in MapServer class initialation
        """
        ags_file = os.path.abspath(os.path.join(_AGS_FOLDER, self.__ags_name))
        if os.path.exists(ags_file):
            os.unlink(ags_file)

        try:
            CreateGISServerConnectionFile(connection_type=self.__connect_type,
                                          out_folder_path=self.__ags_folder,
                                          out_name=self.__ags_name,
                                          server_url=self.__server_url,
                                          server_type=self.__server_type,
                                          use_arcgis_desktop_staging_folder=self.__isuse_stage_folder,
                                          staging_folder_path=self.__stage_folder,
                                          username=self.__user,
                                          password=self.__pwd,
                                          save_username_password=self.__issave_user_pwd)
        except Exception as e:
            emsg = "__create_server_connfile is error: %s" % e.message
            raise Exception(emsg)
        else:
            return ags_file

    def __create_map_sddraft(self, ags_file, service_name, service_mxd, service_type, iscopy_data_to_server, service_folder=None, summary=None, tags=None):
        """
        create_map_sddraft is one step of releasing map services, it create the .sddraft file of service defination draft
        service defination consist of the map document, server informations and service attributes
        :param ags_file: the GIS server connection .ags file
            origin private create_server_connfile method
        :param service_name: the service name
        :param service_mxd: the mapdocument object of map mxd file
        :param service_type: the service type, default is ARCGIS_SERVER
            ARCGIS_SERVER —ArcGIS for Server server type
            FROM_CONNECTION_FILE —Get the server_type as specified in the connection_file_path parameter
            SPATIAL_DATA_SERVER —Spatial Data Server server type
            MY_HOSTED_SERVICES —My Hosted Services server type
        :param service_folder: the service stored folder, default is None
        :param iscopy_data_to_server:  is or not the map document will be copied the server
        :param summary: the service description summary
        :param tags: the service description tags
        :return: the map mxd file sddraft and analysis
            sddraft is the .sddraft file of ervice defination draft
            analysis is a information dict of messages, warnings, errors, help dissolve the map mxd errors
        such as :
            ags_file = "E:\connectToSDE\conFile.ags"
            service_name = "ty_region"
            service_mxd = r"E:\data\ty\ty_region.mxd"
            service_type = SERVER_TYPR.arcgis
            service_folder = "taiyuan"
            iscopy_data_to_server = False
            summary = "tai yuan server test"
            tags = "tai yuan server test"
        """
        if not os.path.exists(ags_file):
            emsg = "__create_map_sddraft ags_file is not exist"
            raise Exception(emsg)
        if not os.path.exists(service_mxd):
            emsg = "__create_map_sddraft service_mxd is not exist"
            raise Exception(emsg)
        sddraft = os.path.abspath(os.path.join(_SERVICE_FOLDER, service_name + ".sddraft"))
        if os.path.exists(sddraft):
            try:
                os.unlink(sddraft)
            except Exception as e:
                emsg = "__create_map_sddraft sddraft is exist and delete error"
                raise Exception(emsg)

        map_doc = MapDocument(service_mxd)
        try:
            analysis = CreateMapSDDraft(map_document=map_doc,
                                        out_sddraft=sddraft,
                                        service_name=service_name,
                                        server_type=service_type,
                                        connection_file_path=ags_file,
                                        copy_data_to_server=iscopy_data_to_server,
                                        folder_name=service_folder,
                                        summary=summary,
                                        tags=tags)
        except Exception as e:
            emsg = " __create_map_sddraft is error: %s" % e.message
            raise Exception(emsg)
        return sddraft, analysis

    def __stage_service_server(self, sddraft, service_name):
        """
        the staging .sd file of service defination contains the all informations of GIS services
        this tool is the .sddraft file transfer to the .sd file
        :param sddraft: the .sddraft file of map services
            origin private create_map_sddraft method
        :param service_name: the service name
        :return: the .sd file of service
        such as:
            sddraft = "D:\Py_file\config\ty_region.sd"
            service_name = "ty_region"
        """
        sd_file = os.path.abspath(os.path.join(_SERVICE_FOLDER, service_name + ".sd"))
        if os.path.exists(sd_file):
            try:
                os.unlink(sd_file)
            except Exception as e:
                emsg = "__stage_service_server sd file is exist and delete error"
                raise Exception(emsg)
        if not os.path.exists(sddraft):
            emsg = "__stage_service_server sddraft is exist"
            raise Exception(emsg)

        try:
            arcpy.StageService_server(sddraft, sd_file)
        except Exception as e:
            emsg = "__stage_service_server is error: %s" % e.message
            raise Exception(emsg)
        else:
            return sd_file

    def __upload_service_definition_server(self, ags_file, sd_file):
        """
        upload and publish GIS services to a specific GIS server
        according to the transition service definition .sd file.
        :param ags_file: the .ags.file
            origin private create_server_connfile method
        :param sd_file: the .sd file
            origin private stage_service_server method
        :return: True
        such as:
            ags_file = "E:\connectToSDE\conFile.ags"
            sd_file = "E:\connectToSDE\ty_region.sd"
        """
        if not os.path.exists(ags_file):
            emsg = "__upload_service_definition_server ags_file is not exist"
            raise Exception(emsg)
        if not os.path.exists(sd_file):
            emsg = "__upload_service_definition_server sd_file is not exist"
            raise Exception(emsg)

        try:
            arcpy.UploadServiceDefinition_server(sd_file, ags_file)
        except Exception as e:
            emsg = "__upload_service_definition_server is error: %s" % e.message
            raise Exception(emsg)
        else:
            return True
