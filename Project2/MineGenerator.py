#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author: li
'''
import random
import sys


class Generator(object):
    # init size and density of map
    def __init__(self, height, weight, density):
        self.height = height
        self.weight = weight
        self.density = density
        self.map_matrix = []
        for k in range(self.height):
            self.map_matrix.append([])
            for j in range(self.weight):
                self.map_matrix[k].append(0)

    # print map to commend line
    def print_matrix(self):
        count_blocked = 0
        for k in range(self.height):
            for j in range(self.weight):
                if self.map_matrix[k][j] == -1:
                    print 'x',
                else:
                    print(self.map_matrix[k][j]),
                if self.map_matrix[k][j] == -1:
                    count_blocked += 1
            print('\n'),
        print(str(count_blocked)+" are mines\n")

    # paint maze randomly
    def paint_random(self):
        matrix = [[0 for j in range(self.weight)] for k in range(self.height)]
        node_list = []
        # init a set of all point could be block
        for k in range(self.height):
            for j in range(self.weight):
                node_list.append((k, j))
        mine_num = int(self.height * self.weight * self.density)
        if mine_num > self.height * self.weight:
            mine_num = self.height * self.weight
        # get some point randomly
        mine_set = random.sample(node_list, mine_num)
        # Paint them 1
        direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for node in mine_set:
            matrix[node[0]][node[1]] = -1
        for k in range(self.height):
            for j in range(self.weight):
                if matrix[k][j] == -1:
                    continue
                count_mines_around = 0
                for direction in direction_list:
                    if (0 <= j+direction[0] < self.weight) and (0 <= k+direction[1] < self.height):
                        if matrix[k+direction[1]][j+direction[0]] == -1:
                            count_mines_around += 1
                    else:
                        continue
                matrix[k][j] = count_mines_around
        self.map_matrix = matrix
        return matrix

    def get_matrix(self):
        return self.map_matrix


if __name__ == "__main__":
    print "script_name", sys.argv[0]
    for i in range(1, len(sys.argv)):
        print "argment", i, sys.argv[i]
    print ('start initialize')
    # set the size and density of this matrix
    generator = Generator(10, 15, 0.3)
    generator.print_matrix()
    generator.paint_random()
    generator.print_matrix()
    print ('start over')