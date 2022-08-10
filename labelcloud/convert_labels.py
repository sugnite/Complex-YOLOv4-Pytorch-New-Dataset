import json
import os
import numpy as np


def importJson(filename,filepath=''):
    # add / to the path
    if filepath != '':
        filename = os.path.join(filepath,filename)
    else:
        os.path.dirname(os.path.realpath(__file__))
    # 
    filename = "{}".format(filename)
    # import the json data categories
    with open(filename, 'r+') as f:
        data = json.load(f)
    return data

def create_str(jsonFile):
    #  
    filename = jsonFile['filename'].replace('.ply','')
    #
    strAllObjs, objClass_list = '', []
    # loop throught objects
    for objs in jsonFile['objects']:
        # get the function ouput
        objToAdd, objClass = objectToStr(objs)
        # add to str
        strAllObjs += objToAdd
        # add the class to the list
        objClass_list.append(objClass)
    # ad t the file
    to_txt(filename, strAllObjs)
    # return obj class
    return objClass_list

def objectToStr(objSon):
    # get the data from the object
    x, y, z = objSon['centroid']['x'], objSon['centroid']['y'], objSon['centroid']['z']
    l, w, h = objSon['dimensions']['length'], objSon['dimensions']['width'], objSon['dimensions']['height']
    rx, ry, rz = objSon['rotations']['x'], objSon['rotations']['y'], objSon['rotations']['z']
    # create an obj list
    objList = [x, y, z, l, w, h, rx, ry, rz]
    # create str obj
    objStr = objSon['name']
    # add to the str
    for elements in objList:
        objStr += ' ' + str(elements)
    # add return 
    objStr+='\n'
    # return the str
    return objStr, objSon['name']

def to_txt(filename, objectStr,filepath='labels_converted/'):
    # svae the ew labels to txt file
    act_path = os.path.dirname(os.path.realpath(__file__))
    newPath = os.path.join(act_path,filepath)
    with open('{}{}.txt'.format(newPath,filename), 'w') as f:
        f.write(objectStr)

def add_labels(objLabels, labelList):
    #   
    [labelList.append(objClass) for objClass in objLabels if objClass not in labelList]
    #
    return labelList

def convertList(LabelList):
    # replace str
    labelSTR = str(LabelList)
    labelSTR = labelSTR.replace('[','')
    labelSTR = labelSTR.replace(']','')
    labelSTR = labelSTR.replace(',','\n')
    labelSTR = labelSTR.replace('\'','')
    labelSTR = labelSTR.replace(' ','')
    return labelSTR

def convertFiles():
    # loop througt files
    print('Start converting')
    path_json = os.path.join(os.path.dirname(os.path.realpath(__file__)),'labels')
    # creta e a counter for the feedback
    count_files = 0
    # create a label list
    label_list = []
    # loop throught files
    for root, dirs, files in os.walk(path_json):
        for file in files:
            if file.endswith(".json"):
                jsonbject = importJson(file, filepath=path_json)
                label_list = add_labels(create_str(jsonbject), label_list)
                count_files += 1
    # save labels
    to_txt('classes_names', convertList(label_list))
    # Print the final state
    print('Sucessfully converted {} file(s)'.format(count_files))
    
  
convertFiles()
