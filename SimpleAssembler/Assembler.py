import sys


program_counter = 0
error1 = ""
pc = -1
flag = 0


# code

def complement(binarynumber):
    ans = ""
    while binarynumber and binarynumber[-1] != "1":
        ans = binarynumber[-1] + ans
        binarynumber = binarynumber[0:-1]
    ans = binarynumber[-1] + ans
    binarynumber = binarynumber[0:-1]

    while binarynumber:
        if binarynumber[-1] == "0":
            ans = "1" + ans
        elif binarynumber[-1] == "1":
            ans = "0" + ans
        binarynumber = binarynumber[0:-1]
    return ans


def decimal_binary_32bits(b):
    a = int(b)
    if a > 0:
        ans = ""
        cnt = 0
        while a != 0:
            ans = str(a % 2) + ans
            a = a // 2
            cnt += 1
        ans = "0" * (32 - cnt) + ans
        return ans
    elif a == 0:
        answer = 32 * "0"
        return answer
    elif a < 0:
        a = abs(a)
        ans = ""
        cnt = 0
        while a != 0:
            ans = str(a % 2) + ans
            a = a // 2
            cnt += 1
        ans = "0" * (32 - cnt) + ans
        ans = complement(ans)
    return ans


opcode_R = {"add": "0110011","sub": "0110011","sll": "0110011","slt": "0110011","sltu": "0110011",
    "xor": "0110011",
    "srl": "0110011",
    "or": "0110011",
    "and": "0110011",
}
R_func7 = {
    "add": "0000000",
    "sub": "0100000",
    "sll": "0000000",
    "slt": "0000000",
    "sltu": "0000000",
    "xor": "0000000",
    "srl": "0000000",
    "or": "0000000",
    "and": "0000000",
}
R_func3 = {
    "add": "000",
    "sub": "000",
    "sll": "001",
    "slt": "010",
    "sltu": "011",
    "xor": "100",
    "srl": "101",
    "or": "110",
    "and": "111",
}
list_R = ["add", "sub", "sll", "slt", "sltu", "xor", "srl", "or", "and"]

opcode_I = {"lw": "0000011", "addi": "0010011", "sltiu": "0010011", "jalr": "1100111"}
I_func3 = {"lw": "010", "addi": "000", "sltiu": "011", "jalr": "000"}
list_I = ["lw", "addi", "sltiu", "jalr"]

opcode_B = {"beq": "1100011", "bne": "1100011", "blt": "1100011", "bge": "1100011", "bltu": "1100011", "bgeu": "1100011"}
list_B = ["beq", "bne", "blt", "bge", "bltu", "bgeu"]
B_func3 = {"beq": "000", "bne": "001", "blt": "100", "bge": "101", "bltu": "110", "bgeu": "111"}

opcode_S = {"sw": "0100011"}
S_func3 = {"sw": "010"}
list_S = ["sw"]

opcode_U = {"lui": "0110111", "auipc": "0010111"}
list_U = ["lui", "auipc"]

opcode_J = {"jal": "1101111"}
list_J = ["jal"]

register_encoding = {
    "zero": "00000",
    "ra": "00001",
    "sp": "00010",
    "gp": "00011",
    "tp": "00100",
    "t0": "00101",
    "t1": "00110",
    "t2": "00111",
    "s0": "01000",
    "fp": "01000",
    "s1": "01001",
    "a0": "01010",
    "a1": "01011",
    "a2": "01100",
    "a3": "01101",
    "a4": "01110",
    "a5": "01111",
    "a6": "10000",
    "a7": "10001",
    "s2": "10010",
    "s3": "10011",
    "s4": "10100",
    "s5": "10101",
    "s6": "10110",
    "s7": "10111",
    "s8": "11000",
    "s9": "11001",
    "s10": "11010",
    "s11": "11011",
    "t3": "11100",
    "t4": "11101",
    "t5": "11110",
    "t6": "11111",
}


def func_U(instruction):
    global program_counter, flag, error1, pc
    try:
        answer = ""
        imm_bin = decimal_binary_32bits(instruction[2])
        answer = imm_bin[:-12] + register_encoding[instruction[1]] + opcode_U[instruction[0]]
        program_counter += 4
        return answer
    except Exception as e:
        flag = 1
        error1 = "Error: " + str(e) + " in " + str(program_counter)
        pc = str(program_counter)


