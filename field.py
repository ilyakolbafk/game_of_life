from random import choice
from cell import *
from time import sleep

_FIELD_SIZE = 41
_CENTER_POSITION = _FIELD_SIZE // 2
_TIME_FOR_SLEEP = 0.5


class Field:
    def __init__(self):
        self.top = 0
        self.bot = 0
        self.left = 0
        self.right = 0
        self.step_counter = 0
        self.configurations = list()
        self.last_configuration = list()
        self.field = [[Cell() for _ in range(_FIELD_SIZE)] for _ in range(_FIELD_SIZE)]

    def append(self, i, j):
        self.field[i - 1][j - 1].is_live = True

    def generate(self, c):
        possible_places = set()
        last_place = (_CENTER_POSITION, _CENTER_POSITION)
        for _ in range(c):
            self.field[last_place[0]][last_place[1]].is_live = True
            for i in range(max(0, last_place[0] - 1), min(last_place[0] + 2, _FIELD_SIZE)):
                for j in range(max(0, last_place[1] - 1), min(last_place[1] + 2, _FIELD_SIZE)):
                    if int(self.field[i][j]) == 0:
                        possible_places.add((i, j))

            if (last_place[0], last_place[1]) in possible_places:
                possible_places.remove((last_place[0], last_place[1]))
            last_place = choice(list(possible_places))

    def field_transfer(self):
        for i in range(_FIELD_SIZE):
            if sum(int(j) for j in self.field[i]) > 0:
                self.top = i
                break
        for i in reversed(range(_FIELD_SIZE)):
            if sum(int(j) for j in self.field[i]) > 0:
                self.bot = i
                break
        for i in range(_FIELD_SIZE):
            if sum(int(self.field[k][i]) for k in range(_FIELD_SIZE)) > 0:
                self.left = i
                break
        for i in reversed(range(_FIELD_SIZE)):
            if sum(int(self.field[k][i]) for k in range(_FIELD_SIZE)) > 0:
                self.right = i
                break

    def find_neighbors(self):
        for i in range(_FIELD_SIZE):
            for j in range(_FIELD_SIZE):
                self.field[i][j].neighbors = [self.field[n][m] for n in range(max(0, i - 1), min(_FIELD_SIZE, i + 2))
                                              for m in range(max(0, j - 1), min(_FIELD_SIZE, j + 2))]
                self.field[i][j].neighbors.remove(self.field[i][j])

    def play(self):
        self.field_transfer()
        self.last_configuration = [(i, j) for i in range(_FIELD_SIZE) for j in range(_FIELD_SIZE)
                                   if self.field[i][j].is_live]
        print(self)
        self.find_neighbors()
        while self.last_configuration != [] and self.last_configuration not in self.configurations:
            self.step_counter += 1
            if not self.step_counter % 4:
                self.field_transfer()
                self.find_neighbors()
            self.configurations.append(self.last_configuration)
            sleep(_TIME_FOR_SLEEP)
            self.step()
        print('Game is over on step ' + str(self.step_counter))

    def step(self):
        for i in self.field:
            for j in i:
                j.count_neighbors()
        for i in self.field:
            for j in i:
                j.step()
        self.last_configuration = [(i, j) for i in range(_FIELD_SIZE) for j in range(_FIELD_SIZE)
                                   if self.field[i][j].is_live]
        print(self)

    def __str__(self):
        result = 'STEP ' + str(self.step_counter) + '\n\t'
        for i in range(max(0, self.left - 3), min(self.right + 4, _FIELD_SIZE)):
            result += '  ' + str(i + 1)
            if i < 9:
                result += ' '
        for i in range(max(0, self.top - 3), min(self.bot + 4, _FIELD_SIZE)):
            if i == 0:
                result += '\n\t' + ',---' + '+---' * (
                        min(self.right + 4, _FIELD_SIZE) - max(0, self.left - 3) - 1) + ',\n'
            else:
                result += '\n\t' + '!---' + '+---' * (
                        min(self.right + 4, _FIELD_SIZE) - max(0, self.left - 3) - 1) + '!\n'
            result += str(i + 1) + '\t' + '|'
            for j in range(max(0, self.left - 3), min(self.right + 4, _FIELD_SIZE)):
                result += str(self.field[i][j]) + '|'
        result += '\n\t' + '\'---' + '+---' * (
                min(self.right + 4, _FIELD_SIZE) - max(0, self.left - 3) - 1) + '\'\n'
        return result
