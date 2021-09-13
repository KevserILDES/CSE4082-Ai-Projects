import copy
import numpy as np

#Node class which holds necessary information
class Node:
    def __init__(self, state, parent, depth, action, cost, est_tot_cost):
        self.state = state
        self.parent = parent
        self.depth = depth
        self.action = action
        self.cost = cost
        self.est_tot_cost = est_tot_cost

#method to display a state
def display_state(state):
    for i in range(len(state)):
        print(" %i\t%i\t%i\t%i\n" %(state[i][0], state[i][1], state[i][2], state[i][3]))
        
#swap used when replacing black tile
def swap(state, index_x1, index_y1, index_x2, index_y2):
    new_state = copy.deepcopy(state)
    temp = new_state[index_y1][index_x1]
    new_state[index_y1][index_x1] = new_state[index_y2][index_x2]
    new_state[index_y2][index_x2] = temp
    return new_state

#to find index of black tile
def findIndex(state):
    for i in range(len(state)):
        try:
            return i, state[i].index(0)
        except ValueError:
            pass
        
#to move black tile up if possible
def move_up(state):
    new_state = copy.deepcopy(state)
    index_y, index_x = findIndex(new_state)
    if index_y > 0:
        return swap(new_state, index_x, index_y, index_x, index_y - 1)
    else:
        return None

#to move black tile down if possible
def move_down(state):
    new_state = copy.deepcopy(state)
    index_y, index_x = findIndex(new_state)
    if index_y < 3:
        return swap(new_state, index_x, index_y, index_x, index_y + 1)
    else:
        return None

#to move black tile right if possible
def move_right(state):
    new_state = copy.deepcopy(state)
    index_y, index_x = findIndex(new_state)
    if index_x < 3:
        return swap(new_state, index_x, index_y, index_x + 1, index_y)
    else:
        return None

#to move black tile left if possible
def move_left(state):
    new_state = copy.deepcopy(state)
    index_y,index_x = findIndex(new_state)
    if index_x > 0:
        return swap(new_state, index_x, index_y, index_x - 1, index_y)
    else:
        return None

#to move black tile up right if possible
def move_diag_ur(state):
    new_state = copy.deepcopy(state)
    index_y, index_x = findIndex(new_state)
    if index_y > 0 and index_x < 3:
        return swap(new_state, index_x, index_y, index_x + 1, index_y - 1)
    else:
        return None

#to move black tile up left if possible
def move_diag_ul(state):
    new_state = copy.deepcopy(state)
    index_y, index_x = findIndex(new_state)
    if index_y > 0 and index_x > 0: # y kodda 3 kalmış, unutma haber vermeyi
        return swap(new_state, index_x, index_y, index_x - 1, index_y - 1)
    else:
        return None

#to move black tile down right if possible
def move_diag_dr(state):
    new_state = copy.deepcopy(state)
    index_y, index_x = findIndex(new_state)
    if index_y < 3 and index_x < 3:
        return swap(new_state, index_x ,index_y ,index_x + 1, index_y + 1)
    else:
        return None

#to move black tile down left if possible
def move_diag_dl(state):
    new_state = copy.deepcopy(state)
    index_y, index_x = findIndex(new_state)
    if index_y < 3 and index_x > 0:
        return swap(new_state, index_x, index_y, index_x - 1, index_y + 1)
    else:
        return None

#All possible actions possible -branching- with incrementing cost (1 for normal, 3 for diagonal) and depth accordingly
def expand_node(node):
    nodes = []
    nodes.append(Node(move_up(node.state), node, node.depth + 1, "up", node.cost + 1, node.cost + 1))
    nodes.append(Node(move_down(node.state), node, node.depth + 1, "down", node.cost + 1, node.cost + 1))
    nodes.append(Node(move_left(node.state), node, node.depth + 1, "left", node.cost + 1, node.cost + 1,))
    nodes.append(Node(move_right(node.state), node, node.depth + 1, "right", node.cost + 1, node.cost + 1,))
    nodes.append(Node(move_diag_ur(node.state), node, node.depth + 1, "upper right", node.cost + 3, node.cost + 3))
    nodes.append(Node(move_diag_dl(node.state), node, node.depth + 1, "down left", node.cost + 3, node.cost + 3))
    nodes.append(Node(move_diag_ul(node.state), node, node.depth + 1, "upper left", node.cost + 3, node.cost + 3))
    nodes.append(Node(move_diag_dr(node.state), node, node.depth + 1, "down right", node.cost + 3, node.cost + 3))
    return [node for node in nodes if node.state != None]  # list comprehension!

