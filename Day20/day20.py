import heapq

def find_character_index(string, char):
  try:
    return string.index(char)
  except ValueError:
    return -1
  
def read_input(file_name):
    start_position = None
    end_position = None
    puzzles = []
    with open('Day20/' + file_name, 'r') as file:
        for line in file.readlines():
            cur_line = line.strip()
            if start_position is None:
                start_j = find_character_index(cur_line, 'S')
                if start_j != -1:
                    start_position = (len(puzzles), start_j)
            if end_position is None:
                end_j = find_character_index(cur_line, 'E')
                if end_j != -1:
                    end_position = (len(puzzles), end_j)
            puzzles.append(cur_line)
    return start_position, end_position, puzzles

def test_read_input():
    start_position, end_position, puzzles = read_input("sample.txt")
    print(start_position, end_position)

# test_read_input()

INDEX_DIFFS = [(0, 1), (0, -1), (-1, 0), (1, 0)]

def find_neighbours(cur_point, line_num, line_length):
    neighbours = []
    for index_diff in INDEX_DIFFS:
        next_x = cur_point[0] + index_diff[0]
        next_y = cur_point[1] + index_diff[1]
        if next_x < 0 or next_x >= line_num or next_y < 0 or next_y >= line_length:
            continue
        neighbours.append((next_x, next_y))
    return neighbours

def find_next_points(cur_point, puzzles, line_num, line_length):
    next_points = []
    for next_point in find_neighbours(cur_point, line_num, line_length):
        if puzzles[next_point[0]][next_point[1]] == '#':
            continue
        next_points.append(next_point)
    return next_points

def build_map(line_number, line_width):
     biggest_value = line_number * line_width + 1
     path_map = []
     for i in range(line_number):
          path_map.append([biggest_value] * line_width)
     return path_map
               
def find_path_to_end(path_map, start_index, puzzles):
    start_point = (0, start_index)
    line_num = len(path_map)
    line_width = len(path_map[0])
    # priority queue, (shortest_step, (x, y))
    cur_points = []
    heapq.heappush(cur_points, start_point)
    while cur_points: 
        cur_point = heapq.heappop(cur_points)
        cur_index = cur_point[1]
        if path_map[cur_index[0]][cur_index[1]] <= cur_point[0]:
            continue
        path_map[cur_index[0]][cur_index[1]] = cur_point[0]
        next_points = find_next_points(cur_index, puzzles, line_num, line_width)
        for next_point in next_points:
            if path_map[next_point[0]][next_point[1]] <= cur_point[0] + 1:
                continue
            heapq.heappush(cur_points, (cur_point[0] + 1,next_point))
   
def find_pre_points(cur_score, path_map, cur_point, line_num, line_length):
    pre_positions = []
    if cur_score == 0:
        return pre_positions
    for pre_point in find_neighbours(cur_point, line_num, line_length):
        if path_map[pre_point[0]][pre_point[1]] != cur_score - 1:
            continue
        pre_positions.append(pre_point)
    return pre_positions

def find_shortest_path(path_map, end_position):
    line_num = len(path_map)
    line_length = len(path_map[0])
    shortest_path_map = [[-1] * line_length for i in range(line_num)]
    cur_positions = [end_position]
    cur_score = path_map[end_position[0]][end_position[1]]
    while cur_positions:
        pre_positions = []
        for cur_position in cur_positions:
            shortest_path_map[cur_position[0]][cur_position[1]] = cur_score
            cur_pre_positions = find_pre_points(cur_score, path_map, cur_position, line_num, line_length)
            pre_positions.extend(cur_pre_positions)
        cur_positions = pre_positions
        cur_score -= 1
    return shortest_path_map

def find_second_neighbours(cur_point, line_num, line_length):
    second_neighbours = []
    for first_neighbour in find_neighbours(cur_point, line_num, line_length):
        second_neighbours.extend(find_neighbours(first_neighbour, line_num, line_length))
    return second_neighbours

