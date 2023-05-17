opCodes={'add':'00000','sub':'00001','mov':['00010', '00011'],'ld':'00100','st':'00101','mul':'00110','div':'00111','rs':'01000','ls':'01001','xor':'01010','or':'01011',
         'and':'00110','not':'01101','cmp':'01110','jmp':'01111','jlt':'11100','jgt':'11101','je':'11111','hlt':'11010'}
registers={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}
labels={}
var_count=0
l=[]

while 1:
    line=input()
    l.append(line)
    if ':' in line and 'hlt' in line:
        continue
    if 'hlt' in line:
        break

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

#function to manage illegal instructions (a to f parts)
def illegal_instr_handl(x):
    if x[0] not in ['add','sub','mov','ld','st','mul','div','rs','ls','xor','or','and','not','cmp','jmp','jlt','jgt','je','hlt']:
        print('Invalid operand')
        return 1
    if len(x)>=3:
        if x[2][0]=='$' and not(str.isdigit(x[2][1:])):
            print(x[2][1:],'is not an integer')
    if x[0] in ['add','sub','mul','xor','or','and']:
        if len(x)!=4:
            print(x[0],'must contain 3 parameters')
            return 1
        if x[1] not in registers.keys() or x[2] not in registers.keys() or x[3] not in registers.keys():
            print('Typo in register name')
            return 1
        if x[1]=='FLAGS' or x[2]=='FLAGS' or x[3]=='FLAGS':
            print('Illegal use of FLAGS register')
            return 1
    if x[0] in ['mov','rs','ls','ld','st']:
        if len(x)!=3:
            print(x[0],'must contain 2 parameters')
            return 1
        if x[1] not in registers.keys():
            print('Typo in register name')
            return 1
        if x[1]=='FLAGS':
            print('Illegal use of FLAGS register')
            return 1
        if x[0]=='mov':
            if x[2][0]!='$' and x[2] not in var_dict.keys() and x[2][0] not in ['R','F']:
                if not(str.isdigit(x[2])):
                    print('No variable named',x[2])
                    return 1
                else:
                    print('Wrong syntax, use $ symbol before immediate value')
                    return 1
    if x[0] in ['div','not','cmp']:
        if len(x)!=3:
            print(x[0],'must contain 2 parameters')
            return 1
        if x[1] not in registers.keys() or x[2] not in registers.keys():
            print('Typo in register name')
            return 1
        if x[1]=='FLAGS' or x[2]=='FLAGS':
            print('Illegal use of FLAGS register')
            return 1
    if x[0] in ['ld','st']:
        if x[2] in labels.keys():
            print('Misuse of labels as variables')
            return 1 
        elif x[2] not in var_dict.keys():
            print('Use of undefined variable',x[2]) 
            return 1
    if x[0] in ['jmp','jlt','jgt','je']:
        if len(x)!=2:
            print(x[0],'must contain 1 parameter')
            return 1
        if x[1] in var_dict.keys():
            print('Misuse of variables as labels') 
            return 1
        elif x[1] not in labels.keys():
            print('Use of undefined label',x[1])
            return 1
    if x[0] in ['mov','rs','ls']:
        if x[2][0]=='$':
            if int(x[2][1:])<0 or int(x[2][1:])>127:
                print('Illegal Immediate values (more than 7 bits/negative number)')
                return 1
    if x[0]=='hlt' and len(x)>1:
        print(x[0],'must contain no parameters')
        return 1
    return 0

hlt_count=0

#check for variable not declared at the beginning (error g) and check if there's statements after halt
for i in range(len(l)):
    if l[i][0:3]=='var':
        if i!=0 and l[i-1][0:3]!='var':
            print('Variables not declared at the beginning')
            break
    if l[i][0:3]=='hlt' and i!=len(l)-1:
        print('Can\'t execute lines after halt')
        break

# writing binary of supported instructions
with open('binary.txt','w') as f2:
    for i in l1:
        if illegal_instr_handl(i)==1:
            continue    
        if len(i)==1:
            hlt_count+=1    
            string=opCodes[i[0]]+'00000000000'
            f2.write(string)
        elif len(i)==2:
            if i[0] in ['jmp','jlt','jgt','je']:
                string=opCodes[i[0]]+'0000'+f'{(labels[i[1]]):07b}'+'\n'
                f2.write(string)
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
                else:
                    if i[0] in ['ls','rs']:
                        string=opCodes[i[0]]+'0'+registers[i[1]]+f'{int(i[2][1:]):07b}'+'\n'
                        f2.write(string)
                    elif i[0] in ['ld','st']:
                        string=opCodes[i[0]]+'0'+registers[i[1]]+var_dict[i[2]]+'\n'
                        f2.write(string)
        elif len(i)==4:
            string=opCodes[i[0]]+'00'+registers[i[1]]+registers[i[2]]+registers[i[3]]+'\n'
            f2.write(string)

if hlt_count>1: #multiple hlt in txt file (error h)
    print('Multiple hlt instructions')

if l1[len(l1)-1][0]!='hlt' or hlt_count==0: #hlt is not last instruction (error i)
    print('halt instruction missing or not used as last instruction')




