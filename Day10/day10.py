# return the map, the zero indices, the map's number of lines and the length of each line
def read_input(file_name):
    zeros = []
    # nines = []
    map = []
    with open('Day10/' + file_name, 'r') as file:
        num_lines = 0
        for line in file.readlines():
            int_line = []
            for i, num in enumerate(line.strip()):
                int_line.append(int(num))
                if num == '0':
                    zeros.append((num_lines, i))
                # elif num == '9':
                #     nines.append((num_lines, i))
            num_lines += 1
            map.append(int_line)
    assert len(map) > 0
    return zeros, map, num_lines, len(map[0])

def test_read_input():
    print(read_input("sample.txt"))

# test_read_input()

def create_score_map(line_num, line_length):
    score_map = []
    for i in range(line_num):
        line_score_map = []
        for j in range(line_length):
            line_score_map.append(set())
        score_map.append(line_score_map)
    return score_map

DIRECTION_DIFF = ((0, 1), (1, 0), (0, -1), (-1, 0))
def find_next_points(point_value, point, hiking_map, line_num, line_length):
    next_points = []
    for next_dir in DIRECTION_DIFF:
        next_i = point[0] + next_dir[0]
        next_j = point[1] + next_dir[1]
        if next_i < 0 or next_i >= line_num or next_j < 0 or next_j >= line_length:
            continue
        if hiking_map[next_i][next_j] != (point_value + 1):
            continue
        next_points.append((next_i, next_j))
    # print(f"find_next_points for {point}")
    # print(next_points)
    return next_points

def test_find_next_points():
    samples = [[3, (2, 3), [(3, 3), (2, 2)]], [0, (6, 6), [(5, 6), (6, 7)]], [9, (6, 4), []]]
    _, hiking_map, line_num, line_length = read_input("sample.txt")
    for sample in samples:
        print("actual_output: {}".format(find_next_points(sample[0], sample[1], hiking_map, line_num, line_length)))
        print(f"expect_output: {sample[2]}")
        
# test_find_next_points()

def print_map(map):
    for line in map:
        print(line)

# The task for one point is: 1) keep going if possible; 2) return the score of this point.
def score_for_one_point(point_value, point, hiking_map, score_map, line_num, line_length):
    # print(f"current point: {point_value}: {point}")
    # print_map(score_map)
    if len(score_map[point[0]][point[1]]) > 0:
        # this point has been walked.
        return
    if point_value == 9:
        score_map[point[0]][point[1]].add(point)
        return
    for next_point in find_next_points(point_value, point, hiking_map, line_num, line_length):
        score_for_one_point(point_value + 1, next_point, hiking_map, score_map, line_num, line_length)
        score_map[point[0]][point[1]] = score_map[point[0]][point[1]] | score_map[next_point[0]][next_point[1]]
    return

def test_score_for_one_point():
    zeros, hiking_map, line_num, line_length = read_input("sample.txt")
    score_map = create_score_map(line_num, line_length)
    expected_output = [5, 6, 5, 3, 1, 3, 5, 3, 5]
    for i, zero in enumerate(zeros):
        score_for_one_point(0, zero, hiking_map, score_map, line_num, line_length)
        print(f"actual_output: {len(score_map[zero[0]][zero[1]])}")
        print(f"expect_output: {expected_output[i]}")

# test_score_for_one_point()

def main_part1():
    scores = 0
    zeros, hiking_map, line_num, line_length = read_input("input.txt")
    score_map = create_score_map(line_num, line_length)
    for zero in zeros:
        score_for_one_point(0, zero, hiking_map, score_map, line_num, line_length)
        scores += len(score_map[zero[0]][zero[1]])
    print(scores)

# main_part1()

def create_rating_map(line_num, line_length):
    rating_map = []
    for i in range(line_num):
        rating_map.append([0] * line_length)
    return rating_map

# The task for one point is: 1) keep going if possible; 2) return the score of this point.
def rating_for_one_point(point_value, point, hiking_map, rating_map, line_num, line_length):
    if rating_map[point[0]][point[1]] > 0:
        # this point has been walked.
        return rating_map[point[0]][point[1]]
    if point_value == 9:
        rating_map[point[0]][point[1]] = 1
        return 1
    for next_point in find_next_points(point_value, point, hiking_map, line_num, line_length):
        rating_map[point[0]][point[1]] += rating_for_one_point(point_value + 1, next_point, hiking_map, rating_map, line_num, line_length)
    return rating_map[point[0]][point[1]]

def test_rating_for_one_point():
    zeros, hiking_map, line_num, line_length = read_input("sample.txt")
    rating_map = create_rating_map(line_num, line_length)
    expected_output = [20, 24, 10, 4, 1, 4, 5, 8, 5]
    for i, zero in enumerate(zeros):
        print(f"actual_output: {rating_for_one_point(0, zero, hiking_map, rating_map, line_num, line_length)}")
        print(f"expect_output: {expected_output[i]}")

# test_rating_for_one_point()

def main_part2():
    scores = 0
    zeros, hiking_map, line_num, line_length = read_input("input.txt")
    rating_map = create_rating_map(line_num, line_length)
    for zero in zeros:
        scores += rating_for_one_point(0, zero, hiking_map, rating_map, line_num, line_length)
    print(scores)

main_part2()
