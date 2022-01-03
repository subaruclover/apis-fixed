"""
Compare MSE (or sth. likely) to check different acc
House ID: E001 ~ E004
created by Qiong
"""

from matplotlib import pyplot as plt
import seaborn as sns

sns.set(style="white")

import pandas as pd
import os
import numpy as np

# import global_var as gl
#
# coeff = int(60 / gl.acc)

inputFile_acc_10 = "sample_acc_10.csv"
inputFile_acc_30 = "sample_acc_10.csv"
inputFile_acc_60 = "sample_acc_10.csv"
inputFile_acc_300 = "sample_acc_10.csv"

inputData_acc_10 = pd.read_csv(inputFile_acc_10)
inputData_acc_30 = pd.read_csv(inputFile_acc_30)
inputData_acc_60 = pd.read_csv(inputFile_acc_60)
inputData_acc_300 = pd.read_csv(inputFile_acc_300)

memory_acc_10 = inputData_acc_10.to_numpy()
memory_acc_30 = inputData_acc_30.to_numpy()
memory_acc_60 = inputData_acc_60.to_numpy()
memory_acc_300 = inputData_acc_300.to_numpy()


def arrange(memory):
    # arrange the memory according to 4 houses    
    rows_e001 = list(range(0, 10000, 4))
    rows_e002 = [x + 1 for x in rows_e001]
    rows_e003 = [x + 2 for x in rows_e001]
    rows_e004 = [x + 3 for x in rows_e001]

    pvc_e001 = memory[rows_e001, 0]
    load_e001 = memory[rows_e001, 1]
    p2_e001 = memory[rows_e001, 2]
    rsoc_e001 = memory[rows_e001, 3]

    pvc_e002 = memory[rows_e002, 0]
    load_e002 = memory[rows_e002, 1]
    p2_e002 = memory[rows_e002, 2]
    rsoc_e002 = memory[rows_e002, 3]

    pvc_e003 = memory[rows_e003, 0]
    load_e003 = memory[rows_e003, 1]
    p2_e003 = memory[rows_e003, 2]
    rsoc_e003 = memory[rows_e003, 3]

    pvc_e004 = memory[rows_e004, 0]
    load_e004 = memory[rows_e004, 1]
    p2_e004 = memory[rows_e004, 2]
    rsoc_e004 = memory[rows_e004, 3]

    return pvc_e001, load_e001, p2_e001, rsoc_e001


pvc_e001_acc_10, load_e001_acc_10, p2_e001_acc_10, rsoc_e001_acc_10 = arrange(memory_acc_10)
pvc_e001_acc_30, load_e001_acc_30, p2_e001_acc_30, rsoc_e001_acc_30 = arrange(memory_acc_30)
pvc_e001_acc_60, load_e001_acc_60, p2_e001_acc_60, rsoc_e001_acc_60 = arrange(memory_acc_60)
pvc_e001_acc_300, load_e001_acc_300, p2_e001_acc_300, rsoc_e001_acc_300 = arrange(memory_acc_300)

"""
Plot data
"""
fig, ax = plt.subplots(1, 1, figsize=(12, 6))
ax2 = ax.twinx()

fig.suptitle("Different acc")

pvc_e001_plot_acc_10 = ax.plot(pvc_e001_acc_10[:24 * 7 * 6], 'm*-', label="PV E001 acc=10")
pvc_e001_plot_acc_30 = ax.plot(pvc_e001_acc_30[:24 * 7 * 6], 'y-', label="PV E001 acc=30")
pvc_e001_plot_acc_60 = ax.plot(pvc_e001_acc_60[:24 * 7 * 6], 'go-', label="PV E001 acc=60")
pvc_e001_plot_acc_300 = ax.plot(pvc_e001_acc_300[:24 * 7 * 6], 'b--', label="PV E001 acc=300")

# load_e001_plot = ax.plot(load_e001[:24 * 7 * coeff], 'y--', label="Load E001")
# p2_e001_plot = ax.plot(p2_e001[:24 * 7 * coeff], 'b', label="p2 E001")
# rsoc_e001_plot = ax2.plot(rsoc_e001[:24 * 7 * coeff], 'g', label="RSOC E001")
# ticks = np.arange(0, 24*7*coeff, 24*coeff)

# ax_ticks = ax.set_xticks(np.linspace(0, 24 * 7 * coeff, 8, endpoint=True))
# hours = np.round(np.linspace(0, 24 * 7 * coeff, 8, endpoint=True) / coeff).astype(int)
# label = []
# for i in range(len(hours)):
#     label.append(str(hours[i]))  # ['0', '24', '48', '72', '96', '120', '144', '168']
# ax_labels = ax.set_xticklabels(label)
# ax.set_xlabel("Hour")
ax.set_ylabel("Power (W)")
ax2.set_ylabel(" % ")
plots_e001 = pvc_e001_plot_acc_10 + pvc_e001_plot_acc_30 + pvc_e001_plot_acc_60 + pvc_e001_plot_acc_300
# + load_e001_plot + p2_e001_plot + rsoc_e001_plot
labels_e001 = [plot.get_label() for plot in plots_e001]
ax.legend(plots_e001, labels_e001, loc='upper left')

plt.show()

# TODO MSE?
