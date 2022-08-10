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

    def __init__(self, label_file_line, labels_list=[], pcd_ratio=[1,0,0,0]):
        data = label_file_line.split(' ')
        data[1:] = np.array([float(x) for x in data[1:]]) 
        # This is the froat of the labels file
        # x, y, z, l, w, h, rx, ry, rz
        # 1, 2, 3, 4, 5, 6,  7,  8,  9
        # extract label, boudning box, orientation
        self.type = data[0]  # 'door', 'strairs', ...
        self.cls_id = self.cls_type_to_id(self.type, labels_list)
        self.truncation = 0  # truncated pixel ratio [0..1]                                 # Useless in our dataset
        self.occlusion = 0  # 0=visible, 1=partly occluded, 2=fully occluded, 3=unknown     # Useless in our dataset   

        # extract 2d bounding box in 0-based coordinates
        # get all the ratios
        multiplied_ratio, x_off, y_off, z_off = pcd_ratio
        # extract 3d bounding box information
        self.x = data[1] * multiplied_ratio + x_off
        self.y = data[2] * multiplied_ratio + y_off
        self.z = data[3] + z_off

        self.rx = math.radians(data[7] / math.pi)
        self.ry = math.radians(data[8] / math.pi)
        self.rz = data[9] * (math.pi/180)
        self.h = data[6]                     # box height                          
        self.w = data[5] * multiplied_ratio # box width                            
        self.l = data[4] * multiplied_ratio # box length (in meters)               
        self.score = -1.0                                                                   
        self.level_str = 'Easy'                                                             
        self.level =  1                                                                     
        # label list of shape x, y, z, h, w, l, ry
        # create new rz
        self.new_rz =  -self.ry - np.pi / 2
        self.labels_bev = [self.x, self.y, self.z, self.h, self.w, self.l, self.rz]

    def cls_type_to_id(self, cls_type, labels_list):
        # transform class into numbers
        if cls_type not in labels_list:
            return -1
        return labels_list.index(cls_type)
    
def read_label(label_filename, labels_list,pcd_ratio=[1,0,0,0]):
    lines = [line.rstrip() for line in open(label_filename)]
    objects = [Object3d(line, labels_list=labels_list, pcd_ratio=pcd_ratio) for line in lines]
    return objects