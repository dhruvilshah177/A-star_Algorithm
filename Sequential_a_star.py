from queue import PriorityQueue
from heapq import heappush, heappop
from collections import defaultdict
import math
import numpy as np
import os
import time


# Heuristic Function based on Manhattan Distance
def heuristic(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
    return abs(x1 - x2) + abs(y1 - y2)

# Euclidean Distance
def eucl_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Diagonal Distance
def diagonal_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    x1, x2, y1, y2 = int(x1), int(x2), int(y1), int(y2)
    return max(abs(x1 - x2), abs(y1 - y2))


def get_cost(grid, current_x, current_y, next_x, next_y, dir):
    current_type = grid[current_x][current_y]
    next_type = grid[next_x][next_y]

    # any 0's lead to very high cost.
    if next_type == '0':
        return float("inf")
    # 1-1
    if current_type == '1' and next_type == '1':
        return 1 if dir == 'side' else math.sqrt(2)
    # 2-2
    elif current_type == '2' and next_type == '2':
        return 2 if dir == 'side' else math.sqrt(8)
    # a-a
    elif current_type == 'a' and next_type == 'a':
        return .25
    # b-b
    elif current_type == 'b' and next_type == 'b':
        return .5
    # 2-1 or 1-2
    elif (current_type == '1' and next_type == '2') or (current_type == '2' and next_type == '1'):
        return 1.5 if dir == 'side' else (math.sqrt(2) + math.sqrt(8)) / 2
    # a-1 or 1-a
    elif (current_type == '1' and next_type == 'a') or (current_type == 'a' and next_type == '1'):
        return 1 if dir == 'side' else math.sqrt(2)
    # a-2 or 2-a
    elif (current_type == '2' and next_type == 'a') or (current_type == 'a' and next_type == '2'):
        return 1.5 if dir == 'side' else (math.sqrt(2) + math.sqrt(8)) / 2
    # b-1 or 1-b
    elif (current_type == '1' and next_type == 'b') or (current_type == 'b' and next_type == '1'):
        return 1.5 if dir == 'side' else (math.sqrt(2) + math.sqrt(8)) / 2
    # b-2 or 2-b
    elif (current_type == '2' and next_type == 'b') or (current_type == 'b' and next_type == '2'):
        return 2 if dir == 'side' else math.sqrt(8)
    # a-b or b-a
    elif (current_type == 'a' and next_type == 'b') or (current_type == 'b' and next_type == 'a'):
        return .375


def expand_state(f_val, state, i, g_score, pq, pq_set, came_from, weight_1, goal, grid):
    # for traversing in 8 directions: right, left, down, up, down-right, down-left, up-left, up-right in order
    x = [0, 0, 1, -1, 1, 1, -1, -1]
    y = [1, -1, 0, 0, 1, -1, -1, 1]
    direction = ['side', 'side', 'side', 'side', 'diagonal', 'diagonal', 'diagonal', 'diagonal']

    x_current = int(state[0])
    y_current = int(state[1])

    state = (x_current, y_current)
    # traversing 4 neighbor nodes
    for row, col, dir in zip(x, y, direction):
        if 0 <= x_current + row < 120 and 0 <= y_current + col < 160:
            temp_g_score = g_score[i][state] + get_cost(grid, x_current, y_current, x_current + row, y_current + col, dir)

            # if temp_g_score is less than the score we had for this node, set that score
            if temp_g_score < g_score[i][(row + x_current, col + y_current)]:
                g_score[i][(row + x_current, col + y_current)] = temp_g_score
                came_from[i][(row + x_current, col + y_current)] = state

                if state not in pq_set[i]:
                    if i == 0:
                        chosen_heuristic = heuristic
                    elif i == 1:
                        chosen_heuristic = eucl_distance
                    elif i == 2:
                        chosen_heuristic = diagonal_distance
                    key_value = g_score[i][(row + x_current, col + y_current)] + weight_1 * chosen_heuristic((row + x_current, col + y_current), goal)
                    heappush(pq[i], (key_value, (row + x_current, col + y_current)))

    return g_score, pq, pq_set, came_from



def seq_a_helper(weight_1, weight_2, pq, pq_set, g_score, came_from, grid, goal, num_hueristic):
    num_nodes_expanded = 0

    while pq[0][0][0] < float('inf'):

        for i in range(1, num_hueristic + 1):
            # If we use inadmissible heuristic
            if pq[i][0][0] <= weight_2 * pq[0][0][0]:
                if g_score[i][goal] <= pq[i][0][0]:
                    if g_score[i][goal] < float('inf'):
                        return i, came_from[i], num_nodes_expanded
                else:
                    f_val, state = heappop(pq[i])
                    g_score, pq, pq_set, came_from = expand_state(f_val, state, i, g_score, pq, pq_set, came_from,
                                                                  weight_1, goal, grid)
                    num_nodes_expanded += 1
                    x_curr = int(state[0])
                    y_curr = int(state[1])
                    pq_set[i].add((f_val, (x_curr, y_curr)))

            # admissible heuristic
            else:
                if g_score[0][goal] <= pq[0][0][0]:
                    if g_score[0][goal] < float('inf'):
                        return 0, came_from[0], num_nodes_expanded
                else:
                    f_val, state = heappop(pq[i])
                    g_score, pq, pq_set, came_from = expand_state(f_val, state, 0, g_score, pq, pq_set, came_from,
                                                                  weight_1, goal, grid)
                    num_nodes_expanded += 1
                    x_curr = int(state[0])
                    y_curr = int(state[1])
                    pq_set[0].add((f_val, (x_curr, y_curr)))

    print("Randomly terminated")
    return None


def main():
    # Priority Queue
    pq = PriorityQueue()

    # Assuming map.txt follows the same format as generated by create_world.py
    # Getting the start, goal and the grid as a 2d list
    with open("map.txt") as textFile:
        first_line = textFile.readline()
        second_line = textFile.readline()

        x_start, y_start = first_line.split()
        x_goal, y_goal = second_line.split()

        grid = [line.split() for line in textFile]

    # g_score of nodes using dictionary with default value "inf"
    start = (int(x_start), int(y_start))
    goal = (int(x_goal), int(y_goal))

    num_hueristic = 2

    g_score = [defaultdict(lambda: float("inf"))]*(num_hueristic+1)
    # f_score = []
    pq = [[]]*(num_hueristic+1)
    pq_set = [set()]*(num_hueristic+1)
    came_from = [defaultdict(lambda: None)]*(num_hueristic+1)


    for i in range(num_hueristic+1):
        # g_score[n] is the cost of the cheapest path from start to n currently known.
        g_score[i][start] = 0

        # #  For node n, f_score[n] := g_score[n] + heuristic(n). f_score[n] represents our current best guess as to
        # #  how short a path from start to finish can be if it goes through n.
        # f_score[i] = defaultdict(lambda: float("inf"))
        # f_score[i][start] = g_score[i][start] + heuristic(start, goal)

        # put start node into Priority Queue
        key = g_score[i][start] + heuristic(start, goal)
        heappush(pq[i], (key, start))


    goal_reached = False
    weight_1 = float(input("Enter w1 : "))
    weight_2 = float(input("Enter w2 : "))

    num_nodes_expanded = 0
    start_time = time.time()

    heuristic_idx, parents, num_nodes_expanded = seq_a_helper(weight_1, weight_2, pq, pq_set, g_score, came_from, grid, goal, num_hueristic)

    #if goal_reached:
    time_taken = time.time() - start_time
    print("Path Found!")
    heuristic_list = ["Manhattan Distance", "Euclidean Distance", "Diagonal Distance"]
    print("Best Heuristic: ", heuristic_list[heuristic_idx])

    # Setting the value 'p' in the grid for our path found
    x, y = parents[goal]
    while True:
        if (x, y) == start:
            break
        grid[x][y] = 'p'
        end = (x, y)
        x, y = parents[end]

    path_counter = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'p':
                path_counter += 1
    #else:
    #    print("No Path found")

    print("Path Length: ", path_counter)
    print("Number of Nodes expanded: ", num_nodes_expanded)
    print("The weighted A* took", time_taken, "seconds to run")

    np.savetxt("seqAstar_finished_map.txt", grid, fmt="%s")
    #create_world code to send in starting coords
    file_name = "seqAstar_finished_map.txt"
    dummy_file = file_name + '.bak'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(str(x_start) + ' ' + str(y_start) + '\n')
        write_obj.write(str(x_goal) + ' ' + str(y_goal) + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

main()
