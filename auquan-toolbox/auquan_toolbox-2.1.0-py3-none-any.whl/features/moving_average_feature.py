from backtester.features.feature import Feature

# Average of feature name over some number of previous data points including current.
# number of data points specified by user


class MovingAverageFeature(Feature):

    @classmethod
    def computeForInstrument(cls, updateNum, time, featureParams, featureKey, instrumentManager):
        instrumentLookbackData = instrumentManager.getLookbackInstrumentFeatures()
        data = instrumentLookbackData.getFeatureDf(featureParams['featureName'])
        avg = data[-featureParams['period']:].mean()
        return avg

    @classmethod
    def computeForMarket(cls, updateNum, time, featureParams, featureKey, currentMarketFeatures, instrumentManager):
        lookbackDataDf = instrumentManager.getDataDf()
        data = lookbackDataDf[featureParams['featureName']]
        avg = data[-featureParams['period']:].mean()
        if len(data) < 1:
            return 0
        return avg
