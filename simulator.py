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
    "01101":["C","not"],
    "01110":["C","cmp"],
    "01111":["E","unconditional_jump"],
    "11100":["E","jump_if_less_than"],
    "11101":["E","jump_if_greater_than"],
    "11111":["E","jump_if_equal"],
    "11010":["F","halt"],
    "11011":["A","expo"],#
    "11100":["B","addi"],#
    "11101":["B","subi"],#
    "11110":["B","muli"],#
    "11111":["B","divi"],#
    
}


register_dictionary={"000":0,"001":1,"010":2,"011":3,
"100":4,"101":5, "110":6,"111":7}

def int_to_binary(num):
    binary_str='{0:016b}'.format(int(num))
    return(binary_str)


def binary_to_int(binary_str):
    return int(binary_str, 2)

def int_to_binary_pc(num):
    binary_str = '{0:07b}'.format(int(num))
    return (binary_str)


def right_shift_integer(num, shift):#num is int 
    shifted_num=num>>shift
    return shifted_num


def left_shift_integer(num, shift):
    shifted_num=num<<shift
    return shifted_num


class Memory:
    def __init__(self):
        self.memory = ["0000000000000000"]*128

    def read(self, address): # we will use it to read th memory with address and address will be a integer 
        return self.memory[int(address)]

    def write(self, address, data):# we will use it to first initialize the memory
        self.memory[int(address)] = data

class RegisterFile:
    def __init__(self):
        self.registers = [0] * 7
        self.flags = [0,0,0,0]

    def read(self, register):
        if register == "111":
            return self.flags
        else:
            register_num = self.registers[register_dictionary[register]] 
            return register_num

    def write(self, register, data):
        if register == "111":
            self.flags = data
        else:
            self.registers[register_dictionary[register]] = data

