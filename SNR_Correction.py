import Subroutine as S

ExcelKeyWord = ['Slot', 'Slot']

xlsFileName = S.FindFile('Slot','Slot','xls')

df = S.ReadDepthFile(xlsFileName[0])

DepthData = df.values.tolist()
for lst in DepthData:
    for i in range(2):
        lst[i] = round(lst[i])

i = 0 

for lst in DepthData:
    i = i+1
    Y_SPTFileName =  S.FindFile(str(lst[0]),'spt','spt')
    X_FFTFileName =  S.FindFile(str(lst[1]),'FFT','spt')
    Common = S.find_common_element(X_FFTFileName, Y_SPTFileName)   
    print('The '+ str(i) + ' pair :', end='')
    print(Common)
