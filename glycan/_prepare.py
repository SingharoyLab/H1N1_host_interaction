import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

def normalize_subArr(numberedExcel):
    minFluor = np.min(numberedExcel['MVF'])
    temp = numberedExcel['MVF'] - minFluor
    maxFluor = np.max(temp)
    numberedExcel['MVF_norm'] = temp/maxFluor
    return numberedExcel

def normalize(numberedExcel):
    normalized = pd.DataFrame()
    listOfSubArr = np.unique(numberedExcel.SubArr)
    for subArr in listOfSubArr:
        subArrData = numberedExcel[numberedExcel.SubArr == subArr]
        subArrData_normed = normalize_subArr(subArrData)
        normalized = normalized.append(subArrData_normed)
    return normalized

def convertGlyc(numberedExcel):
    temp = numberedExcel.copy()
    temp = temp[temp['GlycType'] != 'Lac']
    twoThree = np.zeros(temp.shape[0])
    twoSix = np.zeros(temp.shape[0])
    #Lac = np.zeros(temp.shape[0])
    twoThree[temp.GlycType == '2-3 SiaLac'] = 1
    twoSix[temp.GlycType == '2-6 SiaLac'] = 1
    
    SVMdata = temp.drop(['GlycType'], axis=1)        
    SVMdata['2-3 SiaLac'] = twoThree
    SVMdata['2-6 SiaLac'] = twoSix
    #SVMdata['Lac'] = Lac
    #SVMdata = SVMdata.drop('Lac', axis=1)
    return SVMdata

def getBind(SVMdata, cutoff):
    binding = np.zeros(SVMdata.shape[0])
    binding[(SVMdata['MVF_norm'] > cutoff)] = 1
    SVMdata["Binding"] = binding
    return SVMdata

def scale_features_col(SVMdata, col):
    arr = SVMdata[col]
    if np.min(arr) == np.max(arr):
        arrMin = np.min(arr)
        arrMax = np.max(arr)
    else:
        arrMin = np.min(arr)
        arr2 = arr - arrMin
        arrMax = np.max(arr2)
        arr3 = arr2 * 1.0/arrMax
        SVMdata[col] = arr3
    return arrMin, arrMax


def scale_features(SVMdata):
    colList = []
    minList = []
    maxList = []
    cList = SVMdata.columns.values

    for column in cList:
        if column != 'Binding' and column != 'ExpNum' and column!= 'FileName':
            arrMin, arrMax = scale_features_col(SVMdata, column)
            colList.append(column)
            minList.append(arrMin)
            maxList.append(arrMax)
    minMaxList = pd.DataFrame()
    minMaxList["Feature"] = colList
    minMaxList["Min"] = minList
    minMaxList["Max"] = maxList
    return minMaxList

def getTrainTestExp(SVMdata, expnum, dropDP=False, test_size=0.33):
    experiment = SVMdata[SVMdata.ExpNum == expnum]
    X = experiment[['PrintPol', 'DP', '2-3 SiaLac', '2-6 SiaLac', 'Valency', 'GlycSpace', 'GlycDen', 'ExpNum']]
    if dropDP:
        X = experiment[['PrintPol', '2-3 SiaLac', '2-6 SiaLac', 'Valency', 'GlycSpace', 'GlycDen', 'ExpNum']]
    else:
        pass
    Y = experiment['Binding']
         
    X2 = X.drop(['ExpNum'], axis=1)
    if test_size == 0.0:
        return X2, Y
    else:
        X_train, X_test, Y_train, Y_test = train_test_split(X2, Y, test_size=test_size, random_state=42)
        return X_train, X_test, Y_train, Y_test

def getTrainTest(self, numberedExcel, cutoff=0.2, dropDP=False, test_size=0.33):
    normalized = normalize(numberedExcel)
    SVMdata = convertGlyc(normalized)
    bindData = getBind(SVMdata, cutoff=cutoff)
    mmList = scale_features(bindData)
    mmList.index = mmList.Feature
    minMaxList = mmList.drop(['Feature'], axis=1)
    if test_size == 0.0:
        XX, YY = getTrainTestExp(bindData, 1, dropDP=dropDP, test_size=test_size)
    else:
        X_train, X_test, Y_train, Y_test = getTrainTestExp(bindData, 1, dropDP=dropDP, test_size=test_size)

    for expnum in pd.unique(bindData.ExpNum)[1:]:
        if test_size == 0.0:
            a, b = getTrainTestExp(bindData, expnum, dropDP=dropDP, test_size=test_size)
            XX = XX.append(a)
            YY = YY.append(b)
        else:
            a, b, c, d = getTrainTestExp(bindData, expnum, dropDP=dropDP, test_size=test_size)
            X_train = X_train.append(a)
            X_test = X_test.append(b)
            Y_train = Y_train.append(c)
            Y_test = Y_test.append(d)
    if test_size == 0.0:
        return XX, YY, bindData
    else:
        return X_train, Y_train, X_test, Y_test, bindData 
