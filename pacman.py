"""Pac-Man"""
# Created on 6-11-2019
__author__ = "Rui Ding"
__email__ = "rding@albany.edu"
__version__ = "1.1"

# ToDo:
#   - Add intelligent ghost AI and pathfinding

# Notes:
#   - All coordinates are set like this: [Y, X]

import time, os, random, msvcrt, sys, subprocess
import pacgraphics

game_over = False
debug = False
score = 0  # incremented when a coin is collected
n_ghosts = 4  # maximum of 4 ghosts at once
n_powerups = 4
power_coords = []
ghost_initial_coords = [[10, 8], [10, 9], [10, 10], [9, 9]]
ghost_coords = [[10, 8], [10, 9], [10, 10], [9, 9]]  # matrix
ghost_direction = []
ghost_prev_direction = []
coin_coords = []  # matrix
direction = "STOP"
board = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
const_height = len(board)
const_width = len(board[0])  # 19
wall_list = []
player_str = "O"
ghost_str = "X"
power_str = "*"
coin_str = "."
wall_str = "|"
space_str = " "
power_duration = 100
powered = False
probability_of_changing_direction = 50
max_probability_change_direction = 100
probability_going_back = 0
max_probability_going_back = 100
multiplier = 1


def setup():
    global x, y, wall_list, ghost_coords, board, max_score, enable_death, empty_space, ghost_direction, game_over, power_coords, initial_power_coords
    enable_death = False
    game_over = False
    x = 9
    y = 16
    for yindex, row in enumerate(board):
        for xindex, column in enumerate(row):
            if column == 1:
                wall_list.append([yindex, xindex])
            else:
                coin_coords.append([yindex, xindex])
    empty_space = coin_coords
    max_score = len(coin_coords)
    for x in range(n_ghosts):
        ghost_direction.append("STOP")
        ghost_prev_direction.append("STOP")
    power_coords = [[1, 1], [1, 17], [19, 17], [19, 1]]  # [Y, X]
    initial_power_coords = [[1, 1], [1, 17], [20, 17], [20, 1]]


def repopulate_board():
    global initial_power_coords, power_coords
    for yindex, row in enumerate(board):
        for xindex, column in enumerate(row):
            if column == 0:
                coin_coords.append([yindex, xindex])
    for index, powerup in enumerate(initial_power_coords):
        power_coords[index] = powerup


def draw():
    global enable_death, debug, ghost_available_directions, x, y
    for yindex, row in enumerate(board):  # y
        for xindex, column in enumerate(row):  # x
            if column == 0:
                if [yindex, xindex] == [y, x]:
                    print(player_str, end="")
                elif [yindex, xindex] in ghost_coords:
                    print(ghost_str, end="")
                elif [yindex, xindex] in power_coords:
                    print(power_str, end="")
                else:
                    if [yindex, xindex] in coin_coords:
                        print(coin_str, end="")
                    else:
                        print(space_str, end="")
            if column == 1:
                print(wall_str, end="")  # █ ▓ ■
        print()
    print("Score: " + str(score))
    if debug:
        print("X: " + str(x) + "\nY: " + str(y))
        if not enable_death:
            print("Safe Mode On")
        else:
            print("Safe Mode Off")
        if powered:
            print("Powerup On")
        else:
            print("Powerup Off")
        print("Direction:", direction)
        print("Ghost Coordinates:", ghost_coords)
        print("Ghost Directions:", ghost_direction)
        print("Previous Ghost Directions:", ghost_prev_direction)
        print("Ghost Available Directions:", ghost_available_directions)
        print("Powerup Coordinates:", power_coords)
        if powered:
            print("Powerup Duration:", power_duration)


def check_input():
    global direction, game_over, debug
    if msvcrt.kbhit():
        c = msvcrt.getch()
        try:
            key = c.decode("ascii").lower()
        except:
            return
        if key == "w":
            direction = "UP"
        elif key == "a":
            direction = "LEFT"
        elif key == "s":
            direction = "DOWN"
        elif key == "d":
            direction = "RIGHT"
        elif key == "n":
            game_over = True
        elif key == "o":
            if debug:
                debug = False
            else:
                debug = True


