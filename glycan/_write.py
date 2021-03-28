import pandas as pd

def saveSubset(numberedExcel, X_train, Y_train, X_test, Y_test, pred_train, pred_test, val1, val2, fName=None):
    True_train_ind = X_train[(pred_train == val1) & (Y_train == val2)].index
    True_test_ind = X_test[(pred_test == val1) & (Y_test == val2)].index
    p_train = numberedExcel.loc[True_train_ind]
    p_test = numberedExcel.loc[True_test_ind]
    p = pd.concat([p_train, p_test])
    #True_all_ind = True_train_ind.append(True_test_ind)
    #p = self.sortedExcel.loc[True_all_ind]
    #print(p.shape)
    #return p
    if fName != None:
        p.to_csv(fName, sep=' ', index=False)
    else:
        return p

def saveSubsets(self, numberedExcel, X_train, Y_train, X_test, Y_test, pred_train, pred_test):
    saveSubset(numberedExcel, X_train, Y_train, X_test, Y_test, pred_train, pred_test, 0, 0, fName='a.csv')
    saveSubset(numberedExcel, X_train, Y_train, X_test, Y_test, pred_train, pred_test, 0, 1, fName='b.csv')
    saveSubset(numberedExcel, X_train, Y_train, X_test, Y_test, pred_train, pred_test, 1, 0, fName='c.csv')
    saveSubset(numberedExcel, X_train, Y_train, X_test, Y_test, pred_train, pred_test, 1, 1, fName='d.csv')
