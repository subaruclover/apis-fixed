#!/usr/bin/env python
"""
#  fixed scenario control of APIS

created by : Qiong

All houses use a fixed rule-based scenario.json to update their request and accept actions
Aim to calculate the p2 (powermeter value) of houses as a baseline (default values: 0.9, 0.75, 0.6)

        "batteryStatus": {
            "4320.0-": "excess",
            "3600.0-4320.0": "sufficient",
            "2880.0-3600.0": "scarce",
            "-2880.0": "short"
        },

"""
import time
# from threading import Thread
import os

import requests, json
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

import pandas as pd

import global_var as gl
import config as conf
from agent import APIS, House

print("acc is =%i" % gl.acc)
agent = APIS()
env = House()

agent.CreateSce()

##############################
# Data loading
# get log data for states
host = conf.b_host
port = conf.b_port
# url = "http://0.0.0.0:4390/get/log"
URL = "http://" + host + ":" + str(port) + "/get/log"

# dicts of states for all houses
pvc_charge_power = {}
ups_output_power = {}
p2 = {}  # powermeter.p2, Power consumption to the power storage system [W]
rsoc = {}
wg = {}  # meter.wg, DC Grid power [W]
wb = {}  # meter.wb, Battery Power [W]

pv_list = []
load_list = []
p2_list = []
rsoc_list = []

# max_time: 10,080s -> 2.8hr in run time, 168hr(7 days) in real time when acc=60, sleep=60s
# max_time: 20,160s -> 5.6hr in run time, 168hr(7 days) in real time when acc=30, sleep=60s -> 120s
# max_time: 60,480s -> 16.8hr in run time, 168hr(7 days) in real time when acc=10, sleep=60s
# max_time: 2,016s -> 0.56hr in run time, 168hr(7 days) in real time when acc=300, sleep=60s
max_time = 20160  # int(input('Enter the amount of seconds you want to run this: '))
# 21,600, 6hrs
start_time = time.time()  # remember when we started

# need to refresh the output data every 5s? time.sleep()
# def run_file(agent):
while (time.time() - start_time) < max_time:
    # not gl.sema:  # True, alter for different time periods
    # # refresh every 5 seconds
    # time.sleep(5)
    # read variables from /get/log url
    # print(output_data.text)
    output_data = requests.get(URL).text
    output_data = json.loads(output_data)  # dict

    for ids, dict_ in output_data.items():  # ids: E001, E002, ... house ID
        # print('the name of the dictionary is ', ids)
        # print('the dictionary is ', dict_)
        # when ids is "E001" (change to other house ID for other houses)
        pvc_charge_power[ids] = output_data[ids]["emu"]["pvc_charge_power"]
        ups_output_power[ids] = output_data[ids]["emu"]["ups_output_power"]
        p2[ids] = output_data[ids]["dcdc"]["powermeter"]["p2"]
        rsoc[ids] = output_data[ids]["emu"]["rsoc"]
        wg[ids] = output_data[ids]["dcdc"]["meter"]["wg"]
        wb[ids] = output_data[ids]["dcdc"]["meter"]["wb"]

        print("pv of {ids} is {pv},".format(ids=ids, pv=pvc_charge_power[ids]),
              "load of {ids} is {load},".format(ids=ids, load=ups_output_power[ids]),
              "p2 of {ids} is {p2},".format(ids=ids, p2=p2[ids]),
              "rsoc of {ids} is {rsoc},".format(ids=ids, rsoc=rsoc[ids])
              # "wg of {ids} is {wg},".format(ids=ids, wg=wg[ids]),
              # "wb of {ids} is {wb},".format(ids=ids, wb=wb[ids])
              )
        # rsoc_list.append(rsoc[ids])
        agent.store_value(pvc_charge_power[ids], ups_output_power[ids], p2[ids], rsoc[ids])

        # refresh every 5 seconds
        # print("\n")

    time.sleep(120)  # 60s -> shall this value be adjusted w.r.t. gl.acc? sleep time -> one hr in real time
    # acc = 60, real run time : 1 min == 1 hour in real data time (1 point recorded), sleep(60)
    # acc = 10, real run time : 6 min == 1 hour in real data time (1 point recorded), sleep(360)
    # acc = 30, real run time : 2 min == 1 hour in real data time (1 point recorded), sleep(120)

    end_time = time.time()
    print("running time: {:.2f} mins".format((end_time - start_time)/60 * gl.acc))  # real time

