char_num_map = {'#': -1, '.': 0, 'O': 1, '@': 2}

def parse_map_line(line):
    start_col = -1
    encoded_line = []
    for col, char in enumerate(line):
        encoded_line.append(char_num_map[char])
        if char == '@':
            start_col = col
    return start_col, encoded_line

def read_input(file_name):
    warehouse_map = []
    movements = ""
    first_part = True
    start_pos = None
    with open('Day15/' + file_name, 'r') as file:
        for line in file.readlines():
            if len(line.strip()) == 0:
                first_part = False
                continue
            if first_part:
                start_col, map_line = parse_map_line(line.strip())
                if start_col != -1:
                    start_pos = (len(warehouse_map), start_col)
                warehouse_map.append(map_line)
            else:
                movements += line.strip()
    return start_pos, warehouse_map, movements

def test_read_input():
    print(read_input("sample1.txt"))
    print(read_input("sample2.txt"))

# test_read_input()

def print_map(warehouse_map):
    for line in warehouse_map:
        print(line)

move_pos_map = {'<': (0, -1), '^': (-1, 0), '>': (0, 1), 'v': (1, 0)}

def get_next_pos(start_pos, movement):
    move_pos = move_pos_map[movement]
    return (start_pos[0] + move_pos[0], start_pos[1] + move_pos[1])

def try_to_move(start_pos, movement, warehouse_map, verbose=False):
    start_code = warehouse_map[start_pos[0]][start_pos[1]]
    if start_code == char_num_map['#']:
        return start_pos, False
    if start_code == char_num_map['.']:
        return start_pos, True
    next_pos = get_next_pos(start_pos, movement)
    _, next_move_successful = try_to_move(next_pos, movement, warehouse_map)
    if next_move_successful:
        warehouse_map[next_pos[0]][next_pos[1]] = start_code
        warehouse_map[start_pos[0]][start_pos[1]] = char_num_map['.']
        return next_pos, True
    else:
        return start_pos, False

def perform_movements(start_pos, warehouse_map, movements):
    start_pos, pre_move_successful = try_to_move(start_pos, movements[0], warehouse_map)
    pre_move = movements[0]
    i = 1
    while i < len(movements):
        move_i = movements[i]
        if move_i == pre_move and not pre_move_successful:
            i += 1
            continue
        start_pos, pre_move_successful = try_to_move(start_pos, move_i, warehouse_map, False)
        pre_move = move_i
        i += 1

def test_perform_movements():
    start_pos, warehouse_map, movements = read_input("sample1.txt")
    perform_movements(start_pos, warehouse_map, movements)
    print(warehouse_map)

# test_perform_movements()

def main_part1():
    coord_sum = 0
    start_pos, warehouse_map, movements = read_input("input.txt")
    perform_movements(start_pos, warehouse_map, movements)
    for i, line in enumerate(warehouse_map):
        for j, item in enumerate(line):
            if item == char_num_map['O']:
                coord_sum += (100 * i + j)
    print(coord_sum)
    
# main_part1()

char_num_map = {'#': -1, '.': 0, '[': 1, ']': 2, '@': 3}
single_double_map = {'#': '##', '.': '..', 'O': '[]', '@': '@.'}

def parse_map_line(line):
    start_col = -1
    encoded_line = []
    for col, origin_char in enumerate(line):
        double_chars = single_double_map[origin_char]
        for char in double_chars:
            encoded_line.append(char_num_map[char])
            if char == '@':
                start_col = 2 * col
    return start_col, encoded_line
        
def test_read_input():
    print(read_input("sample1.txt"))
    print(read_input("sample2.txt"))

# test_read_input()
    
