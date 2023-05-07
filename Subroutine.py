import pandas as pd
import fnmatch
import heapq
import os

Die_Num = 169
N_ADieloc = [   0,   1,   2,  13,  14,  26,  #右上
               10,  11,  12,  24,  25,  38,  #右下
              156, 143, 130, 157, 144, 158,  #左上
              166, 167, 154, 168, 155, 142,  #左下
               19,  79,  89, 149]            #右上下左 None Die


def FindFile(string1, string2, extension):
    Filelist = []
    for root, dirs, files in os.walk('.'):
        for filename in fnmatch.filter(files, '*.' + extension):
            if string1 in filename and string2 in filename:
                Filelist.append(os.path.join(root, filename))
    return Filelist


def Read_Excel_File(FilePath):
    # 使用pandas的read_excel函數讀取Excel檔案
    df = pd.read_excel(FilePath, header=1)

    # 選擇列標題為“X”、“Y”、“Z”的列
    columns = df[['X', 'Y', 'Thickness', 'SNR']]

    return columns


# 找到兩個list中有相同字串的兩個元素
def find_common_element(list1, list2):
    for element1 in list1:
        for element2 in list2:
            if element1.find(element2.split('_')[2]) != -1:
                return [element1, element2]


#讀取FFT Value並返回前三個對應peak的深度
def Read_FFT_File(FilePath):
    Depth = []
    PeakValue = []
    with open(FilePath, "r") as file:
        for i in range(7):
            file.readline()
        for line in file:
            x_val, y_val = line.split(maxsplit=1)
            Depth.append(float(x_val))
            PeakValue.append(float(y_val))
    
    
def Find_Top5_Peak_Depth(FilePath):
    Depth = []
    PeakValue = []
    with open(FilePath, "r") as file:
        for i in range(7):
            file.readline()
        for line in file:
            x_val, y_val = line.split(maxsplit=1)
            Depth.append(float(x_val))
            PeakValue.append(float(y_val))
    file.close()

    while PeakValue and PeakValue[0] == 0:
        PeakValue.pop(0)
        Depth.pop(0)

    while PeakValue and PeakValue[-1] == 0:
        PeakValue.pop(-1)
        Depth.pop(-1)

    Top5_Peak_val = heapq.nlargest(5, PeakValue)
    Top5_Peak_indexes = [i for i in range(len(PeakValue)) if PeakValue[i] in Top5_Peak_val]
    Top5_Peak_Depth = [Depth[i] for i in Top5_Peak_indexes]
    return Top5_Peak_Depth


def linear_closest_search(arr, x):
    closest = arr[0]
    diff = abs(x - closest)
    for i in range(1, len(arr)):
        curr_diff = abs(x - arr[i])
        if curr_diff < diff:
            closest = arr[i]
            diff = curr_diff
    return closest