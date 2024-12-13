def insert_in_dict(dict, key, value_list):
    if key not in dict:
        dict[key] = value_list
    else:
        dict[key].extend(value_list)

def parse_line(line_id, line):
    antennas = {}
    for i, item in enumerate(line.strip()):
        if item != ".":
            insert_in_dict(antennas, item, [(line_id, i)])
    return antennas

def test_parse_line():
    line = "...............A................vPT...L..W..e.4..."
    print(parse_line(1, line))

# test_parse_line()

def merge_list_dict(aim_map, to_insert_map):
    for key, value_list in to_insert_map.items():
        insert_in_dict(aim_map, key, value_list)

def read_input(file_name):
    antennas = {}
    with open('Day8/' + file_name, 'r') as file:
        line_id = 0
        for line in file.readlines():
            line_antennas = parse_line(line_id, line)
            line_id += 1
            merge_list_dict(antennas, line_antennas)
        line_length = len(line.strip())
        return line_id, line_length, antennas
    
def test_read_input():
    print(read_input("sample.txt"))
    
# test_read_input()

def calculate_antinodes_per_pair(first_item, second_item, height, width):
    antinodes = set()
    for pair in [(first_item, second_item), (second_item, first_item)]:
        i = pair[0][0] * 2 - pair[1][0]
        j = pair[0][1] * 2 - pair[1][1]
        if i < 0 or i >= height or j < 0 or j >= width:
            continue
        antinodes.add((i, j))
    return antinodes

def calculate_antinodes(height, width, annetas):
    antinodes = set()
    for value_list in annetas.values():
        if len(value_list) == 1:
            continue
        for i, first_item in enumerate(value_list[:-1]):
            for second_item in value_list[i+1:]:
                antinodes_per_pair = calculate_antinodes_per_pair(first_item, second_item, height, width)
                antinodes = antinodes | antinodes_per_pair
    return len(antinodes)

def test_calculate_antinodes(answer):
    height, width, annetas = read_input("sample.txt")
    print("actual output: {}".format(calculate_antinodes(height, width, annetas)))
    print("expected output: {}".format(answer))

# test_calculate_antinodes(14)

def main_part1():
    height, width, annetas = read_input("input.txt")
    print(calculate_antinodes(height, width, annetas))

# main_part1()

def calculate_antinodes_per_direction(pair, height, width, antinodes):
    start_node = pair[0]
    next_node = pair[1]
    diff_i = next_node[0] - start_node[0]
    diff_j = next_node[1] - start_node[1]
    third_i = next_node[0] + diff_i
    third_j = next_node[1] + diff_j
    if third_i < 0 or third_i >= height or third_j < 0 or third_j >= width:
        return antinodes
    third_node = (third_i, third_j)
    antinodes.add(third_node)
    return calculate_antinodes_per_direction([next_node, third_node], height, width, antinodes)

def calculate_antinodes_per_pair(first_item, second_item, height, width):
    antinodes = set()
    for pair in [(first_item, second_item), (second_item, first_item)]:
        one_direction_antinodes = calculate_antinodes_per_direction(pair, height, width, set(pair))
        antinodes = antinodes | one_direction_antinodes
    return antinodes

def test_calculate_antinodes_per_pair():
    first_item = (0, 0)
    second_item = (2, 1)
    height = 10
    width = 10
    print(calculate_antinodes_per_pair(first_item, second_item, height, width))

# test_calculate_antinodes_per_pair()

def test_calculate_antinodes_part2(file_name, answer):
    height, width, annetas = read_input(file_name)
    print("actual output: {}".format(calculate_antinodes(height, width, annetas)))
    print("expected output: {}".format(answer))

# test_calculate_antinodes_part2("sample.txt", 34)

def main_part2():
    height, width, annetas = read_input("input.txt")
    print(calculate_antinodes(height, width, annetas))

main_part2()
