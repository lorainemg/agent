from enum import Enum

class CellType(Enum):
    EMPTY = 0
    AGENT = 1
    OBSTACLE = 2
    DIRT = 3
    CORRAL = 4
    KID = 5

    def __str__(self):
        if self == self.EMPTY:
            return '.'
        elif self == self.AGENT:
            return 'R'
        elif self == self.OBSTACLE:
            return 'O'
        elif self == self.DIRT:
            return 'D'
        elif self == self.CORRAL:
            return 'C'
        elif self == self.KID:
            return 'K'

class Cell:
    def __init__(self, type_=CellType.EMPTY):
        self.content = [type_]
        self.kid = None

    @property
    def is_empty(self):
        return CellType.EMPTY in self.content

    @property
    def is_agent(self):
        return CellType.AGENT in self.content

    @property
    def is_obstacle(self):
        return CellType.OBSTACLE in self.content

    @property
    def is_dirt(self):
        return CellType.DIRT in self.content

    @property
    def is_corral(self):
        return CellType.CORRAL in self.content

    @property
    def is_kid(self):
        return CellType.KID in self.content

    @property
    def is_bussy_corral(self):
        return CellType.KID in self.content and CellType.CORRAL in self.content

    @property
    def is_empty_corral(self):
        return CellType.KID not in self.content and CellType.CORRAL in self.content

    def add(self, typex):
        if self.is_empty:
            self.content.remove(CellType.EMPTY)
        elif typex in self.content:
            return
        self.content.append(typex)
    
    def remove(self, typex):
        if typex not in self.content:
            return
            # raise Exception('That element is not in the cell')
        self.content.remove(typex)
        if len(self.content) == 0:
            self.content.append(CellType.EMPTY)

    def add_child(self, kid):
        self.add(CellType.KID)
        self.kid = kid

    def remove_child(self):
        self.remove(CellType.KID)
        self.kid = None

    def remove_all(self):
        self.content = [CellType.EMPTY]
        self.kid = None

    def __str__(self):
        if CellType.AGENT in self.content:
            return str(CellType.AGENT)
        elif CellType.KID in self.content:
            return str(CellType.KID)
        return str(self.content[0])

    def __eq__(self, other):
        if other == CellType.CORRAL:
            return len(self.content) == 1 and self.content[0] == other
        else:
            return other in self.content