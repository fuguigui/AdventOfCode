import copy

class Direction:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def __str__(self) -> str:
        return f"Direction({self.direction}: {self.x}, {self.y})" 
    
    def set_next(self, next_direction):
        self.next_direction = next_direction

    def get_next(self):
        return self.next_direction


GO_UP = Direction(-1, 0, "up")
GO_RIGHT = Direction(0, 1, "right")
GO_DOWN = Direction(1, 0, "down")
GO_LEFT = Direction(0, -1, "left")

GO_UP.set_next(GO_RIGHT)
GO_RIGHT.set_next(GO_DOWN)
GO_DOWN.set_next(GO_LEFT)
GO_LEFT.set_next(GO_UP)

def parse_direction_symbol(symbol):
    if symbol == "^":
        return GO_UP
    if symbol == ">":
        return GO_RIGHT
    if symbol == "v":
        return GO_DOWN
    return GO_LEFT
        
def read_input(file_name):
    puzzles = []
    start_x, start_y = -1, -1
    start_direction = None
    with open('Day6/' + file_name, 'r') as file:
        for line in file.readlines():
            split_line = []
            for y, point in enumerate(line.strip()):
                if point == "." or point == "#":
                    split_line.append(point)
                else:
                    start_x = len(puzzles)
                    start_y = y
                    start_direction = parse_direction_symbol(point)
                    split_line.append("X")
            # print("length of one line: {}".format(len(split_line)))
            puzzles.append(split_line)    
    return puzzles, start_x, start_y, start_direction

def print_puzzles(puzzles):
    for line in puzzles:
        print(line)
    
def test_read_input():
    puzzles, start_x, start_y, start_direction = read_input("sample.txt")
    print_puzzles(puzzles)
    print("Start point: {}, {}".format(start_x, start_y))
    print("Start Direction: {}".format(start_direction))

# test_read_input()

def find_next_step(puzzle, puzzle_width, puzzle_height, start_x, start_y, move_direction, verbose=False):
    next_direction = move_direction
    while True:
        next_x = start_x + next_direction.x
        next_y = start_y + next_direction.y
        if next_x == -1 or next_x == puzzle_height or next_y == -1 or next_y == puzzle_width:
            break
        if puzzle[next_x][next_y] == "#":
            next_direction = next_direction.get_next()
        else:
            if verbose:
                print("current location: {}, {}, and next move direction: {}".format(start_x, start_y, next_direction))
            return next_x, next_y, next_direction
    return -1, -1, GO_UP

def walk_in_the_puzzle(cur_area, puzzle, puzzle_width, puzzle_height, start_x, start_y, move_direction, verbose = False):
    if verbose:
        print("start: {}, start_location: {}, {}".format(cur_area, start_x, start_y))
        print_puzzles(puzzle)
    next_x = start_x
    next_y = start_y
    next_direction = move_direction
    while True:
        next_x, next_y, next_direction = find_next_step(puzzle, puzzle_width, puzzle_height, next_x, next_y, next_direction)
        if verbose:
            print("current area: {}, next_step: {}, {} and direction: {}".format(cur_area, next_x, next_y, next_direction))
        if next_x == -1:
            return cur_area
        if puzzle[next_x][next_y] != "X":
            puzzle[next_x][next_y] = "X"
            cur_area += 1
            
def test_walk_in_the_puzzle(file_name, answer):
    puzzles, start_x, start_y, start_direction = read_input(file_name)
    route_area = walk_in_the_puzzle(1, puzzles, len(puzzles[0]), len(puzzles), start_x, start_y, start_direction, verbose=True)
    print("actual output: {}".format(route_area))
    print("expected output: {}".format(answer))
        
# test_walk_in_the_puzzle("sample.txt", 41)

def main_part1():
    puzzles, start_x, start_y, start_direction = read_input("input.txt")
    print(walk_in_the_puzzle(1, puzzles, len(puzzles[0]), len(puzzles), start_x, start_y, start_direction))

# main_part1()

def make_index(x,y):
    return f"Index:{x},{y}"
    
def check_loop(puzzle, puzzle_width, puzzle_height, start_x, start_y, move_direction, verbose=False):
    step_history = dict()
    next_x = start_x
    next_y = start_y
    next_direction = move_direction
    while True:
        next_x, next_y, next_direction = find_next_step(puzzle, puzzle_width, puzzle_height, next_x, next_y, next_direction)
        if verbose:
            print("next_step: {}, {} and direction: {}".format(next_x, next_y, next_direction))
        if next_x == -1:
            return False
        next_index = make_index(next_x, next_y)
        if puzzle[next_x][next_y] != "X":
            puzzle[next_x][next_y] = "X"
            step_history[next_index] = set([next_direction])
        else:
            if next_index not in step_history:
                step_history[next_index] = set([next_direction])
            else:
                if next_direction in step_history[next_index]:
                    return True

def put_obstraction(puzzle, puzzle_width, puzzle_height, start_x, start_y, move_direction, verbose = False):
    original_puzzle = copy.deepcopy(puzzle)
    if verbose:
        print("start_location: {}, {}".format(start_x, start_y))
        print_puzzles(puzzle)
    next_x = start_x
    next_y = start_y
    next_direction = move_direction
    obstraction_num = 0
    while True:
        next_x, next_y, next_direction = find_next_step(puzzle, puzzle_width, puzzle_height, next_x, next_y, next_direction)
        if verbose:
            print("next_step: {}, {} and direction: {}".format(next_x, next_y, next_direction))
        if next_x == -1:
            return obstraction_num
        if puzzle[next_x][next_y] != "X":
            puzzle[next_x][next_y] = "X"
            new_puzzle = copy.deepcopy(original_puzzle)
            new_puzzle[next_x][next_y] = "#"
            if check_loop(new_puzzle, puzzle_width, puzzle_height, start_x, start_y, move_direction):
                obstraction_num += 1


def test_put_obstraction(file_name, answer):
    puzzles, start_x, start_y, start_direction = read_input(file_name)
    obst_number = put_obstraction(puzzles, len(puzzles[0]), len(puzzles), start_x, start_y, start_direction, verbose=False)
    print("actual output: {}".format(obst_number))
    print("expected output: {}".format(answer))
        
# test_put_obstraction("sample.txt", 6)

def main_part2():
    puzzles, start_x, start_y, start_direction = read_input("input.txt")
    print(put_obstraction(puzzles, len(puzzles[0]), len(puzzles), start_x, start_y, start_direction))

# main_part2()