"""
# PLOT Houses data
rows_e001 = list(range(0, agent.memory_size, 4))
rows_e002 = [x+1 for x in rows_e001]
rows_e003 = [x+2 for x in rows_e001]
rows_e004 = [x+3 for x in rows_e001]

pvc_e001 = agent.memory[rows_e001, 0]
load_e001 = agent.memory[rows_e001, 1]
p2_e001 = agent.memory[rows_e001, 2]
rsoc_e001 = agent.memory[rows_e001, 3]

pvc_e002 = agent.memory[rows_e002, 0]
load_e002 = agent.memory[rows_e002, 1]
p2_e002 = agent.memory[rows_e002, 2]
rsoc_e002 = agent.memory[rows_e002, 3]

pvc_e003 = agent.memory[rows_e003, 0]
load_e003 = agent.memory[rows_e003, 1]
p2_e003 = agent.memory[rows_e003, 2]
rsoc_e003 = agent.memory[rows_e003, 3]

pvc_e004 = agent.memory[rows_e004, 0]
load_e004 = agent.memory[rows_e004, 1]
p2_e004 = agent.memory[rows_e004, 2]
rsoc_e004 = agent.memory[rows_e004, 3]
"""
"""
Save data into csv files
"""
# export to csv files
new_path = os.getcwd()
# filename = "sample_acc_60.csv"  # 168*4 points data saved
filename = "sample_acc_30.csv"  # 168*8 points data saved
# filename = "sample_acc_300.csv"  # 5 mins
pd.DataFrame(agent.memory).to_csv(os.path.join(new_path, filename), index=False)
# agent.memory.to_csv(os.path.join(new_path, filename), index=False)
# pd.DataFrame(np_array).to_csv("path/to/file.csv")

"""
Plot data

# fig, axs = plt.subplots(2, 2, figsize=(12, 12))
fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(2, 2, figsize=(12, 12))
ax0_2 = ax0.twinx()
ax1_2 = ax1.twinx()
ax2_2 = ax2.twinx()
ax3_2 = ax3.twinx()
fig.suptitle("The default scenario, E001-E004, acc=60")

pvc_e001_plot = ax0.plot(pvc_e001[:24], 'm*-', label="PV E001")
load_e001_plot = ax0.plot(load_e001[:24], 'y--', label="Load E001")
p2_e001_plot = ax0.plot(p2_e001[:24], 'b', label="p2 E001")
rsoc_e001_plot = ax0_2.plot(rsoc_e001[:24], 'g', label="RSOC E001")
ax0.set_xlabel("Hour")
ax0.set_ylabel("Power (W)")
plots_e001 = pvc_e001_plot + load_e001_plot + p2_e001_plot + rsoc_e001_plot
labels_e001 = [plot.get_label() for plot in plots_e001]
ax0.legend(plots_e001, labels_e001, loc='best')

pvc_e002_plot = ax1.plot(pvc_e002[:24], 'm*-', label="PV E002")
load_e002_plot = ax1.plot(load_e002[:24], 'y--', label="Load E002")
p2_e002_plot = ax1.plot(p2_e002[:24], 'b', label="p2 E002")
rsoc_e002_plot = ax1_2.plot(rsoc_e002[:24], 'g', label="RSOC E002")
ax1.set_xlabel("Hour")
# ax1.set_ylabel("Power (W) / %")
plots_e002 = pvc_e002_plot + load_e002_plot + p2_e002_plot + rsoc_e002_plot
labels_e002 = [plot.get_label() for plot in plots_e002]
ax1.legend(plots_e002, labels_e002, loc='best')
ax1_2.set_ylabel(" % ")

pvc_e003_plot = ax2.plot(pvc_e003[:24], 'm*-', label="PV E003")
load_e003_plot = ax2.plot(load_e003[:24], 'y--', label="Load E003")
p2_e003_plot = ax2.plot(p2_e003[:24], 'b', label="p2 E003")
rsoc_e003_plot = ax2_2.plot(rsoc_e003[:24], 'g', label="RSOC E003")
ax2.set_xlabel("Hour")
ax2.set_ylabel("Power (W)")
plots_e003 = pvc_e003_plot + load_e003_plot + p2_e003_plot + rsoc_e003_plot
labels_e003 = [plot.get_label() for plot in plots_e003]
ax2.legend(plots_e003, labels_e003, loc='best')

pvc_e004_plot = ax3.plot(pvc_e004[:24], 'm*-', label="PV E004")
load_e004_plot = ax3.plot(load_e004[:24], 'y--', label="Load E004")
p2_e004_plot = ax3.plot(p2_e004[:24], 'b', label="p2 E004")
rsoc_e004_plot = ax3_2.plot(rsoc_e004[:24], 'g', label="RSOC E004")
ax3.set_xlabel("Hour")
# ax3.set_ylabel("Power (W) / %")
plots_e004 = pvc_e004_plot + load_e004_plot + p2_e004_plot + rsoc_e004_plot
labels_e004 = [plot.get_label() for plot in plots_e004]
ax3.legend(plots_e004, labels_e004, loc='best')
ax3_2.set_ylabel(" % ")

plt.show()
"""