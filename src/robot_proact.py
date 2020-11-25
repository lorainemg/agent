from agent import Agent
from cell import CellType

class ProactiveRobot(Agent):
    def move(self):
        if self.map[self.x][self.y].is_dirt:
            self.map[self.x][self.y].add(CellType.AGENT)
            self.map[self.x][self.y].remove(CellType.DIRT)
            return
        if self.path is not None and len(self.path) > 0:
            self.move_path()
        else:
            self.calculate_path()
            if self.path is not None and len(self.path) > 0:
                self.move_path()


    def calculate_path(self):
        if self.kids == 0:
            self.path = self.path_to_closest_dirt()
        elif self.kid is None:
            self.path = self.path_to_closest_child()
        else:
            self.path = self.path_to_closest_corral()
        if self.path is None:
            self.path = self.path_to_closest_dirt()
        if self.path is None:
            return
        self.path.pop(0)


    def move_path(self):
        if self.path is None:
            return
        x, y = self.path.pop(0)
        if not self.can_pass(x, y, self.kid is None):
            self.calculate_path()
            if self.path is None:
                return
            x, y = self.path.pop(0)
        if self.kid is None:
            self.move_one_pass(x, y)
        else:
            if self.move_with_child(x, y) or len(self.path) <= 0:
                return
            x, y = self.path.pop(0)
            self.move_with_child(x, y)