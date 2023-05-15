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


num_inst=len(l1) 
var_num=num_inst
var_dict={}

#making a lookup dictionary of declared variables
for i in l:
    if i.strip()[0:3]=='var':  
        code=f'{var_num:07b}'
        var_dict[(i.strip())[4:]]=code
        var_num+=1

# writing binary of supported instructions
with open('binary.txt','w') as f2:
    for i in l1:
            if i[0] in ['ld','st']:
                string=opCodes[i[0]]+'0'+registers[i[1]]+var_dict[i[2]]+'\n'
                f2.write(string)