# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 16:05:15 2020

@author: SWannell
"""

from scipy.stats import ttest_ind, chi2_contingency
import pandas as pd

cont = pd.read_csv('AmendedData\\LBLcontingency.csv', index_col='cell')
total = sum(cont['count'])

# Chi sq
for col in ['optin', 'giftaid']:
    [[ctrl_tot, ctrl_cnv],
     [test_tot, test_cnv]] = cont[['count', col]].values
    chisq = pd.DataFrame([[ctrl_tot - ctrl_cnv, ctrl_cnv],
                          [test_tot - test_cnv, test_cnv]],
                         columns=['non-conv', 'conv'], index=['ctrl', 'test'])
    chi2, chi2_p, dof, ex = chi2_contingency(chisq, correction=True)
    vals = cont[['count', col]]
    vals['rate'] = cont[col] / cont['count']
    print(vals)
    print('chi2(df={}, N={}) = {:.2f}, p = {:.2f}\n'.format(dof,
                                                            total,
                                                            chi2,
                                                            chi2_p))

# t-test
lbl = pd.read_csv('AmendedData\\LBL.csv', index_col='id')
lbl = lbl[lbl['value'] < 200]
lbl.groupby('cell').std()  # check variance/std are equal
t_stat, t_p = ttest_ind(lbl[lbl['cell'] == 'ctrl']['value'],
                        lbl[lbl['cell'] == 'test']['value'])
print('t(df={}) = {:.2f}, p = {:.2f}'.format(total-2, t_stat, t_p))