def try_to_move_horizontal(start_pos, movement, warehouse_map):
    start_code = warehouse_map[start_pos[0]][start_pos[1]]
    if start_code == char_num_map['#']:
        return start_pos, False
    if start_code == char_num_map['.']:
        return start_pos, True
    next_pos = get_next_pos(start_pos, movement)
    _, next_move_successful = try_to_move_horizontal(next_pos, movement, warehouse_map)
    if next_move_successful:
        warehouse_map[next_pos[0]][next_pos[1]] = start_code
        warehouse_map[start_pos[0]][start_pos[1]] = char_num_map['.']
        return next_pos, True
    else:
        return start_pos, False
    
def find_next_positions(pos, movement, warehouse_map):
    direct_next_pos = get_next_pos(pos, movement)
    next_code = warehouse_map[direct_next_pos[0]][direct_next_pos[1]] 
    if next_code == char_num_map['[']:
        return set([direct_next_pos, (direct_next_pos[0], direct_next_pos[1] + 1)])
    elif next_code == char_num_map[']']:
        return set([(direct_next_pos[0], direct_next_pos[1] - 1), direct_next_pos])
    return set([direct_next_pos])

def check_movibility(positions, movement, warehouse_map, verbose=False):
    next_check_positions = set()
    if verbose:
        print(f"check_movibility for {positions}")
    for pos in positions:
        for next_pos in find_next_positions(pos, movement, warehouse_map):
            if next_pos in next_check_positions:
                continue
            next_code = warehouse_map[next_pos[0]][next_pos[1]] 
            if next_code == char_num_map['#']:
                return [], False
            if next_code != char_num_map['.']:
                next_check_positions.add(next_pos)
    if len(next_check_positions) == 0:
        if verbose:
            print(f"movable!")
        return [pos for pos in positions], True
    if verbose:
        print(f"next_positions: {next_check_positions}")
    to_move_list, movibility = check_movibility(next_check_positions, movement, warehouse_map, verbose)
    if movibility:
        return to_move_list + [pos for pos in positions], True
    return [], False

def move_items(all_items, movement, warehouse_map, verbose=False):
    next_pos = (-1, -1)
    if verbose:
        print(f"move_items: for {movement}: {all_items}")
    for item in all_items:
        next_pos = get_next_pos(item, movement)
        if verbose:
            print(f"item: {item}, next_pos: {next_pos}")
        warehouse_map[next_pos[0]][next_pos[1]] = warehouse_map[item[0]][item[1]]
        warehouse_map[item[0]][item[1]] = char_num_map['.']
    if verbose:
        print("finish one move")
    return next_pos

def try_to_move_vertical(start_pos, movement, warehouse_map, verbose=False):
    all_items, movibility = check_movibility(set([start_pos]), movement, warehouse_map, verbose)
    if movibility:
        move_items(all_items, movement, warehouse_map, verbose)
        return get_next_pos(start_pos, movement), True
    return start_pos, False


def try_to_move(start_pos, movement, warehouse_map, verbose=False):
    if movement in ('<', '>'):
        return try_to_move_horizontal(start_pos, movement, warehouse_map)
    return try_to_move_vertical(start_pos, movement, warehouse_map, verbose)
    
def test_perform_movements():
    start_pos, warehouse_map, movements = read_input("sample3.txt")
    perform_movements(start_pos, warehouse_map, movements)
    print(warehouse_map)

# test_perform_movements()

def test_part2():
    coord_sum = 0
    start_pos, warehouse_map, movements = read_input("sample2.txt")
    perform_movements(start_pos, warehouse_map, movements)
    print_map(warehouse_map)
    for i, line in enumerate(warehouse_map):
        for j, item in enumerate(line):
            if item == char_num_map['[']:
                coord_sum += (100 * i + j)
    print(f"actual_output: {coord_sum}")

# test_part2()

def main_part2():
    coord_sum = 0
    start_pos, warehouse_map, movements = read_input("input.txt")
    perform_movements(start_pos, warehouse_map, movements)
    for i, line in enumerate(warehouse_map):
        for j, item in enumerate(line):
            if item == char_num_map['[']:
                coord_sum += (100 * i + j)
    print(coord_sum)

main_part2()
