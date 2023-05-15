#func is the dict of operations with their code
func={'add':'00000','sub':'00001'}

#l1 is list of gap separated instructions
l1=[['add', 'R1', 'R2', 'R3'], ['sub', 'R1', 'R2', 'FLAGS'], ['hlt'], ['mov', 'R1', '$12'], ['mov', 'R1', 'R2'], ['mov', 'R1', 'R2']]

#registers stores codes for registers
registers={'R0':'000','R1':'001','R2':'010','R3':'011','R4':'100','R5':'101','R6':'110','FLAGS':'111'}

#var_dict stores variables and their addresses
var_dict={'xyz':'0000110','abc':'0000111'}

#lables stores lables and their addresses
labels={'label1':'0000001','label2':'0000010'}

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

#l is f.readlines() for the txt file read
l=['var xyz\n','var abx\n','var hjk\n','add R1 R2 R3']

#check for variable not declared at the beginning (error g)
for i in range(len(l)):
    if l[i][0:3]=='var':
        if i!=0 and l[i-1][0:3]!='var':
            print('Variables not declared at the beginning')
            break

#to count no of times hlt is called
hlt_count=0

#execute hlt command line
with open('binary.txt','w') as f2:
    for i in l1:
        if len(i)==1:
            hlt_count+=1    
            string=func[i[0]]+'00000000000'
            f2.write(string)

if hlt_count>1: #multiple hlt in txt file (error h)
    print('Multiple hlt instructions')

if l1[len(l1)-1][0]!='hlt' or hlt_count==0: #hlt is not last instruction (error i)
    print('halt instruction missing or not used as last instruction')
    