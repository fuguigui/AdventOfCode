import heapq

def parse_line(line):
    encoded_line = []
    # ignore the first and last characters.
    for i in range(1, len(line) - 1):
        if line[i] == '#':
            encoded_line.append(False)
        else:
            encoded_line.append(True)
    return encoded_line

def print_map(puzzle_map):
    for line in puzzle_map:
        print(line)

def read_input(file_name):
    # read each line from right to left, instead of left to right.
    puzzle_map = []
    pre_line = []
    with open('Day16/' + file_name, 'r') as file:
        i = 0
        for line in file.readlines():
            if i < 2:
                pre_line = parse_line(line.strip())
                i += 1
                continue
            puzzle_map.append(pre_line)
            pre_line = parse_line(line.strip())
            i += 1
    return puzzle_map

def test_read_input():
    print_map(read_input("sample1.txt"))

# test_read_input()

DIR_INDEX_MAP = {'E': (0, 1), 'N': (-1, 0), 'W': (0, -1), 'S': (1, 0)}
DIR_ROTATE_MAP = {'E': ('N', 'S'), 'W': ('N', 'S'), 'N': ('E', 'W'), 'S': ('E', 'W')}

def init_lowest_scores_map(line_num, line_length):
    lowest_scores = dict()
    for direction in DIR_INDEX_MAP.keys():
        cur_dir_lowest_scores = [[-1] * line_length for i in range(line_num)]
        lowest_scores[direction] = cur_dir_lowest_scores
    lowest_scores['E'][line_num-1][0] = 0
    return lowest_scores

def test_init_lowest_scores_map():
    lowest_scores = init_lowest_scores_map(4, 6)
    for key, value in lowest_scores.items():
        print(key)
        print_map(value)

# test_init_lowest_scores_map()

def get_next_indices(cur_index, line_num, line_length, puzzle_map):
    next_indices = set()
    # get_next_indices_via_rotate
    next_directions = DIR_ROTATE_MAP[cur_index[2]]
    for next_dir in next_directions:
        next_indices.add((cur_index[0] + 1000, cur_index[1],  next_dir))
    # get_next_indices_via_move
    cur_dir_pos = DIR_INDEX_MAP[cur_index[2]]
    next_x = cur_index[1][0] + cur_dir_pos[0]
    next_y = cur_index[1][1] + cur_dir_pos[1]
    if next_x >= 0 and next_x < line_num and next_y >= 0 and next_y < line_length and puzzle_map[next_x][next_y]:
        next_indices.add((cur_index[0] + 1, (next_x, next_y), cur_index[2]))
    return next_indices

def update_lowest_scores(indices, lowest_score_records):
    good_indices = []
    for index in sorted(indices, key=lambda x: x[0]):
        x_y_index = index[1]
        cur_value = lowest_score_records[index[2]][x_y_index[0]][x_y_index[1]]
        if  cur_value == -1 or cur_value > index[0]:
            lowest_score_records[index[2]][x_y_index[0]][x_y_index[1]] = index[0]
            good_indices.append(index)
    return good_indices

def calculate_lowest_scores(puzzle_map):
    line_num = len(puzzle_map)
    line_length = len(puzzle_map[0])
    lowest_score_records = init_lowest_scores_map(line_num, line_length)

    # priority queue
    moveable_indices = [] # (score, position, direction)
    heapq.heappush(moveable_indices,  (0, (line_num-1, 0), 'E')) 
    while moveable_indices:
        cur_index = heapq.heappop(moveable_indices)
        next_reachable_indices = get_next_indices(cur_index, line_num, line_length, puzzle_map)
        next_good_indices = update_lowest_scores(next_reachable_indices, lowest_score_records)
        for next_index in next_good_indices:
            heapq.heappush(moveable_indices, next_index)
    return min([lowest_score_records[dir][0][line_length - 1] for dir in DIR_INDEX_MAP.keys()])

