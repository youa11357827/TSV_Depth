import pandas as pd
import fnmatch
import os

#def FindFile(Filepath, Name, Extension):
    # 獲取當前資料夾路徑
    #dir_path = os.getcwd()
    # 使用os.listdir函數獲取資料夾中的所有檔案

    #files = os.listdir(dir_path + Filepath)

    # 遍歷所有檔案，篩選出.xls檔案
    #for file in files:
    #    if file.endswith(Extension):
    #        # 顯示檔案路徑
    #        return file

def FindFile(string1, string2, extension):
    Filelist = []
    for root, dirs, files in os.walk('.'):
        for filename in fnmatch.filter(files, '*.' + extension):
            if string1 in filename and string2 in filename:
                Filelist.append(os.path.join(root, filename))
    return Filelist

def ReadDepthFile(FilePath):
    # 使用pandas的read_excel函數讀取Excel檔案
    df = pd.read_excel(FilePath, header=1)

    # 選擇列標題為“X”、“Y”、“Z”的列
    columns = df[['X', 'Y', 'Thickness', 'SNR']]

    # 顯示前五個X、Y、Z列的值
    return columns

def find_common_element(list1, list2):
    for element1 in list1:
        for element2 in list2:
            if element1.find(element2.split('_')[2]) != -1:
                return [element1, element2]