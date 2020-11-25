import numpy as np
import random
from utils import in_range, empty_positions, FinalState
from kids import Kid
from cell import Cell, CellType
from copy import deepcopy
from agent import Agent
from robot_proact import ProactiveRobot
from robot_react import ReactiveRobot

class Enviroment:
    def __init__(self, rows:int, columns:int, dirt:int, obstacles:int, kids:int, time:int, robot: Agent):
        self.rows, self.columns = rows, columns
        self.time = time
        self.actual_time = 0
        self.map = [[Cell() for _ in range(columns)] for _ in range(rows)]
        self.dx = [0,  0, 1, -1]
        self.dy = [1, -1, 0,  0]        
        
        self.watch = False
        self.mean_dirt = 0
        self.world_distribution(dirt, obstacles, kids)
        pos = random.choice(empty_positions(self.map))
        self.agent = robot(pos[0], pos[1], self.map, len(self.kids_list))
        self.map[pos[0]][pos[1]].add(CellType.AGENT)

    def dirty_cells(self):
        return len([x for row in self.map for x in row if x.is_dirt])

    def start_simulation(self, watch=False):
        self.watch = watch
        while True:
            if watch:
                print(self)
                print('------------------')
            self.mean_dirt += self.dirty_cells()
            self.turn()
            if self.fire():
                if watch:
                    print(self)
                    print('Robot is fired')
                return FinalState.FIRED, (self.mean_dirt / self.actual_time) / (self.columns*self.rows)
            elif self.win():
                if watch:
                    print(self)
                    print('Robot won')
                return FinalState.WON, (self.mean_dirt / self.actual_time) / (self.columns*self.rows)
            elif self.actual_time == 100 * self.time:
                if watch:
                    print(self)
                    print('Finished time')
                return FinalState.TIMEOUT, (self.mean_dirt / self.actual_time) / (self.columns*self.rows)
            if watch:
                input()

    def turn(self):
        self.agent.move()
        for k in self.kids_list:
            k: Kid
            # k.calculate_move()
            k.move()
        self.actual_time += 1
        if self.actual_time % self.time == 0 and random.random() >= 0.5:
            self.world_redistribution()

    def world_distribution(self, dirt, obstacles, kids):
        dirt = int(self.rows*self.columns*dirt / 100)       # calcular las casillas sucias (dirt es porcentual)
        obstacles = int(self.rows*self.columns*obstacles / 100)       # calcular la cantidad de obstaculos
        self.kids_list = []       
        positions = self.occupy_corral(kids)
        for x, y in positions:
            self.map[x][y].add(CellType.CORRAL)
        self.occupy_obstacles(obstacles)
        self.occupy_dirt(dirt)
        self.occupy_kids(kids)

    def world_redistribution(self):
        if self.watch:
            print('WORLD REDISTRIBUTION')
        
        map_ = self.redistribute_corral()
        map_[self.agent.x][self.agent.y].add(CellType.AGENT)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                elem = self.map[i][j]
                if not elem.is_empty:
                    empty_pos = empty_positions(map_)
                    if empty_pos:
                        x, y = random.choice(empty_pos)
                    else:
                        x, y = i, j
                if elem.is_dirt:
                    map_[x][y].add(CellType.DIRT)
                if elem.is_obstacle:
                    map_[x][y].add(CellType.OBSTACLE)
                if elem.is_kid:
                    kid = self.map[i][j].kid
                    if not kid.carried and not kid.in_corral:
                        kid.x, kid.y = x, y
                        map_[x][y].add_child(kid)
                    kid.map = map_
        self.map = map_
        self.agent.map = map_

    def redistribute_corral(self):
        map_ = [[Cell() for _ in range(self.columns)] for _ in range(self.rows)]
        
        corral_positions = self.occupy_corral(len(self.kids_list))
        act_positions = [(i, j) for i in range(len(self.map)) for j in range(len(self.map[i])) if self.map[i][j].is_corral]

        for idx in range(len(act_positions)):
            i, j = act_positions[idx]
            x, y = corral_positions[idx]
            if self.map[i][j].is_kid:
                kid = self.map[i][j].kid
                kid.x, kid.y = x, y
                map_[x][y].add_child(kid)
                kid.map = map_
            map_[x][y].add(CellType.CORRAL)
        return map_

    def occupy_corral(self, kids):
        "Occupy adyecents cells of the corral throw bfs"
        i, j = np.random.randint(0, self.rows), np.random.randint(0, self.rows)
        
        queue = []
        visited = [False]*(self.rows*self.columns)

        queue.insert(0, (i, j))
        visited[i*self.rows + j] = True
        n = 0
    
        positions = []
        while queue and n < kids:
            i, j = queue.pop()
            # self.map[i][j].add(CellType.CORRAL) 
            positions.append((i, j))
            n += 1    
            
            for idx in range(len(self.dx)):
                n_i, n_j = i + self.dx[idx], j + self.dy[idx]
                if in_range(self.map, n_i, n_j) and not visited[n_i*self.rows + n_j]:
                    queue.insert(0, (n_i, n_j))
                    visited[n_i*self.rows + n_j] = True    
        return positions                    

    def occupy_obstacles(self, obstacles):
        tries = 10*self.rows*self.columns
        positions = empty_positions(self.map)
        positions = random.sample(positions, k=obstacles)
        while tries > 0:
            for i, j in positions:
                if self.map[i][j].is_empty:
                    self.map[i][j].add(CellType.OBSTACLE) 
            if not self.disconect(0,0):
                break
            tries -= 1
        return None

    def disconect(self, i, j):
        visited = [False]*(self.rows*self.columns)
        visited[i*self.rows + j] = True
        
        try:
            ni, nj = next(filter(lambda x: in_range(self.map, x[0], x[1]) and not self.map[x[0]][x[1]].is_obstacle, 
                                [(i + self.dx[idx], j + self.dy[idx]) for idx in range(len(self.dx))]))
        except StopIteration:
            return False
        visited[ni*self.rows + nj] = True
        queue = [(ni, nj)]
        while queue:
            i, j = queue.pop()
            
            for idx in range(len(self.dx)):
                n_i, n_j = i + self.dx[idx], j + self.dy[idx]
                if in_range(self.map, n_i, n_j) and not visited[n_i*self.rows + n_j]:
                    if not self.map[n_i][n_j].is_obstacle and not self.map[n_i][n_j].is_empty_corral:
                        queue.insert(0, (n_i, n_j))
                    visited[n_i*self.rows + n_j] = True 
        return not all(visited)

    def occupy_dirt(self, amount: int):
        'Ocuppy the specify amount of empty cells with the specify type'
        positions = empty_positions(self.map)
        positions = random.sample(positions, k=amount)
        for i, j in positions:
            self.map[i][j].add(CellType.DIRT) 

    def occupy_kids(self, amount: int):
        positions = empty_positions(self.map)
        positions = random.sample(positions, amount)
        for i, j in positions:
            kid = Kid(i, j, self.map)
            self.map[i][j].add_child(kid)
            self.kids_list.append(kid)

    def __str__(self):
        return '\n'.join([' '.join([str(cell) for cell in row]) for row in self.map])
        
    def fire(self):
        dirt = self.dirty_cells()
        empty_cells = len(empty_positions(self.map)) + dirt
        return dirt / empty_cells > 0.6

    def win(self):
        dirt = sum([1 for row in self.map for x in row if x.is_dirt])
        return dirt == 0 and all([kid.in_corral for kid in self.kids_list])

if __name__ == '__main__':
    world = Enviroment(rows=5, columns=5, dirt=1, obstacles=30, kids=5, time=10, robot=ReactiveRobot)
    world.start_simulation(watch=True)

    # print(world)