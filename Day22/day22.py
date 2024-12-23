def read_input(file_name):
    seeds = []
    with open('Day22/' + file_name, 'r') as file:
        for line in file.readlines():
            seeds.append(int(line.strip()))
    return seeds


def mix(value, secret_number):
    return value ^ secret_number

def prune(secret_number):
    return secret_number % 16777216

def generate(secret_number):
    step_one = prune(mix(secret_number << 6, secret_number))
    step_two = prune(mix(step_one >> 5, step_one))
    return prune(mix(step_two << 11, step_two))

def generate_nth(init_number, n, verbose=False):
    secret_number = init_number
    for i in range(n):
        secret_number = generate(secret_number)
        if verbose:
            print(secret_number)
    return secret_number

def test_generate_nth():
    generate_nth(123, 10, verbose=True)

# test_generate_nth()

def test_part1():
    seeds = read_input("sample.txt")
    secret_sum = 0
    for seed in seeds:
        secret_sum += generate_nth(seed, 2000)
    print(secret_sum)

# test_part1()

def main_part1():
    seeds = read_input("input.txt")
    secret_sum = 0
    for seed in seeds:
        secret_sum += generate_nth(seed, 2000)
    print(secret_sum)

# main_part1()

def generate_nth(init_number, n, verbose=False):
    secret_number = init_number
    prices = [init_number % 10]
    prices_diff = []
    for i in range(n):
        secret_number = generate(secret_number)
        prices.append(secret_number % 10)
        prices_diff.append(prices[-1] - prices[-2])
    sequence_to_price = {}
    for i in range(n-3):
        single_seq = tuple(prices_diff[i:i+4])
        if single_seq not in sequence_to_price:
            sequence_to_price[single_seq] = prices[i + 4]
    if verbose:
        print(f"prices:{prices}\nprices_diff: {prices_diff}\nsequence_to_price: {sequence_to_price}")
    return sequence_to_price

def test_generate_nth():
    generate_nth(123, 10, verbose=True)

# test_generate_nth()

def test_part2():
    sequence_to_price = {}
    seeds = read_input("sample2.txt")
    # aimed_sequence = (-2,1,-1,3)
    for seed in seeds:
        cur_sequence_to_price = generate_nth(seed, 2000)
        for sequence, price in cur_sequence_to_price.items():
            if sequence not in sequence_to_price:
                sequence_to_price[sequence] = price
            else:
                sequence_to_price[sequence] += price
        # if aimed_sequence in cur_sequence_to_price:
        #     print(cur_sequence_to_price[aimed_sequence])
    print(max(sequence_to_price.values()))

# test_part2()

def main_part2():
    sequence_to_price = {}
    seeds = read_input("input.txt")
    for seed in seeds:
        cur_sequence_to_price = generate_nth(seed, 2000)
        for sequence, price in cur_sequence_to_price.items():
            if sequence not in sequence_to_price:
                sequence_to_price[sequence] = price
            else:
                sequence_to_price[sequence] += price
    print(max(sequence_to_price.values()))

main_part2()
