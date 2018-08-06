import math
import numpy as np
import pandas as pd
import scipy.stats as st
from pprint import pprint
import statsmodels.api as sm

class classifier:
    def ttype_CriticalValues(self, sample_size, seriesType):
        tStat_frame = pd.DataFrame ([[25, 50, 100, 250, 500, 501], [-2.66, -2.62, -2.60, -2.58, -2.58, -2.58], 
                                     [-1.95, -1.95, -1.95, -1.95, -1.95, -1.95], [-1.60, -1.61, -1.61, -1.62, -1.62, -1.62],
                                     [-3.75, -3.58, -3.51, -3.46, -3.44, -3.43], [-3.00, -2.93, -2.89, -2.88, -2.87, -2.86], 
                                     [-2.63, -2.60, -2.58, -2.57, -2.57, -2.57], [-4.38, -4.15, -4.04, -3.99, -3.98, -3.96],
                                     [-3.60, -3.50, -3.45, -3.43, -3.42, -3.41], [-3.24, -3.18, -3.15, -3.13, -3.13, -3.12]])
        '''
        Notes: 
        df.loc[] is a label-based function(that is used on row labels). It returns the entire row as
        a series. The index of a series are the column names of a dataframe.
        
        df.loc[[]] is a label-based function. It returns a dataframe insteady of a series.
        
        df.loc[row index, column name] returns a single data from the dataframe
        
        np.interp(x, xf, xp) returns the y-value; x = x-coordinate (sample size) corresponding 
        to y-value (critical value); xf = x-coordinates of the data points (these are the 
        sample size placed on the x-axis; xp = y-coordinates of the data points (critical values 
        located on the y-axis).
        
        The first three rows of a tStat_frame dataframe correspond to t-type critical values for
        a pure random walk; rows 4, 5, and 6 correspond to t-type values for a random walk with 
        drift.
        '''
        if seriesType == "pure": #"pure_rw":
            t_crValue = [np.interp((sample_size - 1), tStat_frame.loc[0], tStat_frame.loc[1]),
                         np.interp((sample_size - 1), tStat_frame.loc[0], tStat_frame.loc[2]),
                         np.interp((sample_size - 1), tStat_frame.loc[0], tStat_frame.loc[3])]
                         # sample_size - 1 because index starts from zero
            ttype_CrValues = [float('{:.4f}'.format(t_crValue[0])), float('{:.4f}'.format(t_crValue[1])),
                              float('{:.4f}'.format(t_crValue[2]))]
        elif seriesType == "drifting": #"rw_drift":
            t_crValue = [np.interp((sample_size - 1), tStat_frame.loc[0], tStat_frame.loc[4]),
                         np.interp((sample_size - 1), tStat_frame.loc[0], tStat_frame.loc[5]),
                         np.interp((sample_size - 1), tStat_frame.loc[0], tStat_frame.loc[6])]
            ttype_CrValues = [float('{:.4f}'.format(t_crValue[0])), float('{:.4f}'.format(t_crValue[1])),
                             float('{:.4f}'.format(t_crValue[2]))]
        else:
            t_crValue = [np.interp((sample_size - 1), tStat_frame.loc[0], tStat_frame.loc[7]),
                         np.interp((sample_size - 1), tStat_frame.loc[0], tStat_frame.loc[8]),
                         np.interp((sample_size - 1), tStat_frame.loc[0], tStat_frame.loc[9])]
            ttype_CrValues = [float('{:.4f}'.format(t_crValue[0])), float('{:.4f}'.format(t_crValue[1])),
                              float('{:.4f}'.format(t_crValue[2]))]
        return ttype_CrValues    
            
    def ftype_CriticalValues(self, data_vector, sample_size, _s0_Square, _su_Square, phi_stat):
        phiStat = phi_stat
        
        _dt_frame = pd.DataFrame([[25, 50, 100, 250, 500, 501], [7.88, 7.06, 6.70, 6.52, 6.47, 6.43],
                                  [5.18, 4.86, 4.71, 4.63, 4.61, 4.59], [4.12, 3.94, 3.86, 3.81, 3.79, 3.78],
                                  [8.21, 7.02, 6.50, 6.22, 6.15, 6.09], [5.68, 5.13, 4.88, 4.75, 4.71, 4.68],
                                  [4.67, 4.31, 4.16, 4.07, 4.05, 4.03], [10.65, 9.31, 8.73, 8.43, 8.34, 8.27],
                                  [7.24, 6.73, 6.49, 6.34, 6.30, 6.25], [5.91, 5.61, 5.47, 5.39, 5.36, 5.34]])
        '''
        Notes: _dt_frame dataframe structure is the same as for ttype_CriticalValues( ) function
        '''
        if phiStat == "phi_one":
            _phi1_st = (((sample_size - 1) * (_s0_Square)) - ((sample_size - 3) * _su_Square)) / (2 * _su_Square)
            _phi1_CrValues = [np.interp(sample_size, _dt_frame.loc[0], _dt_frame.loc[1]),
                              np.interp(sample_size, _dt_frame.loc[0], _dt_frame.loc[2]),
                              np.interp(sample_size, _dt_frame.loc[0], _dt_frame.loc[3])]
            ftype_CrValues = [float('{:.4f}'.format(_phi1_st)), float('{:.4f}'.format(_phi1_CrValues[0])),
                              float('{:.4f}'.format(_phi1_CrValues[1])), float('{:.4f}'.format(_phi1_CrValues[2]))]
        elif phiStat == "phi_two":
            _phi2_st = (((sample_size - 1) * (_s0_Square)) - ((sample_size - 4) * _su_Square)) / (3 * _su_Square)
            _phi2_CrValues = [np.interp(sample_size, _dt_frame.loc[0], _dt_frame.loc[4]),
                              np.interp(sample_size, _dt_frame.loc[0], _dt_frame.loc[5]),
                              np.interp(sample_size, _dt_frame.loc[0], _dt_frame.loc[6])]
            ftype_CrValues = [float('{:.4f}'.format(_phi2_st)), float('{:.4f}'.format(_phi2_CrValues[0])),
                              float('{:.4f}'.format(_phi2_CrValues[1])), float('{:.4f}'.format(_phi2_CrValues[2]))]
        else:
            y0_hat = (np.sum(data_vector[1:])) / (sample_size - 1)
            y1_hat = (np.sum(data_vector[:-1])) / (sample_size - 1)
            _phi3_st = ((sample_size - 1) * (_s0_Square - np.square(y0_hat - y1_hat)) - (sample_size - 4) * _su_Square) / (2 * _su_Square)
            _phi3_CrValues = [np.interp(sample_size, _dt_frame.loc[0], _dt_frame.loc[7]),
                              np.interp(sample_size, _dt_frame.loc[0], _dt_frame.loc[8]),
                              np.interp(sample_size, _dt_frame.loc[0], _dt_frame.loc[9])]
            ftype_CrValues = [float('{:.4f}'.format(_phi3_st)), float('{:.4f}'.format(_phi3_CrValues[0])),
                              float('{:.4f}'.format(_phi3_CrValues[1])), float('{:.4f}'.format(_phi3_CrValues[2]))]
        return ftype_CrValues
    
    def PhiStatInputs(self, _dtSeries, _resid):
        pd_Series = _dtSeries
        residuals = _resid
        _phiInputs = []
        _s0_Square = (np.sum(np.square(np.diff(pd_Series)))) / (len(pd_Series) - 1)
        _su_Square = (np.sum(np.square(residuals))) / len(pd_Series)
        _phiInputs = [_s0_Square, _su_Square]
        return _phiInputs #_phiInputs
    
    def pdDataFrame(self, Lag_Length, pd_Series, series_type):
        _lags = []
        _StackVars = []
        _lags_names = []
        Response_Variable = []
        _unitRoot_Variable = []
        _time_trend_variable = []
        pd_DataFrame = pd.DataFrame()
    
        s_type = series_type
        LagLength = Lag_Length
        pdSeries = pd_Series
    
        _lagged_pdSeries = pdSeries[:-1] 
        Differenced_pdSeries = np.diff(pdSeries)
    
        Response_Variable = [Differenced_pdSeries[LagLength:]] 
        _unitRoot_Variable = [_lagged_pdSeries[LagLength:]] 
        _time_trend_variable = [np.array([i for i in range(1, (len(pdSeries) - LagLength))])]
        _init = 1
        for _lag_ in range(1, (LagLength + 1)):
            _left_sliced_Series = Differenced_pdSeries[(LagLength - _lag_):]
            _right_sliced_Series = _left_sliced_Series[:-_lag_]
            _lags.append(_right_sliced_Series)
            _lags_names.append("lag" + str(_init))
            if s_type == "general":
                _StackVars = Response_Variable + _unitRoot_Variable + _time_trend_variable
            elif (s_type == "pure") or (s_type == "drifting"):
                _StackVars = Response_Variable + _unitRoot_Variable
            else: #<== s_type == "trend_stationary":
                _StackVars = Response_Variable + _time_trend_variable
            for _lag in _lags:
                _StackVars.append(_lag)
                pd_DataFrame = pd.DataFrame(np.array(_StackVars)).T
            _init = _init + 1
        if s_type == "general":
            _vars_ = ['res', 'L1', '_trend'] + _lags_names
        elif (s_type == "pure") or (s_type == "drifting"):
            _vars_ = ['res', 'L1'] + _lags_names
        else:
            _vars_ = ['res', '_trend'] + _lags_names 
        pd_DataFrame.columns = _vars_
        return pd_DataFrame
    
    def InformationCriteria(self, lagLength, obs, et_e, _Pars, series_type):  # _signPars ==> significant parameters from the model
        stype = series_type
        _criteria = []
        _kStar = [1, 2, 3]  # 1: pure random walk; 2: random walk with drift; 3: trend stationary (deterministic trend) <== y(t) = y(t-1) + bo + b(t) + u(t)
        _aStar_aic = 2
        if stype == "pure":
            k_star = _kStar[0]
        elif stype == "drifting":
            k_star = _kStar[1]
        else: #<== self.series_type == "trend_stationary"
            k_star = _kStar[2]
        _aStar_bic = math.log1p(obs - lagLength - k_star)
        ICp_bic = math.log(et_e / (obs - lagLength - k_star)) + ((_Pars + k_star) * (_aStar_bic / (obs - lagLength - k_star)))
        ICp_aic = math.log(et_e / (obs - lagLength - k_star)) + ((_Pars + k_star) * (_aStar_aic / (obs - lagLength - k_star)))
        _criteria = [ICp_aic, ICp_bic]
        return _criteria
    
    def ols_calibrate(self, _type, _series): #OLSModel_Calibration():
        _modelIndex = 0
        _aic_ = []
        _bic_ = []
        _model = []
        pValues = []
        _residuals = []
        seriesType = _type #<== series_type = ['general', 'pure', 'drifting', 'trend_stationary']
        _MaxlagLength = int(12 * (len(_series) / 100) ** 0.25)
        if seriesType == "general":
            for _lag_ in range(1, (_MaxlagLength + 1)):
                _dataSet = self.pdDataFrame(_lag_, _series, seriesType) #<== New name: pdDataFrame
                X = _dataSet.loc[:, 'L1'::]  # slice from 1 to the end by a single increment
                _lm = sm.OLS(_dataSet[_dataSet.columns[0]], sm.add_constant(X)).fit()
                _model.append(_lm)
                pValues.append(float('{:.4f}'.format(_lm.pvalues[_lag_ + 2])))
                _residuals.append(_lm)
                for p in range(len(pValues)):
                    if pValues[len(pValues) - (p + 1)] <= 0.05:
                        _modelIndex = pValues.index(pValues[len(pValues) - (p + 1)])
                        break
        elif seriesType == "drifting":
            for _lag_ in range(1, (_MaxlagLength + 1)):
                _dataSet = self.pdDataFrame(_lag_, _series, seriesType) #<== New name: pdDataFrame
                X = _dataSet.loc[:, 'L1'::]  # slice from 1 to the end by a single increment
                _lm = sm.OLS(_dataSet[_dataSet.columns[0]], sm.add_constant(X)).fit()
                _model.append(_lm)
            
                et_e = np.dot(_lm.resid.transpose(), _lm.resid)
                _criteria = self.InformationCriteria(_MaxlagLength, len(_series), et_e, (_lag_ + 1), seriesType)
                _aic_.append(_criteria[0])
                _bic_.append(_criteria[1])
            if _aic_.index(min(_aic_)) < _bic_.index(min(_bic_)):
                _modelIndex = _aic_.index(min(_aic_))
            else:
                _modelIndex = _bic_.index(min(_bic_))
        elif seriesType == "pure":
            for _lag_ in range(1, (_MaxlagLength + 1)):
                _dataSet = self.pdDataFrame(_lag_, _series, seriesType) #<== New name: pdDataFrame
                X = _dataSet.loc[:, 'L1'::]  # slice from 1 to the end by a single increment
                _lm = sm.OLS(_dataSet[_dataSet.columns[0]], sm.add_constant(X)).fit()
                _model.append(_lm)
            
                et_e = np.dot(_lm.resid.transpose(), _lm.resid)
                _criteria = self.InformationCriteria(_MaxlagLength, len(_series), et_e, (_lag_ + 1), seriesType)
                _aic_.append(_criteria[0])
                _bic_.append(_criteria[1])
            if _aic_.index(min(_aic_)) < _bic_.index(min(_bic_)):
                _modelIndex = _aic_.index(min(_aic_))
            else:
                _modelIndex = _bic_.index(min(_bic_))
        else: #<== seriesType == "trend_stationary":
            for _lag_ in range(1, (_MaxlagLength + 1)):
                _dataSet = self.pdDataFrame(_lag_, _series, seriesType) #<== New name: pdDataFrame
                X = _dataSet.loc[:, '_trend'::]  # slice from 1 to the end by a single increment
                _lm = sm.OLS(_dataSet[_dataSet.columns[0]], sm.add_constant(X)).fit()
                _model.append(_lm)
            
                et_e = np.dot(_lm.resid.transpose(), _lm.resid)
                _criteria = self.InformationCriteria(_MaxlagLength, len(_series), et_e, (_lag_ + 1), seriesType)
                _aic_.append(_criteria[0])
                _bic_.append(_criteria[1])
            if _aic_.index(min(_aic_)) < _bic_.index(min(_bic_)):
                _modelIndex = _aic_.index(min(_aic_))
            else:
                _modelIndex = _bic_.index(min(_bic_))
        return _model[_modelIndex]
    
    def classify_series(self, data):
        _dtSet = data
        _col_name = []
        for i in _dtSet: # store symbols
            _col_name.append(i)
        
        _no_trendSet = []
        _dtrendSet = []
        pure_series_Set = []
        generalModel_Set = []
        drifting_series_Set = []
        trend_stationary_Set = []
        _CrVal_lower1 = st.norm.ppf(.995) # p( z <= -2.56 or z >= 2.56) ==> two-sided test for 1% significant level
        _CrVal_lower5 = st.norm.ppf(.975) # p( z <= -1.96 or z >= 1.96) ==> two-sided test for 5% significant level
        _CrVal_lower10 = st.norm.ppf(.95) # p( z <= -1.64 or z >= 1.64) ==> two-sided test for 10% significant level
        i = 0
        for _r in _dtSet.columns:
            _dataSeries = _dtSet.loc[:, _r:_r:].dropna()
            if len(_dataSeries) >= 60:
                if (_dataSeries.isnull().sum())[0] != 0: # <== count the NaN values & check if it is not equal to zero
                    data_series = _dataSeries.dropna() # <== drop rows with NaN
                else:
                    data_series = _dataSeries
                _series = data_series[data_series.columns[0]]
                series_type = ['general', 'pure', 'drifting', 'trend_stationary']
                general_model = self.ols_calibrate(series_type[0], _series)
                _phi_stats = self.PhiStatInputs(_series, general_model.resid)
                Phi3Stat = self.ftype_CriticalValues(_series, len(_series), _phi_stats[0], _phi_stats[1], "phi_three")
                if (Phi3Stat[0] < Phi3Stat[1] or Phi3Stat[0] < Phi3Stat[2] or Phi3Stat[0] < Phi3Stat[3]):  # <== fail to reject H0: (alpha, beta, phi) = (alpha, 0, 0). ==> Test H0: phi = 0
                    _ctStatPhi = self.ttype_CriticalValues(len(_series), "general")
                    _tStat = float('{:.4f}'.format((general_model.params[1] / general_model.bse[1])))
                    if (_tStat > _ctStatPhi[0] or _tStat > _ctStatPhi[1] or _tStat > _ctStatPhi[2]):  # <== fail to reject H0: phi = 0. ==> Unit root exist. ==> test H0: (alpha, beta, phi) = (0,0,1)
                        Phi2Stat = self.ftype_CriticalValues(_series, len(_series), _phi_stats[0], _phi_stats[1], "phi_two")
                        if (Phi2Stat[0] < Phi2Stat[1] or Phi2Stat[0] < Phi2Stat[2] or Phi2Stat[0] < Phi2Stat[3]): # <== fail to reject H0: (alpha, beta, phi) = (0,0,1). ==> test H0: (alpha, phi) = (0,0)
                            #include_trend = "False"
                            drifting_model = self.ols_calibrate(series_type[2], _series) #self._dataVector, self.include_trend)
                            _phi_stats = self.PhiStatInputs(_series, drifting_model.resid)
                            Phi1Stat = self.ftype_CriticalValues(_series, len(_series), _phi_stats[0], _phi_stats[1], "phi_one")
                            if (Phi1Stat[0] < Phi1Stat[2] or Phi1Stat[0] < Phi1Stat[2] or Phi1Stat[0] < Phi1Stat[3]):  # <== fail to reject H0: (alpha, phi) = (0,0)
                                pure_series = _r #{_r} #: {'L1': (float('{:.4f}'.format(self._lm.params[0])) + 1), 'Stat_L1  ': [self._tStat] + self._ctStatPhi, "phi3_" + self._dataVector.columns[0]: self.Phi3Stat, "phi2_" + self._dataVector.columns[0]: self.Phi2Stat, "phi1_" + self._dataVector.columns[0]: self.Phi1Stat}}
                                pure_series_Set.append(pure_series)
                            else: # H0: (alpha, phi) = (0,0) is rejected.
                                drifting_series = _r #self._dataVector.columns[0]: {'Cons': [float('{:.4f}'.format(self._lm.params[0])), float('{:.4f}'.format((self._lm.params[0] / self._lm.bse[0])))], 'L1': (float('{:.4f}'.format(self._lm.params[1])) + 1), 'Stat_L1  ': [self._tStat] + self._ctStatPhi, "phi3_" + self._dataVector.columns[0]: self.Phi3Stat, "phi2_" + self._dataVector.columns[0]: self.Phi2Stat, "phi1_" + self._dataVector.columns[0]: self.Phi1Stat}}
                                #print(drifting_model.summary())
                                drifting_series_Set.append(drifting_series)
                else:  # H0: (alpha, beta, phi) = (alpha, 0, 0) is rejected. ==> STATIONARY SERIES
                    _tStat_phiCoef = float('{:.4f}'.format((general_model.params[1]/general_model.bse[1])))  # <== t_stat for phi var
                    if ((_tStat_phiCoef >= - _CrVal_lower1 or _tStat_phiCoef <= _CrVal_lower1) or (_tStat_phiCoef >= - _CrVal_lower5 or _tStat_phiCoef <= _CrVal_lower5) or (_tStat_phiCoef >= - _CrVal_lower10 or _tStat_phiCoef <= _CrVal_lower10)):
                        # fail to reject H0: phi = 0. ==> beta = 0. test H0: alpha = 0
                        _tStat_alphaCoef = float('{:.4f}'.format((general_model.params[0]/general_model.bse[0])))
                        if ((_tStat_alphaCoef >= - _CrVal_lower1 or _tStat_alphaCoef <= _CrVal_lower1) or (_tStat_alphaCoef >= - _CrVal_lower5 or _tStat_alphaCoef <= _CrVal_lower5) or (_tStat_alphaCoef >= - _CrVal_lower10 or _tStat_alphaCoef <= _CrVal_lower10)):
                            # fail to reject H0: alpha = 0. ==> NON STATIONARY SERIES WITH DETERMINISTIC TREND (trend stationary)
                            trend_stationary_series = _r #{_dataVector.columns[0]: {'Cons': [float('{:.4f}'.format(general_model.params[0])), float('{:.4f}'.format((self._lm.params[0] / self._lm.bse[0])))], 'L1': [float('{:.4f}'.format(self._lm.params[1])), float('{:.4f}'.format((self._lm.params[1] / self._lm.bse[1])))], '_trend': [float('{:.4f}'.format(self._lm.params[2])), float('{:.4f}'.format((self._lm.params[2] / self._lm.bse[2])))]}}
                            trend_stationary_Set.append(trend_stationary_series)
                        else: # reject H0: alpha = 0. ==> NON STATIONARY SERIES WITH LINEAR TREND AND DRIFT (General model)
                            generalModel = _r #_series_with_trend = {_dataVector.columns[0]: {'Cons': [float('{:.4f}'.format(_lm.params[0])), float('{:.4f}'.format((_lm.params[0] / _lm.bse[0])))], 'L1': [float('{:.4f}'.format(_lm.params[1])), float('{:.4f}'.format((_lm.params[1] / _lm.bse[1])))], '_trend': [float('{:.4f}'.format(_lm.params[2])), float('{:.4f}'.format((_lm.params[2] / _lm.bse[2])))]}}
                            generalModel_Set.append(generalModel) #_series_with_trendSet.update(_series_with_trend)
                    else: # reject H0: phi = 0. ==> phi != 0. test H0: beta = 0
                        _tStat_trendCoef = float('{:.4f}'.format((general_model.params[2] / general_model.bse[2])))  # t_stat for trend var
                        if ((_tStat_trendCoef >= - _CrVal_lower1 or _tStat_trendCoef <= _CrVal_lower1) or (_tStat_trendCoef >= - _CrVal_lower5 or _tStat_trendCoef <= _CrVal_lower5) or (_tStat_trendCoef >= - _CrVal_lower10 or _tStat_trendCoef <= _CrVal_lower10)):
                            # fail to reject H0: beta = 0. test H0: alpha(const) = 0
                            _tStat_consCoef = float('{:.4f}'.format((general_model.params[0] / general_model.bse[0])))  # t_stat for const var
                            if ((_tStat_consCoef < - _CrVal_lower1 or _tStat_consCoef > _CrVal_lower1) or (_tStat_consCoef < - _CrVal_lower5 or _tStat_consCoef > _CrVal_lower5) or (_tStat_consCoef < - _CrVal_lower10 or _tStat_consCoef > _CrVal_lower10)):
                                # H0: const = 0 is rejected. ==> STATIONARY SERIES WITH LINEAR TREND
                                _dtSeries = _r #{_dataVector.columns[0]: {'Cons': [float('{:.4f}'.format(general_model.params[0])), float('{:.4f}'.format((general_model.params[0] / general_model.bse[0])))], 'L1': [float('{:.4f}'.format(general_model.params[1])), float('{:.4f}'.format((general_model.params[1] / general_model.bse[1])))], '_trend': [float('{:.4f}'.format(general_model.params[2])), float('{:.4f}'.format((general_model.params[2] / general_model.bse[2])))]}}
                                _dtrendSet.append(_dtSeries) #update(_dtSeries)
                                # _trendSeries.append(_colName)
                            else: # H0: const = 0 is not rejected
                                _no_trendSeries = _r #{_dataVector.columns[0]: {'Cons': [float('{:.4f}'.format(general_model.params[0])), float('{:.4f}'.format((general_model.params[0] / general_model.bse[0])))], 'L1': [float('{:.4f}'.format(general_model.params[1])), float('{:.4f}'.format((general_model.params[1] / general_model.bse[1])))], '_trend': [float('{:.4f}'.format(general_model.params[2])), float('{:.4f}'.format((general_model.params[2] / general_model.bse[2])))]}}
                                _no_trendSet.append(_no_trendSeries) #update(_no_trendSeries)
            i += 1
        _classes = {"pure series       ": pure_series_Set, "drifting series   ": drifting_series_Set, "trending series   ": trend_stationary_Set, "generalized series": generalModel_Set}
        classes = dict( [(k,v) for k,v in _classes.items() if len(v) > 0])
        print(" ")
        print("=================================================")
        print("Total series from loaded data:              |" + str(len(_dtSet.columns)))
        print("--------------------------------------------|----")
        print("Total classified series (age >= 60 months): |" + str(i))
        print("=================================================")
        return classes







