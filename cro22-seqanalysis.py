# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:47:11 2020

@author: SWannell
"""

from SeqAnalysis import SeqAnalysis as seqan

two_month_vol, cvr = 2748, 0.155
target = int(two_month_vol * cvr)
ttl = 'CR022 email opt-in design'

seq = seqan(target, ttl)  # returns the plot!!
seq.cvr_plot(ttl)
seq.crossed()
#seq.summary()

#print(seq.z_score)
#print(seq.results)
#help(seq)  # Prints doc string as expected