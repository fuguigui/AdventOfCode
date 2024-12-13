import re

def parse_one_puzzle(three_line_per_puzzle):
    pattern = r"\d+"
    A = tuple(int(i) for i in re.findall(pattern, three_line_per_puzzle[0]))
    B = tuple(int(i) for i in re.findall(pattern, three_line_per_puzzle[1]))
    goal = tuple(int(i) for i in re.findall(pattern, three_line_per_puzzle[2]))
    return A, B, goal

def test_parse_one_puzzle():
    three_line_per_puzzle = ["Button A: X+94, Y+34", "Button B: X+22, Y+67", "Prize: X=8400, Y=5400"]
    print(parse_one_puzzle(three_line_per_puzzle))

# test_parse_one_puzzle()

def read_input(file_name):
    puzzles = []
    with open('Day13/' + file_name, 'r') as file:
        one_puzzle_input = []
        for line in file.readlines():
            if len(line.strip()) == 0:
                puzzles.append(parse_one_puzzle(one_puzzle_input))
                one_puzzle_input = []
            else:
                one_puzzle_input.append(line.strip())
        # parse the last puzzle
        puzzles.append(parse_one_puzzle(one_puzzle_input))   
    return puzzles

def test_read_input():
    print(read_input("sample.txt"))

# test_read_input()

######### Part1 #########
def calculate_button_a(a, b, goal):
    divenden = goal[0] * b[1] - goal[1] * b[0]
    divisor = a[0] * b[1] - a[1] * b[0]
    if divisor != 0 and (divenden * divisor >= 0) and (divenden % divisor) == 0:
        return divenden // divisor
    return -1

def calculate_button_b(a, b, goal):
    divenden = goal[0] * a[1] - goal[1] * a[0]
    divisor = a[1] * b[0] - a[0] * b[1]
    if divisor != 0 and (divenden * divisor >= 0) and (divenden % divisor) == 0:
        return divenden // divisor
    return -1

def find_token(puzzle):
    button_a_times = calculate_button_a(puzzle[0], puzzle[1], puzzle[2])
    button_b_times = calculate_button_b(puzzle[0], puzzle[1], puzzle[2])
    # print(f"find_token for {puzzle} with {button_a_times} and {button_b_times}")
    if button_a_times >= 0 and button_a_times <= 100 and button_b_times >= 0 and button_b_times <= 100:
        return 3 * button_a_times + button_b_times
    return -1

def test_find_token():
    answers = [-1, 459236326669, -1, 416082282239]
    for i, puzzle in enumerate(read_input("sample.txt")):
        print(f"actual_output: {find_token(puzzle)}")
        print(f"expect_output: {answers[i]}")

# test_find_token()

def main_part1():
    tokens = 0
    for puzzle in read_input("input.txt"):
        cur_puzzle_token = find_token(puzzle)
        if cur_puzzle_token > -1:
            tokens += cur_puzzle_token
    print(tokens)

# main_part1()

######### Part2 #########

def parse_one_puzzle(three_line_per_puzzle):
    pattern = r"\d+"
    A = tuple(int(i) for i in re.findall(pattern, three_line_per_puzzle[0]))
    B = tuple(int(i) for i in re.findall(pattern, three_line_per_puzzle[1]))
    goal = tuple(10000000000000 + int(i) for i in re.findall(pattern, three_line_per_puzzle[2]))
    return A, B, goal

# test_parse_one_puzzle()

def main_part2():
    tokens = 0
    for puzzle in read_input("input.txt"):
        cur_puzzle_token = find_token(puzzle)
        if cur_puzzle_token > -1:
            tokens += cur_puzzle_token
    print(tokens)

# main_part2()
