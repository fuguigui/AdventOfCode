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

def parse_line(line, name_to_nodes):
    if ":" in line:
        split_line = line.split(":")
        name = split_line[0]
        value = int(split_line[1])
        node = Node(name, value=value)
        name_to_nodes[name] = node
    elif "->" in line:
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

def read_input(file_name):
    name_to_nodes = {}
    with open('Day24/' + file_name, 'r') as file:
        for line in file.readlines():
            parse_line(line.strip(), name_to_nodes)
    return name_to_nodes

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
    name_to_nodes = read_input("input.txt")
    result = []
    for name in name_to_nodes.keys():
        if name[0] == 'z':
            root_report = name_to_nodes[name].check_root(name[1:])
            if not root_report[0]:
                result.append(root_report[1])
    print(",".join(sorted(result)))

# main_part1()

ncw XOR btr -> z07
y07 XOR x07 -> btr
wgj OR qth -> ncw
x06 AND y06 -> wgj
qnr AND mpn -> qth
fqb OR jrk -> qnr
x06 XOR y06 -> mpn
y05 AND x05 -> fqb
skf AND qph -> jrk
x05 XOR y05 -> skf
hgw OR jjg -> qph
gwg AND ggg -> hgw
x04 AND y04 -> jjg
kfr OR wjq -> gwg
y04 XOR x04 -> ggg
y03 AND x03 -> kfr
dnk AND wcj -> wjq
x03 XOR y03 -> dnk
nvs OR nnt -> wcj
x02 AND y02 -> nvs
jvk AND jpt -> nnt
y02 XOR x02 -> jvk
npn OR jjv -> jpt
y01 AND x01 -> npn
kjh AND kkc -> jjv
y01 XOR x01 -> kjh
x00 AND y00 -> kkc

y00 XOR x00 -> z00
(y01 XOR x01 ) XOR (x00 AND y00) -> z01
kjh XOR kkc -> z01
(y02 XOR x02) XOR ((y01 AND x01) OR ((y01 XOR x01) AND (x00 AND y00))) -> z02
jvk XOR jpt -> z02
npn OR jjv -> jpt
kjh AND kkc -> jjv