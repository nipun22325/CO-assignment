import sys
opcodes= {
    "00000":["A","add"], 
    "00001":["A","sub"],
    "00010":["B","mov_immediate"],
    "00011":["C","mpv_register"],
    "00100":["D","load"],
    "00101":["D", "store"],
    "00110":["A","multiply"],
    "00111":["C","divide"],
    "01000":["B","right_shift"],
    "01001":["B","left_shift"],
    "01010":["A","xor"],
    "01011":["A","or"],
    "01100":["A","and"],
    "01101":["C","inverse"],
    "01110":["C","cmp"],
    "01111":["E","unconditional_jump"],
    "11100":["E","jump_if_less_than"],
    "11101":["E","jump_if_greater_than"],
    "11111":["E","jump_if_equal"],
    "11010":["F","halt"],
    "11011":["A","expo"],
    "11100":["B","addi"],
    "11101":["B","subi"],
    "11110":["B","muli"],
    "11111":["B","divi"],
    
}

reg_dict={"000":0,"001":1,"010":2,"011":3,"100":4,"101":5, "110":6,"111":7}

def bin_to_int(binary_str):
    return int(binary_str, 2)

def int_to_bin_pc(num):
    binary_str = '{0:07b}'.format(int(num))
    return (binary_str)

def int_to_bin(num):
    binary_str='{0:016b}'.format(int(num))
    return(binary_str)

def r_shift_int(num, shift):
    s_num=num>>shift
    return s_num

def l_shift_int(num, shift):
    s_num=num<<shift
    return s_num


class Mem:
    def __init__(self):
        self.memory = ["0000000000000000"]*128

    def read(self, addr): 
        return self.memory[int(addr)]

    def write(self,addr, data):
        self.memory[int(addr)] = data

class regfile:
    def __init__(self):
        self.regs = [0] * 7  
        self.flags = [0,0,0,0]

    def read(self, reg):
        if reg == "111":
            return self.flags
        else:
            reg_num = self.regs[reg_dict[reg]]  
            return reg_num

    def write(self, reg, data):
        if reg == "111":
            self.flags = data
        else:
            self.regs[reg_dict[reg]] = data

