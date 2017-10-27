# coding : utf-8
#author : GE, Heng-Shao

import sys
import MineGenerator
import Queue
import collections
from itertools import product


class minesweeper_probability(object):
    def __init__(self):
        self.close = dict()   # inner boundary(has clue)
        self.frontier = collections.OrderedDict()  # outer boundary
        self.has_been_travelled = dict() #all cells that have been uncovered
        self.matrix = generator.map_matrix
        self.width = 0
        self.height = 0

    def minesweeper_init(self, matrix, height, width):
        self.width = width
        self.height = height
        cell = (0,0)
        while True:
            debug = [[-5 for j in range(self.width)] for k in range(self.height)]
            clue = matrix[cell[0]][cell[1]]
            self.has_been_travelled[cell] = clue

            for i in range(0, self.width - 1):
                for j in range(0, self.height - 1):
                    if self.has_been_travelled.has_key((i,j)):
                        debug[i][j] = self.has_been_travelled.get((i,j))
            #print debug
            for i in range(self.height):
                for j in range(self.width):
                    print(debug[i][j]),
                print('\n'),
            print('\n')

            if clue == -1:
                print "Fail 1"
                return

            # close --> save the point already visit
            self.close[cell] = clue
            self.extend_surround(cell)
            if len(self.frontier) == 0:
                cell = (0,generator.width - 1)
            else:
                cell = self.find_next()
                self.frontier.pop(cell)

            if len(self.has_been_travelled) == self.height * self.width:
                break

        for i in range(0, self.height):
            for j in range(0,self.width):
                if matrix[i][j] != self.has_been_travelled.get((i,j)):
                    print "Fail 2"
                    return
        print "Success!"

    def find_next(self):
        length = len(self.frontier)
        q = Queue.Queue()
        valid_combinations = []
        for i in product(range(-1, 1), repeat=length):
            q.put(i)

        while not q.empty():
            combination = q.get()
            j = 0
            mark = 0

            for (k,v) in self.frontier.items():
                self.frontier[k] = combination[j]
                j = j + 1

            for (key, value) in self.close.items():
                #for every cell in frontier, set its value to possible number
                deltaX = [-1, 0, 1, -1, 1, -1, 0, 1]
                deltaY = [-1, -1, -1, 0, 0, 1, 1, 1]
                sum = 0

                for i in range(0, 8):
                    neighborNode = (key[0] + deltaX[i],key[1] + deltaY[i])
                    if neighborNode[0] < 0 or neighborNode[1] < 0 or neighborNode[1] \
                            >= self.height or neighborNode[0] >= self.width:
                        continue
                    if self.has_been_travelled.has_key(neighborNode):
                        continue
                    if self.frontier.has_key(neighborNode):
                        sum += self.frontier.get(neighborNode)

                if sum != value:
                    mark = 1
                    break
            if mark == 0:
                valid_combinations.append(combination)

        next_cell = (-1,-1)
        max_unlikely = 1

        for (k,v) in self.frontier.items():
            query_prob = 0
            e = 0
            for arr in valid_combinations:
                prob = 1
                if arr[e] == 0:
                    for j in range(0, len(arr)):
                        if(j != e and arr[j] == 0):
                            prob *= 1 - generator.density
                        if(arr[j] == -1):
                            prob *= generator.density

                query_prob += prob
                e = e + 1
            if max_unlikely > query_prob:
                max_unlikely = query_prob
                next_cell = k
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
                    >= self.height or neighborNode[0] >= self.width:
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
    generator = MineGenerator.Generator(3, 3, 0.2)
    generator.print_matrix()
    generator.paint_random()
    generator.print_matrix()

    ms_prob = minesweeper_probability()
    ms_prob.minesweeper_init(generator.map_matrix, generator.height, generator.width)