def find_shortcuts(shortest_path_map, line_num, line_length, score_threshold):
    shortcuts_cnt = {}
    for i in range(line_num):
        for j in range(line_length):
            cur_score = shortest_path_map[i][j]
            if cur_score == -1:
                continue
            second_neighbours = find_second_neighbours((i, j), line_num, line_length)
            # print(f"cur_point {(i, j)}: second_neighbours: {second_neighbours}")
            for second_neighbour in second_neighbours:
                score_diff = shortest_path_map[second_neighbour[0]][second_neighbour[1]] - cur_score - 2
                if score_diff <= 0:
                    continue
                if score_diff in shortcuts_cnt:
                    shortcuts_cnt[score_diff] += 1
                else:
                    shortcuts_cnt[score_diff] = 1
                # print(f"cur_point {(i, j)}: second_neighbour: {second_neighbour}")
    # return shortcuts_cnt
    sum = 0
    for key, val in shortcuts_cnt.items():
        if key >= score_threshold:
            sum += val
    return sum

def print_map(a_map):
    for line in a_map:
        print(line)

def test_part1():
    start_position, end_position, puzzles = read_input("sample.txt")
    # print_map(puzzles)
    line_num = len(puzzles)
    line_length = len(puzzles[0])
    path_map = build_map(line_num, line_length)
    find_path_to_end(path_map, start_position, puzzles)
    # print_map(path_map)
    # print(f"start_position: {path_map[start_position[0]][start_position[1]]}")
    # print(f"end_position: {path_map[end_position[0]][end_position[1]]}")
    shortest_path_map = find_shortest_path(path_map, end_position)
    # print_map(shortest_path_map)
    print(find_shortcuts(shortest_path_map, line_num, line_length, 10))

# test_part1()

def main_part1():
    start_position, end_position, puzzles = read_input("input.txt")
    line_num = len(puzzles)
    line_length = len(puzzles[0])
    path_map = build_map(line_num, line_length)
    find_path_to_end(path_map, start_position, puzzles)
    shortest_path_map = find_shortest_path(path_map, end_position)
    print(find_shortcuts(shortest_path_map, line_num, line_length, 100))

# main_part1()

def find_further_neighbours(cur_point, line_num, line_length, limit, shortest_path_map, score_threshold):
    # (-limit, 0), (-limit + 1, -1), ... (-limit, 1), (- limit + 2, -2), ..., (limit + 2, 2), (0, -limit), .... (0, 0), (0, limit)..
    eligible_neigh_cnt = 0
    cur_score = shortest_path_map[cur_point[0]][cur_point[1]]
    for i in range(-limit, limit + 1):
        j_diff = limit - abs(i)
        for j in range(-j_diff, j_diff + 1):
            next_i = cur_point[0] + i
            next_j = cur_point[1] + j
            score_diff = abs(i) + abs(j)
            if next_i < 0 or next_i >= line_num or next_j < 0 or next_j >= line_length or shortest_path_map[next_i][next_j] - cur_score < score_diff + score_threshold:
                continue
            eligible_neigh_cnt += 1
    return eligible_neigh_cnt

def find_shortcuts(shortest_path_map, line_num, line_length, score_threshold):
    shortcuts_cnt = 0
    for i in range(line_num):
        for j in range(line_length):
            cur_score = shortest_path_map[i][j]
            if cur_score == -1:
                continue
            shortcuts_cnt += find_further_neighbours((i, j), line_num, line_length, 20, shortest_path_map, score_threshold)
    return shortcuts_cnt

def test_part2():
    start_position, end_position, puzzles = read_input("sample.txt")
    line_num = len(puzzles)
    line_length = len(puzzles[0])
    path_map = build_map(line_num, line_length)
    find_path_to_end(path_map, start_position, puzzles)
    shortest_path_map = find_shortest_path(path_map, end_position)
    for example in [(76, 3), (74, 7), (72, 29), (70, 41), (68, 55)]:
        print(f"actual_output:{find_shortcuts(shortest_path_map, line_num, line_length, example[0])}")
        print(f"expect_output:{example[1]}")

# test_part2()

def main_part2():
    start_position, end_position, puzzles = read_input("input.txt")
    line_num = len(puzzles)
    line_length = len(puzzles[0])
    path_map = build_map(line_num, line_length)
    find_path_to_end(path_map, start_position, puzzles)
    shortest_path_map = find_shortest_path(path_map, end_position)
    print(find_shortcuts(shortest_path_map, line_num, line_length, 100))

main_part2()
