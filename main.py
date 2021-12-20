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

import requests, json
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

import global_var as gl
import config as conf
from agent import APIS, House

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

max_time = int(input('Enter the amount of seconds you want to run this: '))
start_time = time.time()  # remember when we started

# need to refresh the output data every 5s? time.sleep()
# def run_file(agent):
while (time.time() - start_time) < max_time:
    #not gl.sema:  # True, alter for different time periods
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

    time.sleep(60)  # 60s

        # States  pvc_charge_power[ids], for house E001
        # if ids == "E001":
        #     pv_e001 = np.array([pvc_charge_power["E001"]])
        #     load_e001 = np.array([ups_output_power["E001"]])
        #     p2_e001 = np.array([p2["E001"]])
        #     rsoc_e001 = np.array([rsoc["E001"]])
        #
        #     x_e001 = np.concatenate([pv_e001, load_e001, p2_e001, rsoc_e001], axis=-1)
        #     # print(x_e001)  # [39.14 575.58 734.    29.98] E001

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

plt.plot(pvc_e001, 'm*-', label="PV E001")
plt.plot(load_e001, 'y--', label="Load E001")
plt.plot(p2_e001, 'b', label="p2 E001")
plt.plot(rsoc_e001, 'g', label="RSOC E001")

plt.xlabel("time")
plt.ylabel("Power (W) / %")
plt.title("The default scenario")
plt.xlim(0, 359)
plt.legend()
plt.show()
