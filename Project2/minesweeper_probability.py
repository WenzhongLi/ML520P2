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

    def __minesweeper_init(self, matrix, height, width):
        self.close[[0,0]] = matrix[0][0]
        while True:
            cell = [0,0]
            self.extend_surround(cell)




    # discover the node's surrounding environment
    def extend_surround(self, q):
        xs = [-1,0,1,-1,1,-1,0,1]
        ys = [-1,-1,-1,0,0,1,1,1]
        open_size = 0
        # establish new nodes by changing the given node's coordinates in 4 directions
        for xx, yy in zip(xs,ys):
            new_x,  new_y = xx + q.x, yy + q.y

            #judge if the new node is valid, a valid node means the node is inside the bound and it isn't a block
            if not self.is_valid(new_x, new_y):
                continue

            node = Node(q, new_x, new_y, q.distance + 1)
            if self.close.has_key((node.x, node.y)):
                continue

            if self.open.has_key((node.x, node.y)):
                if self.open.get((node.x, node.y)).distance > node.distance:
                    self.open[(node.x, node.y)] = node
                continue
            self.open[(node.x, node.y)] = node

        if open_size < len(self.open):
            open_size = len(self.open)
        return open_size

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