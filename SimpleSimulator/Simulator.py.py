import sys
import os

def sext(imm):
    if imm[0] == '0':
            imm = '0'*(32-len(imm)) + imm
    else:
        imm = '1'*(32-len(imm)) + imm
    return imm
def decimaltobinary(num):
    num1=num
    num=int(num1)
    if num >= 0:
        a = num
        c=""
        s = ""
        while a != 0:
            b = a%2
            d=s+str(b)
            s = s + str(b)
            d = a//2
            a=d
        s = s[::-1]
        filler = 32 - len(s)
        if filler <= 0:
            s=str('-1')
            return s
        s = filler*"0" + s
        return s
    else:
        z = abs(num)
        s = ""
        cnt = 1
        c=1
        temp = z
        while temp != 0 and c==1:
            cnt += 1
            temp = temp//2
        a = (2**cnt) - z
        while a != 0 and c==1:
            
            c=1
            s = s + str(a%2)
            a = a//2
        s = s[::-1]
        filler = 32 - len(s)
        if filler <= 0 and c==1:
            
            s='-1'
            s=str(s)
            return s
        s = filler*"1" + s
        return s 
    

def printt(imm):
    print(imm/2)
def signed_conversion(imm):
    return -(int(''.join('1' if bit == '0' else '0' for bit in imm), 2) + 1) if imm[0] == '1' else int(imm, 2)


def beq(rs1, rs2, imm, pc):
    
    if signed_conversion(sext(rs1)) != signed_conversion(sext(rs2)):
        pc += 4                               
    else:
        pc+=signed_conversion(imm)                               
    return pc


def bne(rs1, rs2, imm, pc): 
    
    
    if signed_conversion(sext(rs1)) == signed_conversion(sext(rs2)):
        pc += 4 
                                     
    else:
        pc += signed_conversion(imm)                             
    return pc

def bge(rs1, rs2, imm, pc):
    
   
    if signed_conversion(sext(rs1)) < signed_conversion(sext(rs2)):
        
        pc += 4                                
    else:
        pc += signed_conversion(imm)                              
    return pc

def blt(rs1, rs2, imm, pc):
    
    if signed_conversion(sext(rs1)) < signed_conversion(sext(rs2)):
        pc += signed_conversion(imm)                             
    else:
        pc += 4                                                                      
    return pc
def B(i, pc, reg_dic):
    ti = i[::-1]
    c=0
 
    func3=ti[12:15]
    func3 = ti[12:15][::-1]
    rs1=ti[15:20]
    rs1 = ti[15:20][::-1]
    rs2=ti[20:25]
    rs2 = ti[20:25][::-1]
    if func3 == "000" and c==0:
        pc = beq(reg_dic[rs1], reg_dic[rs2], sext(i[0] + ti[7] + i[1:7] + ti[8:12][::-1] + '0'), pc)
    if func3 == "001" and c==0:
        pc = bne(reg_dic[rs1], reg_dic[rs2], sext(i[0] + ti[7] + i[1:7] + ti[8:12][::-1] + '0'), pc)
    if func3 == "100" and c==0:
        pc = blt(reg_dic[rs1], reg_dic[rs2], sext(i[0] + ti[7] + i[1:7] + ti[8:12][::-1] + '0'), pc)
    if func3 == "101" and c==0:
        pc = bge(reg_dic[rs1], reg_dic[rs2], sext(i[0] + ti[7] + i[1:7] + ti[8:12][::-1] + '0'), pc)
    return pc                               

def add(rd, rs1, rs2, pc, reg_dic):
    
    res=signed_conversion(sext(rs1))+signed_conversion(sext(rs2))
    reg_dic[rd] = decimaltobinary(res)   
    return pc + 4                              

 
def sub(rd, rs1, rs2, pc, reg_dic):
    
    res=signed_conversion(sext(rs1))-signed_conversion(sext(rs2))
    reg_dic[rd] = decimaltobinary(res)  
    return pc + 4                              

def slt(rd, rs1, rs2, pc, reg_dic):
    if signed_conversion(sext(rs1)) < signed_conversion(sext(rs2)):
        reg_dic[rd] = decimaltobinary(1)
    return pc + 4                              
def sltu(rd, rs1, rs2, pc, reg_dic):

    if rs1 < rs2 and pc>0:
        reg_dic[rd] = decimaltobinary(1)
    return pc + 4                              
def xor(rd, rs1, rs2, pc, reg_dic):
    ra=rd
    reg_dic[ra] = decimaltobinary(rs1 ^ rs2)
    return pc + 4                              

def sll(rd, rs1, rs2, pc, reg_dic):
    rs2 = rs2[-5:]
    ra=rs2
    rb=rs1
    reg_dic[rd] = decimaltobinary(int(rb, 2) << int(ra, 2))
    return pc + 4                              


