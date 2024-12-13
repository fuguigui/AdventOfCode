import re

def read_input(file_name):
    input = ""
    with open('Day3/' + file_name, 'r') as file:
        for line in file.readlines():
            input += line.strip()
    return input

def extract_valid_expression(input):
    pattern = r"mul\(\d{1,3}\,\d{1,3}\)"
    matches = re.findall(pattern, input)
    return matches

def valid_multiply(input):
    matches = extract_valid_expression(input)
    sum = 0
    for match in matches:
        multipliers = re.findall(r"\d{1,3}", match)
        assert(len(multipliers) == 2)
        sum += int(multipliers[0]) * int(multipliers[1])
    return sum    

def valid_multiply_from_file(file_name):
    return valid_multiply(read_input(file_name))

def test_valid_multiply_from_file(file_name, answer):
    print("actual output: {}".format(valid_multiply_from_file(file_name)))
    print("expected output: {}".format(answer))
        
# test_valid_multiply_from_file("sample.txt", 161)

def main_part1():
    print(valid_multiply("input.txt"))

# main_part1()

def find_do_snippets(input):
    default_prefix_input = "do()" + input
    snippets = default_prefix_input.split("don\'t")
    do_snippets = []
    for snippet in snippets:
        do_snippet = snippet.split("do()")
        if len(do_snippet) == 1:
            continue
        do_snippets.extend(do_snippet[1:])
    return do_snippets

def do_valid_multiply(input):
    do_snippets = find_do_snippets(input)
    sum = 0
    for snippet in do_snippets:
        sum += valid_multiply(snippet)
    return sum

def do_valid_multiply_from_file(file_name):
    return do_valid_multiply(read_input(file_name))

def test_do_valid_multiply(file_name, answer):
    print("actual output: {}".format(do_valid_multiply_from_file(file_name)))
    print("expected output: {}".format(answer))

# test_do_valid_multiply("sample2.txt", 48)

def main_part2():
    print(do_valid_multiply_from_file("input.txt"))

# main_part2()
