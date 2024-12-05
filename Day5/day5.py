# the item looks like a number to a set, e.g. 1: {2,3,5}
# The value set includes all the numbers smaller than the key based on the given order definition.

def check_order(input_list, num_to_smaller_map):
    if len(input_list) <= 1:
        return True
    first_item, second_item = input_list[0], input_list[1]
    if second_item in num_to_smaller_map[first_item]:
        return False
    return check_order(input_list[1:], num_to_smaller_map)

def test_check_order():
    num_to_smaller_map = {
        13: {29, 53, 61, 47, 75, 97}, 
        29: {53, 61, 47, 75, 97},
        53: {61, 47, 75, 97},
        61: {47, 75, 97},
        47: {75, 97},
        75: {97},
        97: {}}
    input_lists = [
        [75,47,61,53,29],
        [97,61,53,29,13],
        [75,29,13],
        [75,97,47,61,53],
        [61,13,29],
        [97,13,75,29,47]
    ]
    expected_output = [True, True, True, False, False, False]
    for i, input_list in enumerate(input_lists):
        print("actual output: {}".format(check_order(input_list, num_to_smaller_map)))
        print("expected output: {}".format(expected_output[i]))

# test_check_order()

def parse_pair_list(inputs):
    pair_list = []
    for line in inputs:
        split_line = line.split("|")
        assert(len(split_line) == 2)
        pair_list.append([int(split_line[0]), int(split_line[1])])
    return pair_list

def parse_to_check_list(list):
    return [int(item) for item in list.split(",")]

def parse_to_check_lists(lists):
    parsed_lists = []
    for list in lists:
        parsed_lists.append(parse_to_check_list(list))
    return parsed_lists

def read_input(file_name):
    parsed_rules = []
    parsed_lists = []
    with open('Day5/' + file_name, 'r') as file:
        rules = []
        to_check_lists = []
        reach_break = False
        for line in file.readlines():
            cleaned_line = line.strip()
            if len(cleaned_line) == 0:
                reach_break = True
            elif not reach_break:
                rules.append(cleaned_line)
            else:
                to_check_lists.append(cleaned_line)
        parsed_rules = parse_pair_list(rules)
        parsed_lists = parse_to_check_lists(to_check_lists)
    return parsed_rules, parsed_lists

def test_read_input():
    parsed_rules, parse_lists = read_input("sample.txt")
    print("Parsed rules: {}".format(parsed_rules))
    print("Parsed lists: {}".format(parse_lists))

# test_read_input()

class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    def get_all_children_value(self):
        return [child.data for child in self.children]
    
    def __str__(self):
        return f"Node({self.data}, childrens: {self.get_all_children_value()})" 

def print_num_to_node_map(num_to_node_map):
    for node in num_to_node_map.values():
        print(node)

def get_or_insert(dictionary, key, default_value):
    value = dictionary.get(key)
    if value is None:
        dictionary[key] = default_value
        return default_value
    return value

def build_smaller_trees(pair_list):
    number_to_node_map = {}
    roots = set()
    for pair in pair_list:
        smaller_num, greater_num = pair[0], pair[1]
        # print("smaller_num: {}, greater_num: {}, roots: {}".format(smaller_num, greater_num, roots))
        if greater_num not in roots and greater_num not in number_to_node_map:
            roots.add(greater_num)
        if smaller_num in roots:
            roots.remove(smaller_num)
        print("roots: {}".format(roots))
        smaller_node = get_or_insert(number_to_node_map, smaller_num, Node(smaller_num))
        greater_node = get_or_insert(number_to_node_map, greater_num, Node(greater_num))
        greater_node.children.append(smaller_node)
    return roots, number_to_node_map

def test_build_smaller_trees():
    parsed_rules, _ = read_input("sample.txt")
    roots, num_to_node_map = build_smaller_trees(parsed_rules)
    print(roots)
    print_num_to_node_map(num_to_node_map)

# test_build_smaller_trees()

num_to_smaller_map = {} # This is a global variable.

def traverse_tree(root, number_to_node_map):
    if len(number_to_node_map[root].children) == 0:
        num_to_smaller_map[root] = {}
        # print(num_to_smaller_map)
        return
    children_set = set()
    # print("traverse for the root: {}, with childer: {}".format(root, number_to_node_map[root].get_all_children_value()))
    for child in number_to_node_map[root].children:
        # print("traverse for the child: {}".format(child.data))
        if child.data not in num_to_smaller_map:
            traverse_tree(child.data, number_to_node_map)
        children_set.add(child.data)
        children_set.union(num_to_smaller_map[child.data])
    num_to_smaller_map[root] = children_set
    # print("after traverse, num_to_smaller_map {}".format(num_to_smaller_map))
    return


def traverse_trees(roots, number_to_node_map):
    for root in roots:
        traverse_tree(root, number_to_node_map)

def build_smaller_map(pair_list):
    roots, num_to_node_map = build_smaller_trees(pair_list)
    traverse_trees(roots, num_to_node_map)
    return

def test_build_smaller_map():
    parsed_rules, _ = read_input("input.txt")
    build_smaller_map(parsed_rules)
    print(num_to_smaller_map)

# 67 | 98, 98 | 87, 87 | 67. There is a circle in the input.
test_build_smaller_map()

def get_middle_number(input_list):
    assert(len(input_list) % 2 == 1)
    return input_list[int((len(input_list) - 1 )/2)]

def test_sample():
    parsed_rules, parsed_lists = read_input("sample.txt")
    build_smaller_map(parsed_rules)
    middle_sum = 0
    for parsed_list in parsed_lists:
        if check_order(parsed_list, num_to_smaller_map):
            middle_sum += get_middle_number(parsed_list)
    print("actual output: {}".format(middle_sum))
    print("expected output: {}".format(143))


# test_sample()

def main_part1():
    parsed_rules, parsed_lists = read_input("input.txt")
    build_smaller_map(parsed_rules)
    middle_sum = 0
    for parsed_list in parsed_lists:
        if check_order(parsed_list, num_to_smaller_map):
            middle_sum += get_middle_number(parsed_list)
    print(middle_sum)

# main_part1()