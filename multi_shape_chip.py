# -*- coding: utf-8 -*-

"""
------------------------------------------------
@version: 1.0v
@author: PyGoHU
@contact: gaoming971366@163.com
@software: PyCharm Community Edition
@file: multi_shape_clip_arcpy.py
@time: 2016/8/12 10:23
@describe: deal with many shape layer clip to designated region
@remark: shape is not null interact to chip
------------------------------------------------
"""

# 导入包
import datetime
import os
import shutil
import time

import arcpy

IS_COPY_MXD = True
CLUSTER_TOLERANCE = "0.0000001 DecimalDegrees"


def copy_mxd(input_dir, output_dir):
    """
    copy input dir mxd file to output dir
    :param input_dir: input dir
    :param output_dir: output dir
    :return:
    """
    files = os.listdir(input_dir)
    for f in files:
        if f.endswith(".mxd"):
            mxd_file_sour = os.path.join(input_dir, f)
            mxd_file_target = os.path.join(output_dir, f)
            if os.path.exists(mxd_file_target):
                os.remove(mxd_file_target)
            else:
                shutil.copyfile(mxd_file_sour, mxd_file_target)
                print "%s to %s copy finish" % (mxd_file_sour, mxd_file_target)


def do_clip(input_dir, output_dir, clip_feature, is_copy_mxd):
    """
    deal with shape and working to clip
    :param input_dir: input dir
    :param output_dir: output dir
    :param clip_feature: clip feature(path + name)
    :param is_copy_mxd: is or not copy mxd to output_dir
    :return:clip num and failure clip features name
    """
    assert isinstance(input_dir, basestring)
    assert isinstance(output_dir, basestring)
    assert isinstance(clip_feature, basestring)
    assert isinstance(is_copy_mxd, bool)
    if not os.path.exists(input_dir) or not os.path.exists(clip_feature):
        return 0, []
    input_cur_dir = os.path.basename(input_dir)
    output_dir = os.path.join(output_dir, (input_cur_dir + "_" + os.path.splitext(os.path.split(clip_feature)[1])[0]))
    print output_dir
    if os.path.exists(output_dir):
        print "Output dir is exist, delete."
        shutil.rmtree(output_dir)
        time.sleep(1)
        os.makedirs(output_dir)
    else:
        os.makedirs(output_dir)

    clip_num = 1
    fail_features = []
    # 设置工作空间
    arcpy.env.workspace = input_dir
    for input_feature in arcpy.ListFiles("*.shp"):
        input_feature_name = os.path.splitext(input_feature)[0]
        out_feature = os.path.join(output_dir, input_feature_name)

        print "Execute clip num = %d, chip feature is: %s" % (clip_num, input_feature_name)
        try:
            arcpy.Clip_analysis(input_feature,
                                clip_feature,
                                out_feature)
            print "Finish."
            clip_num += 1
        except Exception as clip_e:
            fail_features.append(input_feature_name)
            print "%s occur exception is : %s" % (input_feature_name, clip_e.message)

    if is_copy_mxd:
        copy_mxd(input_dir, output_dir)

    return clip_num - 1, fail_features


if __name__ == "__main__":

    # 裁剪文件的工作空间
    input_dir = r"E:\__Project\Map2013City"
    # 结果文件的存放目录
    output_dir = r"E:\data\jn"
    # 被裁剪文件的文件夹
    clip_dir = r"E:\data\jn\clip2"
    start_time = datetime.datetime.now()
    arcpy.env.workspace = clip_dir
    for clip_feature in arcpy.ListFiles("*.shp"):
        print "----------Execute %s clip----------" % clip_feature
        clip_feature = os.path.join(clip_dir, clip_feature)
        try:
            clip_num, fail_features = do_clip(input_dir, output_dir, clip_feature, IS_COPY_MXD)
            if clip_num == 0:
                print "Input dir or feature error, please input."
            if fail_features is not None:
                print "Failure feature is %s. " % fail_features
        except Exception as e:
            print "do_clip occur exception: %s, ahead of the end" % e.message
            import sys
            sys.exit(1)
    end_time = datetime.datetime.now()
    exe_time = (end_time - start_time).seconds
    print "All features finish and cost time is : %s s." % exe_time
