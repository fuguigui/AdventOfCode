def letter_int_mp(letter):
    if letter == 'X':
        return 0
    if letter == 'M':
        return 1
    if letter == 'A':
        return 2
    if letter == 'S':
        return 3
    return 4

# Read from a file and return a matrix of integer. Where the original letter X will
# be displayed by 0, M will be displayed by 1, A will be displayed at 2 and S will
# be displayed as 3. All other letters will be dispalyed as 4.
def read_input(file_name):
    input = []
    with open('Day4/' + file_name, 'r') as file:
        for line in file.readlines():
            line_map = []
            for letter in line.strip():
                line_map.append(letter_int_mp(letter))
            input.append(line_map)
    return input

def test_read_input(file_name):
    print(read_input(file_name))

def print_matrix(input_matrix):
    print("matrix: ")
    for line in input_matrix:
        print(line)

def flip_matrix(input_matrix):
    output_matrix = []
    height = len(input_matrix)
    for i in range(height-1,-1,-1):
        new_line = input_matrix[i][::-1]
        output_matrix.append(new_line)
    # print_matrix(input_matrix)
    # print_matrix(output_matrix)
    return output_matrix

def check_first_four_letters(input):
    for i, item in enumerate(input):
        if i != item:
            return 0
    return 1

# test_read_input("sample.txt")

# Given a list of input, check if "XMAS" or the encoded [0,1,2,3] pattern appears in this list.
def check_one_line(line):
    if len(line) < 4:
        return 0
    # print(line)
    pattern_cnt = 0
    for i, item in enumerate(line[:-3]):
        if item == 0:
            pattern_cnt += check_first_four_letters(line[i:i+4])
    return pattern_cnt

def test_check_one_line(input, answer):
    print("actual output: {}".format(check_one_line(input)))
    print("expected ouput: {}".format(answer))

# test_check_one_line([1, 1, 1, 3, 0, 0, 1, 2, 3, 1], 1)

def check_horizontal(input_matrix):
    pattern_cnt = 0
    for line in input_matrix:
        pattern_cnt += check_one_line(line)
    return pattern_cnt

def test_check_horizontal(file_nanme, answer1, answer2):
    input_matrix = read_input(file_nanme)
    print("actual output: {}".format(check_horizontal(input_matrix)))
    print("expected ouput: {}".format(answer1))
    print("actual output flipped: {}".format(check_horizontal(flip_matrix(input_matrix))))
    print("expected ouput flipped: {}".format(answer2))

# test_check_horizontal("sample.txt", 3, 2)

def check_vertical(input_matrix):
    if len(input_matrix) < 1:
        return 0
    new_line_size = len(input_matrix[0])
    pattern_cnt = 0
    for vert_index in range(new_line_size):
        transformed_line = []
        for line in input_matrix:
            transformed_line.append(line[vert_index])
        pattern_cnt += check_one_line(transformed_line)
    return pattern_cnt

def test_check_vertical(file_nanme, answer1, answer2):
    input_matrix = read_input(file_nanme)
    print("actual output: {}".format(check_vertical(input_matrix)))
    print("expected ouput: {}".format(answer1))
    print("actual output flipped: {}".format(check_vertical(flip_matrix(input_matrix))))
    print("expected ouput flipped: {}".format(answer2))

# test_check_vertical("sample.txt", 1, 2)

def check_diagonal(input_matrix):
    height = len(input_matrix)
    if height < 4:
        return 0
    width = len(input_matrix[0])
    pattern_cnt = 0
    # the index of start point [[height-4,0], [height-3,0], ... [0, width-4]]
    for i in range(height-4 , 0, -1):
        transformed_line = []
        for length in range(0, height-i):
            transformed_line.append(input_matrix[i+length][length])
        pattern_cnt += check_one_line(transformed_line)
    for j in range(width - 3):
        transformed_line = []
        for length in range(0, width - j):
            transformed_line.append(input_matrix[length][j + length])
        pattern_cnt+=check_one_line(transformed_line)
    return pattern_cnt
    
def test_check_diagonal(file_nanme, answer1, answer2):
    input_matrix = read_input(file_nanme)
    print("actual output: {}".format(check_diagonal(input_matrix)))
    print("expected ouput: {}".format(answer1))
    print("actual output flipped: {}".format(check_diagonal(flip_matrix(input_matrix))))
    print("expected ouput flipped: {}".format(answer2))

# test_check_diagonal("sample.txt", 1, 4)

def check_anti_diagonal(input_matrix):
    height = len(input_matrix)
    if height < 4:
        return 0
    width = len(input_matrix[0])
    pattern_cnt = 0
    # the index of start point [[0, 3], ...,[0, width-2], [0,width-1], [1, width-1], ..., [height-4, width-1]]
    for j in range(3, width-1):
        transformed_line = []
        for length in range(j+1):
            transformed_line.append(input_matrix[length][j-length])
        pattern_cnt += check_one_line(transformed_line)
    for i in range(height - 3):
        transformed_line = []
        for length in range(height-i):
            transformed_line.append(input_matrix[i+length][width-1-length])
        pattern_cnt+=check_one_line(transformed_line)
    return pattern_cnt

def test_check_anti_diagonal(file_nanme, answer):
    input_matrix = read_input(file_nanme)
    print("actual output: {}".format(check_anti_diagonal(input_matrix)))
    print("expected ouput: {}".format(answer))

# test_check_anti_diagonal("sample.txt", 1), 4

def check_matrix(input_matrix):
    pattern_cnt = 0
    pattern_cnt += check_horizontal(input_matrix)
    pattern_cnt += check_vertical(input_matrix)
    pattern_cnt += check_diagonal(input_matrix)
    pattern_cnt += check_anti_diagonal(input_matrix)
    return pattern_cnt

def check_matrix_all_directions(input_matrix):
    return check_matrix(input_matrix) + check_matrix(flip_matrix(input_matrix))

def test_check_matrix_all_directions(file_nanme, answer):
    input_matrix = read_input(file_nanme)
    print("actual output: {}".format(check_matrix_all_directions(input_matrix)))
    print("expected ouput: {}".format(answer))

# test_check_matrix_all_directions("sample.txt", 18)
 
def main_part1():
    print(check_matrix_all_directions(read_input("input.txt")))

# main_part1()

def check_ms(upper, down):
    if upper == 1:
        return down == 3
    if upper == 3:
        return down == 1
    return False

def check_x_mas(upper_left, down_right, upper_right, down_left):
    if check_ms(upper_left, down_right) and check_ms(upper_right, down_left):
        # print("find a x-mas")
        return 1
    return 0

def locate_a(input_matrix):
    height = len(input_matrix)
    width = len(input_matrix[0])
    pattern_cnt = 0
    if height < 3 or width < 3:
        return pattern_cnt
    for i in range(1, height-1):
        for j in range(1, width - 1):
            if input_matrix[i][j] == 2:
                # print("a location: {},{}".format(i,j))
                pattern_cnt += check_x_mas(input_matrix[i-1][j-1], input_matrix[i+1][j+1], input_matrix[i-1][j+1], input_matrix[i+1][j-1])
    return pattern_cnt

def test_locate_a(file_nanme, answer):
    input_matrix = read_input(file_nanme)
    print("actual output: {}".format(locate_a(input_matrix)))
    print("expected ouput: {}".format(answer))

# test_locate_a("sample.txt", 9)

def main_part2():
    print(locate_a(read_input("input.txt")))

main_part2()
