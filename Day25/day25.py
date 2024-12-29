def parse_block(block):
    key = "lock"
    if block[0][0] == ".":
        key = "key"
    count = [0] * 5
    for i in range(1, 6):
        for j in range(5):
            if block[i][j] == "#":
                count[j] += 1
    return (key, count)

def read_input(file_name):
    locks_keys = {"lock": [], "key": []}
    with open('Day25/' + file_name, 'r') as file:
        block = []
        for line in file.readlines():
            if len(line.strip()) == 0:
                block_map = parse_block(block)
                locks_keys[block_map[0]].append(block_map[1])
                block = []
            else:
                block.append(line.strip())
    block_map = parse_block(block)
    locks_keys[block_map[0]].append(block_map[1])
    return locks_keys

def test_read_input():
    locks_keys = read_input("sample.txt")
    for key, val in locks_keys.items():
        print(key)
        print(val)

# test_read_input()

def create_key_for_lock(lock):
    return [5 - item for item in lock]

def smaller_key(first_key, second_key):
    for i in range(5):
        if first_key[i] > second_key[i]:
            return False
    return True

def test_part1():
    locks_keys = read_input("sample.txt")
    fit_cnt = 0
    for lock in locks_keys["lock"]:
        biggest_key = create_key_for_lock(lock)
        for key in locks_keys["key"]:
            if smaller_key(key, biggest_key):
                fit_cnt += 1
    print(fit_cnt)

# test_part1()

def main_part1():
    locks_keys = read_input("input.txt")
    fit_cnt = 0
    for lock in locks_keys["lock"]:
        biggest_key = create_key_for_lock(lock)
        for key in locks_keys["key"]:
            if smaller_key(key, biggest_key):
                fit_cnt += 1
    print(fit_cnt)

main_part1()