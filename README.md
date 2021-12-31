# apis-fixed
Rule-based control of APIS system
Using fixed scenario to update the DC/DC exchange among different houses.

All houses use a fixed rule-based scenario.json to update their request and accept actions
Aim to calculate the p2 (powermeter value) of houses as a baseline (default values: 0.9, 0.75, 0.6)

        "batteryStatus": {
            "4320.0-": "excess",
            "3600.0-4320.0": "sufficient",
            "2880.0-3600.0": "scarce",
            "-2880.0": "short"
        }

