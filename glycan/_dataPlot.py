import matplotlib.pyplot as plt
import numpy as np
import plotly
import plotly.graph_objects as go
import pandas as pd
from sklearn.metrics import confusion_matrix
import seaborn as sns

def fixAxes(ax, xLabel=None, yLabel=None, xLim=None, yLim=None, fs=24):
    if xLabel == None:
        xLabel = ax.get_xlabel()
    if yLabel == None:
        yLabel = ax.get_ylabel()

    if xLim != None:
        try:
            xMin = xLim[0]
            xMax = xLim[1]
        except:
            print("Ignoring x-limit")
            xMin = None
            xMax = None
    else:
        xMin = None
        xMax = None

    if yLim != None:
        try:
            yMin = yLim[0]
            yMax = yLim[1]
        except:
            print("Ignoring y-limit")
            yMin = None
            yMax = None
    else:
        yMin = None
        yMax = None

    ax.set_ylabel(yLabel, fontsize=fs)
    ax.set_xlabel(xLabel, fontsize=fs)
    ax.xaxis.set_tick_params(labelsize=fs)
    ax.yaxis.set_tick_params(labelsize=fs)
    if (xMin != None) and (xMax != None):
        ax.set_xlim(xMin, xMax)
    if (yMin != None) and (yMax != None):
        ax.set_ylim(yMin, yMax)
        
def plotConfusion(self, cm, classes, ax=None, figName=None):
    if ax == None:
        fig, ax = plt.subplots(1)
        fig.set_figwidth(8)
        fig.set_figheight(6)
    ax.imshow(cm, interpolation='nearest', cmap=plt.cm.autumn_r)
    ax.set(xticks=np.arange(cm.shape[1]), yticks=np.arange(cm.shape[0]), xticklabels=classes, yticklabels=classes)
    fixAxes(ax, 'Predicted label', 'True label', fs=18)
   
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j]), ha="center", va="center", fontsize=16)

def prepareForPlot(X, minMaxList):
    X_copy = X.copy()
    X_copy.insert(0, 'GlycType', '2-3 SiaLac')
    X_copy.loc[X_copy['2-6 SiaLac'] == 1, 'GlycType'] = '2-6 SiaLac'
    X_copy.VALENCY = (X.Valency * minMaxList.loc['Valency'].Max) + minMaxList.loc['Valency'].Min
    X_copy['PolSpace'] = (X['PolSpace'] * minMaxList.loc['PolSpace'].Max) + minMaxList.loc['PolSpace'].Min
    return X_copy

def plotReport(self, t, X, Y, preds, classes, figName=None):
    colors = ['b','r','0.5']

    trueNeg = t.loc[X[(preds == 0) & (Y == 0)].index]
    truePos = t.loc[X[(preds == 1) & (Y == 1)].index]

    fig, ax = plt.subplots(3,2)
    fig.set_figwidth(16)
    fig.set_figheight(18)
    cm = confusion_matrix(Y,preds)

    twoThree = t.GlycType == '2-3 SiaLac'
    twoSix = t.GlycType == '2-6 SiaLac'
    #cm2 = confusion_matrix(Y, X['2-3 SiaLac'])

    #plotConfusion(self, cm2, ['A','B'], ax=ax[0][0])
    plotConfusion(self, cm, classes, ax=ax[0][0])
    ax[0][1].set_visible(False)

    temp = pd.unique(trueNeg.GlycType)
    tempSize = temp.shape[0]
    sns.scatterplot(data=trueNeg, x = "Valency", y = "GlycDen", hue='GlycType', ax=ax[1][0], palette=colors[:tempSize])
    temp = pd.unique(truePos.GlycType)
    tempSize = temp.shape[0]
    sns.scatterplot(data=truePos, x="Valency", y="GlycDen", hue='GlycType', ax=ax[2][0], palette=colors[:tempSize])

    xMin = min(ax[1][0].get_xlim()[0], ax[2][0].get_xlim()[0])
    xMax = max(ax[1][0].get_xlim()[1], ax[2][0].get_xlim()[1])
    fixAxes(ax[1][0], xLim=(xMin,xMax), fs=18)
    fixAxes(ax[2][0], xLim=(xMin,xMax), fs=18)
    ax[1][0].legend('')
    ax[2][0].legend('')
    trueNegPlot = pd.value_counts(trueNeg.GlycType)
    trueNegPlot.name = 'True negative (' + str(cm[0][0]) + ')'
    trueNegPlot.plot.pie(autopct='%1.1f%%', fontsize=18, ax=ax[1][1], startangle=-30, colors=['b','r'])
    fixAxes(ax[1][1], fs=18)
    truePosPlot = pd.value_counts(truePos.GlycType)
    truePosPlot.name = 'True positive (' + str(cm[1][1]) + ')'
    truePosPlot.plot.pie(startangle=-20, autopct='%1.1f%%', fontsize=18, ax=ax[2][1], colors=['r','b'])
    fixAxes(ax[2][1], fs=18)

    if figName != None:
        plt.savefig(figName)

def get3Dplot(fName, figName=""):
    #fName = "TruePositives.csv"
    df = pd.read_csv(fName, sep=' ')
    twoSix = df[df.GlycType == '2-6 SiaLac']
    twoThree = df[df.GlycType == '2-3 SiaLac']
    print(twoSix.shape, twoThree.shape)
    fig = go.Figure()

    fig.add_trace(go.Scatter3d(
        x=twoSix['PolSpace'],
        y=twoSix['Valency'],
        #z=twoSix[' GLYCAN SPACING ON POLYMER'],
        z=twoSix['MVF'],
        name="2-6 SiaLac",
        text=["Text A", "Text B", "Text C"],
        textposition="top center",
        mode="markers",
        marker=dict(
            color=twoSix['MVF'], 
            colorscale='Blues',
            opacity=1.0,
            #showscale=True
        )
    ))

    fig.add_trace(go.Scatter3d(
        x=twoThree['PolSpace'],
        y=twoThree['Valency'],
        #z=twoThree[' GLYCAN SPACING ON POLYMER'],
        z=twoThree['MVF'],
        name="2-3 SiaLac",
        text=["Text A", "Text B", "Text C"],
        textposition="top center",
        mode="markers",
        marker=dict(
            color=twoThree['MVF'], 
            colorscale='Reds',
            opacity=1.0,
            #showscale=True
        )
    ))
    

    xMin = np.min(df['PolSpace'])
    xMax = np.max(df['PolSpace'])
    x = np.linspace(xMin, xMax, 100)

    yMin = np.min(df['Valency'])
    yMax = np.max(df['Valency'])
    y = np.linspace(yMin, yMax, 100)

    xGrid, yGrid = np.meshgrid(y, x)
    z = 0.2 * np.ones(xGrid.shape)
    fig.add_trace(
    go.Surface(x=x, y=y, z=z, colorscale='Greys', showscale=False)
    )

    fig.update_layout(scene = dict(
        xaxis_title='Polymer spacing',
        yaxis_title='Valency',
        zaxis_title='Mean viral fluorescence'),
        width=700,
        margin=dict(r=20, b=10, l=10, t=10))

    if figName == "":
        plotly.offline.plot(fig)
    else:
        plotly.offline.plot(fig, filename=figName)
    #plotly.offline.plot(fig, filename="TruePositives_Quantitative.html")
    #plotly.offline.plot(fig, filename="TruePositives_MVF.html")
    
    fig.show()