def func_R(instruction):
    global program_counter, flag, error1, pc
    try:
        answer = ""
        answer = (
            R_func7[instruction[0]]
            + register_encoding[instruction[3]]
            + register_encoding[instruction[2]]
            + R_func3[instruction[0]]
            + register_encoding[instruction[1]]
            + opcode_R[instruction[0]]
        )
        program_counter += 4
        return answer
    except Exception as e:
        flag = 1
        error1 = "Error: " + str(e) + " in " + str(program_counter)
        pc = str(program_counter)


def func_S(instruction):
    global program_counter, flag, error1, pc
    answer = ""
    try:
        if instruction[0] == "sw":
            instruction.append(instruction[2][-3] + instruction[2][-2])
            instruction[2] = instruction[2][0:-4]
            imm_binary = decimal_binary_32bits(instruction[2])
            answer = (
                imm_binary[-12:-5]
                + register_encoding[instruction[1]]
                + register_encoding[instruction[3]]
                + S_func3[instruction[0]]
                + imm_binary[27:32]
                + opcode_S[instruction[0]]
            )
            program_counter += 4
            return answer
        else:
            imm_binary = decimal_binary_32bits(instruction[2])
            answer = (
                imm_binary[-5:-12]
                + register_encoding[instruction[1]]
                + register_encoding[instruction[3]]
                + S_func3[instruction[0]]
                + imm_binary[29:33]
                + opcode_S[instruction[0]]
            )
            program_counter += 4
            return answer
    except Exception as e:
        flag = 1
        error1 = "Error: " + str(e) + " in " + str(program_counter)
        pc = str(program_counter)


def func_I(instruction):
    global program_counter, flag, error1, pc
    try:
        answer = ""
        if instruction[0] == "lw":
            instruction.append(instruction[2][-3] + instruction[2][-2])
            instruction[2] = instruction[2][0:-4]
            answer = (
                decimal_binary_32bits(instruction[2])[20:]
                + register_encoding[instruction[3]]
                + I_func3["lw"]
                + register_encoding[instruction[1]]
                + opcode_I[instruction[0]]
            )
        else:
            answer = (
                decimal_binary_32bits(instruction[3])[20:]
                + register_encoding[instruction[2]]
                + I_func3[instruction[0]]
                + register_encoding[instruction[1]]
                + opcode_I[instruction[0]]
            )
        program_counter += 4
        return answer
    except Exception as e:
        flag = 1
        error1 = "Error: " + str(e) + " in " + str(program_counter)
        pc = str(program_counter)


def func_J(instruction):
    global program_counter, flag, error1, pc
    try:
        answer = ""
        imm_bin = decimal_binary_32bits(instruction[2])
        answer = (
            imm_bin[11]
            + imm_bin[21:31]
            + imm_bin[20]
            + imm_bin[12:20]
            + register_encoding[instruction[1]]
            + opcode_J[instruction[0]]
        )
        program_counter += 4
        return answer
    except Exception as e:
        flag = 1
        error1 = "Error: " + str(e) + " in " + str(program_counter)
        pc = str(program_counter)


def func_B(instruction):
    global program_counter, flag, error1, pc
    try:
        answer = (
            decimal_binary_32bits(instruction[-1])[-13]
            + decimal_binary_32bits(instruction[-1])[-11:-5]
            + register_encoding[instruction[2]]
            + register_encoding[instruction[1]]
            + B_func3[instruction[0]]
            + decimal_binary_32bits(instruction[-1])[-5:-1]
            + decimal_binary_32bits(instruction[-1])[-12]
            + opcode_B[instruction[0]]
        )
        program_counter += 4
        return answer
    except Exception as e:
        flag = 1
        error1 = "Error: " + str(e) + " in " + str(program_counter)
        pc = str(program_counter)


# program starts
list1 = []

# data=sys.stdin.readlines()
# with open(r"C:\Users\HP\OneDrive\Desktop\co project\CO Project evaluation framework\automatedTesting\tests\assembly\simpleBin\test.txt","r") as file:
#     data = file.readlines()

