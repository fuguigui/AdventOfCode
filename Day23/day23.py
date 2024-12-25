def read_input(file_name):
    lans = {}
    with open('Day23/' + file_name, 'r') as file:
        for line in file.readlines():
            computers = line.strip().split('-')
            computer_a = computers[0]
            computer_b = computers[1]
            if computer_a in lans:
                lans[computer_a].add(computer_b)
            else:
                lans[computer_a] = {computer_b}
            if computer_b in lans:
                lans[computer_b].add(computer_a)
            else:
                lans[computer_b] = {computer_a}
    return lans

def find_connected_neighbours(neighbours, visited_t, lans):
    # print(neighbours, visited_t, lans)
    connected_cnt = 0
    sorted_neighours = sorted(list(neighbours))
    for neigh in sorted_neighours:
        if neigh in visited_t:
            continue
        neigh_neighbours = lans[neigh]
        valid_neigh_neighbours = neigh_neighbours - visited_t
        connected_cnt += len(neighbours.intersection(valid_neigh_neighbours))
    return connected_cnt // 2

def test_find_connected_neighbours():
    lans = read_input("sample.txt")
    for example in [('ta', 3), ('tb', 1), ('tc', 1), ('td', 3)]:
        print(f"actual_output:{find_connected_neighbours(lans[example[0]], {}, lans)}")
        print(f"expect_output:{example[1]}")
        
# test_find_connected_neighbours()

def test_part1():
    lans = read_input("sample.txt")
    visited_t = set()
    three_clusters = 0
    for computer, connections in lans.items():
        if computer[0] != 't':
            continue
        visited_t.add(computer)
        three_clusters += find_connected_neighbours(connections, visited_t, lans)
    print(three_clusters)

# test_part1()

def main_part1():
    lans = read_input("input.txt")
    visited_t = set()
    three_clusters = 0
    for computer, connections in lans.items():
        if computer[0] != 't':
            continue
        visited_t.add(computer)
        three_clusters += find_connected_neighbours(connections, visited_t, lans)
    print(three_clusters)

# main_part1()

def find_clusters(cur_computers, lans):
    cur_cluster = ""
    intersection = lans[cur_computers[0]]
    for i in range(1, len(cur_computers)):
        intersection = intersection.intersection(lans[cur_computers[i]])
    filtered_intersection = [item for item in intersection if item > cur_computers[-1]]
    if len(filtered_intersection) == 0:
        return ",".join(cur_computers)
    for next_computer in filtered_intersection:
        cur_computers.append(next_computer)
        next_cluster = find_clusters(cur_computers, lans)
        cur_computers.pop()
        if len(next_cluster) > len(cur_cluster):
            cur_cluster = next_cluster
    return cur_cluster

def test_find_clusters():
    lans = read_input("sample.txt")
    for example in [('ta', 3), ('tb', 1), ('tc', 1), ('td', 3)]:
        print(f"actual_output:{find_clusters([example[0]], lans)}")

# test_find_clusters()

def test_part2():
    lans = read_input("sample.txt")
    sorted_computers = sorted(lans.keys())
    largest_cluster = ""
    for computer in sorted_computers:
        cur_cluster = find_clusters([computer], lans)
        if len(cur_cluster) > len(largest_cluster):
            largest_cluster = cur_cluster
    print(largest_cluster)
 
# test_part2()

def main_part2():
    lans = read_input("input.txt")
    sorted_computers = sorted(lans.keys())
    largest_cluster = ""
    for computer in sorted_computers:
        cur_cluster = find_clusters([computer], lans)
        if len(cur_cluster) > len(largest_cluster):
            largest_cluster = cur_cluster
    print(largest_cluster)
 
main_part2()
