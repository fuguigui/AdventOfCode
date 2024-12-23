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

def decode(code):
    return ""

def main_part1():
    codes = read_input("input.txt")
    result = 0
    for code in codes:
        num = parse_code(code)
        decoded_len = len(decode(code))
        result += (num * decoded_len)
    print(result)
