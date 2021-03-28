class glycan(object):
    def __init__(self):
        self.subArr = 0

    from ._read import getData
    from ._prepare import getTrainTest
    from ._dataPlot import plotConfusion, plotReport
    from ._write import saveSubsets
