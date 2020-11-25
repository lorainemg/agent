from collections import deque
from utils import in_range
from cell import CellType

class Agent:
    def __init__(self, x, y, map_, kids):
        self.x = x
        self.y = y
        self.map = map_
        self.rows = len(map_)
        self.columns = len(map_[0])
        self.dx = [0,  0, 1, -1]
        self.dy = [1, -1, 0,  0]
        self.kid = None
        self.kids = kids
        self.path = None

    def move(self):
        raise NotImplementedError()

    def path_to_closest_dirt(self):
        return self.path_to_closest(CellType.DIRT)

    def path_to_closest_child(self):
        return self.path_to_closest(CellType.KID)

    def path_to_closest_corral(self):
        return self.path_to_closest(CellType.CORRAL)

    def path_to_closest(self, cell_type: CellType):
        queue = deque()
        queue.appendleft((self.x, self.y))
        father = [-1]*(self.rows*self.columns)
        father[self.x*self.rows+self.y] = 0
        to_child = cell_type == CellType.KID
        while queue:
            x, y = queue.pop()
            if self.map[x][y] == cell_type and self.can_pass(x, y, to_child):
                return self._get_path(x, y, father)
            for idx in range(len(self.dx)):
                nx = x + self.dx[idx]
                ny = y + self.dy[idx]
                if in_range(self.map, nx, ny) and father[nx*self.rows+ny] == -1 and self.can_pass(nx, ny, to_child):
                    father[nx*self.rows+ny] = (x, y)
                    queue.appendleft((nx, ny))

    def _get_path(self, x, y, father):
        path = [(x, y)]
        i, j = x, y
        while father[i*self.rows+j] != 0:
            i, j = father[i*self.rows+j]
            path.append((i,j))
        return list(reversed(path))

    def can_pass(self, x, y, admit_child=False):
        "Returns if the agent can pass through a specific cell"
        obstacles = not self.map[x][y].is_obstacle and not self.map[x][y].is_bussy_corral
        if admit_child:
            return obstacles
        else:
            return obstacles and not self.map[x][y].is_kid

    def move_one_pass(self, x, y):
        if self.can_pass(x, y, admit_child=True):
            self.map[self.x][self.y].remove(CellType.AGENT)
            self.map[x][y].add(CellType.AGENT) 
            self.x, self.y = x, y
            if self.map[x][y].is_kid:
                self.kid = self.map[x][y].kid
                self.kid.carried = True
                self.map[x][y].remove_child()
                

    def move_with_child(self, x, y):
        if self.can_pass(x, y):
            self.map[self.x][self.y].remove(CellType.AGENT)
            self.map[x][y].add(CellType.AGENT)
            self.x, self.y = x, y
            if self.map[x][y].is_empty_corral:
                self.map[x][y].add_child(self.kid)
                self.kid.x, self.kid.y = x, y
                self.kid.in_corral = True
                self.kid.carried = False
                self.kids -= 1
                self.kid = None
                return True
            return False

