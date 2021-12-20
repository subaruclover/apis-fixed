"""
# create by Qiong
# create scenario files for updating the energy exchange rules
# put it under the dir of apis-main/exe
"""

import json
import os


class CreateScenario():
    def __init__(self):

        # set time periods for scenario files
        # self.timePeriods = ["00:00:00-12:00:00", "12:00:00-24:00:00"]
        self.timePeriods = ["00:00:00-24:00:00"]
        # per hour: TimePeriods[0],...,TimePeriods[23]
        self.TimePeriods = ["00:00:00-01:00:00", "01:00:00-02:00:00", "02:00:00-03:00:00",
                            "03:00:00-04:00:00", "04:00:00-05:00:00", "05:00:00-06:00:00",
                            "06:00:00-07:00:00", "07:00:00-08:00:00", "08:00:00-09:00:00",
                            "09:00:00-10:00:00", "10:00:00-11:00:00", "11:00:00-12:00:00",
                            "12:00:00-13:00:00", "13:00:00-14:00:00", "14:00:00-15:00:00",
                            "15:00:00-16:00:00", "16:00:00-17:00:00", "17:00:00-18:00:00",
                            "18:00:00-19:00:00", "19:00:00-20:00:00", "20:00:00-21:00:00",
                            "21:00:00-22:00:00", "22:00:00-23:00:00", "23:00:00-24:00:00"]
        self.batterySize = 4800
        # batteryLevel : 4 levels
        self.batteryLevel = ["excess", "sufficient", "scarce", "short"]
        self.data = {
            "#": "place this file at the path defined by 'scenarioFile' in config file",
            "refreshingPeriodMsec": 5000,

            "acceptSelection": {
                "strategy": "pointAndAmount"
            },

            self.timePeriods[0]: {
                "batteryStatus": {  # batteryLevels
                    # list of actions
                    str(self.batterySize * 0.9) + "-": self.batteryLevel[0],
                    str(str(self.batterySize * 0.75) + "-" + str(self.batterySize * 0.9)): self.batteryLevel[1],
                    str(str(self.batterySize * 0.6) + "-" + str(self.batterySize * 0.75)): self.batteryLevel[2],
                    "-" + str(self.batterySize * 0.6): self.batteryLevel[3]
                },
                "request": {
                    self.batteryLevel[0]: {"discharge": {
                        "limitWh": self.batterySize * 0.9,  # 0.8,
                        "pointPerWh": 10
                    }},
                    self.batteryLevel[1]: {},
                    self.batteryLevel[2]: {},
                    self.batteryLevel[3]: {"charge": {
                        "limitWh": self.batterySize * 0.6,  # 0.4,
                        "pointPerWh": 10
                    }}
                },
                "accept": {
                    self.batteryLevel[0]: {"discharge": {
                        "limitWh": self.batterySize * 0.75,  # 0.5,
                        "pointPerWh": 10
                    }},
                    self.batteryLevel[1]: {"discharge": {
                        "limitWh": self.batterySize * 0.75,  # 0.5,
                        "pointPerWh": 10
                    }},
                    self.batteryLevel[2]: {"charge": {
                        "limitWh": self.batterySize * 0.75,  # 0.5,
                        "pointPerWh": 10
                    }},
                    self.batteryLevel[3]: {"charge": {
                        "limitWh": self.batterySize * 0.75,  # 0.5,
                        "pointPerWh": 10
                    }}
                }
            },

            # self.timePeriods[1]: {
            #     "batteryStatus": {
            #         str(self.batterySize * 0.7) + "-": self.batteryLevel[0],
            #         str(str(self.batterySize * 0.5) + "-" + str(self.batterySize * 0.7)): self.batteryLevel[1],
            #         str(str(self.batterySize * 0.3) + "-" + str(self.batterySize * 0.5)): self.batteryLevel[2],
            #         "-" + str(self.batterySize * 0.3): self.batteryLevel[3]
            #     },
            #     "request": {
            #         self.batteryLevel[0]: {"discharge": {
            #             "limitWh": self.batterySize * 0.7,
            #             "pointPerWh": 10
            #         }},
            #         self.batteryLevel[1]: {},
            #         self.batteryLevel[2]: {},
            #         self.batteryLevel[3]: {"charge": {
            #             "limitWh": self.batterySize * 0.3,
            #             "pointPerWh": 10
            #         }}
            #     },
            #     "accept": {
            #         self.batteryLevel[0]: {"discharge": {
            #             "limitWh": self.batterySize * 0.5,
            #             "pointPerWh": 10
            #         }},
            #         self.batteryLevel[1]: {"discharge": {
            #             "limitWh": self.batterySize * 0.5,
            #             "pointPerWh": 10
            #         }},
            #         self.batteryLevel[2]: {"charge": {
            #             "limitWh": self.batterySize * 0.5,
            #             "pointPerWh": 10
            #         }},
            #         self.batteryLevel[3]: {"charge": {
            #             "limitWh": self.batterySize * 0.5,
            #             "pointPerWh": 10
            #         }}
            #     }
            # }

        }
        self.filename1 = "scenario.json"
        self.filename2 = "scenario2.json"
        self.filename3 = "scenario3.json"
        self.filename4 = "scenario4.json"
        self.desired_dir = "/home/doya/Documents/APIS/apis-main/exe/"
        # self.desired_dir = "/Users/Huang/Documents/APIS/apis-main/exe/"
        self.full_path1 = os.path.join(self.desired_dir, self.filename1)
        self.full_path2 = os.path.join(self.desired_dir, self.filename2)
        self.full_path3 = os.path.join(self.desired_dir, self.filename3)
        self.full_path4 = os.path.join(self.desired_dir, self.filename4)

    def write_json(self):
        with open(self.full_path1, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        with open(self.full_path2, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        with open(self.full_path3, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        with open(self.full_path4, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)


# if __name__ == "__main__":
#     interval = 60 * 60  # every 60 * 60s
#     command = createJson()
#     run(interval, command)
