from queue import Queue
from matplotlib.axes import Axes
from typing import List, Tuple
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
from requests import get, Response
from collections import deque
import json

def get_new_speed() -> Tuple[datetime, float]:
    resp: Response = get("https://www.iceportal.de/api1/rs/status")
    j = json.loads(resp.text)
    timeInt: int = j["serverTime"]
    time: datetime = datetime.fromtimestamp(int(timeInt / 1000))
    time += timedelta(milliseconds=timeInt % 1000)
    speed: float = j["speed"]
    return (time, speed)
    
timeList: Queue[datetime] = deque(maxlen=600)
speedList: Queue[float] = deque(maxlen=600)

def plot_speed(ax: Axes) -> None:
    global timeList
    global speedList

    ax.cla()
    ax.clear()
    ax.set_xticks(ax.get_xticks(), ax.get_xticklabels(), rotation = -90)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
    ax.xaxis.set_major_locator(mdates.SecondLocator(interval=10))

    ax.plot(timeList, speedList, linewidth=1.0, label=f'ICE (max: {round(max(speedList), 2)}, cur: {speedList[-1]})', color="red", marker="x")
    ax.set_xlim([min(timeList), max(timeList)])
    ax.set_ylabel("Speed (km/h)")
    ax.set_xlabel("Time")
    ax.legend(loc='upper left')
    ax.grid(axis="y")

def animate(i, ax)  -> None:
    global timeList
    global speedList

    try:
        newVal: Tuple[datetime, float] = get_new_speed()
        timeList.append(newVal[0])
        speedList.append(newVal[1])
        plot_speed(ax)
    except:
        print("Failed to get train speed.")

fig, ax = plt.subplots(constrained_layout=True)
fig.suptitle("ICE Speed", fontsize=16)
ani = FuncAnimation(fig, animate, interval=1000, fargs=(ax,))
plt.show()
