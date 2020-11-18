import copy
import os
import numpy as np
from numpy import random
import math


def create_grid():
    rows = 120
    cols = 160
    grid = [['1' for i in range(cols)] for j in range(rows)]
    # rows' points will be from 15 to 105
    # cols' points will be from 15 to 145
    x_rand = random.randint(15, 105, size=8)
    y_rand = random.randint(15, 145, size=8)
    for (x, y) in zip(x_rand, y_rand):
        for i in range(1, 16):
            for j in range(1, 16):
                # Top Left
                if random.randint(2) == 1:
                    grid[x - i][y - j] = '2'
                # Top Right
                if random.randint(2) == 1:
                    grid[x + i][y - j] = '2'
                # Bottom Left
                if random.randint(2) == 1:
                    grid[x - i][y + j] = '2'
                # Bottom Right
                if random.randint(2) == 1:
                    grid[x + i][y + j] = '2'
                # Right
                if random.randint(2) == 1:
                    grid[x][y + j] = '2'
                # Left
                if random.randint(2) == 1:
                    grid[x][y - j] = '2'
            # Bottom
            if random.randint(2) == 1:
                grid[x + i][y] = '2'
            # Top
            if random.randint(2) == 1:
                grid[x - i][y] = '2'
        # Itself
        if random.randint(2) == 1:
            grid[x][y] = '2'
    # np.savetxt("array.txt", grid, fmt="%s")
    # Highways
    checker = True
    counter = 1
    while (checker):
        # print(counter)
        length = 0
        grid_copy = copy.deepcopy(grid)
        side = random.randint(4)  # 0-left wall, 1-top wall, 2-right wall, 3-bottom wall
        if side == 0:
            col = 0
            row = random.randint(0, 119)
            grid_copy = make_highway(row, col, 'right', grid_copy, length)
        elif side == 1:
            row = 0
            col = random.randint(0, 159)
            grid_copy = make_highway(row, col, 'down', grid_copy, length)
        elif side == 2:
            col = 159
            row = random.randint(0, 119)
            grid_copy = make_highway(row, col, 'left', grid_copy, length)
        else:
            row = 119
            col = random.randint(0, 159)
            grid_copy = make_highway(row, col, 'up', grid_copy, length)
        # np.savetxt("array.txt", grid, fmt="%s")
        if not grid_copy:
            checker = True
            continue
        # print(np.shape(grid_copy))
        counter += 1
        if counter == 5:
            checker = False
        grid = copy.deepcopy(grid_copy)
    # Blocked
    x_rand = random.randint(120, size=3840)
    y_rand = random.randint(160, size=3840)
    for (x, y) in zip(x_rand, y_rand):
        bool_guy = True
        if grid[x][y] == '1' or grid[x][y] == '2' or grid[x][y] == '0':
            grid[x][y] = '0'
        else:
            while bool_guy:
                x_new = random.randint(120)
                y_new = random.randint(160)
                # print(x, y, x_new, y_new, x_rand, y_rand)
                if grid[x_new][y_new] == '1' or grid[x_new][y_new] == '2' or grid[x_new][y_new] == '0':
                    grid[x_new][y_new] = '0'
                    bool_guy = False

    # Start
    x_rand = random.randint(0,40)
    y_rand = random.randint(0,40)
    x = x_rand if x_rand < 20 else (80 + x_rand)
    y = y_rand if y_rand < 20 else (120 + y_rand)
    #print(x, y)
    while grid[x][y] == 'a' or grid[x][y] == 'b' or grid[x][y] == '0':
        x_rand = random.randint(0, 40)
        y_rand = random.randint(0, 40)
        x = x_rand if x_rand < 20 else (80 + x_rand)
        y = y_rand if y_rand < 20 else (120 + y_rand)
        #print(x, y)
    x_start = x
    y_start = y

    # Goal
    x_rand = random.randint(0, 40)
    y_rand = random.randint(0, 40)
    x = x_rand if x_rand < 20 else (80 + x_rand)
    y = y_rand if y_rand < 20 else (120 + y_rand)
    distance = math.sqrt((x_start-x)**2 + (y_start-y)**2)
    #print(x, y)
    while (grid[x][y] == 'a' or grid[x][y] == 'b' or grid[x][y] == '0') and distance < 100:
        x_rand = random.randint(0, 40)
        y_rand = random.randint(0, 40)
        x = x_rand if x_rand < 20 else (80 + x_rand)
        y = y_rand if y_rand < 20 else (120 + y_rand)
        #print(x, y)
        distance = math.sqrt((x_start-x)**2 + (y_start-y)**2)
    x_goal = x
    y_goal = y

    #print(x_start, y_start, x_goal, y_goal)

    np.savetxt("map.txt", grid, fmt="%s")
    file_name = "map.txt"

    dummy_file = file_name + '.bak'
    # open original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Write given line to the dummy file
        write_obj.write(str(x_start)+ ' ' + str(y_start) + '\n')
        write_obj.write(str(x_goal) + ' ' + str(y_goal) + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)
    return grid


