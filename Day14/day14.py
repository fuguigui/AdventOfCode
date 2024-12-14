import math

def parse_index(index_str):
    numbers = index_str.split("=")[1]
    return tuple([int(i) for i in numbers.split(",")])

def parse_line(line):
    point, vel = line.strip().split(" ")
    return parse_index(point), parse_index(vel)

def test_parse_line():
    print(parse_line("p=0,4 v=3,-3"))

# test_parse_line()

def get_last_position(start_i, vel_i, max_i, steps):
    # print(f"{start_i}: {vel_i}: {max_i}, {steps}")
    last_i = (start_i + steps * vel_i) % max_i
    if last_i < 0:
        return last_i + max_i
    return last_i

def move_robot(robot, max_x, max_y, seconds):
    robot_start_point = robot[0]
    robot_velocity = robot[1]
    return (get_last_position(robot_start_point[0], robot_velocity[0], max_x, seconds), get_last_position(robot_start_point[1], robot_velocity[1], max_y, seconds))

def test_move_robot():
    with open('Day14/sample.txt', 'r') as file:
        # robots_count = [0] * 4
        for line in file.readlines():
            robot = parse_line(line)
            robot_stop = move_robot(robot, 11, 7, 100)
            print(robot_stop)

# test_move_robot()

def get_half_id(i, max_i):
    middle_i = (max_i - 1) // 2
    if i < middle_i:
        return 0
    if i > middle_i:
        return 1
    return -1

def get_quadrant_id(cur_position, max_x, max_y):
    x_half = get_half_id(cur_position[0], max_x)
    if x_half == -1:
        return -1
    y_half = get_half_id(cur_position[1], max_y)
    if y_half == -1:
        return -1
    return x_half + y_half * 2

def test_whole():
    with open('Day14/sample.txt', 'r') as file:
        robots_count = [0] * 4
        for line in file.readlines():
            robot = parse_line(line)
            robot_stop = move_robot(robot, 11, 7, 100)
            print(robot_stop)
            quadrant_id = get_quadrant_id(robot_stop, 11, 7)
            if quadrant_id >= 0:
                robots_count[quadrant_id] += 1
        print(robots_count)
    print(math.prod(robots_count))

# test_whole()

def main_part1():
    with open('Day14/input.txt', 'r') as file:
        robots_count = [0] * 4
        for line in file.readlines():
            robot = parse_line(line)
            robot_stop = move_robot(robot, 101, 103, 100)
            quadrant_id = get_quadrant_id(robot_stop, 101, 103)
            if quadrant_id >= 0:
                robots_count[quadrant_id] += 1
    print(math.prod(robots_count))

# main_part1()

# I think the easter egg means no collision.
def read_input(file_name):
    robots = []
    with open('Day14/' + file_name, 'r') as file:
        robots_count = [0] * 4
        for line in file.readlines():
            robots.append(parse_line(line))
    return robots

def main_part2():
    robots = read_input("input.txt")
    seconds = 1
    while True:
        moved_robots = set()
        for robot in robots:
            robot_stop = move_robot(robot, 101, 103, seconds)
            if robot_stop in moved_robots:
                break
            else:
                moved_robots.add(robot_stop)
        if len(moved_robots) != len(robots):
            seconds += 1
        else:
            break
    print(seconds)

main_part2()
