import numpy as np
import string
printable = set(string.printable)
import pandas as pd

def processHead(l):
    #print("Slide used :", l[0].split()[-1])
    #print("Polymer length :", float(l[1].split()[3]))
    #print("Labeling efficiency :", float(l[2].split()[-1]))
    print("For now, we are skipping the header")

def getCol(nData, l, col, typeOf='numeric'):
    if typeOf == 'numeric':
        column = np.zeros(nData)
    else:
        column = []
    for i in range(6, len(l)):
        temp2 = l[i].split(',')[col]
        temp2 = list(filter(lambda x: x in printable, temp2))
 
        if temp2 != []:
            temp = ''
            for t in temp2:
                temp = temp + str(t)
            last = temp
        else:
            temp = last

        if typeOf == 'numeric':
            column[i-6] = temp
        else:
            column.append(temp)
    return column

def processRest_old(l, tab=0):
    headers = ['PrintPol', 'GlycType', 'Valency', 'GlycSpace', 'PolSpace', 'GlycDen', 'MVF']
    nData = len(l) - 6

    printPol = getCol(nData, l, 0)
    glycType = getCol(nData, l, 1, typeOf='string')
    
    valency = getCol(nData, l, 2)
    glycanSpacing = getCol(nData, l, 3)

    dat = np.zeros((nData, 3))
    for i in range(6, len(l)):
        try:
            map(float, l[i].split(',')[4 + tab:7 + tab])
            dat[i-6] = np.array(l[i].split(',')[4 + tab:7 + tab])
        except ValueError as e:
            e2 = str(e)
            if "*" in e2:
                dat[i-6] = -9999 * np.ones(3)
            else:
                print("Something wrong (line 56, possibly missing value)")

    df1 = pd.DataFrame({'a': printPol, 'b': glycType, 'c': valency, 'd': glycanSpacing})
    df2 = pd.DataFrame(dat)
    excel = pd.concat([df1, df2], axis=1)
    excel.columns = headers
    excel['DP'] = 190. * np.ones(excel.shape[0])
    return excel


def processRest_new(l, tab=0):
    # tab = 17
    headers = ['PrintPol', 'GlycType', 'DP', 'Valency', 'GlycSpace', 'PolSpace', 'GlycDen', 'MVF']
    nData = len(l) - 6

    printPol = getCol(nData, l, 0 + tab)
    glycType = getCol(nData, l, 1 + tab, typeOf='string')
    dp = getCol(nData, l, 2 + tab)
    valency = getCol(nData, l, 4 + tab)
    glycanSpacing = getCol(nData, l, 5 + tab)


    dat = np.zeros((nData, 3))
    for i in range(6, len(l)):
        try:
            map(float, l[i].split(',')[12 + tab:15 + tab])
            #print(np.array(l[i].split(','))) 
            dat[i-6] = np.array(l[i].split(',')[12 + tab:15 + tab])
        except ValueError as e:
            e2 = str(e)
            if "*" in e2:
                dat[i-6] = -9999 * np.ones(3)
            else:
                print("Something wrong (line 88)")
                #print(i, l[i])
    df1 = pd.DataFrame({'a': printPol, 'b': glycType, 'c': dp, 'd': valency, 'e': glycanSpacing})
    df2 = pd.DataFrame(dat)
    excel = pd.concat([df1, df2], axis=1)
    excel.columns = headers 
    return excel

def readFile(fileName, wh='new', tab=0):
    f = open(fileName)
    l = f.readlines()
    f.close()
    processHead(l)

    if wh == 'new':
        t = processRest_new(l, tab=tab)
    else:
        t = processRest_old(l, tab=tab)
    return t

def number_experiments(excel, startExp=1):
    exp_size = 6
    data_size = excel.shape[0]
    numbers = np.zeros(data_size)
    if data_size % exp_size:
        print("Something wrong (line 122)")
        print(data_size, exp_size)
    else:
        count = 0 
        for i in range(startExp, startExp + int(data_size/exp_size) + 1):
            #print(i)
            numbers[count: count+6] = i
            count += 6
    excel['ExpNum'] = numbers.astype(int)
    excel = excel[~(excel[excel.columns.values[4:9]] == -9999.000).any(axis=1)]
    return excel, i-1     

def getData(self, fileName, wh='new', totalTabs=0, startExp=1):
    if wh == 'new':
        excel1 = readFile(fileName, wh=wh, tab=0)
        excel1['SubArr'] = self.subArr
        self.subArr += 1
        excel = excel1

        tab = 0
        #if totalTabs:
        for thisTab in range(1, totalTabs):
            tab += 17
            #print("For now, assuming 2 tabs for file ", fileName)
            excel2 = readFile(fileName, wh=wh, tab=tab)
            excel2['SubArr'] = self.subArr
            self.subArr += 1
            excel = pd.concat([excel, excel2], axis=0)

    else:
        excel1 = readFile(fileName, wh=wh, tab=0)
        excel1['SubArr'] = self.subArr
        self.subArr += 1
        excel = excel1

        tab = 0
        for thisTab in range(1, totalTabs):
            tab += 3
            excel2 = readFile(fileName, wh=wh, tab=tab)
            excel2['SubArr'] = self.subArr
            self.subArr += 1
            excel = pd.concat([excel, excel2], axis=0)

        #excel3 = readFile(fileName, wh=wh, tab=6)
        #excel3['SubArr'] = self.subArr
        #self.subArr += 1
        #excel = pd.concat([excel1, excel2, excel3], axis=0)
    numberedExcel, b = number_experiments(excel, startExp=startExp)
    #numberedExcel2 = numberedExcel[numberedExcel.MVF > -1000]
    numberedExcel['FileName'] = fileName
    return numberedExcel, b
