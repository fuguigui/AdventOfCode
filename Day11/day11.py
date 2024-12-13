def read_input(file_name):
    with open('Day11/' + file_name, 'r') as file:
        stones  = [int(num) for num in file.readline().strip().split()]
        return stones
    
def test_read_input():
    print(read_input("sample.txt"))

# test_read_input()

def is_even_stone(num):
    return len(str(num)) % 2 == 0

def test_is_even_stone():
    examples = [(10, True), (111, False), (1, False), (1000, True)]
    for example in examples:
        print(f"actual_output: {is_even_stone(example[0])}")
        print(f"expect_output: {example[1]}")

# test_is_even_stone()

def split_even_stone(stone):
    stone_str = str(stone)
    half_stone_length = len(stone_str) // 2
    return int(stone_str[:half_stone_length]), int(stone_str[half_stone_length:])

def test_split_even_stone():
    examples = [(10, (1, 0)), (1112, (11, 12)), (1000, (10, 0)), (2024, (20, 24))]
    for example in examples:
        print(f"actual_output: {split_even_stone(example[0])}")
        print(f"expect_output: {example[1]}")

# test_split_even_stone()

def stone_transform(stone, left_times):
    if left_times == 0:
        return [stone]
    if stone == 0:
        return stone_transform(1, left_times - 1)
    if is_even_stone(stone):
        left_stone, right_stone = split_even_stone(stone)
        return stone_transform(left_stone, left_times - 1) + stone_transform(right_stone, left_times - 1)
    return stone_transform(stone * 2024, left_times - 1)

def main_part1():
    stones = read_input("input.txt")
    num_stones = 0
    for stone in stones:
        num_stones += len(stone_transform(stone, 25))
    print(num_stones)

# main_part1()

def stone_transform_with_memory(stone, left_times, memory):
    if (stone, left_times) in memory:
        return memory[(stone, left_times)]
    if left_times == 0:
        memory[(stone, left_times)] = 1
    elif stone == 0:
        memory[(stone, left_times)] = stone_transform_with_memory(1, left_times - 1, memory)
    elif is_even_stone(stone):
        left_stone, right_stone = split_even_stone(stone)
        memory[(stone, left_times)] = stone_transform_with_memory(left_stone, left_times - 1, memory) + stone_transform_with_memory(right_stone, left_times - 1, memory)
    else:
        memory[(stone, left_times)] = stone_transform_with_memory(stone * 2024, left_times - 1, memory)
    return memory[(stone, left_times)]

def main_part2():
    stones = read_input("input.txt")
    num_stones = 0
    memory = dict()
    for stone in stones:
        num_stones += stone_transform_with_memory(stone, 75, memory)
    print(num_stones)

# main_part2()
