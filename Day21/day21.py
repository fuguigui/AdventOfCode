from functools import cache

def read_input(file_name):
    codes = []
    with open('Day21/' + file_name, 'r') as file:
        for line in file.readlines():
            codes.append(line.strip())
    return codes

def parse_code(code):
    return int(code[:-1])

def test_parse_code():
    for example in [("029A", 29), ("980A", 980), ("456A", 456)]:
        print(f"actual_output:{parse_code(example[0])}")
        print(f"expect_output:{example[1]}")

# test_parse_code()

PAD = {"7": (0, 0), "8": (0, 1), "9": (0, 2), "4": (1, 0), "5": (1, 1), "6": (1, 2), "1": (2, 0), "2": (2, 1), "3": (2, 2), "0": (3, 1), "A": (3, 2), "<": (4, 0), "v": (4, 1), ">": (4, 2)}

@cache
def decode_snippet(code_snippet):
    start_code, end_code = PAD[code_snippet[0]], PAD[code_snippet[1]]
    path = ">" * (end_code[1] - start_code[1]) + "v" * (end_code[0] - start_code[0]) + "0" * (start_code[0] - end_code[0]) + "<" * (start_code[1] - end_code[1])
    if (3, 0) in [(end_code[0], start_code[1]), (start_code[0], end_code[1])]: 
        return path + "A"
    return path[::-1] + "A"

@cache
def decode(code, r=2):
    if r < 0:
        return code
    code = "A" + code
    command = ""
    for i in range(1, len(code)):
        command += decode(decode_snippet(code[i-1: i+1]), r-1)
    return command

def test_decode():
    print(decode("029A"))

# test_decode()

def test_part1():
    codes = read_input("sample.txt")
    result = 0
    for code in codes:
        num = parse_code(code)
        decoded = decode(code)
        print(code, num, decoded)
        result += (num * len(decoded))
    print(result)

# test_part1()

def main_part1():
    codes = read_input("input.txt")
    result = 0
    for code in codes:
        num = parse_code(code)
        decoded = decode(code)
        result += (num * len(decoded))
    print(result)

# main_part1()

@cache
def decode(code, r=2):
    if r < 0:
        return len(code)
    code = "A" + code
    command_len = 0
    for i in range(1, len(code)):
        command_len += decode(decode_snippet(code[i-1: i+1]), r-1)
    return command_len

def main_part2():
    codes = read_input("input.txt")
    result = 0
    for code in codes:
        num = parse_code(code)
        code_len = decode(code, 25)
        result += (num * code_len)
    print(result)

main_part2()
