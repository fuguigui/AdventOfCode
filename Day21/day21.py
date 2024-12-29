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

NUMERICAL_PAD = {"7": (0, 0), "8": (0, 1), "9": (0, 2), "4": (1, 0), "5": (1, 1), "6": (1, 2), "1": (2, 0), "2": (2, 1), "3": (2, 2), "0": (3, 1), "A": (3, 2)}
DIR_PAD = {"^": (0, 1), "A": (0, 2), "<": (1, 0), "v": (1, 1), ">": (1, 2)}

def translate_diff(start_code, end_code, avoid_point):
    path = "^" * (start_code[0] - end_code[0]) + "v" * (end_code[0] - start_code[0]) + "<" * (start_code[1] - end_code[1]) + ">" * (end_code[1] - start_code[1])
    if (end_code[0], start_code[1]) == avoid_point:
        return path[::-1]
    return path

def test_translate_diff():
    print(translate_diff((2, 1), (0, 2), (3, 0)))
    print(translate_diff((2, 1), (1, 1), (3, 0)))
    print(translate_diff((0, 0), (3, 1), (3, 0)))
    print(translate_diff((3, 1), (0, 0), (3, 0)))

# test_translate_diff()

@cache
def decode_numerical_snippet(code_snippet):
    if code_snippet[0] == code_snippet[1]:
        return "A"
    start_code, end_code = NUMERICAL_PAD[code_snippet[0]], NUMERICAL_PAD[code_snippet[1]]
    return translate_diff(start_code, end_code, (3, 0)) + "A"

def test_decode_numerical_snippet():
    print(decode_numerical_snippet("29"))
    print(decode_numerical_snippet("92"))
    print(decode_numerical_snippet("01"))
    print(decode_numerical_snippet("70"))
    print(decode_numerical_snippet("77"))
    print(decode_numerical_snippet("74"))

# test_decode_numerical_snippet()

def decode_numerical(code):
    code = "A" + code
    command = ""
    for i in range(1, len(code)):
        command += decode_numerical_snippet(code[i-1: i+1])
    return command

def test_decode_numerical():
    print(decode_numerical("029A"))

# test_decode_numerical()

def decode_direction_snippet(code_snippet):
    if code_snippet[0] == code_snippet[1]:
        return "A"
    start_code, end_code = DIR_PAD[code_snippet[0]], DIR_PAD[code_snippet[1]]
    return translate_diff(start_code, end_code, (0, 0)) + "A"

def test_decode_direction_snippet():
    print(decode_direction_snippet("<A"))
    print(decode_direction_snippet("<<"))
    print(decode_direction_snippet("^<"))
    print(decode_direction_snippet(">A"))

# test_decode_direction_snippet()

@cache
def decode_direction(code):
    code = "A" + code
    command = ""
    for i in range(1, len(code)):
        command += decode_direction_snippet(code[i-1: i+1])
    return command

def test_decode_direction():
    decoded = decode_direction("<A^A>^^AvvvA")
    print(decoded)
    print(decode_direction(decoded))

# test_decode_direction()

def decode(code, r=2):
    dir_command = decode_numerical(code)
    for i in range(r):
        dir_command = decode_direction(dir_command)
    print(dir_command)
    return len(dir_command)

def test_decode():
    print(decode("029A"))

# test_decode()

def test_part1():
    codes = read_input("sample.txt")
    result = 0
    for code in codes:
        num = parse_code(code)
        code_len = decode(code)
        print(code, num, code_len)
        result += (num * code_len)
    print(result)

# test_part1()

def main_part1():
    codes = read_input("input.txt")
    result = 0
    for code in codes:
        num = parse_code(code)
        code_len = decode(code)
        print(code, num, code_len)
        result += (num * code_len)
    print(result)

main_part1()