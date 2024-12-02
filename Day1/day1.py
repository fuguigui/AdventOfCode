from collections import defaultdict

def parse_line(line):
    splits = line.split()
    assert(len(splits) == 2)
    left_id = int(splits[0].strip())
    right_id = int(splits[1].strip())
    return left_id, right_id

def read_input():
    left_list = []
    right_list = []
    with open('Day1/input.txt', 'r') as file:
        for line in file:
            left_id, right_id = parse_line(line.strip())
            left_list.append(left_id)
            right_list.append(right_id)
    return left_list, right_list

def absolute_distance(left_list, right_list):
    left_list.sort()
    right_list.sort()

    distance = 0
    for i, left_id in enumerate(left_list):
        distance += abs(left_id - right_list[i])
    return distance

def test_absolute_distance():
    left_list = [3, 4, 2, 1, 3, 3]
    right_list = [4,3,5,3,9,3]
    print("actual output: {}".format(absolute_distance(left_list, right_list)))
    print("expected output: 11")

def count_frequency(numbers):
    frequency_map = defaultdict(int)
    for i in numbers:
        frequency_map[i] += 1
    return frequency_map

def similarity_score(left_list, right_list):
    left_map = count_frequency(left_list)
    right_map = count_frequency(right_list)
    score = 0
    for key, val in left_map.items():
        score += val * right_map[key] * key
    return score

def test_similarity_score():
    left_list = [3, 4, 2, 1, 3, 3]
    right_list = [4,3,5,3,9,3]
    print("actual output: {}".format(similarity_score(left_list, right_list)))
    print("expected output: 31")

######### Part1 #########
# test_absolute_distance()
# left_list, right_list = read_input()
# print(absolute_distance(left_list, right_list))

######### Part2 #########
# test_similarity_score()

left_list, right_list = read_input()
print(similarity_score(left_list, right_list))