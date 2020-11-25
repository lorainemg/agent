from random import choice, sample, randint
from utils import in_range, empty_positions
from cell import CellType

class Kid:
    def __init__(self, x, y, map_):
        self.x = x  
        self.y = y
        self.map = map_
        self.carried = False        # guarda si el nino esta siendo cargado por el robot
        self.in_corral = False
        self.dx = [0,  0, 1, -1]
        self.dy = [1, -1, 0,  0]

    # def move(self):
    #     if self.carried or self.in_corral:
    #         return
    #     # Se actualiza la posición de la casilla
    #     if self.x != self.pos_x or self.y != self.pos_y:
    #         self.map[self.x][self.y].remove_child()
    #         self.x, self.y = self.pos_x, self.pos_y
    #         self.map[self.x][self.y].add_child(self) 


    def move(self):
        if self.carried or self.in_corral:
            return
        x, y = self._move()
        if x == self.x and y == self.y:     # It didn't move
            return
        
        self.map[self.x][self.y].remove_child()
        self.map[x][y].add_child(self) 

        # Si se movió se genera basura en la cuadricula anterior
        kids = 1
        # determina la cantidad de niños en la cuadricula de 3x3
        positions = []
        for idx in range(len(self.dx)):
            nx = self.x + self.dx[idx]
            ny = self.y + self.dy[idx]
            if in_range(self.map, nx, ny):
                if self.map[nx][ny].is_kid:
                    kids += 1
                elif self.map[nx][ny].is_empty:
                    positions.append((nx, ny))

        self.x, self.y = x, y

        if kids == 1:
            self.choose_dirty_cells(randint(0,1), positions)
        elif kids == 2:
            self.choose_dirty_cells(randint(0, 3), positions)
        elif kids >= 3:
            self.choose_dirty_cells(randint(0, 6), positions)
    
    def choose_dirty_cells(self, k, positions):
        k = min(k, len(positions))
        cells = sample(positions, k=k)
        for i, j in cells:
            if self.map[i][j].is_empty:
                self.map[i][j].add(CellType.DIRT)

    def _move(self): 
        idx = randint(0, len(self.dx)-1)
        ix, iy = self.dx[idx], self.dy[idx]
        new_x = self.x + self.dx[idx]
        new_y = self.y + self.dy[idx]

        # Si la casilla está fuera de los límites o está ocupada el niño no se puede mover
        if not in_range(self.map, new_x, new_y) or self.is_busy(new_x, new_y):  
            return (self.x, self.y)
        elif self.map[new_x][new_y].is_obstacle:
            if not self.push_obstacles(new_x, new_y, ix, iy):
                return (self.x, self.y)
        return (new_x, new_y)
        

    def is_busy(self, x, y):
        return not self.map[x][y].is_empty and not self.map[x][y].is_obstacle

    def push_obstacles(self, x, y, i, j):
        '''
        Function to recursively push the obstacles.
        x: row were the current obstacle is
        y: column were the current obstacle is
        i: direction were the movement is going in the rows 
        j: direction were the movement is going in the columns 
        '''
        if self.map[x][y].is_empty:
            return True
        elif self.map[x][y].is_obstacle:
            if in_range(self.map, x+i, y+j):
                moved = self.push_obstacles(x+i, y+j, i, j)
                if moved:
                    self.map[x+i][y+j].add(CellType.OBSTACLE)
                return moved
        return False