#used in A* h1 to find number of misplaced tiles
def misplaced(state, goal_state):
    num_misplaced = 0
    for i in range(len(goal_state)):
        for j in range(len(goal_state[0])):
            if state[i][j] != goal_state[i][j]:
                num_misplaced += 1
    return num_misplaced

#heuristic 1 used in A*
def h1(node_list, goal_state):
    new_list = copy.deepcopy(node_list)
    for i in new_list:
        num_misplaced = misplaced(i.state, goal_state)
        i.est_tot_cost = i.cost + num_misplaced
    return new_list

#city block distances calculated for heuristic 2
def city_block(state, goal_state):
    city_bl_dist = 0
    for i in range(len(goal_state)):
        for j in range(len(goal_state[0])):
            if state[i][j] == 0:
                continue
            for row in range(len(goal_state)):
                if state[i][j] in goal_state[row]:
                    index = goal_state[row].index(state[i][j])
                    city_bl_dist += (abs(row - i) + abs(index - j))
                    break
    return city_bl_dist

#heuristic 2 used in A*
def h2(node_list, goal_state):
    new_list = copy.deepcopy(node_list)
    for i in new_list:
        manhattan_distance = city_block(i.state, goal_state)
        i.est_tot_cost = i.cost + manhattan_distance
    return new_list

#General graph search algorithm to find solution with strategy parameter
def General_Graph_Search(init_state, goal_state, strategy):
    frontier = []
    frontier.append(Node(init_state, None, 0, None, 0, 0))    #initialize frontier with start state -root
    root = frontier.pop(0)
    curr_node = root

    explored_set = []

    num_of_expanded_nodes = 0
    max_num_of_stored_nodes = 0
    
    while curr_node.state != goal_state:   #check if reach goal state
        explored_set.append(curr_node)
        expanded = expand_node(curr_node)
        num_of_expanded_nodes += 1

        for i in expanded:
            if (i not in explored_set) and (i not in frontier):
                frontier.append(i)
                
        if max_num_of_stored_nodes < len(frontier):
            max_num_of_stored_nodes = len(frontier)

        #UCS
        if strategy == 0:     
            frontier.sort(key = lambda x: x.cost) #priority queue behaviour sorting by minimum cost
        #A* h1
        elif strategy == 2:    
            frontier = h1(frontier, goal_state)
            frontier.sort(key = lambda x: x.est_tot_cost) #priority queue behaviour sorting by minimum estimated cost
        #A* h2
        elif strategy == 3:     
            frontier = h2(frontier,goal_state)
            frontier.sort(key = lambda x: x.est_tot_cost) #priority queue behaviour sorting by minimum estimated cost
            
        curr_node = frontier.pop(0)

        if not frontier:                  #if frontier is empty
            print("Empty!!!")
            return None
               
    #return necessary information of the solution found
    cost = curr_node.cost
    path = []
    while(curr_node.parent != None):
        path.insert(0, curr_node.action)
        curr_node = curr_node.parent
    return path, cost, max_num_of_stored_nodes, num_of_expanded_nodes

#for iterative lengthening search ucs with cost limit
def ucs_il(init_state, goal_state, cost_limit):
    frontier=[]
    frontier.append(Node(init_state, None, 0, None, 0, 0))    #initialize frontier with start state -root
    explored_set = []
    root = frontier.pop(0)
    curr_node = root
    num_of_expanded_nodes = 0
    max_num_of_stored_nodes = 0
    
    while curr_node.state != goal_state:   #check if reach goal state
        explored_set.append(curr_node)
        expanded = expand_node(curr_node)
        num_of_expanded_nodes += 1

        for i in expanded:
            if (i not in explored_set) and (i not in frontier) and (i.cost <= cost_limit): #add according to cost limit
                frontier.append(i)
                
        if max_num_of_stored_nodes < len(frontier):
            max_num_of_stored_nodes = len(frontier)

        if not frontier:
            return num_of_expanded_nodes

        frontier.sort(key = lambda x: x.cost) #sort by cost
        
        curr_node = frontier.pop(0)

    cost = curr_node.cost
    path = []
    while(curr_node.parent != None):
        path.insert(0, curr_node.action)
        curr_node = curr_node.parent
    return path, cost, max_num_of_stored_nodes, num_of_expanded_nodes

#iterative lengthening search
def ils(init_state, goal_state, max_cost):
    cost_limit = 0
    num_of_expanded_nodes = 0

    #with the stopping consition, call ucs_il in each incferasing cost_limit iteratively
    while cost_limit <= max_cost:
        result = ucs_il(init_state, goal_state, cost_limit)
        if type(result) is int:
            cost_limit += 1
            num_of_expanded_nodes += result
        else:
            return result[0], result[1], result[2], result[3] + num_of_expanded_nodes
    return None

