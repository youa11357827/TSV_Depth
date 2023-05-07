import Subroutine as S
import pandas as pd

TSV = 'S15_3_1'
xlsFileName = S.FindFile('Slot','Slot','xls')
OutputFileName = TSV + '_Depth_Correction.xlsx'

df = S.Read_Excel_File(xlsFileName[0])
DepthData = df.values.tolist()

for EveryDieList in DepthData:
    #計算四捨五入的X座標與Y座標
    for i in range(2):
        EveryDieList[i] = round(EveryDieList[i])
    #將不在die上的Depth與SNR變None
    loc = DepthData.index(EveryDieList)
    if loc in S.N_ADieloc:
        for i in range(2,4):
            EveryDieList[i] = None

#計算TSV不含None點的平均SNR
AvgSNR = sum(EveryDieList[3] for EveryDieList in DepthData if EveryDieList[3] is not None) / len([EveryDieList for EveryDieList in DepthData if EveryDieList[3] is not None])


# Find the same file
PairFileNameList = []
for EveryDieList in DepthData:
    X_SPTFileName =  S.FindFile(str(EveryDieList[0]),'spt','spt')
    Y_FFTFileName =  S.FindFile(str(EveryDieList[1]),'FFT','spt')
    Common = S.find_common_element(X_SPTFileName, Y_FFTFileName)   
    PairFileNameList.append(Common)



for EveryDieList in DepthData:
    loc = DepthData.index(EveryDieList)
    # 1. 確認SNR大小是否在平均之上
    if EveryDieList[3] == None:
        pass
    elif EveryDieList[3] > AvgSNR:
        pass
    elif EveryDieList[3] <= AvgSNR:
        EveryDieList[2] = 'unknown'
        EveryDieList[3] = 'unknown'

#Depths = []
#SNRs = []
#for EveryDieList in DepthData:
#    Depths.append(EveryDieList[2])
#    Depths.append(EveryDieList[3])



# 修正Depth數值並標記SNR較低的點
marks = []
for EveryDieList in DepthData:
    if  EveryDieList[3] == 'unknown':

        marks.append(1)

        loc = DepthData.index(EveryDieList)
        Top5_Peak_Depth = S.Find_Top5_Peak_Depth(PairFileNameList[loc][1])

        #找到"前"一個非None的Depth值
        prev_depth_loc = loc - 1
        prev_depth = None
        if prev_depth_loc >= 0:
            while (prev_depth == None) or (prev_depth == 'unknown'):
                prev_depth = DepthData[prev_depth_loc][2]
                prev_depth_loc = prev_depth_loc - 1
                #當往前超出範圍時
                if prev_depth_loc <= 0:
                    break

        #找到"後"一個非None的Depth值
        next_depth_loc = loc + 1
        next_depth = None
        if next_depth_loc <= (S.Die_Num - 1):
            while (next_depth == None) or (next_depth == 'unknown'):
                next_depth = DepthData[next_depth_loc][2]
                next_depth_loc = next_depth_loc + 1
                #當往後超出範圍時
                if next_depth_loc >= (S.Die_Num - 1):
                    break


        if (prev_depth == None) | (prev_depth == 'unknown'):
            pred = next_depth
        elif (next_depth == None) | (next_depth == 'unknown'):
            pred = prev_depth
        else:
            pred = (prev_depth + next_depth)/2
        
        pred = S.linear_closest_search(Top5_Peak_Depth, pred)
        EveryDieList[2] = pred
    else:
        marks.append(0)
    
Depths = []
for EveryDieList in DepthData:
    if EveryDieList[2] == None:
        Depths.append('NA')
    else:
        Depths.append(EveryDieList[2])

# 將list轉換為pandas DataFrame物件
df = pd.DataFrame({'Depth': Depths, 'Mark': marks})

# 將DataFrame存成Excel檔案
df.to_excel(OutputFileName, index=False)