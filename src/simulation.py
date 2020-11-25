from enviroment import Enviroment
from utils import FinalState
from robot_proact import ProactiveRobot
from robot_react import ReactiveRobot
import json

def simulate(rows, columns, dirt, obstacles, kids, time, robot):
    fired = 0
    won = 0
    timeout = 0
    mean_dirt = 0
    for _ in range(30):
        world = Enviroment(rows, columns, dirt, obstacles, kids, time, robot)
        state, dirt = world.start_simulation()
        if state == FinalState.WON:
            won += 1
        elif state == FinalState.FIRED:
            fired += 1
        elif state == FinalState.TIMEOUT:
            timeout += 1
        mean_dirt += dirt
    return mean_dirt / 30, won / 30, fired / 30, timeout / 30 

def generate_enviroments():
    enviroments = [
        {'rows': 10, 'columns': 10, 'dirt': 1,  'obstacles': 2,  'kids': 7,  'time': 10},
        {'rows': 10, 'columns': 10, 'dirt': 1,  'obstacles': 2,  'kids': 7,  'time': 5},
        {'rows': 10, 'columns': 10, 'dirt': 1,  'obstacles': 2,  'kids': 7,  'time': 100},
        {'rows': 10, 'columns': 10, 'dirt': 1,  'obstacles': 2,  'kids': 10, 'time': 20},
        {'rows': 10, 'columns': 10, 'dirt': 1,  'obstacles': 2,  'kids': 5,  'time': 10},
        {'rows': 7,  'columns': 7,  'dirt': 5,  'obstacles': 9,  'kids': 5,  'time': 10},
        {'rows': 15, 'columns': 15, 'dirt': 10, 'obstacles': 10, 'kids': 7,  'time': 50},
        {'rows': 10, 'columns': 10, 'dirt': 10, 'obstacles': 30, 'kids': 7,  'time': 50},
        {'rows': 5,  'columns': 5,  'dirt': 2,  'obstacles': 10, 'kids': 5,  'time': 10},
        {'rows': 10, 'columns': 10, 'dirt': 40, 'obstacles': 5,  'kids': 5,  'time': 10},
        # {'rows': 12, 'columns': 13, 'dirt': 10, 'obstacles': 10, 'kids': 5,  'time': 10},
        # {'rows': 10, 'columns': 10, 'dirt': 10, 'obstacles': 10, 'kids': 6,  'time': 10},
        # {'rows': 5,  'columns': 5,  'dirt': 1,  'obstacles': 2,  'kids': 7,  'time': 10},
        # {'rows': 10, 'columns': 10, 'dirt': 2,  'obstacles': 2,  'kids': 5,  'time': 50},
        # {'rows': 10, 'columns': 10, 'dirt': 1,  'obstacles': 10, 'kids': 6,  'time': 20}
    ]
    data = {'Reactive': {}, 'Proactive': {}}
    for idx, enviroment in enumerate(enviroments):
        dirt, won, fired, timeout = simulate(**enviroment, robot=ReactiveRobot)
        data['Reactive'][idx] = {'dirt': dirt, 'won': won, 'fired': fired, 'timeout': timeout}
        dirt, won, fired, timeout = simulate(**enviroment, robot=ProactiveRobot)
        data['Proactive'][idx] = {'dirt': dirt, 'won': won, 'fired': fired, 'timeout': timeout}
    json.dump(data, open('results.json', 'w+'))


if __name__ == "__main__":
    generate_enviroments()