class execute:
    def __init__(self, memory, reg_file): 
        self.memory = memory
        self.reg_file = reg_file
    
    def execute(self, instr, PC):  
        instr=instr.strip()
        opcode = instr[0:5]
        sys.stdout.write(int_to_bin_pc(PC))

        new_PC = None
        hlt = False
        if opcodes[str(opcode)][0]=="A":
            reg1=instr[7:10]
            reg2=instr[10:13]
            reg3=instr[13:]
            if opcodes[str(opcode)][1]=="add":
                sum=self.reg_file.read(reg1)+self.reg_file.read(reg3)
                if 0<sum and sum<128:
                    self.reg_file.write((reg1),self.reg_file.read(reg2)+self.reg_file.read(reg3))
                else:
                    self.reg_file.write(reg1,0)
                    self.reg_file.flags[0]=1

            elif opcodes[str(opcode)][1]=="sub":
                output=self.reg_file.read(reg2)-self.reg_file.read(reg3)
                if output<0 :
                    self.reg_file.flags[0]=1
                    self.reg_file.write(reg1,0)
                else:
                    self.reg_file.write((reg1),self.reg_file.read(reg2)-self.reg_file.read(reg3))

            elif opcodes[str(opcode)][1]=="multiply":
                output=self.reg_file.read(reg2)*self.reg_file.read(reg3)
                if output<0 or output>=128:
                    self.reg_file.flags[0]=1
                    self.reg_file.write(reg1,0)

                else:
                    self.reg_file.write(reg1,self.reg_file.read(reg2) * self.reg_file.read(reg3))
            
            elif opcodes[str(opcode)][1]=="xor":
                self.reg_file.write((reg1),self.reg_file.read(reg2 ) ^ self.reg_file.read(reg3))
            elif opcodes[str(opcode)][1]=="or":
                self.reg_file.write((reg1),self.reg_file.read(reg2) | self.reg_file.read(reg3))
            elif opcodes[str(opcode)][1]=="and":
                self.reg_file.write((reg1),self.reg_file.read(reg2) & self.reg_file.read(reg3))

        elif opcodes[str(opcode)][0]=="C":
            reg1=instr[10:13]
            reg2= instr[13:]

            if opcodes[str(opcode)][1]=="mov_reg":
                self.reg_file.write(reg1,self.reg_file.read(reg2))
            
            elif opcodes[str(opcode)][1]=="divide":
                if self.reg_file.read(reg2)==0:
                    self.reg_file.flags[0]=1
                    self.reg_file.write("000",0)
                    self.reg_file.write("001",0)
                else:
                    quotient= (self.reg_file.read(reg1))/self.reg_file.read(reg2)
                    remainder=(self.reg_file.read(reg1))%self.reg_file.read(reg2)
                    self.reg_file.write("000",quotient)
                    self.reg_file.write("001",remainder)
            
            elif opcodes[str(opcode)][1]=="inverse":
                self.reg_file.write(reg1,~(self.reg_file.read(reg2)))
            
            elif opcodes[str(opcode)][1]=="cmp":
                r1=self.reg_file.read(reg2)
                r2=self.reg_file.read(reg1)
                if r1>r2:
                    self.reg_file.flags[1]=1
                elif r1<r2:
                    self.reg_file.flags[2]=1
                else:
                    self.reg_file.flags[3]=1
            new_PC=PC+1
        

        elif opcodes[str(opcode)][0]=="D":
            reg1= instr[6:9]
            addr= instr[9:]
            if opcodes[str(opcode)][1]=="load":
                self.reg_file.write(reg1,self.memory.read(bin_to_int( addr)))
            elif opcodes[str(opcode)][1]=="store":
                self.memory.write(bin_to_int(addr),self.reg_file.read(reg1))
            new_PC=PC+1

        elif opcodes[str(opcode)][0]=="E":
            addr=instr[9:]
            if opcodes[str(opcode)][1]=="unconditional_jump":
                new_PC=bin_to_int(addr)
            elif opcodes[str(opcode)][1]=="jump_if_less_than":
                if self.reg_file.flags[2]==1:
                    new_PC=bin_to_int(addr) 
            elif opcodes[str(opcode)][1]=="jump_if_greater_than":
                if self.reg_file.flags[1]==1:
                    new_PC=bin_to_int(addr)
            elif opcodes[str(opcode)][1]=="jump_if_equal":
                if self.reg_file.flags[3]==1:
                    new_PC=bin_to_int(addr)
            else:
                new_PC=PC+1

        elif opcodes[str(opcode)][0]=="F":
            hlt=True

        sys.stdout.write("        "+str(int_to_bin(self.reg_file.read("000")))+" "+str(int_to_bin(self.reg_file.read("001")))+" "+str(int_to_bin(self.reg_file.read("010")))+" "+str(int_to_bin(self.reg_file.read("011")))+" "+str(int_to_bin(self.reg_file.read("100")))+" "+str(int_to_bin(self.reg_file.read("101")))+" "+str(int_to_bin(self.reg_file.read("110")))+" "+"0"*12+str(self.reg_file.read("111")[1])+str(self.reg_file.read("111")[1])+str(self.reg_file.read("111")[2])+str(self.reg_file.read("111")[3])+"\n")

        return hlt,new_PC


codelist=sys.stdin.readlines()

memory = Mem()
pc=0
for line in codelist:
    memory.write(pc,line)
    pc+=1
pc=0
reg_file = regfile()
engine = execute(memory, reg_file)
pc=0
hlt=False
while not hlt:
    hlt,pc=engine.execute(memory.read(pc),pc)
    if hlt:
        pc=0
        while 128-pc:
            if 128-pc!=1:
                sys.stdout.write(memory.read(pc)+"\n")
            if 128-pc==1:
                sys.stdout.write(memory.read(pc))
            pc+=1



