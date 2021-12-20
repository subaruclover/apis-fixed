"""
#  setting the environment for each nodes (agent)
#  get the log data from apis-emulator for states

@author: Qiong
"""

import logging.config
import time

import numpy as np
import random
import gym
from gym.utils import seeding

logger = logging.getLogger(__name__)

import global_var as gl
import config as conf
import requests, json

from createScenario import CreateScenario

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

class APIS():
    def __init__(self, memory_size=10000):
        self.memory_size = memory_size
        self.memory = np.zeros((self.memory_size, 4))

    def CreateSce(self):
        newSce = CreateScenario()
        newSce.write_json()

        # if __name__ == "__main__":
        #     interval = 60 * 60  # every 60 * 60s
        #     command = createJson()
        #     run(interval, command)

    def store_value(self, pvc, load, p2, rsoc):
        if not hasattr(self, 'memory_counter'):
            self.memory_counter = 0
        store_values = np.hstack((pvc, load, p2, rsoc))
        index = self.memory_counter % self.memory_size
        self.memory[index, :] = store_values
        self.memory_counter += 1


# House Model, step function (reward)

class House():

    def __init__(self):

        self.action_request_space = np.linspace(0.2, 0.9, 8).tolist()
        self.action_accept_space = np.linspace(0.2, 0.9, 8).tolist()

        # list of possible actions
        # reward

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, state, action_request, action_accept):
        # how actions changes the states?

        # current_pv = state[0]
        # current_load = state[1]
        # current_p2 = state[2]
        # current_rsoc = state[3]
        # current_rsoc_ave = state[4]

        current_pvc_e001, current_load_e001, current_p2_e001, current_rsoc_e001, current_rsoc_ave = self.state
        # current_pvc = gl.oesunits[ids]["emu"]["pvc_charge_power"]
        # current_rsoc = core.rsocUpdate()

        output_data = requests.get(URL).text
        output_data = json.loads(output_data)  # dict

        rsoc_list = []

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

            rsoc_list.append(rsoc[ids])
            # refresh every 60 seconds
            # print("\n")
            # time.sleep(60)

            # States  pvc_charge_power[ids], for house E001
            if ids == "E001":
                current_pvc_e001 = np.array([pvc_charge_power["E001"]])
                current_load_e001 = np.array([ups_output_power["E001"]])
                current_p2_e001 = np.array([p2["E001"]])
                current_rsoc_e001 = np.array([rsoc["E001"]])

                current_all_e001 = np.concatenate([current_pvc_e001,
                                                   current_load_e001,
                                                   current_p2_e001,
                                                   current_rsoc_e001], axis=-1)
                # print(current_all_e001, type(current_all_e001))  # [39.14 575.58 734.    29.98] E001

        # print(rsoc)
        # {'E001': 29.98, 'E002': 29.99, 'E003': 29.98, 'E004': 29.99}
        current_rsoc_ave = np.mean(rsoc_list)  # get average rsoc of this community
        # print(rsoc_ave)
        self.state = np.concatenate([current_all_e001, np.array([current_rsoc_ave])], axis=-1)

        reward = current_p2_e001
        # done = time.sleep(5)  # time, e.g., one hour(time.sleep(60*60)) or given #EPI

        return np.array(self.state, dtype=np.float32), reward,  {}  # done

    def reset(self):
        # reset the states according to standard.json file (../apis-emulator/jsontmp)
        # all values are the same to each house
        # super().reset(seed=seed)

        # init state
        pvc_charge_power = np.array([0.])
        ups_output_power = np.array([0.])
        p2 = np.array([0.])
        rsoc = np.array([50.])
        # wg = np.array([0])
        # wb = np.array([-4.5])
        rsoc_ave = np.array([50.])  # average rsoc in the same community

        # self.state = np.array([self.state])
        self.state = np.concatenate([pvc_charge_power, ups_output_power, p2, rsoc, rsoc_ave], axis=-1)

        # return np.array(self.state, dtype=np.float32)
        return np.array(self.state, dtype=np.float32)
