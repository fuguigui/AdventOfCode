import re
import math

# Global variable: the opcode to the function map
OPCODE_FUNC_MAP = {}
REGISTERS = {'A': 0, 'B': 0, 'C': 0}
COMBO_REGISTER_MAP = {4: 'A', 5: 'B', 6: 'C'}

def init_register(line):
    pattern = r"\d+"
    name_value = line.split(':')
    value = re.findall(pattern, name_value[1])[0]
    REGISTERS[name_value[0][-1]] = int(value)

def test_init_register():
    init_register("Register A: 729")
    print(REGISTERS)
    init_register("Register B: 0")
    print(REGISTERS)
    init_register("Register A: 29")
    print(REGISTERS)

# test_init_register()

def parse_program(line):
    return [int(i) for i in line.split(": ")[1].split(",")]

def test_parse_program():
    print(parse_program("Program: 0,1,5,4,3,0"))

# test_parse_program()

def read_input(file_name):
    line_id = 0
    with open('Day17/' + file_name, 'r') as file:
        for line in file.readlines():
            line_id += 1
            if line_id < 4:
                init_register(line.strip())
            elif line_id == 4:
                continue
            else:
                return parse_program(line.strip())

def evaluate_combo(num):
    if num < 4:
        return num
    return REGISTERS[COMBO_REGISTER_MAP[num]]

def opcode_adv(num):
    # REGISTERS['A'] = math.floor(REGISTERS['A'] / ( 2** evaluate_combo(num)))
    REGISTERS['A'] >>= evaluate_combo(num)
    return None, -1

def opcode_bxl(num):
    REGISTERS['B'] ^= num
    return None, -1

def opcode_bst(num):
    REGISTERS['B'] = evaluate_combo(num) % 8
    return None, -1

def opcode_jnz(num):
    if REGISTERS['A'] == 0:
        return None, -1
    return None, num

def opcode_bxc(num):
    REGISTERS['B'] ^= REGISTERS['C']
    return None, -1

def opcode_out(num):
    return evaluate_combo(num) % 8, -1

def opcode_bdv(num):
    # REGISTERS['B'] = math.floor(REGISTERS['A'] / ( 2** evaluate_combo(num)))
    REGISTERS['B'] = REGISTERS['A'] >> evaluate_combo(num)
    return None, -1

def opcode_cdv(num):
    # REGISTERS['C'] = math.floor(REGISTERS['A'] / ( 2**  evaluate_combo(num)))
    REGISTERS['C'] = REGISTERS['A'] >> evaluate_combo(num)
    return None, -1

OPCODE_FUNC_MAP = {0: opcode_adv, 1: opcode_bxl, 2: opcode_bst, 3: opcode_jnz, 4: opcode_bxc, 5: opcode_out, 6: opcode_bdv, 7: opcode_cdv}

def perform_instructions(instructions):
    outputs = []
    ins_pointer = 0
    while ins_pointer < len(instructions):
        opcode = instructions[ins_pointer]
        operand = instructions[ins_pointer + 1]
        output, next_ins_pointer = OPCODE_FUNC_MAP[opcode](operand)
        print(opcode, operand, output, next_ins_pointer)
        print(REGISTERS)
        if output != None:
            # print(opcode, operand, output, next_ins_pointer)
            # print(REGISTERS)
            outputs.append(output)
        if next_ins_pointer == -1:
            ins_pointer += 2
        else:
            ins_pointer = next_ins_pointer
    return ",".join([str(output) for output in outputs])

def test_part1():
    for i in range(1, 7):
        program = read_input(f"sample{i}.txt")
        print(f"Testing for the {i}th example: outputs: {perform_instructions(program)}, registers: {REGISTERS}")

# test_part1()

def main_part1():
    program = read_input("input.txt")
    print(perform_instructions(program))

# main_part1()

def perform_instructions_part2(instructions):
    outputs = []
    ins_pointer = 0
    # print(f"perform_instructions_part2: {REGISTERS}, {instructions}")
    while ins_pointer < len(instructions):
        opcode = instructions[ins_pointer]
        operand = instructions[ins_pointer + 1]
        output, next_ins_pointer = OPCODE_FUNC_MAP[opcode](operand)
        if output != None:
            outputs.append(output)
        if next_ins_pointer == -1:
            ins_pointer += 2
        else:
            ins_pointer = next_ins_pointer
    return outputs

def test_perform_instructions_part2():
    program = read_input("input.txt")
    REGISTERS['A'] = 59674
    print(f"Testing for the example: outputs: {perform_instructions_part2(program)}, registers: {REGISTERS}")

# test_perform_instructions_part2()

# 2, 4: REG['B'] = (REG['A'] % 8 ) ^ 1
# 1, 1: REG['B'] = REG['B'] ^ 1
# 7, 5: REG['C'] = REG['A'] >> REG['B']
# 4, 7: REG['B'] = REG['C'] ^ REG['B']
# 1, 4: REG['B'] = REG['B'] ^ 4
# 0, 3: REG['A'] = REG['A'] >> 3
# 5, 5: REG['B'] % 8

def find_register_a(instructions, i=0, testa=0, results=[]):
    if i  == len(instructions):
        results.append(testa)
        return
    for digit in range(8):
        nexta = (testa << 3) + digit
        REGISTERS['A'] = nexta
        outputs = perform_instructions_part2(instructions)
        if outputs[-i-1] == instructions[-i - 1]:
            # print(outputs)
            find_register_a(instructions, i + 1, nexta, results)

def main_part2():
    program = read_input("input.txt")
    results = []
    find_register_a(program, 0, 0, results)
    print(min(results))

main_part2()

