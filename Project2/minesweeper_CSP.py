'''
@author: Juntao Tan
'''


import MineGenerator
import random
import copy
import itertools

def printmap(matrix, a):
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if (matrix[i][j] == -1):
                if a == 0:
                    print 'x',
                if a == 1:
                    print 'P',
            elif (matrix[i][j] == -2):
                print '?',
            else:
                print (matrix[i][j]),
        print ('\n'),
    print '\n'

def print_kb(tree):
    print tree[0]
    # print level1
    for i in range(1,len(tree)):
        print tree[i][0],
        print '    ',
    print '\n',
    # print level 2
    for i in range(1,len(tree)):
        for j in range(1, len(tree[i])):
            print tree[i][j][0],
        print '  ',
    print '\n',
    # print level 3
    for i in range(1, len(tree)):
        for j in range(1, len(tree[i])):
            for k in range(1, len(tree[i][j])):
                print tree[i][j][k],
            print ' ',
        print '        ',
    print '\n',

class MineSweeper(object):
    def __init__(self):
        self.height = 0
        self.width = 0
        self.map = None # real map
        self.current_map = None # current updated map
        self.current_block = None
        self.block_to_be_analysis = []
        self.block_to_be_check = []
        self.block_to_be_uncover = []
        self.block_unchecked = None
        self.KB = ['c', ]

    def solve(self):
        self.block_to_be_uncover.append([random.randint(0, self.height - 1), random.randint(0, self.width - 1)])
        for i in range(0, len(self.block_to_be_uncover)):
            self.uncover_block(self.block_to_be_uncover[i])
        printmap(self.current_map, 1)
        #print 'Block to be analysis', self.block_to_be_analysis
        while (1):
            self.analysis()
            self.search()
            for i in range(0, len(self.block_to_be_uncover)):
                self.uncover_block(self.block_to_be_uncover[i])
            all_value_in_current_map = []
            for i in range(len(self.current_map)):
                for j in range(len(self.current_map[i])):
                    all_value_in_current_map.append(copy.copy(self.current_map[i][j]))
            if -2 not in all_value_in_current_map:
                printmap(self.current_map, 1)
                print 'finish!!!!!!!'
                exit()



        #self.analysis()    # generate KB

    def get_map(self, matrix):
        self.map = copy.deepcopy(matrix)
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.current_map = [[-2 for i in range(self.width)] for i in range(self.height)]

    def uncover_block(self, block):
        # print 'uncover block', block
        if self.map[block[0]][block[1]] == -1:
            print block
            print 'fail'
            #exit()
        elif self.map[block[0]][block[1]] == 0:
            self.current_map[block[0]][block[1]] = copy.copy(self.map[block[0]][block[1]])
            around_block = self.get_around_block(block)
            for i in range(0, len(around_block)):
                self.uncover_block(around_block[i])
        else:
            if block not in self.block_to_be_analysis:
                self.block_to_be_analysis.append(copy.copy(block))
            around_block = self.get_around_block(block)
            for i in range(0, len(around_block)):
                if around_block[i] not in self.block_to_be_check:
                    self.block_to_be_check.append(copy.copy(around_block[i]))
        self.current_map[block[0]][block[1]] = copy.copy(self.map[block[0]][block[1]])
        # print 'temp_block_to_be_check', self.temp_block_to_be_check

    # for a block, find the around block which is -2(not uncover)
    def get_around_block(self, block):
        around_block =[]
        if (0 <= block[0] - 1 < self.height and 0 <= block[1]-1 < self.width and self.current_map[block[0]-1][block[1]-1] == -2):
            around_block.append([block[0] - 1, block[1] - 1])
        if (0 <= block[0] - 1 < self.height and 0 <= block[1] < self.width and self.current_map[block[0]-1][block[1]] == -2):
            around_block.append([block[0] - 1, block[1]])
        if (0 <= block[0] - 1 < self.height and 0 <= block[1]+1 < self.width and self.current_map[block[0]-1][block[1]+1] == -2):
            around_block.append([block[0] - 1, block[1] + 1])

        if (0 <= block[0] < self.height and 0 <= block[1]-1 < self.width and self.current_map[block[0]][block[1]-1] == -2):
            around_block.append([block[0], block[1] - 1])
        if (0 <= block[0] < self.height and 0 <= block[1] +1 < self.width and self.current_map[block[0]][block[1]+1] == -2):
            around_block.append([block[0], block[1] + 1])

        if (0 <= block[0]+1 < self.height and 0 <= block[1]-1 < self.width and self.current_map[block[0]+1][block[1]-1] == -2):
            around_block.append([block[0]+1, block[1] - 1])
        if (0 <= block[0]+1 < self.height and 0 <= block[1] < self.width and self.current_map[block[0]+1][block[1]] == -2):
            around_block.append([block[0]+1, block[1]])
        if (0 <= block[0]+1 < self.height and 0 <= block[1]+1 < self.width and self.current_map[block[0]+1][block[1]+1] == -2):
            around_block.append([block[0]+1, block[1] + 1])
        return around_block

    # analysis a block , add the new information to KB
    def analysis(self):
        self.update_block_to_be_analysis()
        for block in self.block_to_be_analysis:
            # print 'block', block

            self.KB.append(['d'])    # each time analysis a block, and a 'V' branch to 2ed level
            around = self.get_around_block(block)
            count_mines_already_shown = 0

            if (0 <= block[0] - 1 < self.height and 0 <= block[1] - 1 < self.width and self.current_map[block[0] - 1][
                    block[1] - 1] != -2):
                if self.current_map[block[0] - 1][block[1] - 1] == -1:
                    count_mines_already_shown += 1
            if (0 <= block[0] - 1 < self.height and 0 <= block[1] < self.width and self.current_map[block[0] - 1][
                block[1]] != -2):
                if self.current_map[block[0] - 1][block[1]] == -1:
                    count_mines_already_shown += 1
            if (0 <= block[0] - 1 < self.height and 0 <= block[1] + 1 < self.width and self.current_map[block[0] - 1][
                    block[1] + 1] == -2):
                if self.current_map[block[0] - 1][block[1] + 1] == -1:
                    count_mines_already_shown += 1
            if (0 <= block[0] < self.height and 0 <= block[1] - 1 < self.width and self.current_map[block[0]][
                    block[1] - 1] == -2):
                if self.current_map[block[0]][block[1] - 1] == -1:
                    count_mines_already_shown += 1
            if (0 <= block[0] < self.height and 0 <= block[1] + 1 < self.width and self.current_map[block[0]][
                    block[1] + 1] == -2):
                if self.current_map[block[0]][block[1] + 1] == -1:
                    count_mines_already_shown += 1
            if (0 <= block[0] + 1 < self.height and 0 <= block[1] - 1 < self.width and self.current_map[block[0] + 1][
                    block[1] - 1] == -2):
                if self.current_map[block[0] + 1][block[1] - 1]  == -1:
                    count_mines_already_shown += 1
            if (0 <= block[0] + 1 < self.height and 0 <= block[1] < self.width and self.current_map[block[0] + 1][
                block[1]] == -2):
                if self.current_map[block[0] + 1][block[1]]  == -1:
                    count_mines_already_shown += 1
            if (0 <= block[0] + 1 < self.height and 0 <= block[1] + 1 < self.width and self.current_map[block[0] + 1][
                    block[1] + 1] == -2):
                if self.current_map[block[0] + 1][block[1] + 1]  == -1:
                    count_mines_already_shown += 1
            comb = list(itertools.combinations(around, self.map[block[0]][block[1]]-count_mines_already_shown))

            append_position_3 = len(self.KB) - 1   # where to insert the branch at 3rd level
            for i in range(0, len(comb)):
                self.KB[append_position_3].append(['c'])  # for each combination add a 'C' to 3rd level
                append_position_4 = len(self.KB[append_position_3]) - 1
                for j in range(0, len(around)):   # for each block to be check(around), add it to 4th level
                    if around[j] in comb[i]:
                        self.KB[append_position_3][append_position_4].append([around[j][0], around[j][1], 1])
                    else:
                        self.KB[append_position_3][append_position_4].append([around[j][0], around[j][1], 0])
        #print 'length of level 3', len(self.KB[1])

    def update_block_to_be_check(self):
        temp_block_to_be_check = copy.deepcopy(self.block_to_be_check)
        self.block_to_be_check = []
        for i in temp_block_to_be_check:
            if self.current_map[i[0]][i[1]] == -2:
                self.block_to_be_check.append(copy.copy(i))

    def update_block_to_be_analysis(self):
        temp_block_to_be_analysis = copy.deepcopy(self.block_to_be_analysis)
        self.block_to_be_analysis = []
        for i in range(len(temp_block_to_be_analysis)):
            # print 'temp_block_to_be_analysis[i]', temp_block_to_be_analysis[i]
            around = self.get_around_block(temp_block_to_be_analysis[i])
            if len(around) != 0:
                self.block_to_be_analysis.append(copy.copy(temp_block_to_be_analysis[i]))

    # use all combinations generate by block_to_be_analysis, use it to search the KB
    def search(self):
        printmap(self.current_map, 1)
        truth_table = []  # reserve suitable combination
        value_table = []  # compare truth table reserve the certain value
        # generate block_to_be_check delete the block which are already uncovered
        self.update_block_to_be_check()
        # print self.block_to_be_check

        search_com = []
        # for the block to be check, generate every combination
        for i in (itertools.product(range(2), repeat=len(self.block_to_be_check))):
            temp = copy.deepcopy(self.block_to_be_check)
            for j in range(len(self.block_to_be_check)):
                temp[j].append(i[j])
            search_com.append(temp)

        # for each combination, search KB and delete the branches not suitable. If it's a solution, add to truth table
        for i in range(len(search_com)):
            temp_KB = copy.deepcopy(self.KB)
            for j in range(len(search_com[i])):
                opposite_search_block = copy.copy(search_com[i][j])  # opposite to search block. if exist in the branch , not suitable
                if opposite_search_block[2] == 0:
                    opposite_search_block[2] = 1
                else:
                    opposite_search_block[2] = 0
                for k in range(1, len(temp_KB)):
                    for l in range(1, len(temp_KB[k])):
                        if temp_KB[k][l][1] != 'n':
                            if opposite_search_block in temp_KB[k][l]:
                                temp_KB[k][l].insert(1, 'n')
            # To see this KB can not be a solution
            for m in range(1, len(temp_KB)):
                count = 0
                for n in range(1, len(temp_KB[m])):
                    if temp_KB[m][n][1] != 'n':
                        count = 1
                if count == 0:
                    break
                if m == len(temp_KB) - 1:
                    truth_table.append(copy.deepcopy(search_com[i]))
        #print 'truth table', truth_table
        for i in range(len(self.block_to_be_check)):
            if_0 = 0  # see if this block has value 0 in the truth table
            if_1 = 0  # see if this block has value 1 in the truth table
            for j in range(len(truth_table)):
                #print truth_table[j][i]
                if truth_table[j][i][2] == 0:
                    if_0 = 1
                if truth_table[j][i][2] == 1:
                    if_1 = 1
            if if_0 != if_1:
                value_table.append(copy.copy(truth_table[0][i]))
        #print value_table
        temp = []
        self.block_to_be_uncover = []
        if len(value_table) == 0:        # if no new information. over
            printmap(self.current_map, 1)
            print 'No solution, pick up a new block'
            #exit()
            self.block_to_be_check = []
            for i in range(len(self.current_map)):
                for j in range(len(self.current_map[i])):
                    if self.current_map[i][j] == -2:
                        temp.append([i, j])
            self.block_to_be_uncover.append(copy.copy(temp[0]))
            print self.block_to_be_uncover



        for i in range(len(value_table)):
            if value_table[i][2] == 0:
                self.block_to_be_uncover.append([value_table[i][0], value_table[i][1]])
            else:
                self.current_map[value_table[i][0]][value_table[i][1]] = -1
        printmap(self.current_map, 1)


if __name__ == "__main__":
    minesweeper = MineSweeper()
    map_ = MineGenerator.Generator(8, 8, 0.2)
    map_.paint_random()
    minesweeper.get_map(map_.map_matrix)
    printmap(minesweeper.map, 0)
    minesweeper.solve()