if len(sys.argv) != 3:
    print("Usage: python3 runnerfile.py input_file output_file")
    sys.exit()

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]
with open(input_file_path, 'r') as input_file:
    data = input_file.readlines()

instruction_processed = []
for instruction in data:
    instructions = instruction.split()
    instructions[-1] = instructions[-1].split(",")
    for int1 in instructions[-1]:
        instructions.insert(-1, int1)
    instructions.pop(-1)
    instruction_processed.append(instructions)

dict = {}
dict2 = {}
for instruction_s in instruction_processed:
    if instruction_s[0][-1] == ":":
        dict[instruction_s[0][0:-1]] = program_counter
        program_counter += 4
        instruction_s.pop(0)
    else:
        program_counter += 4

if not bool(dict):
    for instruction_s in instruction_processed:
        if instruction_s[0] in list_R:
            list1.append(func_R(instruction_s))
        elif instruction_s[0] in list_I:
            list1.append(func_I(instruction_s))
        elif instruction_s[0] in list_B:
            list1.append(func_B(instruction_s))
        elif instruction_s[0] in list_S:
            list1.append(func_S(instruction_s))
        elif instruction_s[0] in list_U:
            list1.append(func_U(instruction_s))
        elif instruction_s[0] in list_J:
            list1.append(func_J(instruction_s))
else:
    program_counter = 0
    cnt = 0
    for instruction_i in instruction_processed:
        if instruction_i[-1] in list(dict.keys()):
            dict2[program_counter] = instruction_i[-1]
            program_counter += 4
        else:
            program_counter += 4

    for instruction_s in instruction_processed:
        if instruction_s[0] in list_R:
            if (
                instruction_s[-1] in list(dict.keys())
                and cnt in list(dict2.keys())
            ):
                instruction_s[-1] = str(dict[instruction_s[-1]] - cnt)
                list1.append(func_R(instruction_s))
            else:
                list1.append(func_R(instruction_s))
            cnt += 4
        elif instruction_s[0] in list_I:
            if (
                instruction_s[-1] in list(dict.keys())
                and cnt in list(dict2.keys())
            ):
                instruction_s[-1] = str(dict[instruction_s[-1]] - cnt)
                list1.append(func_I(instruction_s))
            else:
                list1.append(func_I(instruction_s))
            cnt += 4
        elif instruction_s[0] in list_B:
            if (
                instruction_s[-1] in list(dict.keys())
                and cnt in list(dict2.keys())
            ):
                instruction_s[-1] = str(dict[instruction_s[-1]] - cnt)
                list1.append(func_B(instruction_s))
            else:
                list1.append(func_B(instruction_s))
            cnt += 4
        elif instruction_s[0] in list_S:
            if (
                instruction_s[-1] in list(dict.keys())
                and cnt in list(dict2.keys())
            ):
                instruction_s[-1] = str(dict[instruction_s[-1]] - cnt)
                list1.append(func_S(instruction_s))
            else:
                list1.append(func_S(instruction_s))
            cnt += 4
        elif instruction_s[0] in list_U:
            if (
                instruction_s[-1] in list(dict.keys())
                and cnt in list(dict2.keys())
            ):
                instruction_s[-1] = str(dict[instruction_s[-1]] - cnt)
                list1.append(func_U(instruction_s))
            else:
                list1.append(func_U(instruction_s))
            cnt += 4
        elif instruction_s[0] in list_J:
            if (
                instruction_s[-1] in list(dict.keys())
                and cnt in list(dict2.keys())
            ):
                instruction_s[-1] = str(dict[instruction_s[-1]] - cnt)
                list1.append(func_J(instruction_s))
            else:
                list1.append(func_J(instruction_s))
            cnt += 4



if flag == 1:
    with open(output_file_path, 'w') as output_file:
        output_file.write(error1)
        output_file.write(pc)
else:
    with open(output_file_path, "w") as output_file:
        for i,line in enumerate(list1):
            if(i==len(list1)-1):
                output_file.write(line)
            else:
                output_file.write(line+"\n")
        


