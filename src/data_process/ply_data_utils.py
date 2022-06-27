"""
# -*- coding: utf-8 -*-
-----------------------------------------------------------------------------------
MODIFIED CODE FROM  https://github.com/ghimiredhikura/Complex-YOLOv3
-----------------------------------------------------------------------------------
Adapted to work with labelCloud labelling software output

"""

from __future__ import print_function

import numpy as np
import cv2
import math

class Object3d(object):
    ''' 3d object label '''

    def __init__(self, label_file_line, labels_list=[], multiplied_ratio=1):
        data = label_file_line.split(' ')
        data[1:] = np.array([float(x) for x in data[1:]]) 
        # This is the froat of the labels file
        # x, y, z, l, w, h, rx, ry, rz
        # 1, 2, 3, 4, 5, 6,  7,  8,  9
        # extract label, boudning box, orientation
        self.type = data[0]  # 'door', 'strairs', ...
        self.cls_id = self.cls_type_to_id(self.type, labels_list)
        self.truncation = 0  # truncated pixel ratio [0..1]                                 # USeless
        self.occlusion = 0  # 0=visible, 1=partly occluded, 2=fully occluded, 3=unknown     # Useless
        # self.alpha = 0  # object observation angle [-pi..pi]   was data3                    # ??????        

        # extract 2d bounding box in 0-based coordinates
        # self.xmin = data[4]  # left                                                         # ??????
        # self.ymin = data[5]  # top                                                          # ??????
        # self.xmax = data[6]  # right                                                        # ??????
        # self.ymax = data[7]  # bottom                                                       # ??????
        # self.box2d = np.array([self.xmin, self.ymin, self.xmax, self.ymax])                 # Combination of before

        # extract 3d bounding box information
        self.x = data[1] * multiplied_ratio
        self.y = data[2] * multiplied_ratio
        self.z = data[3] * multiplied_ratio
        self.rx = math.radians(data[7] / math.pi)
        self.ry = math.radians(data[8] / math.pi)
        # self.rz = math.radians(data[9] / math.pi)
        self.rz = data[9] * (math.pi/180)
        self.h = data[6] * multiplied_ratio # box height                                                      # OK
        self.w = data[5] * multiplied_ratio # box width                                                       # OK
        self.l = data[4] * multiplied_ratio # box length (in meters)                                          # OK bu not in meters ??
        # self.t = (data[11], data[12], data[13])  # location (x,y,z) in camera coord.        # ??????                                                     
        # self.dis_to_cam = np.linalg.norm(self.t)                                            # Useless -- ????
        # self.ry = data[14]  # yaw angle (around Y-axis in camera coordinates) [-pi..pi]
        self.score = -1.0                                                                   # Useless -- ????
        self.level_str = 'Easy'                                                             # Useless                 OK
        self.level =  1                                                                     # Useless                 OK
        # label list of shape x, y, z, h, w, l, ry
        # create new rz
        self.new_rz =  -self.ry - np.pi / 2
        self.labels_bev = [self.x, self.y, self.z, self.h, self.w, self.l, self.rz]

    def cls_type_to_id(self, cls_type, labels_list):
        # transform class into numbers
        if cls_type not in labels_list:
            return -1
        return labels_list.index(cls_type)
    
def read_label(label_filename, labels_list,multiplied_ratio=1):
    lines = [line.rstrip() for line in open(label_filename)]
    objects = [Object3d(line, labels_list=labels_list,multiplied_ratio=multiplied_ratio) for line in lines]
    return objects
