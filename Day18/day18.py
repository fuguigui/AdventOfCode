import heapq

def read_input(file_name, limit_cnt):
     corruptions = set()
     with open('Day18/' + file_name, 'r') as file:
          for line in file.readlines():
               indices = [int(i)for i in line.strip().split(',')]
               assert len(indices) == 2
               corruptions.add((indices[1], indices[0]))
               if len(corruptions) == limit_cnt:
                    return corruptions
               
def test_read_input():
     print(read_input("sample.txt", 12))

# test_read_input()

def find_next_points(cur_point, corruptions, map_size):
     next_points = []
     for index_diff in [(0, 1), (0, -1), (-1, 0), (1, 0)]:
          next_x = cur_point[1] + index_diff[0]
          next_y = cur_point[2] + index_diff[1]
          if next_x < 0 or next_x >= map_size or next_y < 0 or next_y >= map_size or (next_x, next_y) in corruptions:
               continue
          next_points.append((next_x, next_y))
     return next_points

def find_shortest_path(path_map, corruptions):
     start_point = (0, 0, 0)
     map_size = len(path_map)
     # priority queue, (shortest_step, x, y)
     cur_points = []
     heapq.heappush(cur_points, start_point)
     cnt = 0
     while cur_points: 
          cnt += 1
          cur_point = heapq.heappop(cur_points)
          if path_map[cur_point[1]][cur_point[2]] <= cur_point[0]:
               continue
          path_map[cur_point[1]][cur_point[2]] = cur_point[0]
          next_points = find_next_points(cur_point, corruptions, map_size)
          for next_point in next_points:
               if path_map[next_point[0]][next_point[1]] <= cur_point[0] + 1:
                    continue
               heapq.heappush(cur_points, (cur_point[0] + 1, next_point[0], next_point[1]))
     return path_map[-1][-1]

def build_map(size):
     biggest_value = size * size + 1
     path_map = []
     for i in range(size):
          path_map.append([biggest_value] * size)
     return path_map
               
def test_part1():
     corruptions = read_input("sample.txt", 12)
     path_map = build_map(7)
     print(find_shortest_path(path_map, corruptions))

# test_part1()
               
def main_part1():
     corruptions = read_input("input.txt", 1024)
     path_map = build_map(71)
     print(find_shortest_path(path_map, corruptions))

# main_part1()

def read_input(file_name):
     corruptions = []
     with open('Day18/' + file_name, 'r') as file:
          for line in file.readlines():
               indices = [int(i)for i in line.strip().split(',')]
               assert len(indices) == 2
               corruptions.append((indices[1], indices[0]))
     return corruptions

def search_the_key_corruption(corruptions, map_size):
     l = 0
     r = len(corruptions) - 1
     while l < r:
        middle = (l + r) // 2
        path_map = build_map(map_size)
        max_value = path_map[0][0]
        # print(f"left: {l}, middle: {middle}, right: {r}")
        latest_value = find_shortest_path(path_map, corruptions[:middle + 1])
        # print(latest_value)
        if latest_value == max_value:
             r = middle
        else:
             l = middle + 1
     return corruptions[r]

def test_part2():
     corruptions = read_input("sample.txt")
     print(search_the_key_corruption(corruptions, 7))

# test_part2()    

def main_part2():
     corruptions = read_input("input.txt")
     corruption = search_the_key_corruption(corruptions, 71)
     print(f"{corruption[1]},{corruption[0]}")

main_part2()    
     