def read_input(file_name):
    towels = {}
    patterns = []
    read_patterns = False
    with open('Day19/' + file_name, 'r') as file:
        for line in file.readlines():
            if read_patterns:
                patterns.append(line.strip())
            elif len(line.strip()) == 0:
                    read_patterns = True
            else:
                for towel in line.strip().split(', '):
                    if towel[0] in towels:
                        towels[towel[0]].append(towel)
                    else:
                        towels[towel[0]] = [towel]
    return towels, patterns

def find_towel_for_snippet(pattern_snippet, towels, snippet_i):
    next_is = []
    if pattern_snippet[0] not in towels:
        return next_is
    for towel in towels[pattern_snippet[0]]:
        towel_len = len(towel)
        if towel_len <= len(pattern_snippet) and pattern_snippet[:towel_len] == towel:
            next_is.append(snippet_i + towel_len)
    return next_is

def pattern_possibility(pattern, towels):
    possiblilty = [False] * (len(pattern) + 1)
    possiblilty[-1] = True
    for i in range(len(pattern) - 1, -1, -1):
        next_is = find_towel_for_snippet(pattern[i:], towels, i)
        for next_i in next_is:
            if possiblilty[next_i]:
                possiblilty[i] = True
                break
    return possiblilty[0]

def test_part1():
    towels, patterns = read_input("sample.txt")
    possible_cnt = 0
    for pattern in patterns:
        if pattern_possibility(pattern, towels):
            possible_cnt += 1
    print(possible_cnt)

# test_part1()

def main_part1():
    towels, patterns = read_input("input.txt")
    possible_cnt = 0
    for pattern in patterns:
        if pattern_possibility(pattern, towels):
            possible_cnt += 1
    print(possible_cnt)

# main_part1()

def pattern_possibility(pattern, towels):
    possiblilty = [0] * (len(pattern) + 1)
    possiblilty[-1] = 1
    for i in range(len(pattern) - 1, -1, -1):
        next_is = find_towel_for_snippet(pattern[i:], towels, i)
        for next_i in next_is:
            if possiblilty[next_i] > 0:
                possiblilty[i] += possiblilty[next_i]
    return possiblilty[0]

def test_part2():
    towels, patterns = read_input("sample.txt")
    possible_cnt = 0
    for pattern in patterns:
        possible_cnt += pattern_possibility(pattern, towels)
    print(possible_cnt)

# test_part2()

def main_part2():
    towels, patterns = read_input("input.txt")
    possible_cnt = 0
    for pattern in patterns:
        possible_cnt += pattern_possibility(pattern, towels)
    print(possible_cnt)

main_part2()
