#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
@author: li
'''

import copy
import random
import sys
import MineGenerator_PB


class MineSweeper(object):
    def __init__(self):
        self.height = 0
        self.weight = 0
        self.map = None
        self.moves = None
        self.node_to_be_check = None
        self.node_to_be_check_index = -1
        self.node_unchecked = None
        self.node_state = None
        self.node_to_analysis = None
        #

    def solve(self, mine_map, height, weight):
        removed_list = []
        self.moves = []
        self.height = height
        self.weight = weight
        self.map = mine_map
        self.node_to_be_check = []
        # self.node_to_be_check_index = -1
        self.node_unchecked = []
        self.node_state = dict()
        self.node_to_analysis = dict()
        for h in range(self.height):
            for w in range(self.weight):
                self.node_unchecked.append((h, w))
                self.node_state[(h, w)] = -2  # have not checked
        # get a start node
        current_node = copy.copy(random.choice(self.node_unchecked))
        while self.map[current_node[0]][current_node[1]] == -1:
            current_node = random.choice(self.node_unchecked)
        # maybe remove this later
        # self.node_unchecked.remove(current_node)
        self.node_to_be_check.append(current_node)
        # self.node_to_be_check_index += 1
        # Start search
        # timer = 0
        random_time = 0
        while len(self.node_unchecked) > 0:
            # timer += 1
            # print timer, removed_list
            if len(self.node_to_be_check) == 0:
                # Get a point randomly TODO
                current_node = copy.copy(random.choice(self.node_unchecked))
                self.node_state[current_node] = -3
                self.node_to_be_check.append(current_node)
                random_time += 1
                print 'random', current_node, random_time
            print 'self.node_to_be_check', self.node_to_be_check
            for node in self.node_to_be_check:
                if self.map[node[0]][node[1]] == -1:
                    # bomb!! gg =,=
                    self.node_state[current_node] = '!'
                    self.print_current()
                    self.moves.append(node)
                    return 0, self.moves
                else:
                    self.node_state[node] = self.map[node[0]][node[1]]
                    if self.node_state[node] != -4:
                        self.add_around(node)
                    self.moves.append(node)
                    removed_list.append(node)
                    # print node, self.node_unchecked
                    self.node_unchecked.remove(node)
            while 1:
                self.print_current()
                self.node_to_be_check = []
                # add current node to list
                remove_list = []
                print 'self.node_to_analysis', self.node_to_analysis
                for node in self.node_to_analysis:
                    if self.node_state[node] != -2:
                        remove_list.append(node)
                        continue
                    # check around satisfy -> blank
                    # check around that remain one satisfy -> mine
                    # check sub-set for mine
                    # check sub-set for blank
                    result = self.analysis_point(node)
                    if result[0] == 1:
                        remove_list.append(node)
                        # self.node_to_analysis.pop(node)
                        if self.node_state[node] != -2:
                            continue
                        if result[1] is True:
                            self.node_state[node] = -1
                            removed_list.append(node)
                            # print node, self.node_unchecked
                            self.node_unchecked.remove(node)
                        else:
                            self.node_state[node] = -3
                            self.node_to_be_check.append(node)
                for node_need_remove in remove_list:
                    self.node_to_analysis.pop(node_need_remove)
                if len(self.node_to_be_check) == 0:
                    r = self.sub_set_analysis()
                    for node_need_remove in r[1]:
                        self.node_to_analysis.pop(node_need_remove)
                    if len(self.node_to_be_check) != 0:
                        break
                    if r[0] is True:
                        continue
                    else:
                        break
                else:
                    break
        self.print_current()
        return 1, copy.deepcopy(self.moves)

    def add_around(self, point):
        # add around node to the node_to_analysis
        direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for direction in direction_list:
            if (0 <= point[1] + direction[1] < self.weight) and (0 <= point[0] + direction[0] < self.height):
                if self.node_state[(point[0] + direction[0], point[1] + direction[1])] == -2:
                    # add to list
                    self.node_to_analysis[(point[0] + direction[0], point[1] + direction[1])] = 1
            else:
                continue
        return self.map[point[0]][point[1]]

    def analysis_point(self, point):
        # check sub-set for mine
        # check sub-set for blank
        direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for direction in direction_list:
            if (0 <= point[1] + direction[1] < self.weight) and (0 <= point[0] + direction[0] < self.height):
                current = (point[0] + direction[0], point[1] + direction[1])
                mine_count = self.node_state[current]
                if mine_count == -1 or mine_count == -3 or mine_count == -4:
                    continue
                if mine_count == 0:
                    return 1, False
                # check around satisfy -> blank
                # check around that remain satisfy -> mine
                current_mine_count = 0
                current_not_mine_count = 0
                for d in direction_list:
                    if (0 <= current[1] + d[1] < self.weight) and (0 <= current[0] + d[0] < self.height):
                        c = (current[0] + d[0], current[1] + d[1])
                        m = self.node_state[c]
                        if m == -1:
                            current_mine_count += 1
                        elif m >= 0 or m == -4:
                            current_not_mine_count += 1
                    else:
                        current_not_mine_count += 1
                if current_mine_count == mine_count:
                    # not a mine
                    return 1, False
                if current_not_mine_count == 8 - mine_count:
                    # is mine
                    return 1, True
            else:
                continue
        return 0, None

    def sub_set_analysis(self):
        # check sub-set for mine
        # check sub-set for blank
        analysis_list = set()
        set_compare = dict()
        remove_list = []
        for point in self.node_to_analysis:
            direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
            for direction in direction_list:
                if (0 <= point[1] + direction[1] < self.weight) and (0 <= point[0] + direction[0] < self.height):
                    current = (point[0] + direction[0], point[1] + direction[1])
                    mine_count = self.node_state[current]
                    if mine_count == -1 or mine_count == -2 or mine_count == -3 or mine_count == -4:
                        continue
                    # check sub-set for mine
                    # check sub-set for blank
                    if mine_count == 0:
                        print current, 'error'
                    analysis_list.add(current)
        for node in analysis_list:
            tmp = self.add_set(node)
            if tmp:
                set_compare[tmp[0]] = tmp[1]
            direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1),
                              (2, 0), (2, 1), (2, 2), (1, 2), (0, 2), (-1, 2), (-2, 2), (-2, 1),
                              (-2, 0), (-2, -1), (-2, -2), (-1, -2), (0, -2), (1, -2), (2, -2), (2, -1)]
            for d in direction_list:
                if (0 <= node[1] + d[1] < self.weight) and (0 <= node[0] + d[0] < self.height):
                    c = (node[0] + d[0], node[1] + d[1])
                    m = self.node_state[c]
                    if m <= 0:
                        continue
                    elif m >= 0:
                        tmp = self.add_set(node)
                        if tmp:
                            set_compare[tmp[0]] = tmp[1]
            new_set_map = dict()
            old_size = len(set_compare)
            new_size = 0
            while old_size != new_size:
                old_size = len(set_compare)
                for mine_set1 in set_compare:
                    for mine_set2 in set_compare:
                        set1 = set(mine_set1)
                        set2 = set(mine_set2)
                        set12 = set1 - set2
                        set21 = set2 - set1
                        if len(set12) * len(set21) != 0:
                            # continue
                            # if no intersection then no brother
                            if len(set1 & set2) == 0:
                                continue
                            # to check this
                            # ?
                            # p 2 2 3
                            intersection = set1 & set2
                            min_mines_in_intersection1 = set_compare[mine_set1]\
                                - (len(set1) - len(intersection))
                            min_mines_in_intersection2 = set_compare[mine_set2] \
                                - (len(set2) - len(intersection))
                            min_mines_in_intersection = max(min_mines_in_intersection1, min_mines_in_intersection2)
                            if min_mines_in_intersection <= 0:
                                continue
                            elif min_mines_in_intersection == set_compare[mine_set1]:
                                # set1-set2 is blank
                                for new_point_to_check in set12:
                                    if new_point_to_check not in self.node_to_be_check:
                                        self.node_state[new_point_to_check] = -3
                                        self.node_to_be_check.append(new_point_to_check)
                                        remove_list.append(new_point_to_check)
                                return False, remove_list
                            elif min_mines_in_intersection == set_compare[mine_set2]:
                                # set2-set1 is blank
                                for new_point_to_check in set21:
                                    if new_point_to_check not in self.node_to_be_check:
                                        self.node_state[new_point_to_check] = -3
                                        self.node_to_be_check.append(new_point_to_check)
                                        remove_list.append(new_point_to_check)
                                return False, remove_list
                            #   p p
                            #   3 3
                            #   2 1
                            # ? 1 0
                            # to conclude this
                            max_mines_in_intersection = min(set_compare[mine_set1], set_compare[mine_set2])
                            if set_compare[mine_set1] - max_mines_in_intersection > 0 and \
                                    len(set12) == (set_compare[mine_set1] - max_mines_in_intersection):
                                # all set1 - set2 are mine
                                for new_mine_found in set12:
                                    self.node_state[new_mine_found] = -1
                                    self.node_unchecked.remove(new_mine_found)
                                    remove_list.append(new_mine_found)
                                return True, remove_list
                            elif set_compare[mine_set2] - max_mines_in_intersection > 0 and \
                                    len(set21) == (set_compare[mine_set2] - max_mines_in_intersection):
                                # all set2 - set1 are mine
                                for new_mine_found in set21:
                                    self.node_state[new_mine_found] = -1
                                    self.node_unchecked.remove(new_mine_found)
                                    remove_list.append(new_mine_found)
                                return True, remove_list
                            continue
                        elif len(set12) + len(set21) == 0:
                            # same set
                            continue
                        elif len(set21) != 0:
                            new_set_mine_count = set_compare[mine_set2] - set_compare[mine_set1]
                            if new_set_mine_count < 0:
                                print 'error ', mine_set2, set_compare[mine_set2], \
                                    mine_set1, set_compare[mine_set1]
                            elif new_set_mine_count == 0:
                                # all point in the tup are blank
                                for new_point_to_check in set21:
                                    if new_point_to_check not in self.node_to_be_check:
                                        self.node_state[new_point_to_check] = -3
                                        self.node_to_be_check.append(new_point_to_check)
                                        remove_list.append(new_point_to_check)
                                return False, remove_list
                            elif new_set_mine_count == len(set21):
                                # all point in the tup are mines
                                for new_found_mine in set21:
                                    self.node_state[new_found_mine] = -1
                                    # print 'remove', new_found_mine, mine_set2, set_compare[mine_set2], \
                                    #    mine_set1, set_compare[mine_set1]
                                    self.node_unchecked.remove(new_found_mine)
                                    remove_list.append(new_found_mine)
                                return True, remove_list
                            else:
                                tp = ()
                                for e in set21:
                                    tp = tp + (e,)
                                new_set_map[tp] = new_set_mine_count
                        elif len(set12) != 0:
                            new_set_mine_count = set_compare[mine_set1] - set_compare[mine_set2]
                            if new_set_mine_count < 0:
                                print 'error ', mine_set1, set_compare[mine_set1], \
                                    mine_set2, set_compare[mine_set2]
                            elif new_set_mine_count == 0:
                                # all point in the tup are blank
                                for new_point_to_check in set12:
                                    if new_point_to_check not in self.node_to_be_check:
                                        self.node_state[new_point_to_check] = -3
                                        self.node_to_be_check.append(new_point_to_check)
                                        remove_list.append(new_point_to_check)
                                return False, remove_list
                            elif new_set_mine_count == len(set12):
                                # all point in the tup are mines
                                for new_found_mine in set12:
                                    self.node_state[new_found_mine] = -1
                                    print 'remove', new_found_mine, mine_set2, set_compare[mine_set2], \
                                        mine_set1, set_compare[mine_set1]
                                    self.node_unchecked.remove(new_found_mine)
                                    remove_list.append(new_found_mine)
                                return True, remove_list
                            else:
                                tp = ()
                                for e in set12:
                                    tp = tp + (e,)
                                new_set_map[tp] = new_set_mine_count
                for key in new_set_map:
                    set_compare[key] = new_set_map[key]
                new_set_map = dict()
                new_size = len(set_compare)
        return False, remove_list

    def add_set(self, point):
        mine_count = self.node_state[point]
        blank_tup = ()
        if mine_count <= 0:
            print 'add_set error', mine_count
        current_mine_count = 0
        current_not_mine_count = 0
        direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        for d in direction_list:
            if (0 <= point[1] + d[1] < self.weight) and (0 <= point[0] + d[0] < self.height):
                c = (point[0] + d[0], point[1] + d[1])
                m = self.node_state[c]
                if m == -1:
                    current_mine_count += 1
                elif m >= 0 or m == -4:
                    current_not_mine_count += 1
                else:
                    blank_tup = blank_tup + (c,)
            else:
                current_not_mine_count += 1
        # if current_mine_count == mine_count or current_not_mine_count == 8 - mine_count:
        #    print 'error, should find in above', point
        if len(blank_tup) == 0:
            return None
        else:
            return blank_tup, mine_count - current_mine_count

    def print_current(self):
        for h in range(self.height):
            for w in range(self.weight):
                sf = ''
                if (h, w) in self.node_to_analysis:
                    sf = '\033[1;35m\033[0m'
                else:
                    sf = '\033[0m'
                if self.node_state[(h, w)] == -1:
                    print sf+'p',
                elif self.node_state[(h, w)] == -2 or self.node_state[(h, w)] == -3:
                    print sf+'_',
                elif self.node_state[(h, w)] == -4:
                    print sf+'B',
                elif self.node_state[(h, w)] >= 0:
                    print sf+str(self.node_state[(h, w)]),
                else:
                    print "error", self.node_state[(h, w)]
            print '\n',
        print '\033[0m',

if __name__ == "__main__":
    print "script_name", sys.argv[0]
    for i in range(1, len(sys.argv)):
        print "argment", i, sys.argv[i]
    print ('start initialize')
    # set the size and density of this matrix
    height = 16
    weight = 30
    generator = MineGenerator_PB.Generator(height, weight, 0.13, 0.13)
    # generator.print_matrix()
    generator.paint_random()
    generator.print_matrix()
    player = MineSweeper()
    result = player.solve(generator.get_matrix(), height, weight)
    print result
    print ('start over')
