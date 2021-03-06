# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 14:15:05 2019

@author: SWannell
"""

from datetime import datetime, timedelta
import pandas as pd
import GAAccess as ga

# =============================================================================
# Define metadata
# =============================================================================
metrics = ["ga:users"]
dimensions = ["ga:experimentCombination", "ga:date"]
ga_cols = ['cell', 'date', 'count']
segment = "gaid::-1"  # All Users
gaid = "ga:149197394"  # Master View
start = "2020-02-04"
end = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

# Input token on run
# Get 60 min token from https://ga-dev-tools.appspot.com/query-explorer/
token = input('GA token from query explorer:')

# test ID
expid = "qLNA6j26TwOom3VTMYmC4Q"
exp_codes = {expid + ':0': 'ctrl',
             expid + ':1': 'test'}
fltr = "ga:experimentId==" + expid

# =============================================================================
# Extract GA user data, format
# =============================================================================

tots = ga.get_data(gaid=gaid, start=start, end=end, metrics=metrics,
                   segment=segment, dims=dimensions, token=token, filters=fltr)
tots = ga.to_df(tots)

# Raw data
time_period = start.replace('-', '') + '-' + end.replace('-', '')
tots.to_csv('RawData\\GADataTotal' + time_period + '.csv')
print(tots.head(1).T)

# Amended data
tots.columns = ga_cols
tots['date'] = pd.to_datetime(tots['date'])
tots['count'] = pd.to_numeric(tots['count'])
tots['cell'] = tots['cell'].replace(exp_codes)
tots.to_csv('AmendedData\\GADataTotal' + time_period + '.csv')

# =============================================================================
# Extract GA conversion data, format
# =============================================================================

conv_filters = fltr + ";\
ga:eventCategory==Page Components;\
ga:eventAction==Email opt-in;\
ga:eventLabel==Click_Donate"

conv_metrics = ["ga:uniqueEvents"]
conv_dimensions = ["ga:experimentCombination", "ga:date"]
conv_ga_cols = ['cell', 'date', 'count']

convs = ga.get_data(gaid=gaid, metrics=conv_metrics, start=start, end=end,
                    dims=conv_dimensions, segment=segment, token=token,
                    filters=conv_filters)
convs = ga.to_df(convs)

# Raw data
convs.to_csv('RawData\\GADataConvs' + time_period + '.csv')
print(convs.head(1).T)

# Amended data
convs.columns = conv_ga_cols
convs['date'] = pd.to_datetime(convs['date'])
convs['count'] = pd.to_numeric(convs['count'])
convs['cell'] = convs['cell'].replace(exp_codes)
convs.to_csv('AmendedData\\GADataConvs' + time_period + '.csv')

# =============================================================================
# For chi2
# =============================================================================

totals = tots.groupby('cell').sum()
totals.columns = ['total']
clickers = convs.groupby('cell').sum()
clickers.columns = ['count']
contingency = totals.join(clickers)
contingency.to_csv('AmendedData\\Contingency' + time_period + '.csv')

cumu_cols = ['n', 'conv', 'ctr', 'var']
cumulative_cols = {'n': tots, 'conv': convs}

res = {'ctrl': "", 'test': ""}
for cell, cumu_dat in res.items():
    cumu_dat = pd.DataFrame(index=pd.date_range(start=start, end=end),
                            columns=cumu_cols)
    for mtrc, df in cumulative_cols.items():
        by_day = df[df['cell'] == cell].set_index('date')['count']
        cumu = []
        for i in cumu_dat.index:
            last_date = i.strftime('%Y-%m-%d')
            cumu.append(by_day.loc[start:last_date].sum())
        cumu_dat[mtrc] = cumu
    cumu_dat.to_pickle('AmendedData\\CumuData' + cell + '.pkl')
    res[cell] = cumu_dat

# =============================================================================
# Extract GA transaction data, format
# =============================================================================

trans_metrics = ["ga:uniquePurchases"]
trans_dimensions = ["ga:experimentCombination", "ga:transactionId"]
trans_ga_cols = ['cell', 'id', 'count']

trans = ga.get_data(gaid=gaid, metrics=trans_metrics, start=start, end=end,
                    dims=trans_dimensions, segment=segment, token=token,
                    filters=fltr)
trans = ga.to_df(trans)

# Raw data
trans.to_csv('RawData\\GADataTrans' + time_period + '.csv')
print(trans.head(1).T)

# Amended data
trans.columns = trans_ga_cols
trans['count'] = pd.to_numeric(trans['count'])
trans['cell'] = trans['cell'].replace(exp_codes)
trans = trans.set_index('id')
trans.to_csv('AmendedData\\GADataTrans' + time_period + '.csv')