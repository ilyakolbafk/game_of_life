class Cell:
    def __init__(self):
        self.is_live = False
        self.neighbors = list()
        self.living_neighbors = 0

    def __int__(self):
        return int(self.is_live)

    def __str__(self):
        return '███' if self.is_live else '   '

    def count_neighbors(self):
        self.living_neighbors = sum(int(i) for i in self.neighbors)

    def step(self):
        if self.is_live:
            if self.living_neighbors not in [2, 3]:
                self.is_live = False
        elif self.living_neighbors == 3:
            self.is_live = True
