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

def check_order(input_list, num_to_bigger_map):
    if len(input_list) <= 1:
        return True
    first_item, second_item = input_list[0], input_list[1]
    # print("check_order  for the list: {}".format(input_list[:2]))
    if first_item not in num_to_bigger_map or second_item not in num_to_bigger_map[first_item]:
        return False
    return check_order(input_list[1:], num_to_bigger_map)


def get_or_insert(dictionary, key, default_value):
    value = dictionary.get(key)
    if value is None:
        dictionary[key] = default_value
        return default_value
    return value

def build_num_to_bigger_map(pair_lists):
    num_to_bigger_map = {}
    for pair in pair_lists:
        bigger_set = get_or_insert(num_to_bigger_map, pair[0], set())
        if pair[1] not in bigger_set:
            bigger_set.add(pair[1])
    return num_to_bigger_map

def get_middle_number(input_list):
    assert(len(input_list) % 2 == 1)
    return input_list[int((len(input_list) - 1 )/2)]

def get_middle_sums(file_name):
    parsed_rules, parsed_lists = read_input(file_name)
    num_to_bigger_map = build_num_to_bigger_map(parsed_rules)
    # print(num_to_bigger_map)
    middle_sum = 0
    for parsed_list in parsed_lists:
        if check_order(parsed_list, num_to_bigger_map):
            middle_sum += get_middle_number(parsed_list)
    return middle_sum


def test_sample():
    print("actual output: {}".format(get_middle_sums("sample.txt")))
    print("expected output: {}".format(143))

# test_sample()

######### Part1 #########
# print(get_middle_sums("input.txt"))


######### Part2 #########

def filter_bigger_map(input_list, num_to_bigger_map):
    in_list_map = {}
    for item in input_list:
        in_list_map[item] = num_to_bigger_map[item]
    key_sets = set(in_list_map.keys())
    for item, value in in_list_map.items():
        in_list_map[item] = key_sets.intersection(value)
    return in_list_map

def get_middle_number_reordered(input_list, bigger_map, cur_index, aim_index):
    biggest_num = -1
    for key, values in bigger_map.items():
        if len(values) == 0:
            biggest_num = key
            break
    assert(biggest_num != -1)
    if cur_index == aim_index:
        return biggest_num
    new_bigger_map = {}
    new_input_list = []
    for input in input_list:
        if input == biggest_num:
            continue
        new_input_list.append(input)
        old_values = bigger_map[input]
        if biggest_num in old_values:
            old_values.remove(biggest_num)
        new_bigger_map[input] = old_values
    return get_middle_number_reordered(new_input_list, new_bigger_map, cur_index + 1, aim_index)
            

def get_middle_sums_reordered(file_name):
    parsed_rules, parsed_lists = read_input(file_name)
    num_to_bigger_map = build_num_to_bigger_map(parsed_rules)
    # print(num_to_bigger_map)
    middle_sum = 0
    for parsed_list in parsed_lists:
        if not check_order(parsed_list, num_to_bigger_map):
            filtered_bigger_map = filter_bigger_map(parsed_list, num_to_bigger_map)
            middle_sum += get_middle_number_reordered(parsed_list, filtered_bigger_map, 0, int((len(parsed_list) - 1) / 2))
    return middle_sum

print(get_middle_sums_reordered("input.txt"))
