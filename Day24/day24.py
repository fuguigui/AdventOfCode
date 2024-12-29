class Node:
    def __init__(self, name, value=None, children=None, op=None):
        self.name = name
        self.value = value
        self.children = children
        self.op = op

    def __str__(self) -> str:
        return f"{self.name}:value={self.value},children={self.children},op={self.op}"

    def get_value(self):
        return self.value
    
    def get_children(self):
        return self.children
    
    def add_children_op(self, children, op):
        self.children = children
        self.op = op
    
    def evaluate(self):
        if self.op == "XOR":
            self.value = self.children[0].evaluate() ^ self.children[1].evaluate()
        if self.op == "AND":
            self.value = self.children[0].evaluate() & self.children[1].evaluate()
        if self.op == "OR":
            self.value = self.children[0].evaluate() | self.children[1].evaluate()
        return self.value
    
    def get_op(self):
        return self.op
    
    def get_name(self):
        return self.name

def parse_line(line, name_to_nodes):
    if ":" in line:
        split_line = line.split(":")
        name = split_line[0]
        value = int(split_line[1])
        node = Node(name, value=value)
        name_to_nodes[name] = node
        return name, node
    if "->" in line:
        split_line = line.split("->")
        operands = split_line[0].split()
        result = split_line[1].split()
        left_operand = operands[0]
        right_operand = operands[2]
        result_name = result[0]
        left_node = None
        right_node = None
        if left_operand in name_to_nodes:
            left_node = name_to_nodes[left_operand]
        else:
            left_node = Node(left_operand)
            name_to_nodes[left_operand] = left_node
        if right_operand in name_to_nodes:
            right_node = name_to_nodes[right_operand]
        else:
            right_node = Node(right_operand)
            name_to_nodes[right_operand] = right_node
        if result_name in name_to_nodes:
            name_to_nodes[result_name].add_children_op([left_node, right_node], operands[1])
        else:
            result_node = Node(result_name, children=[left_node, right_node], op=operands[1])
            name_to_nodes[result_name] = result_node
        return result_name, result_node

def read_input(file_name):
    name_to_nodes = {}
    highest_z = 0
    with open('Day24/' + file_name, 'r') as file:
        for line in file.readlines():
            name, node = parse_line(line.strip(), name_to_nodes)
            if name[0] == 'z' and int(name[1:]) > highest_z:
                highest_z = int(name[1:])
    return name_to_nodes, highest_z

def test_read_input():
    name_to_nodes =read_input("sample.txt")
    for node in name_to_nodes.values():
        print(node)

# test_read_input()

def test_part1():
    name_to_nodes = read_input("sample.txt")
    result = 0
    for name in name_to_nodes.keys():
        if name[0] == 'z':
            bit_move = int(name[1:])
            cur_bit = name_to_nodes[name].evaluate()
            result += (cur_bit << bit_move)
    print(result)

# test_part1()

def main_part1():
    name_to_nodes, _ = read_input("input.txt")
    result = []
    for name in name_to_nodes.keys():
        if name[0] == 'z':
            root_report = name_to_nodes[name].check_root(name[1:])
            if not root_report[0]:
                result.append(root_report[1])
    print(",".join(sorted(result)))

# main_part1()

def read_input(file_name):
    highest_z = 0
    operations = []
    with open('Day24/' + file_name, 'r') as file:
        for line in file.readlines():
            if "->" not in line:
                continue
            op1, op, op2, _, res = line.strip().split(" ")
            operations.append((op1, op, op2, res))
            if res[0] == "z" and int(res[1:]) > highest_z:
                highest_z = int(res[1:])
    return operations, highest_z

def find_wrong_sets(operations, highest_z):
    wrong = set()
    for op1, op, op2, res in operations:
        if op != "XOR" and res[0] == "z" and int(res[1:]) != highest_z:
            wrong.add(res)
        if op == "AND" and "x00" not in [op1, op2]:
            for subop1, subop, subop2, _ in operations:
                if (res == subop1 or res == subop2) and subop != "OR":
                    wrong.add(res)
        if op == "XOR":
            for subop1, subop, subop2, _ in operations:
                if (res == subop1 or res == subop2) and subop == "OR":
                    wrong.add(res)
            if res[0] not in ["x", "y", "z"] and op1[0] not in ["x", "y", "z"] and op2[0] not in ["x", "y", "z"]:
                wrong.add(res)
    return wrong

def main_part2():
    operations, highest_z = read_input("input.txt")
    result = find_wrong_sets(operations, highest_z)
    print(",".join(sorted(result)))

main_part2()
