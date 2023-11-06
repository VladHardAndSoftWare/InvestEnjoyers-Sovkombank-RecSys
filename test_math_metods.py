import datetime
import matplotlib.pyplot as plt
import numpy as np

from Methods import investor_analysis as ina

S0=100000
Sr=5000
H=36
T=1
S=200000

print('r=', ina.iter_expected_profitability(S0, Sr, S, H, T))