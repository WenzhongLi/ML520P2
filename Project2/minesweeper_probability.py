# coding : utf-8
#author : GE, Heng-Shao

import sys
import MineGenerator
import Queue
import collections
from itertools import product



class Node:
    def __init__(self, x, y, priority):
        self.x = x
        self.y = y
        self.priority = priority


class minesweeper_probability(object):
    def __init__(self):
        self.close = dict()   # inner boundary(has clue)
        self.frontier = collections.OrderedDict()  # outer boundary
        self.has_been_travelled = dict() #all cells that have been uncovered

    def __minesweeper_init(self, matrix, height, width):
        deltaX = [-1, 0, 1, -1, 1, -1, 0, 1]
        deltaY = [-1, -1, -1, 0, 0, 1, 1, 1]
        cell = [0,0]
        while True:
            # close --> save the point already visit
            clue = matrix[cell[0]][cell[1]]
            if clue == -1:
                print "Fail"
                break

            self.close[cell] = clue
            self.has_been_travelled[cell] = clue
            self.extend_surround(cell)
            if len(self.frontier) == 0:
                cell = [0][generator.width]
            else:
                cell = self.find_next(self.frontier,self.close)
                self.frontier.pop(cell)


    def find_next(self):
        length = len(self.frontier)
        q = Queue.Queue()
        for i in product(range(-1, 0), repeat=length):
            q.put(i)

        for (key, value) in self.close:
            #for every cell in frontier, set its value to possible number
            combination = q.pop()

            j = 0
            for (k,v) in self.frontier:
                self.frontier[k] = combination[j]
                j = j + 1

            deltaX = [-1, 0, 1, -1, 1, -1, 0, 1]
            deltaY = [-1, -1, -1, 0, 0, 1, 1, 1]
            sum = 0
            for i in range(0, 8):
                neighborNode = (self.key[0] + deltaX[i], self.key[1] + deltaY[i])
                if neighborNode[0] < 0 or neighborNode[1] < 0 or neighborNode[1] \
                        >= self.size or neighborNode[0] >= self.size:
                    continue
                if self.has_been_travelled.has_key(neighborNode):
                    continue
                if self.frontier.has_key(neighborNode):
                    sum += self.frontier.get(neighborNode)
            if sum != value:
                break




        next_cell = [1,1]
        return next_cell

    # discover the node's surrounding environment, and put into frontal
    def extend_surround(self, cell):
        deltaX = [-1,0,1,-1,1,-1,0,1]
        deltaY = [-1,-1,-1,0,0,1,1,1]

        # establish new nodes by changing the given node's coordinates in 4 directions
        possible = dict()
        for i in range(0, 8):
            neighborNode = (cell[0] + deltaX[i], cell[1] + deltaY[i])

            # check the boundary, if reach boundary --> continue
            if neighborNode[0] < 0 or neighborNode[1] < 0 or neighborNode[1] \
                    >= self.size or neighborNode[0] >= self.size:
                continue

            if self.has_been_travelled.has_key(neighborNode):
                continue

            possible[neighborNode] = -1

        if len(possible) ==  self.close.get(cell):
            self.has_been_travelled = dict(self.has_been_travelled.items() + possible.items())
        else:
            self.frontier = dict(self.frontier.items() + possible.items())


if __name__ == "__main__":
    print "script_name", sys.argv[0]
    for i in range(1, len(sys.argv)):
        print "argument", i, sys.argv[i]
    generator = MineGenerator.Generator(10, 10, 0.3)
    generator.print_matrix()
    generator.paint_random()
    generator.print_matrix()

    ms_prob = minesweeper_probability()
    ms_prob.minesweeper_init(generator.map_matrix, generator.height, generator.width)