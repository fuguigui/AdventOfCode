def parse_report(line):
    splits = line.split()
    return list(map(int, splits))

    
# Method 1
def check_report(report):
    if len(report) == 1:
        return 0
    if (report[0] == report[1]):
        return 0
    if (report[0] > report[1]):
        for i in range(0, len(report) - 1):
            diff = report[i] - report[i + 1]
            if diff < 1 or diff > 3:
                return 0
        return 1
    for i in range(len(report)-1, 0, -1):
        diff = report[i] - report[i-1]
        if diff < 1 or diff > 3:
            return 0
    return 1


# Method 2
def check_diff(diffs):
    if diffs[0] == 0:
        return 0
    if diffs[0] < 0:
        for i, diff in enumerate(diffs):
            if diff < -3 or diff > -1:
                return i
    if diffs[0] > 0:
        for i, diff in enumerate(diffs):
            if diff > 3 or diff < 1:
                return i
    # print('in check_diffs passed', diffs)
    return len(diffs)

def check_report_2(one_report):
    report_length = len(one_report)
    diffs = [0] * (report_length-1)
    for i in range(0, report_length-1):
        diffs[i] = one_report[i] - one_report[i+1]
    bad_id = check_diff(diffs)
    if bad_id == report_length - 1:
        return 1
    return 0

def count_safe_report(file_name):
    with open('Day2/' + file_name, 'r') as file:
        safe_count = 0
        for line in file:
            one_report = parse_report(line)
            report_safety = check_report(one_report)
            # report_safety = check_report_2(one_report)
            if (report_safety == 1):
                print(one_report)
            safe_count += report_safety
    return safe_count

def test_count_safe_report():
    print("actual output: {}".format(count_safe_report('sample.txt')))
    print("expected output: 2")

# test_count_safe_report()

def main_part1():
    print(count_safe_report('input.txt'))

# main_part1()

# Method 1
def check_report_with_dampener_brute_force(report):
    if (check_report(report)):
        return 1
    for i in range(len(report)):
        one_item_dropped_report = report[:i] + report[i+1:]
        if (check_report(one_item_dropped_report)):
            return 1
    return 0

# Method 2
def remove_bad_diff(old_diffs, bad_id, left_or_right):
    if left_or_right == 'l':
        if bad_id == 0:
            return old_diffs[1:]
        new_diffs = old_diffs[:bad_id-1] + [old_diffs[bad_id-1]+old_diffs[bad_id]] + old_diffs[bad_id+1:]
        return new_diffs
    if bad_id == len(old_diffs) - 1:
        return old_diffs[: bad_id]
    new_diffs = old_diffs[:bad_id] + [old_diffs[bad_id] + old_diffs[bad_id + 1]]+ old_diffs[bad_id + 2:]
    return new_diffs

def get_diff(one_report):
    report_length = len(one_report)
    diffs = [0] * (report_length-1)
    for i in range(report_length-1):
        diffs[i] = one_report[i] - one_report[i+1]
    return diffs

def check_report_with_dampener(one_report):
    report_length = len(one_report)
    diffs = get_diff(one_report)
    bad_id = check_diff(diffs)
    if bad_id == report_length - 1:
        return 1
    # The neighbour two diffs have different directions, either can be the wrong bad id.
    pre_bad_id = bad_id - 1
    good_id = report_length - 2
    if (pre_bad_id >= 0 ):
        new_diffs = remove_bad_diff(diffs, pre_bad_id, 'l')
        new_bad_id = check_diff(new_diffs)
        if new_bad_id == good_id:
            return 1
        new_diffs = remove_bad_diff(diffs, pre_bad_id, 'r')
        new_bad_id = check_diff(new_diffs)
        if new_bad_id == good_id:
            return 1
    new_diffs = remove_bad_diff(diffs, bad_id, 'l')
    new_bad_id = check_diff(new_diffs)
    if new_bad_id == good_id:
        return 1
    new_diffs = remove_bad_diff(diffs, bad_id, 'r')
    new_bad_id = check_diff(new_diffs)
    if new_bad_id == good_id:
        return 1
    return 0

def count_safe_report_with_dampener(file_name):
    with open('Day2/' + file_name, 'r') as file:
        safe_count = 0
        for line in file:
            one_report = parse_report(line)
            # safe_count += check_report_with_dampener_brute_force(one_report)
            safe_count += check_report_with_dampener(one_report)
    return safe_count


def test_count_safe_report_with_dampener():
    examples = [('sample.txt', 10), ('sample2.txt', 4)]
    for example in examples:
        print("actual output: {}".format(count_safe_report_with_dampener(example[0])))
        print("expected output: {}".format(example[1]))

# test_count_safe_report_with_dampener()

def main_part2():
    print(count_safe_report_with_dampener('input.txt'))

# main_part2()