class ExecutionEngine:
    def __init__(self, memory, register_file):
        self.memory = memory
        self.register_file = register_file
    
    def execute(self, instruction, PC):  
        instruction=instruction.strip()
        opcode = instruction[0:5]
        sys.stdout.write(int_to_binary_pc(PC))
        new_PC = None
        halted = False
        if opcodes[str(opcode)][0]=="A":
            reg1=instruction[7:10]
            reg2=instruction[10:13]
            reg3=instruction[13:]
            if opcodes[str(opcode)][1]=="add":
                sum=self.register_file.read(reg1)+self.register_file.read(reg3)
                if 0<sum and sum<128:
                    self.register_file.write((reg1),self.register_file.read(reg2)+self.register_file.read(reg3))
                else:
                    self.register_file.write(reg1,0)
                    self.register_file.flags[0]=1

            elif opcodes[str(opcode)][1]=="sub":
                result=self.register_file.read(reg2)-self.register_file.read(reg3)
                if result<0 :
                    self.register_file.flags[0]=1
                    self.register_file.write(reg1,0)
                else:

                    self.register_file.write((reg1),self.register_file.read(reg2)-self.register_file.read(reg3))

            elif opcodes[str(opcode)][1]=="multiply":
                result=self.register_file.read(reg2)*self.register_file.read(reg3)
                if result<0 or result>=128:
                    self.register_file.flags[0]=1
                    self.register_file.write(reg1,0)

                else:
                    self.register_file.write(reg1,self.register_file.read(reg2) * self.register_file.read(reg3))
            
            elif opcodes[str(opcode)][1]=="xor":
                self.register_file.write((reg1),self.register_file.read(reg2 ) ^ self.register_file.read(reg3))
            elif opcodes[str(opcode)][1]=="or":
                self.register_file.write((reg1),self.register_file.read(reg2) | self.register_file.read(reg3))
            elif opcodes[str(opcode)][1]=="and":
                self.register_file.write((reg1),self.register_file.read(reg2) & self.register_file.read(reg3))
                
            new_PC=PC+1


        elif opcodes[str(opcode)][0]=="B":
            reg1=instruction[6:9]
            immediate=instruction[9:]
            if opcodes[str(opcode)][1]=="mov_immediate":
                self.register_file.write(reg1,binary_to_int(immediate))
            elif opcodes[str(opcode)][1]=="right_shift":
                self.register_file.write(reg1,(right_shift_integer(self.register_file.read(reg1),binary_to_int(immediate))))
            elif opcodes[str(opcode)][1]=="left_shift":
                self.register_file.write(reg1,(left_shift_integer(self.register_file.read(reg1),binary_to_int(immediate))))
            new_PC=PC+1

        elif opcodes[str(opcode)][0]=="C":
            reg1=instruction[10:13]
            reg2= instruction[13:]

            if opcodes[str(opcode)][1]=="mov_register":
                self.register_file.write(reg1,self.register_file.read(reg2))
            
            elif opcodes[str(opcode)][1]=="divide":
                if self.register_file.read(reg2)==0:
                    self.register_file.flags[0]=1
                    self.register_file.write("000",0)
                    self.register_file.write("001",0)
                else:
                    
                    quotient= self.register_file.read(reg1)/self.register_file.read(reg2)
                    remainder=self.register_file.read(reg1)%self.register_file.read(reg2)
                    self.register_file.write("000",quotient)
                    self.register_file.write("001",remainder)
            
            elif opcodes[str(opcode)][1]=="not":
                self.register_file.write(reg1,~(self.register_file.read(reg2)))
            
            elif opcodes[str(opcode)][1]=="cmp":
                r1=self.register_file.read(reg2)
                r2=self.register_file.read(reg1)
                if r1>r2:
                    self.register_file.flags[1]=1
                elif r1<r2:
                    self.register_file.flags[2]=1
                else:
                    self.register_file.flags[3]=1
            new_PC=PC+1
        

        elif opcodes[str(opcode)][0]=="D":
            reg1= instruction[6:9]
            address= instruction[9:]
            if opcodes[str(opcode)][1]=="load":
                self.register_file.write(reg1,self.memory.read(binary_to_int( address)))
            elif opcodes[str(opcode)][1]=="store":
                self.memory.write(binary_to_int(address),self.register_file.read(reg1))
            new_PC=PC+1

        elif opcodes[str(opcode)][0]=="E":
            address=instruction[9:]
            if opcodes[str(opcode)][1]=="unconditional_jump":
                new_PC=binary_to_int(address)
            elif opcodes[str(opcode)][1]=="jump_if_less_than":
                if self.register_file.flags[2]==1:
                    new_PC=binary_to_int(address) 
            elif opcodes[str(opcode)][1]=="jump_if_greater_than":
                if self.register_file.flags[1]==1:
                    new_PC=binary_to_int(address)
            elif opcodes[str(opcode)][1]=="jump_if_equal":
                if self.register_file.flags[3]==1:
                    new_PC=binary_to_int(address)
            else:
                new_PC=PC+1

        elif opcodes[str(opcode)][0]=="F":
            halted=True

        sys.stdout.write("        "+str(int_to_binary(self.register_file.read("000")))+" "+str(int_to_binary(self.register_file.read("001")))+" "+str(int_to_binary(self.register_file.read("010")))+" "+str(int_to_binary(self.register_file.read("011")))+" "+str(int_to_binary(self.register_file.read("100")))+" "+str(int_to_binary(self.register_file.read("101")))+" "+str(int_to_binary(self.register_file.read("110")))+" "+"0"*12+str(self.register_file.read("111")[1])+str(self.register_file.read("111")[1])+str(self.register_file.read("111")[2])+str(self.register_file.read("111")[3])+"\n")
        return halted,new_PC


codelist=sys.stdin.readlines()

memory = Memory()#128 elements of storage
pc=0
for line in codelist:
    memory.write(pc,line)
    pc+=1

pc=0

register_file = RegisterFile()

engine = ExecutionEngine(memory, register_file)
pc=0
halted=False
while not halted:
    halted,pc=engine.execute(memory.read(pc),pc)
    if halted:
        pc=0
        while 128-pc:
            if 128-pc!=1:
                sys.stdout.write(str(memory.read(pc))+"\n")
            if 128-pc==1:
                sys.stdout.write(str(memory.read(pc)))

            pc+=1



