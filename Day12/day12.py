import itertools

def read_input(file_name):
     maps = []
     visit_maps = []
     with open('Day12/' + file_name, 'r') as file:
        for line in file.readlines():
            visit_maps.append([0] * len(line.strip()))
            maps.append(line.strip())
        return maps, visit_maps
    
def test_read_input():
    print(read_input("sample.txt"))

# test_read_input()

DIRECTIONS = [(0, -1), (-1, 0), (0, 1), (1, 0)]

######### Part1 #########
def is_not_valid_index(i, j, max_i, max_j):
    return i < 0 or i >= max_i or j < 0 or j >= max_j

def determin_region(i, j, maps, visit_maps, line_num, line_length):
    character = maps[i][j]
    area = 1
    perimeter = 4
    visit_maps[i][j] = 1
    for direction in DIRECTIONS:
        new_i, new_j = i + direction[0], j + direction[1]
        if is_not_valid_index(new_i, new_j, line_num, line_length):
            continue
        if maps[new_i][new_j] == character:
            perimeter -= 1
            if visit_maps[new_i][new_j] == 0:
                sub_area, sub_perimeter = determin_region(new_i, new_j, maps, visit_maps, line_num, line_length)
                area += sub_area
                perimeter += sub_perimeter
    return area, perimeter

def test_determin_region():
    maps, visit_maps = read_input("sample.txt")
    line_num = len(maps)
    line_length = len(maps[0])
    examples = [(0, 0, 12, 18), (0, 4, 4, 8), (0, 6, 14, 28), (0, 8, 10, 18)]
    for example in examples:
        area, perimeter = determin_region(example[0], example[1], maps, visit_maps, line_num, line_length)
        print(f"actual_output: {area}, {perimeter}")
        print(f"expect_output: {example[2]}, {example[3]}")
        
# test_determin_region()

def main_part1():
    maps, visit_maps = read_input("input.txt")
    line_num = len(maps)
    line_length = len(maps[0])
    price = 0
    for i in range(line_num):
        for j in range(line_length):
            # The point has been included in some region
            if visit_maps[i][j] != 0:
                continue
            area, perimeter = determin_region(i, j, maps, visit_maps, line_num, line_length)
            price += (area * perimeter)
    print(price)

# main_part1()

######### Part2 #########
def init_fence(i, j):
    block_fences = set()
    for dir in DIRECTIONS:
        block_fences.add((i, j, dir[0], dir[1]))
    return block_fences

def determin_region(i, j, maps, visit_maps, line_num, line_length):
    character = maps[i][j]
    area = 1
    fences = init_fence(i, j)
    visit_maps[i][j] = 1
    for direction in DIRECTIONS:
        new_i, new_j = i + direction[0], j + direction[1]
        if is_not_valid_index(new_i, new_j, line_num, line_length):
            continue
        if maps[new_i][new_j] == character:
            fences.remove((i, j, direction[0], direction[1]))
            if visit_maps[new_i][new_j] == 0:
                sub_area, sub_fences = determin_region(new_i, new_j, maps, visit_maps, line_num, line_length)
                area += sub_area
                fences.update(sub_fences)
    return area, fences

def test_determin_region():
    maps, visit_maps = read_input("sample.txt")
    line_num = len(maps)
    line_length = len(maps[0])
    examples = [(0, 0, 12, 18), (0, 4, 4, 8), (0, 6, 14, 28), (0, 8, 10, 18)]
    for example in examples:
        area, fences = determin_region(example[0], example[1], maps, visit_maps, line_num, line_length)
        print(f"actual_output: {area}, {len(fences)}")
        print(f"expect_output: {example[2]}, {example[3]}")
    
# test_determin_region()

def compute_sides(fences):
    sides = 0
    while fences:
        x, y, side_x, side_y = fences.pop()
        sides += 1
        for move_direction in (1, -1):
            for i in itertools.count(move_direction, move_direction):
                f = (x + i * side_y, y + i * side_x, side_x, side_y)
                if f in fences:
                    fences.remove(f)
                else:
                    break
    return sides

def test_compute_sides():
    maps, visit_maps = read_input("sample.txt")
    line_num = len(maps)
    line_length = len(maps[0])
    examples = [(0, 0, 12, 10), (0, 4, 4, 4), (0, 6, 14, 22), (0, 8, 10, 12)]
    for example in examples:
        area, fences = determin_region(example[0], example[1], maps, visit_maps, line_num, line_length)
        print(f"actual_output: {area}, {compute_sides(fences)}")
        print(f"expect_output: {example[2]}, {example[3]}")

# test_compute_sides()

def main_part2():
    maps, visit_maps = read_input("input.txt")
    line_num = len(maps)
    line_length = len(maps[0])
    price = 0
    for i in range(line_num):
        for j in range(line_length):
            if visit_maps[i][j] != 0:
                continue
            area, fences = determin_region(i, j, maps, visit_maps, line_num, line_length)
            price += (area * compute_sides(fences))
    print(price)

# main_part2()