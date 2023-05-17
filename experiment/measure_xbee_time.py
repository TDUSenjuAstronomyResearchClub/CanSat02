import datetime

import cansatapi.XBee

json_data = """"{
  "time": "8533/09/03 20:33:39",
  "gps": {
    "latitude": 5558822.156561226,
    "longitude": -22438785.878990024,
    "altitude": 82103611.27749738,
    "distance": {
      "sample": 4058044.045954019,
      "goal": -83127993.71467139
    },
    "azimuth": {
      "sample": 22504725.54897973,
      "goal": -99687446.2850228
    }
  },
  "nine-axis": {
    "acceleration": {
      "x": 13483892.350464448,
      "y": -39867413.76800813,
      "z": -36402760.73793136
    },
    "angular-velocity": {
      "x": -40901366.786130786,
      "y": 9327305.964930415,
      "z": -95932679.86728047
    },
    "azimuth": 18263485.435562596
  },
  "bme280": {
    "temperature": 20476320.206689015,
    "humidity": 4165199.488262281,
    "pressure": 41843311.01652777
  },
  "lps25hb": {
    "temperature": -12297314.349553108,
    "pressure": 613910.426940307,
    "altitude": 4071961.877873063
  },
  "battery": 20723059.396707416,
  "distance": 41335678.7646867,
}"""

print("start at:" + datetime.datetime.now().isoformat())
cansatapi.XBee.send(json_data)
print("done at:" + datetime.datetime.now().isoformat())
