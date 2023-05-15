opCodes={'add':'00000','sub':'00001','mov':['00010', '00011'],'ld':'00100','st':'00101','mul':'00110','div':'00111','rs':'01000','ls':'01001','xor':'01010','or':'01011',
         'and':'00110','not':'01101','cmp':'01110','jmp':'01111','jlt':'11100','jgt':'11101','je':'11111','hlt':'11010'}
registers={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}
labels={}
var_count=0

file=input('Enter file\'s name: ')
f1=open(file,'r')
l=f1.readlines()
l1=[]
for i in l:
    if i!='\n' and i.find(':')== -1 and i[0:3]!='var':
        l1.append(i.strip().split())
    elif i[0:3]=='var':
        var_count+=1
    #making a lookup dictionary of label definitions
    elif i.find(':') != -1 and i!='\n' and i[0:3]!='var':
        labels[i[:i.find(':')]]=l.index(i)-var_count   
        l1.append((i[i.find(':')+1:]).strip().split())

num_inst=len(l1) 
var_num=num_inst
var_dict={}

#making a lookup dictionary of declared variables
for i in l:
    if i.strip()[0:3]=='var':  
        code=f'{var_num:07b}'
        var_dict[(i.strip())[4:]]=code
        var_num+=1

#this function checks if a line is a legal instruction
def illegal_instr_handl(i):
    pass

with open('binary.txt','w') as f2:
    for i in l1:
        if illegal_instr_handl(i)==1:
            continue
        #handling type C instructions and mov reg $Imm from type B instructions
        elif len(i)==3: 
            if i[0]=='mov':
                if i[2][0]=='R' or i[2][0]=='F':
                    string=opCodes[i[0]][1]+'00000'+registers[i[1]]+registers[i[2]]+'\n'
                    f2.write(string)
                elif i[2][0]=='$':
                    string=opCodes[i[0]][0]+'0'+registers[i[1]]+f'{int(i[2][1:]):07b}'+'\n'
                    f2.write(string)
            else:
                if i[0] in ['div','not','cmp']:
                    string=opCodes[i[0]]+'00000'+registers[i[1]]+registers[i[2]]+'\n'
                    f2.write(string)
        #handling type A instructions
        elif len(i)==4:
            string=opCodes[i[0]]+'00'+registers[i[1]]+registers[i[2]]+registers[i[3]]+'\n'
            f2.write(string)

#error checking
#check for variable not declared at the beginning (error g) and check if there's statements after halt
for i in range(len(l)):
    if l[i][0:3]=='var':
        if i!=0 and l[i-1][0:3]!='var':
            print('Variables not declared at the beginning')
            break
    if l[i][0:3]=='hlt' and i!=len(l)-1:
        print('Can\'t execute lines after halt')
        break