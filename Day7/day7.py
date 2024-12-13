def parse_line(line):
    test_value, numbers = line.strip().split(":")
    parsed_numbers = [int(num) for num in numbers.split()]
    return int(test_value), parsed_numbers

def test_parse_line():
    line = "190: 10 19"
    print(parse_line(line))

# test_parse_line()

def get_min_max_range(numbers):
    min_range = [0] * len(numbers)
    max_range = [0] * len(numbers)
    min_range[0] = numbers[0]
    max_range[0] = numbers[0]
    for i, num in enumerate(numbers[1:]):
        min_range[i+1] = min(min_range[i] + num, min_range[i] * num)
        max_range[i+1] = max(max_range[i] + num, max_range[i] * num)
    return min_range, max_range

def get_possible_values(test_values_set, number, min_range, max_range):
    new_test_values = set()
    for cur_test_value in test_values_set:
        if cur_test_value % number == 0:
            divided = cur_test_value // number
            if divided <= max_range and divided >= min_range:
                new_test_values.add(divided)
        minused = cur_test_value - number
        if minused <= max_range and minused >= min_range:
            new_test_values.add(minused)
    return new_test_values

def check_equation_with_min_max(test_values_set, numbers, min_range, max_range, verbose=False):
    if verbose:
        print("check case for: test_value: {}, numbers: {}, min_range: {}, max_range: {}".format(test_values_set, numbers, min_range, max_range))
    if len(numbers) == 1:
        return numbers[0] in test_values_set
    last_number = numbers[-1]
    next_test_values_set = get_possible_values(test_values_set, last_number, min_range[-2], max_range[-2])
    if verbose:
        print("next possible test values: {}".format(next_test_values_set))
    if len(next_test_values_set) == 0:
        return False
    return check_equation_with_min_max(next_test_values_set, numbers[:-1], min_range[:-1], max_range[:-1], verbose)
    
def check_equation(test_value, parsed_numbers, verbose=False):
    if verbose:
        print("input: {}, {}".format(test_value, parsed_numbers))
    min_range, max_range = get_min_max_range(parsed_numbers)
    if verbose:
        print("min_range: {}".format(min_range))
        print("max_range: {}".format(max_range))
    return check_equation_with_min_max(set([test_value]), parsed_numbers, min_range, max_range, verbose=verbose)

def test_check_equation_on_sample():
    answers = [True, True, False, False, False, False, False, False, True]
    with open('Day7/sample.txt', 'r') as file:
        for line in file.readlines():
            test_value, parsed_numbers= parse_line(line)
            print("actual output: {}".format(check_equation(test_value, parsed_numbers)))
            print("expected output: {}".format(answers[cnt]))

# test_check_equation_on_sample()

def main_part1():
    with open('Day7/input.txt', 'r') as file:
        ttl_sum = 0
        for line in file.readlines():
            test_value, parsed_numbers = parse_line(line)
            if check_equation(test_value, parsed_numbers):
                ttl_sum += test_value
        print(ttl_sum)

# main_part1()

def check_equation_with_concat(test_value, parsed_numbers):
    if len(parsed_numbers) == 1:
        return test_value == parsed_numbers[0]
    if check_equation_with_concat(test_value, [parsed_numbers[0] + parsed_numbers[1]] + parsed_numbers[2:]):
        return True
    if check_equation_with_concat(test_value, [parsed_numbers[0] * parsed_numbers[1]] + parsed_numbers[2:]):
        return True
    return check_equation_with_concat(test_value, [int(str(parsed_numbers[0]) + str(parsed_numbers[1]))] + parsed_numbers[2:])

def main_part2():
    with open('Day7/input.txt', 'r') as file:
        ttl_sum = 0
        for line in file.readlines():
            test_value, parsed_numbers = parse_line(line)
            if check_equation_with_concat(test_value, parsed_numbers):
                ttl_sum += test_value
        print(ttl_sum)

# main_part2()