import random  
#To generate random initial states with given depth --by checking cycles--
def randomGenerator(goal_state, depth):
    possible_moves = [move_up, move_down, move_left, move_right,
                      move_diag_ul, move_diag_dr, move_diag_ur, move_diag_dl]
    moves = ["up", "down", "left", "right","upper left","down right","upper right","down left"]

    created_state = copy.deepcopy(goal_state)
    rand2 = None
    for i in range(int(depth / 2)):
        rand1 = random.randint(0, 7) #random number for action
        if rand2: #to control cycles -- dont return to same place--
            if rand2 in [1, 3, 5, 7]:
                while rand1 == rand2 - 1:
                    rand1 = random.randint(0, 7)
            elif rand2 in [0, 2, 4, 6]:
                while rand1 == rand2 + 1:
                    rand1 = random.randint(0, 7)      
        
        temp1 = possible_moves[rand1](created_state)
        while temp1 == None:    #repeat till action is valid
             rand1 = random.randint(0, 7)
             if rand2:
                 if rand2 in [1, 3, 5, 7]:
                    while rand1 == rand2 - 1:
                        rand1=random.randint(0, 7)
                 elif rand2 in [0, 2, 4, 6]:
                    while rand1 == rand2 + 1:
                        rand1 = random.randint(0, 7) 
             temp1 = possible_moves[rand1](created_state)
        created_state = temp1
        
        rand2 = random.randint(0, 7) 
        #to prevent returning same place
        if rand1 in [1, 3, 5, 7]:
            while rand2 == rand1 - 1:
                rand2=random.randint(0, 7)
        elif rand1 in [0, 2, 4, 6]:
            while rand2 == rand1 + 1:
                rand2 = random.randint(0, 7)      
        temp2 = possible_moves[rand2](created_state)

        while temp2 == None:    #repeat till action is valid
             rand2 = random.randint(0, 7)
             if rand1 in [1, 3, 5, 7]:
                 while rand2 == rand1 - 1 or rand2 == rand1:
                     rand2 = random.randint(0, 7)
             elif rand1 in [0, 2, 4, 6]:
                while rand2 == rand1+ 1 or rand2 == rand1:
                    rand2 = random.randint(0, 7)
             temp2 = possible_moves[rand2](created_state)
        created_state = temp2

        print("moves:", moves[rand1], "->", moves[rand2])
        
    return created_state

#to display solution information
def print_information(method_name, puzzle, goal_state, method_num):
    if (method_num == 1):
        path, cost, max_num_of_stored_nodes, num_of_expanded_nodes = ils(puzzle, goal_state, 500)
    else: 
        path, cost, max_num_of_stored_nodes, num_of_expanded_nodes = General_Graph_Search(puzzle, goal_state, method_num)
    print("-------------", method_name, "--------------")
    print("Total cost:", cost)
    print("Solution path:", path)
    print("Total number of expanded nodes:", num_of_expanded_nodes)
    print("Maximum number of nodes stored in memory:", max_num_of_stored_nodes, "\n")

def main(depth):
    goal_state = [[1, 2, 3, 4], [12, 13, 14, 5], [11, 0, 15, 6], [10, 9, 8, 7]]
    puzzles = []
    for i in range(10):
        puzzles.append(randomGenerator(goal_state, depth))
        print("****************** DEPTH", depth, "/ PUZZLE", i + 1, "********************\n")
        display_state(puzzles[i])
        print_information("UCS", puzzles[i], goal_state, 0)
        print_information("ILS", puzzles[i], goal_state, 1)
        print_information("A* h1", puzzles[i], goal_state, 2)
        print_information("A* h2", puzzles[i], goal_state, 3)
    
    """
    puzzle1 = [[0, 1, 3, 4], [12, 13, 2, 5], [11, 14, 15, 6], [10, 9, 8, 7]]
    puzzle2 = [[1, 3, 5, 4], [2, 13, 14, 15], [11, 12, 9, 6], [0, 10, 8, 7]]
    puzzle3 = [[1, 13, 3, 4], [12, 11, 2, 5], [9, 8, 15, 7], [10, 6, 14, 0]]

    display_state(puzzle3)
    print_information("UCS", puzzle3, goal_state, 0)
    print_information("ILS", puzzle3, goal_state, 1)
    print_information("A* h1", puzzle3, goal_state, 2)
    print_information("A* h2", puzzle3, goal_state, 3)
    """

if __name__ == '__main__':
    main(2) #2, 4, 6, 8 ...28