"""
Show the results of different acc with plots
input data files: .csv files with one week data from sample data
House ID: E001 ~ E004
created by Qiong
"""

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="white")

import pandas as pd
import os
import global_var as gl

inputFile = "sample_acc_10.csv"
inputData = pd.read_csv(inputFile)
memory = inputData.to_numpy()

# calculate the coefficient w.r.t gl.acc
filename = os.path.splitext(inputFile)[0]
check_acc = filename.split("_")[2]
coeff = int(60 / gl.acc)

if int(check_acc) == gl.acc:

    print("acc correctly received")
    # PLOT Houses data
    rows_e001 = list(range(0, 10000, 4))
    rows_e002 = [x+1 for x in rows_e001]
    rows_e003 = [x+2 for x in rows_e001]
    rows_e004 = [x+3 for x in rows_e001]

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


    """
    Plot data
    """
    # fig, axs = plt.subplots(2, 2, figsize=(12, 12))
    fig, (ax0, ax1, ax2, ax3) = plt.subplots(4, 1, figsize=(12, 12))
    ax0_2 = ax0.twinx()
    ax1_2 = ax1.twinx()
    ax2_2 = ax2.twinx()
    ax3_2 = ax3.twinx()
    fig.suptitle("The default scenario, E001-E004, acc=%i" % gl.acc)

    pvc_e001_plot = ax0.plot(pvc_e001[:24*7*coeff], 'm*-', label="PV E001")
    load_e001_plot = ax0.plot(load_e001[:24*7*coeff], 'y--', label="Load E001")
    p2_e001_plot = ax0.plot(p2_e001[:24*7*coeff], 'b', label="p2 E001")
    rsoc_e001_plot = ax0_2.plot(rsoc_e001[:24*7*coeff], 'g', label="RSOC E001")
    # ax0.set_xlabel("Hour")
    ax0.set_ylabel("Power (W)")
    ax0_2.set_ylabel(" % ")
    plots_e001 = pvc_e001_plot + load_e001_plot + p2_e001_plot + rsoc_e001_plot
    labels_e001 = [plot.get_label() for plot in plots_e001]
    ax0.legend(plots_e001, labels_e001, loc='upper left')

    pvc_e002_plot = ax1.plot(pvc_e002[:24*7*coeff], 'm*-', label="PV E002")
    load_e002_plot = ax1.plot(load_e002[:24*7*coeff], 'y--', label="Load E002")
    p2_e002_plot = ax1.plot(p2_e002[:24*7*coeff], 'b', label="p2 E002")
    rsoc_e002_plot = ax1_2.plot(rsoc_e002[:24*7*coeff], 'g', label="RSOC E002")
    # ax1.set_xlabel("Hour")
    ax1.set_ylabel("Power (W)")
    ax1_2.set_ylabel(" % ")
    plots_e002 = pvc_e002_plot + load_e002_plot + p2_e002_plot + rsoc_e002_plot
    labels_e002 = [plot.get_label() for plot in plots_e002]
    ax1.legend(plots_e002, labels_e002, loc='upper left')


    pvc_e003_plot = ax2.plot(pvc_e003[:24*7*coeff], 'm*-', label="PV E003")
    load_e003_plot = ax2.plot(load_e003[:24*7*coeff], 'y--', label="Load E003")
    p2_e003_plot = ax2.plot(p2_e003[:24*7*coeff], 'b', label="p2 E003")
    rsoc_e003_plot = ax2_2.plot(rsoc_e003[:24*7*coeff], 'g', label="RSOC E003")
    # ax2.set_xlabel("Hour")
    ax2.set_ylabel("Power (W)")
    ax2_2.set_ylabel(" % ")
    plots_e003 = pvc_e003_plot + load_e003_plot + p2_e003_plot + rsoc_e003_plot
    labels_e003 = [plot.get_label() for plot in plots_e003]
    ax2.legend(plots_e003, labels_e003, loc='upper left')

    pvc_e004_plot = ax3.plot(pvc_e004[:24*7*coeff], 'm*-', label="PV E004")
    load_e004_plot = ax3.plot(load_e004[:24*7*coeff], 'y--', label="Load E004")
    p2_e004_plot = ax3.plot(p2_e004[:24*7*coeff], 'b', label="p2 E004")
    rsoc_e004_plot = ax3_2.plot(rsoc_e004[:24*7*coeff], 'g', label="RSOC E004")
    ax3.set_xlabel("Hour")
    ax3.set_ylabel("Power (W)")
    ax3_2.set_ylabel(" % ")
    plots_e004 = pvc_e004_plot + load_e004_plot + p2_e004_plot + rsoc_e004_plot
    labels_e004 = [plot.get_label() for plot in plots_e004]
    ax3.legend(plots_e004, labels_e004, loc='upper left')

    plt.show()
else:
    print("check acc value")
