#
#   Filename:   homework1.py
#   Date:       09/28/2021
#   Author:     James Anyabine
#   Email:      joa170000@utdallas.edu
#   Version:    1.0
#   Copyright:  2021, All Rights Reserved

#   Description:
#   
#

import sys
import argparse
import time
import timeit
import math
from collections import deque

#Global Variables 
goalState = [1, 2, 3, 4, 0, 5, 6, 7, 8]
goalNode = None 
maxDepth = 0
maxFrontier = 0
nodesExpanded = 0


class GridState:
    def __init__(self, state, parent, move, depth, cost, key):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth 
        self.cost = cost
        self.key = key
        if self.state:
            self.map = ''.join(str(i) for i in self.state)
    def __eq__(self, other):
        return self.map == other.map
    def __lt__(self, other):
        return self.map < other.map
    def __str__(self):
        return str(self.map)


 
intialState = []

def list_to_grid(list):
    """
    Turns the 1D input list and returns it as a two dimensional representation 
    [1, 2, 3, 4, 0, 5, 6, 7, 8] --> [[1, 2, 3],[4, 0 ,5],[6, 7, 8]]
    """
    sqroot = int(math.sqrt(len(list)))
    grid = []

    for i in range(0, len(list), sqroot):
        line = []
        for j in range(0, sqroot):
            line.append(list[i+j])
        grid.append(line)

    return grid


#This function is what swaps the positions of the list values depending on
# the position of 0 (the blank tile).
def move(state, direction):
    #Make a safe copy of the Node state
    copyState = state[:]

    #find where 0 (aka the blank tile) is
    index = copyState.index(0)

    if(index == 0):
        if(direction == 1):
            return None 
        if(direction == 2):
            temp = copyState[0]
            copyState[0] = copyState[3]
            copyState[3] = temp
        if(direction == 3):
            return None
        if(direction == 4):
            temp = copyState[0]
            copyState[0] = copyState[1]
            copyState[1] = temp
        return copyState
    if(index == 1):
        if(direction == 1):
            return None 
        if(direction == 2):
            temp = copyState[1]
            copyState[1] = copyState[4]
            copyState[4] = temp
        if(direction == 3):
            temp = copyState[1]
            copyState[1] = copyState[0]
            copyState[0] = temp
        if(direction == 4):
            temp = copyState[1]
            copyState[1] = copyState[2]
            copyState[2] = temp
        return copyState
    if(index == 2):
        if(direction == 1):
            return None 
        if(direction == 2):
            temp = copyState[2]
            copyState[2] = copyState[5]
            copyState[5] = temp
        if(direction == 3):
            temp = copyState[2]
            copyState[2] = copyState[1]
            copyState[1] = temp
        if(direction == 4):
           return None
        return copyState
    if(index == 3):
        if(direction == 1):
            temp = copyState[3]
            copyState[3] = copyState[0]
            copyState[0] = temp
        if(direction == 2):
            temp = copyState[3]
            copyState[3] = copyState[6]
            copyState[6] = temp
        if(direction == 3):
            return None
        if(direction == 4):
            temp = copyState[3]
            copyState[3] = copyState[4]
            copyState[4] = temp
        return copyState
    if(index == 4):
        if(direction == 1):
            temp = copyState[4]
            copyState[4] = copyState[1]
            copyState[1] = temp
        if(direction == 2):
            temp = copyState[4]
            copyState[4] = copyState[7]
            copyState[7] = temp
        if(direction == 3):
            temp = copyState[4]
            copyState[4] = copyState[3]
            copyState[3] = temp
        if(direction == 4):
            temp = copyState[4]
            copyState[4] = copyState[5]
            copyState[5] = temp
        return copyState
    if(index == 5):
        if(direction == 1):
            temp = copyState[5]
            copyState[5] = copyState[2]
            copyState[2] = temp
        if(direction == 2):
            temp = copyState[5]
            copyState[5] = copyState[8]
            copyState[8] = temp
        if(direction == 3):
            temp = copyState[5]
            copyState[5] = copyState[4]
            copyState[4] = temp
        if(direction == 4):
            return None
        return copyState
    if(index == 6):
        if(direction == 1):
            temp = copyState[6]
            copyState[6] = copyState[3]
            copyState[3] = temp
        if(direction == 2):
            return None
        if(direction == 3):
            return None
        if(direction == 4):
            temp = copyState[6]
            copyState[6] = copyState[7]
            copyState[7] = temp
        return copyState
    if(index == 7):
        if(direction == 1):
            temp = copyState[7]
            copyState[7] = copyState[4]
            copyState[4] = temp
        if(direction == 2):
            return None
        if(direction == 3):
            temp = copyState[7]
            copyState[7] = copyState[6]
            copyState[6] = temp
        if(direction == 4):
            temp = copyState[7]
            copyState[7] = copyState[8]
            copyState[8] = temp
        return copyState
    if(index == 8):
        if(direction == 1):
            temp = copyState[8]
            copyState[8] = copyState[5]
            copyState[5] = temp
        if(direction == 2):
            return None
        if(direction == 3):
            temp = copyState[8]
            copyState[8] = copyState[7]
            copyState[7] = temp
        if(direction == 4):
            return None
        return copyState
#-----------------------------------------------------------------------------------



goalMatrix = list_to_grid(goalState)


def otherNodes(node):

    global nodesExpanded
    nodesExpanded = nodesExpanded + 1

    futurePath = []
    for i in range (1, 5):
        futurePath.append(GridState(move(node.state, i), node, 1, node.depth + 1, node.cost+1, 0))
        #Need to complete otherNodes Function
    nodes = []
    for paths in futurePath:
        if(paths.state != None):
            nodes.append(paths)
    return nodes


def dfs(initalNode):

    global maxFrontier, goalNode, maxDepth

    visited = set()
    stack = list([GridState(intialState, None, None, 0 , 0, 0)])
    while stack:
        node = stack.pop()
        visited.add(node.map)
        if node.state == goalState:
            goalNode = node
            return stack
        #reverse the
        paths = reversed(otherNodes(node))






def ids():
    return 0

def astar1():
    return 0

def astar2():
    return 0

def main():

    global goalNode
    #Parse command line statement for proper algorithm 
    
    parser = argparse.ArgumentParser()
    parser.add_argument('algorithm_name')
    parser.add_argument('input_file_path')
    args, unknown = parser.parse_known_args()
    list = args.input_file_path.split(" ")
    #List that will store input data
    InputList = []

    #Fills list from command line input list representation of 3x3 matrix
    for i in range (2,11):
        InputList.append(int(sys.argv[i]))
        print(sys.argv[i])

    #Changes which algorithm is used depending on user input in the command line 
    algo = args.algorithm_name
    if(algo == "dfs"):
        print("aye we read dfs properly")
        print(' '.join(str(x) for x in InputList))
        pass
    if(algo == "ids"):
        pass
    if(algo == "astar1"):
        pass
    if(algo == "astar2"):
        pass

    if(goalNode.depth > 10 and InputList != goalNode.state):
        return print("Sorry, we failed to find the solution within a depth of 10!")
    while InputList != goalNode.state:
        if(goalNode.move == 1):
            pass


if __name__ == "__main__":
    main()