def srl(rd, rs1, rs2, pc, reg_dic):
    rs2 = rs2[-5:]          
    ra=rs2
    rb=rs1                   
    reg_dic[rd] = decimaltobinary(int(rb, 2) >> int(ra, 2))
    return pc + 4                              
def or_(rd, rs1, rs2, pc, reg_dic):
    ra=rs2
    rb=rs1      
    reg_dic[rd] = decimaltobinary(int(rb,2) | int(ra, 2))
    return pc + 4                              
def and_(rd, rs1, rs2, pc, reg_dic):
    ra=rs2
    rb=rs1      
    reg_dic[rd] = decimaltobinary(int(rb, 2) & int(ra, 2))
    return pc + 4                             

def R(i, pc, reg_dic):
    ti = i[::-1]
    rd = ti[7:12][::-1]
    rs1 = ti[15:20][::-1]
    rs2 = ti[20:25][::-1]
    funct3 = ti[12:15][::-1]
    funct7 = i[:7]  
    c=1
    if (funct3 == "000") and (funct7 == "0000000") and c==1 :
        pc = add(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "000") and (funct7 == "0100000") and c==1:
        pc = sub(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "010") and (funct7 == "0000000") and c==1:
        pc = slt(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "011") and (funct7 == "0000000") and c==1:
        pc = sltu(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "100") and (funct7 == "0000000") and c==1:
        pc = xor(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "001") and (funct7 == "0000000") and c==1:
        pc = sll(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "101") and (funct7 == "0000000") and c==1:
        pc = srl(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "110") and (funct7 == "0000000") and c==1:
        pc = or_(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    if (funct3 == "111") and (funct7 == "0000000") and c==1:
        pc = and_(rd, reg_dic[rs1], reg_dic[rs2], pc, reg_dic)
    return pc

def lw(rd, rs1, imm, pc, reg_dic, mem_dic):        
    rs1 = signed_conversion(rs1)
    rs1 = f"0x{rs1:08X}"          
    
    imm = signed_conversion(imm)
    immt = f"0x{imm:08X}"
    t= hex(int(rs1[2:], 16) + int(immt[2:], 16))
    t32 = f"0x{int(t, 16):08X}"

    
    reg_dic[rd] = mem_dic[t32.lower()]             
    return pc + 4                             
def addi(rd, rs1, imm, pc, reg_dic):
    
    reg_dic[rd] = decimaltobinary(signed_conversion(sext(rs1)) + signed_conversion(imm) )  
    return pc + 4                              

def jalr(rd, x6, imm, pc, reg_dic):
    reg_dic[rd] = decimaltobinary(pc + 4)      
    
    pc = decimaltobinary(signed_conversion(x6) + signed_conversion(imm))           
    pc = pc[:-1]
    pc+="0"
    pc = int(pc, 2)                        
    return pc 

def I(i, pc, reg_dic, mem_dic):
    ti = i[::-1]
    imm = sext(i[:12])
    func3 = ti[12:15][::-1]
 
    opcode = i[-7:]
    if (func3 == "010") and (opcode == "0000011"):
        pc = lw(ti[7:12][::-1], reg_dic[ti[15:20][::-1] ], imm, pc, reg_dic, mem_dic)
    if func3 == "000" and (opcode == "0010011"):
        pc = addi(ti[7:12][::-1], reg_dic[ti[15:20][::-1] ], imm, pc, reg_dic)
    if func3 == "000" and (opcode == "1100111"):
        pc = jalr(ti[7:12][::-1], reg_dic[ti[15:20][::-1] ], imm, pc, reg_dic)
    return pc

def S_sw(i, pc, reg_opc_to_mem_add, mem_dic):
    ti = i[::-1]
    
    
    imm = signed_conversion(sext(i[:7]+i[20:25]))
    
    rs1 = ti[15:20][::-1]                        
    rs1 = signed_conversion(sext(reg_dic[rs1]))  
    num = f"0x{rs1+imm:08X}"
    rs2 = ti[20:25][::-1]
   
    mem_dic[num.lower()] = reg_dic[rs2]
    
    return pc + 4                                                          

def lui(rd, imm, pc, reg_dic):

    reg_dic[rd] = decimaltobinary(signed_conversion(imm))  
    return pc + 4                            

def aiupc(rd, imm, pc, reg_dic):
    
   
    reg_dic[rd] = decimaltobinary(signed_conversion(imm)+pc)
    return pc + 4                           

def U(i, pc, reg_dic):
    c=0
    ti = i[::-1]
    imm = ti[12:][::-1]+"000000000000"
    rd = ti[7:12][::-1]
    opcode = i[-7:]
    if opcode == "0110111" and c==0:
        pc = lui(rd, imm, pc, reg_dic)
    if opcode == "0010111" and c==0:
        pc = aiupc(rd, imm, pc, reg_dic)
    return pc

def J_jal(i, pc, reg_dic):
    ti = i[::-1]
    
    imm = signed_conversion(sext(i[0] + ti[12:20][::-1] + ti[20] + i[1:11]))
    reg_dic[ti[7:12][::-1]] = decimaltobinary(pc + 4)     
    pc = decimaltobinary(pc + imm)           
    pc = pc[:-1] + "0"
    pc=int(pc,2)
    return pc                                                                           

def simulator(reg_dic, mem_dic, pc_dic, reg_opc_to_mem_add):
    with open(output, "w") as f:
        pc = 0
        while (int(pc) <= 252):
            inst = pc_dic[pc]
            opc = inst[25:]
            
            if inst == "00000000000000000000000001100011":
                for i in reg_dic.keys():
                    if i!="_counter":
                        f.write('0b'+reg_dic[i] + " ") 
                        
                    else:
                        f.write(reg_dic[i] + " ") 
                f.write("\n")           
                break
            if opc == "0110011" and pc>-11111:
                pc = R(inst, pc, reg_dic)
            if opc == "0000011" or opc == "0010011" or opc == "1100111" and pc>-11111:
                pc = I(inst, pc, reg_dic, mem_dic)
            if opc == "0100011" and pc>-11111:
                pc = S_sw(inst, pc, reg_opc_to_mem_add, mem_dic)
            if opc == "1100011" and pc>-11111:
                pc = B(inst, pc, reg_dic)
            if opc == "0010111" or opc == "0110111" and pc>-11111:
                pc = U(inst, pc, reg_dic)
            if opc == "1101111" and pc>-11111:
                pc = J_jal(inst, pc, reg_dic)
            
            reg_dic["_counter"] = "0b" + decimaltobinary(pc)
            
            for i in reg_dic.keys():
                if i!="_counter":
                    f.write('0b'+reg_dic[i] + " ")   
                else:
                    f.write(reg_dic[i] + " ")  
            f.write("\n")  




reg_dic = {'_counter': '0b00000000000000000000000000000000', '00000': '00000000000000000000000000000000', '00001': '00000000000000000000000000000000', '00010': '00000000000000000000000100000000', '00011': '00000000000000000000000000000000', '00100': '00000000000000000000000000000000', '00101': '00000000000000000000000000000000', '00110': '00000000000000000000000000000000', '00111': '00000000000000000000000000000000', 
    '01000': '00000000000000000000000000000000', '01001': '00000000000000000000000000000000', '01010': '00000000000000000000000000000000', '01011': '00000000000000000000000000000000', '01100': '00000000000000000000000000000000', '01101': '00000000000000000000000000000000', '01110': '00000000000000000000000000000000', '01111': '00000000000000000000000000000000', 
    '10000': '00000000000000000000000000000000', '10001': '00000000000000000000000000000000', '10010': '00000000000000000000000000000000', '10011': '00000000000000000000000000000000', '10100': '00000000000000000000000000000000', '10101': '00000000000000000000000000000000', '10110': '00000000000000000000000000000000', '10111': '00000000000000000000000000000000', 
    '11000': '00000000000000000000000000000000', '11001': '00000000000000000000000000000000', '11010': '00000000000000000000000000000000', '11011': '00000000000000000000000000000000', '11100': '00000000000000000000000000000000', '11101': '00000000000000000000000000000000', '11110': '00000000000000000000000000000000', '11111': '00000000000000000000000000000000'}

mem_dic = {}
reg_opc_to_mem_add = {}



for i in range(32):  
    address = f'0x{int(0x00010000 + i*4):08X}'.lower() 
    mem_dic[address] = '0' * 32

mem_keys = list(mem_dic.keys())

keys1 = list(reg_dic.keys())
keys1.remove('_counter')
keys2 = list(mem_dic.keys())
for key1, key2 in zip(keys1, keys2):
    reg_opc_to_mem_add[key1] = key2




input = sys.argv[1]
output = sys.argv[2]




with open(input, "r") as input_file:

    if not input_file:
        sys.exit("Input file is empty")
    x = input_file.readlines()
    pc_dic = {}
    pc = 0
    
    for line in x:
        pc_dic[pc] = line.strip("\n")
        pc += 4

simulator(reg_dic, mem_dic, pc_dic, reg_opc_to_mem_add)

f = open(output, "a")
for i in mem_dic.keys():
    f.write(i + ":" + "0b" + mem_dic[i] + "\n")
f.close()

sys.exit()
