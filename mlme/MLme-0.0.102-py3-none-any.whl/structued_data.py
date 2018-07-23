import pandas as pd
import numpy as np


def summarizeColumns(dataframe, filename=None):
	"""
	The function analyzes each column in the DataFrame 'dataframe' for
		(1) data type;
		(2) number of unique values;
		(3) percentage of missing data points.
	The summary of the analysis is saved into a CSV file for a given filename when it is not None.

	INPUTS:
	dataframe -- a pandas' DataFrame data to analyze.
	filename -- (optional) a filename to save the analysis summary

	OUTPUTS: dataframe of the summary
	"""
    cols = dataframe.columns.values
    summary = pd.DataFrame(columns=['dtype', 'unique num', 'null %']
                                      , index=dataframe.columns.values)

    N = dataframe.shape[0]

    for col in cols:
        summary.loc[col, 'dtype'] = dataframe[col].dtype
        summary.loc[col, 'unique num'] = dataframe[col].unique().size
        summary.loc[col,'null %'] = dataframe[col].isnull().sum()/N*100

    if filename not None:
    	summary.to_csv(filename)

    return summary


def getLabelDict(dataframe):
    """
    The function walks through each column of the given dataframe. If the column has dtype as object, it finds unique values and assigns a unique numerica label for it.

    INPUT:
    dataframe -- a pandas' DataFrame data to analyze

    OUTPUTS: a dictionary binding the column name to another dictionary binding unique value to a unique numeric label.
    """

    output = dict()
    obj_cols = dataframe.select_dtypes('object').columns.values # a numpy array
    
    for col in obj_cols:
        
        unique_vals = dataframe[col].unique()
        N = unique_vals.size
        
        label = dict()
        count = 0
        for val in unique_vals:
            label[val] = count
            count += 1
        
        output[col] = label
        
    return output



def convertObjToLabel(df, labelDict, verbose=False):
	"""
    Convert all entries in dataframe's column whose origingal dtype is 'object' to a corresponding unique label according to the given labelDict

    INPUTS:
    df -- a pandas' DataFrame data to analyze
    labelDict -- a value-label dictionary resulted from a function getLabelDict()
    verbose -- (optional) True or False to show the progress of converting to label

    OUTPUTS: a dataframe with all object-type value converted to correct numerical labels
    """
    for col_name, enc_dict in labelDict.items():
        for value, label in enc_dict.items():
            if verbose==True:
                print('In {}, replace {} with {}'.format(col_name, value, label))
            df[col_name].replace(value, label, inplace=True)
    return df



def getOneHotDict(df, labelDict):
    """
    The function returns a dictionary from the column name, listed in labelDict, to an index-matching dataframe whose row is now converted to a onehot representation of the original numerical label.

    INPUTS:
    df -- pandas' DataFrame that has all elements being numeric, i.e. been through convertObjToLabel().
    labelDict -- a value-label dictionary resulted from a function getLabelDict()

    OUTPUT: a dictionary from the column name, listed in labelDict, to an index-matching dataframe whose row is now converted to a onehot representation of the original numerical label.
    """
    onehot = dict()
    for col_name, enc_dict in labelDict.items():
        vals = df[col_name].values
        converted = to_categorical(vals, len(enc_dict))
        converted = pd.DataFrame(converted, index=df.index)
        onehot[col_name] = to_categorical(vals, len(enc_dict))
        onehot[col_name] = converted

    return onehot


def NColumnOnehot(df, ohdict):
	"""
	Calculate the new number of column if the label-encoded dataframe, df, would be turned into a onehot encoding.

	INPUTS:
	df -- pandas' DataFrame that has all elements being numeric, i.e. been through convertObjToLabel().
	ohdict -- a dictionary output from getOneHotDict(...)
	"""
    n_col = df.shape[1]
    n_new_col = 0
    for key, val in ohdict.items():
        n_new_col += val.shape[1]-1

    N = n_col+n_new_col
    return N



def to_categorical(y, num_classes=None):
    """Converts a class vector (integers) to binary class matrix.
    E.g. for use with categorical_crossentropy.
    # Arguments
        y: class vector to be converted into a matrix
            (integers from 0 to num_classes).
        num_classes: total number of classes.
    # Returns
        A binary matrix representation of the input. The classes axis
        is placed last.

    # COPIED FROM https://github.com/keras-team/keras/blob/master/keras/utils/np_utils.py
    """
    y = np.array(y, dtype='int')
    input_shape = y.shape
    if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
        input_shape = tuple(input_shape[:-1])
    y = y.ravel()
    if not num_classes:
        num_classes = np.max(y) + 1
    n = y.shape[0]
    categorical = np.zeros((n, num_classes), dtype=np.float32)
    categorical[np.arange(n), y] = 1
    output_shape = input_shape + (num_classes,)
    categorical = np.reshape(categorical, output_shape)
    return categorical



def getNormFactors(df, cols):
    """
    Return a dictionary with column names as keys and (mean, std) tuple as value.

    INPUTS:
    df -- pandas' DataFrame that has all elements being numeric, i.e. been through convertObjToLabel().
    cols -- a list of column names in df that would be analyzed for mean and std values. If some members of cols are not in df, error will be raised.
    """
    normFactors = dict()
    for col in cols:
        vals = df[col].values
        normFactors[col] = (np.mean(vals), np.std(vals))
    return normFactors



def convertDFtoNP(df, ohdict=None, normdict=None):
	"""
	Return a numpy array of values from the dataframe where the onehot conversion and normalization can be optionally done.
	INPUTS:
	df -- pandas' DataFrame that has all elements being numeric, i.e. been through convertObjToLabel().
	ohdict -- a dictionary output from getOneHotDict(...)
	normdict -- a dictionary output from getNormFactors(...)

	Note that the index of df and those in ohdict must match to avoid wrong conversion.
	"""

	if ohdict is None and normdict is None:
		return df.values

    n_col = df.shape[1]
    n_new_col = 0
    if ohdict not None:
	    for key, val in ohdict.items():
	        n_new_col += val.shape[1]-1

    N = n_col+n_new_col
    Nrow = df.shape[0]
    data = np.zeros((Nrow, N), dtype=np.float)

    cols = df.columns.values
    nextcolid = 0

    idx = df.index

    if idx.size>0:
	    for col in cols:
	        # print('{}, {}'.format(col, nextcolid))
	        if ohdict not None and col in list(ohdict.keys()):
	            size = ohdict[col].shape[1]
	            data[:, nextcolid:nextcolid+size] = ohdict[col].loc[idx,:]
	            nextcolid += size
	            continue
	        if col in list(normdict.keys()):
	            org_val = df[col].values
	            mean, std = normdict[col]
	            data[:, nextcolid] = (org_val-mean)/std
	            nextcolid += 1
	            continue
	        else:
	            org_val = df[col].values
	            data[:, nextcolid] = org_val
	            nextcolid += 1
	            continue
            
    return data