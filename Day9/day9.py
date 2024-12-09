def compute_each_file_checksum(file_id, start_id, length, verbose=False):
    if verbose:
        print(f"Compute for file_id: {file_id}, start_from: {start_id} and length: {length}")
    return (start_id + start_id + length - 1) * length // 2 * file_id

def test_compute_each_file_checksum():
    print(compute_each_file_checksum(0, 0, 2))
    print(compute_each_file_checksum(9, 2, 2))

# test_compute_each_file_checksum()

def checksum(coimpressed_file, verbose=False):
    # left_pointer points to the digit starting from left.
    left_pointer = 0
    # right_file_pointer points to the file block starting from right.
    right_file_pointer = len(coimpressed_file) - 1
    checksum = 0
    start_id = 0
    right_length = int(coimpressed_file[-1])
    while True:
        # The current pointer points to a file digit.
        if left_pointer % 2 == 0:
            if right_file_pointer <= left_pointer:
                checksum += compute_each_file_checksum(left_pointer // 2, start_id, right_length, verbose)
                break
            else:
                left_file_length = int(coimpressed_file[left_pointer])
                checksum += compute_each_file_checksum(left_pointer // 2, start_id, left_file_length, verbose)
                start_id += left_file_length
        else:
            if right_file_pointer < left_pointer:
                break
            # The current pointer points to a blank digit.
            blank_size = int(coimpressed_file[left_pointer])
            while right_length <= blank_size:
                checksum += compute_each_file_checksum(right_file_pointer // 2, start_id, right_length, verbose)
                start_id += right_length
                blank_size -= right_length
                right_file_pointer -= 2
                if right_file_pointer < left_pointer:
                    break
                right_length = int(coimpressed_file[right_file_pointer])
            if blank_size > 0:
                checksum += compute_each_file_checksum(right_file_pointer // 2, start_id, blank_size, verbose)
                start_id += blank_size
                right_length -= blank_size
                while right_length == 0:
                    right_file_pointer -= 2
                    right_length = int(coimpressed_file[right_file_pointer])
        left_pointer += 1
    return checksum

def read_input(file_name):
    with open('Day9/' + file_name, 'r') as file:
        for line in file.readlines():
            return line.strip()

def test_checksum():
    input = read_input("sample.txt")
    print("actual output: {}".format(checksum(input, verbose=False)))
    print("expected output: {}".format(1928))

# test_checksum()

######### Part1 #########
def main_part1():
    print("actual output: {}".format(checksum(read_input("input.txt"))))

# main_part1()

######### Part2 #########

def read_input(file_name):
    with open('Day9/' + file_name, 'r') as file:
        for line in file.readlines():
            return [int(a) for a in line.strip()]
        
def test_read_input():
    print(read_input("sample.txt"))

# test_read_input()

def compute_file_start_ids(coimpressed_file):
    start_ids = [0]
    for i in range(1, len(coimpressed_file)):
        start_ids.append(coimpressed_file[i - 1] + start_ids[-1])
    return start_ids

def test_compute_file_start_ids():
    print(compute_file_start_ids(read_input("sample.txt")))

# test_compute_file_start_ids()

def try_to_move_file(file_length, possible_part):
    for i in range(len(possible_part) // 2):
        if possible_part[2 * i + 1] >= file_length:
            return 2 * i + 1
    return -1

def checksum2(coimpressed_file, verbose=False):
    right_file_pointer = len(coimpressed_file) - 1
    checksum = 0
    file_start_ids = compute_file_start_ids(coimpressed_file)
    while right_file_pointer > 0:
        file_length = coimpressed_file[right_file_pointer]
        move_to_blank_id = try_to_move_file(file_length, coimpressed_file[:right_file_pointer])
        if move_to_blank_id != -1:
            blank_start_id = file_start_ids[move_to_blank_id]
            checksum += compute_each_file_checksum(right_file_pointer // 2, blank_start_id, file_length, verbose)
            coimpressed_file[move_to_blank_id] -= file_length
            file_start_ids[move_to_blank_id] += file_length
        else:
            checksum += compute_each_file_checksum(right_file_pointer // 2, file_start_ids[right_file_pointer], file_length, verbose)
        right_file_pointer -= 2
    return checksum

def test_checksum2():
    print("actual output: {}".format(checksum2(read_input("sample.txt"), verbose=True)))
    print("expected output: {}".format(2858))
        
# test_checksum2()

def main_part2():
    print("actual output: {}".format(checksum2(read_input("input.txt"))))

main_part2()