def test_calculate_lowest_scores():
    for example in [('sample1.txt', 7036), ('sample2.txt', 11048)]:
    # for example in [('sample1.txt', 7036)]:
        print(f"actual_output: {calculate_lowest_scores(read_input(example[0]))}")
        print(f"expect_output: {example[1]}")
    
# test_calculate_lowest_scores()

def main_part1():
    print(calculate_lowest_scores(read_input("input.txt")))

# main_part1()

def walk_back(index, dir, line_number, line_length):
    dir_index = DIR_INDEX_MAP[dir]
    pre_i = index[0] - dir_index[0]
    pre_j = index[1] - dir_index[1]
    walkable = True
    if pre_i < 0 or pre_i >= line_number or pre_j < 0 or pre_j >= line_length:
        walkable = False
    return (pre_i, pre_j), walkable

def find_next_points(lowest_score_records, start_point, line_number, line_length):
    next_points = set()
    cur_dir = start_point[0]
    cur_score = lowest_score_records[cur_dir][start_point[1][0]][start_point[1][1]]
    if cur_score < 0:
        return next_points
    same_direction_xy, walkable = walk_back(start_point[1], cur_dir, line_number, line_length)
    if walkable:
        next_score = lowest_score_records[cur_dir][same_direction_xy[0]][same_direction_xy[1]] 
        if next_score == cur_score - 1 and next_score >= 0:
            next_points.add((cur_dir, same_direction_xy))
    for next_dir in DIR_ROTATE_MAP[cur_dir]:
        diff_direction_xy, walkable = walk_back(start_point[1], next_dir, line_number, line_length)
        if not walkable:
            continue
        next_score = lowest_score_records[next_dir][diff_direction_xy[0]][diff_direction_xy[1]]
        if next_score == cur_score - 1001 and next_score >= 0:
            next_points.add((next_dir, diff_direction_xy))
    return next_points

def walk_back_best_paths(lowest_score_records, start_points, line_number, line_length, visited_xys, visited_points):
    for start_point in start_points:
        if start_point in visited_points:
            continue
        next_points = find_next_points(lowest_score_records, start_point, line_number, line_length)
        walk_back_best_paths(lowest_score_records, next_points, line_number, line_length, visited_xys, visited_points)
        visited_points.add(start_point)
        visited_xys.add(start_point[1])

def calculate_lowest_scores_part2(puzzle_map):
    line_num = len(puzzle_map)
    line_length = len(puzzle_map[0])
    lowest_score_records = init_lowest_scores_map(line_num, line_length)

    # priority queue
    moveable_indices = [] # (score, position, direction)
    heapq.heappush(moveable_indices,  (0, (line_num-1, 0), 'E')) 
    while moveable_indices:
        cur_index = heapq.heappop(moveable_indices)
        next_reachable_indices = get_next_indices(cur_index, line_num, line_length, puzzle_map)
        next_good_indices = update_lowest_scores(next_reachable_indices, lowest_score_records)
        for next_index in next_good_indices:
            heapq.heappush(moveable_indices, next_index)
    start_point = (0, line_length - 1)
    min_score = min([lowest_score_records[dir][start_point[0]][start_point[1]] for dir in DIR_INDEX_MAP.keys()])
    start_points = set()
    for dir in DIR_INDEX_MAP.keys():
        if lowest_score_records[dir][start_point[0]][start_point[1]] == min_score:
            start_points.add((dir, start_point))
    visited_points = set()
    visited_xys = set()
    walk_back_best_paths(lowest_score_records, start_points, line_num, line_length, visited_xys, visited_points)
    return len(visited_xys)

def test_calculate_lowest_scores_part2():
    for example in [('sample1.txt', 45), ('sample2.txt', 64)]:
    # for example in [('sample1.txt', 45)]:
    # for example in [('sample2.txt', 64)]:
        print(f"actual_output: {calculate_lowest_scores_part2(read_input(example[0]))}")
        print(f"expect_output: {example[1]}")
    
# test_calculate_lowest_scores_part2()

def main_part2():
    print(calculate_lowest_scores_part2(read_input("input.txt")))

main_part2()
