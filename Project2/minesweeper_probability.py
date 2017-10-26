# coding : utf-8
#author : GE, Heng-Shao

import sys
import MineGenerator
import Queue

class Node:
    def __init__(self, x, y, priority):
        self.x = x
        self.y = y
        self.priority = priority


class minesweeper_probability(object):
    def __init__(self):
        self.close = dict()
        self.frontier = dict()

    def __minesweeper_init(self, matrix, height, width):
        cell = [0,0]

        while True:
            # close --> save the point already visit
            clue = matrix[cell[0]][cell[1]]
            if clue == -1:
                print "Fail"
                break

            self.close[cell] = clue
            self.extend_surround(cell)
            cell = find_next(self.frontier,self.close)
            self.frontier.pop(cell)


    def find_next(self, frontier):

        return next_cell

    # discover the node's surrounding environment, and put into frontal
    def extend_surround(self, cell):
        deltaX = [-1,0,1,-1,1,-1,0,1]
        deltaY = [-1,-1,-1,0,0,1,1,1]

        # establish new nodes by changing the given node's coordinates in 4 directions
        for i in range(0, 8):
            neighborNode = (cell[0] + deltaX[i], cell[1] + deltaY[i])

            # check the boundary, if reach boundary --> continue
            if neighborNode[0] < 0 or neighborNode[1] < 0 or neighborNode[1] \
                    >= self.size or neighborNode[0] >= self.size:
                continue

            if self.frontier.has_key(neighborNode)
                continue

            self.frontier[neighborNode]


if __name__ == "__main__":
    print "script_name", sys.argv[0]
    for i in range(1, len(sys.argv)):
        print "argument", i, sys.argv[i]
    generator = MineGenerator.Generator(10, 15, 0.3)
    generator.print_matrix()
    generator.paint_random()
    generator.print_matrix()

    ms_prob = minesweeper_probability()
    ms_prob.minesweeper_init(generator.map_matrix, generator.height, generator.width)