def make_highway(x, y, direction, grid, length):
    if direction == 'right':
        # print(grid[x][y])
        for i in range(20):
            if grid[x][y] == '1':
                grid[x][y] = 'a'
            elif grid[x][y] == '2':
                grid[x][y] = 'b'
            else:
                return False
            y += 1
        length += 20
        looper = True
        while looper:
            grid, looper, direction, length, x, y = finish_highway(x, y, direction, grid, length)
        if not grid:
            return False
    elif direction == 'down':
        for i in range(20):
            # print(grid[x][y])
            if grid[x][y] == '1':
                grid[x][y] = 'a'
            elif grid[x][y] == '2':
                grid[x][y] = 'b'
            else:
                return False
            x += 1
        length += 20
        looper = True
        while looper:
            grid, looper, direction, length, x, y = finish_highway(x, y, direction, grid, length)
        if not grid:
            return False
    elif direction == 'left':
        for i in range(20):
            # print(grid[x][y])
            if grid[x][y] == '1':
                grid[x][y] = 'a'
            elif grid[x][y] == '2':
                grid[x][y] = 'b'
            else:
                return False
            y -= 1
        length += 20
        looper = True
        while looper:
            grid, looper, direction, length, x, y = finish_highway(x, y, direction, grid, length)
        if not grid:
            return False
    else:
        for i in range(20):
            # print(grid[x][y])
            if grid[x][y] == '1':
                grid[x][y] = 'a'
            elif grid[x][y] == '2':
                grid[x][y] = 'b'
            else:
                return False
            x -= 1
        length += 20
        looper = True
        while looper:
            grid, looper, direction, length, x, y = finish_highway(x, y, direction, grid, length)
        if not grid:
            return False
    return grid


def finish_highway(x, y, direction, grid, length):
    if direction == 'right':
        side = random.randint(10)  # 0-5:right, 6-7:up, 8-9:down
        if 0 <= side <= 5:
            direction = 'right'
        elif 6 <= side <= 7:
            direction = 'up'
        else:
            direction = 'down'
    elif direction == 'down':
        side = random.randint(10)  # 0-5:down, 6-7:right, 8-9:left
        if 0 <= side <= 5:
            direction = 'down'
        elif 6 <= side <= 7:
            direction = 'right'
        else:
            direction = 'left'
    elif direction == 'left':
        side = random.randint(10)  # 0-5:left, 6-7:down, 8-9:up
        if 0 <= side <= 5:
            direction = 'left'
        elif 6 <= side <= 7:
            direction = 'down'
        else:
            direction = 'up'
    else:
        side = random.randint(10)  # 0-5:up, 6-7:left, 8-9:right
        if 0 <= side <= 5:
            direction = 'up'
        elif 6 <= side <= 7:
            direction = 'left'
        else:
            direction = 'right'

    if direction == 'right':
        # print(grid[x][y])
        for i in range(20):
            if grid[x][y] == '1':
                grid[x][y] = 'a'
            elif grid[x][y] == '2':
                grid[x][y] = 'b'
            else:
                return False, False, direction, length, x, y
            y += 1
            if y > 159:
                length += i
                if length >= 100:
                    return grid, False, direction, length, x, y
                else:
                    return False, False, direction, length, x, y
        length += 20
    elif direction == 'down':
        for i in range(20):
            # print(grid[x][y])
            if grid[x][y] == '1':
                grid[x][y] = 'a'
            elif grid[x][y] == '2':
                grid[x][y] = 'b'
            else:
                return False, False, direction, length, x, y
            x += 1
            if x > 119:
                length += i
                if length >= 100:
                    return grid, False, direction, length, x, y
                else:
                    return False, False, direction, length, x, y
        length += 20

    elif direction == 'left':
        for i in range(20):
            # print(grid[x][y])
            if grid[x][y] == '1':
                grid[x][y] = 'a'
            elif grid[x][y] == '2':
                grid[x][y] = 'b'
            else:
                return False, False, direction, length, x, y
            y -= 1
            if y < 0:
                length += i
                if length >= 100:
                    return grid, False, direction, length, x, y
                else:
                    return False, False, direction, length, x, y
        length += 20
    else:
        for i in range(20):
            # print(grid[x][y])
            if grid[x][y] == '1':
                grid[x][y] = 'a'
            elif grid[x][y] == '2':
                grid[x][y] = 'b'
            else:
                return False, False, direction, length, x, y
            x -= 1
            if x < 0:
                length += i
                if length >= 100:
                    return grid, False, direction, length, x, y
                else:
                    return False, False, direction, length, x, y
        length += 20
    return grid, True, direction, length, x, y


create_grid()