def logic():
    global x, y, direction, wall_list, score, game_over, game_win, max_score, enable_death, \
        coin_coords, prev_direction, ghost_available_directions, ghost_str, power_duration, powered, \
        probability_of_changing_direction, max_probability_change_direction, multiplier

    if len(coin_coords) == 0:
        repopulate_board()

    if [y, x] in coin_coords:
        score += 10
        coin_coords.remove([y, x])

    if [y, x] in power_coords:
        powered = True
        power_coords.remove([y, x])
        ghost_str = "0"
        power_duration = 100

    if powered:
        for index, ghost in enumerate(ghost_coords):
            if [y, x] == ghost:
                ghost_coords[index] = ghost_initial_coords[index]
                score += 200 * multiplier
                multiplier += 1
        power_duration -= 1
        if power_duration < 20:
            if power_duration % 2 == 0:
                ghost_str = "%"
            else:
                ghost_str = "0"

        if power_duration <= 0:
            powered = False
            ghost_str = "X"
            multiplier = 1

    if direction == "UP":
        y -= 1
    elif direction == "LEFT":
        x -= 1
    elif direction == "DOWN":
        y += 1
    elif direction == "RIGHT":
        x += 1

    if x >= const_width:
        x = 0
    elif x < 0:
        x = const_width

    if [y, x] in wall_list:
        if direction == "UP":
            y += 1
            direction = "STOP"
        elif direction == "LEFT":
            x += 1
            direction = "STOP"
        elif direction == "DOWN":
            y -= 1
            direction = "STOP"
        elif direction == "RIGHT":
            x -= 1
            direction = "STOP"
    # ghost logic start
    if not powered:
        if enable_death:
            if [y, x] in ghost_coords:
                game_over = True

    ghost_available_directions = []
    for index, ghost in enumerate(ghost_coords):
        # x = ghost[1] <--
        # y = ghost[0] <--

        if ghost[1] >= const_width:
            ghost_coords[index] = [ghost[0], ghost[1] - 1]
        elif ghost[1] < 0:
            ghost_coords[index] = [ghost[0], ghost[1] + 1]

        # start of main movement logic \\
        if ghost_direction[index] == "STOP":
            if board[ghost[0]][ghost[1] - 1] == 0:
                ghost_available_directions.append("LEFT")
            if board[ghost[0]][ghost[1] + 1] == 0:
                ghost_available_directions.append("RIGHT")
            if board[ghost[0] - 1][ghost[1]] == 0:
                ghost_available_directions.append("UP")
            if board[ghost[0] + 1][ghost[1]] == 0:
                ghost_available_directions.append("DOWN")

            if ghost_prev_direction[index] in ghost_available_directions:
                # prev_index = ghost_available_directions.index(ghost_prev_direction[index])
                if len(ghost_available_directions) > 1:
                    ghost_available_directions.remove(ghost_prev_direction[index])
            num = random.randint(0, max_probability_going_back)
            if num >= max_probability_going_back - probability_going_back:
                ghost_direction[index] = ghost_prev_direction[index]
            else:
                ghost_direction[index] = random.choice(ghost_available_directions)
        move_bool = False
        if ghost_direction[index] == "UP":
            ghost_coords[index] = [ghost[0] - 1, ghost[1]]
            num = random.randint(0, max_probability_change_direction)
            if board[ghost[0]][ghost[1] - 1] == 0 and not move_bool:  # and ghost_prev_direction[index] != "RIGHT":
                if num <= probability_of_changing_direction:
                    ghost_prev_direction[index] = "RIGHT"
                    ghost_direction[index] == "LEFT"
                    ghost_coords[index] = [ghost[0], ghost[1] - 1]
                    move_bool = True
            if board[ghost[0]][ghost[1] + 1] == 0 and not move_bool:  # and ghost_prev_direction[index] != "LEFT":
                if num <= probability_of_changing_direction:
                    ghost_coords[index] = [ghost[0], ghost[1] + 1]
                    ghost_prev_direction[index] = "LEFT"
                    ghost_direction[index] == "RIGHT"
                    move_bool = True
        elif ghost_direction[index] == "LEFT":
            ghost_coords[index] = [ghost[0], ghost[1] - 1]
            num = random.randint(0, max_probability_change_direction)
            if board[ghost[0] - 1][ghost[1]] == 0 and not move_bool:  # and ghost_prev_direction[index] != "DOWN":
                if num <= probability_of_changing_direction:
                    ghost_prev_direction[index] = "DOWN"
                    ghost_direction[index] == "UP"
                    ghost_coords[index] = [ghost[0] - 1, ghost[1]]
                    move_bool = True
            if board[ghost[0] + 1][ghost[1]] == 0 and not move_bool:  # and ghost_prev_direction[index] != "UP":
                if num <= probability_of_changing_direction:
                    ghost_prev_direction[index] = "UP"
                    ghost_direction[index] == "DOWN"
                    ghost_coords[index] = [ghost[0] + 1, ghost[1]]
                    move_bool = True
        elif ghost_direction[index] == "DOWN":
            ghost_coords[index] = [ghost[0] + 1, ghost[1]]
            num = random.randint(0, max_probability_change_direction)
            if board[ghost[0]][ghost[1] - 1] == 0 and not move_bool:  # and ghost_prev_direction[index] != "RIGHT":
                if num <= probability_of_changing_direction:
                    ghost_prev_direction[index] = "RIGHT"
                    ghost_direction[index] == "LEFT"
                    ghost_coords[index] = [ghost[0], ghost[1] - 1]
                    move_bool = True
            if board[ghost[0]][ghost[1] + 1] == 0 and not move_bool:  # and ghost_prev_direction[index] != "LEFT":
                if num <= probability_of_changing_direction:
                    ghost_prev_direction[index] = "LEFT"
                    ghost_direction[index] == "RIGHT"
                    ghost_coords[index] = [ghost[0], ghost[1] + 1]
                    move_bool = True
        elif ghost_direction[index] == "RIGHT":
            ghost_coords[index] = [ghost[0], ghost[1] + 1]
            num = random.randint(0, max_probability_change_direction)
            if board[ghost[0] - 1][ghost[1]] == 0 and not move_bool:  # and ghost_prev_direction[index] != "DOWN":
                if num <= probability_of_changing_direction:
                    ghost_prev_direction[index] = "DOWN"
                    ghost_direction[index] == "UP"
                    ghost_coords[index] = [ghost[0] - 1, ghost[1]]
                    move_bool = True
            if board[ghost[0] + 1][ghost[1]] == 0 and not move_bool:  # and ghost_prev_direction[index] != "UP":
                if num <= probability_of_changing_direction:
                    ghost_prev_direction[index] = "UP"
                    ghost_direction[index] == "DOWN"
                    ghost_coords[index] = [ghost[0] + 1, ghost[1]]
                    move_bool = True
        # End of main movement logic //
        if [ghost[0], ghost[1]] in wall_list:
            if ghost_direction[index] == "UP":
                ghost_prev_direction[index] = "DOWN"
                ghost_coords[index] = [ghost[0] + 1, ghost[1]]
                ghost_direction[index] = "STOP"
            elif ghost_direction[index] == "LEFT":
                ghost_prev_direction[index] = "RIGHT"
                ghost_coords[index] = [ghost[0], ghost[1] + 1]
                ghost_direction[index] = "STOP"
            elif ghost_direction[index] == "DOWN":
                ghost_prev_direction[index] = "UP"
                ghost_coords[index] = [ghost[0] - 1, ghost[1]]
                ghost_direction[index] = "STOP"
            elif ghost_direction[index] == "RIGHT":
                ghost_prev_direction[index] = "LEFT"
                ghost_coords[index] = [ghost[0], ghost[1] - 1]
                ghost_direction[index] = "STOP"
    print()


def main():
    global game_over
    setup()
    while not game_over:
        if not idle:
            os.system("cls")
        draw()
        check_input()
        logic()
        #pass values to graphics rendering+
        window = pacgraphics.drawWindow()
        pacgraphics.otherRedraw(window, board, coin_coords, ghost_coords, power_coords, wall_list, score)
        time.sleep(0.2)  # game speed
    print("Game Over!")
    input("Press enter to continue . . . ")


if __name__ == "__main__":
    if "idlelib.run" in sys.modules:  # if running through IDLE
        try:
            subprocess.call(["python", "pac-man_main.py"])  # try running through a console window
        except:
            print("This game will not run properly in IDLE.")
            print("It is highly recommended that you run it through a console window instead.\n")
            choice = input("Would you like to proceed anyway? [Y/N]: ").strip().lower()
            if choice == "y":
                idle = True
                main()
    else:
        idle = False
        main()
