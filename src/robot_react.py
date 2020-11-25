from agent import Agent
from cell import CellType

class ReactiveRobot(Agent):
    def move(self):
        if self.map[self.x][self.y].is_dirt:
            self.map[self.x][self.y].add(CellType.AGENT)
            self.map[self.x][self.y].remove(CellType.DIRT)
            return
        if self.kids == 0:
            self.move_to_dirt()
        elif self.kid is None:
            self.move_to_kid()
        else:
            self.move_to_corral()

    def move_to_kid(self): 
        path = self.path_to_closest_child()
        if path is None:
            self.move_to_dirt()
        else:
            x, y = path[1]
            self.move_one_pass(x, y)

    def move_to_corral(self):
        path = self.path_to_closest_corral()
        if path is None:
            self.move_to_dirt()
        else:
            x, y = path[1]
            if self.move_with_child(x, y):
                return
            x, y = path[2]
            self.move_with_child(x, y)


    def move_to_dirt(self):
        path = self.path_to_closest_dirt()
        if path is not None:
            x, y = path[1]
            self.move_one_pass(x, y)
