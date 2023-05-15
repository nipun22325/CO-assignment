opCodes = {'add': '00000', 'sub': '00001', 'mov': ['00010', '00011'], 'ld': '00100', 'st': '00101', 'mul': '00110', 'div': '00111', 'rs': '01000', 'ls': '01001', 'xor': '01010', 'or': '01011',
           'and': '00110', 'not': '01101', 'cmp': '01110', 'jmp': '01111', 'jlt': '11100', 'jgt': '11101', 'je': '11111', 'hlt': '11010'}

labels = {}

# labels is the dictionary containing addresses of labels

registers = {'R0': '000', 'R1': '001', 'R2': '010', 'R3': '011',
             'R4': '100', 'R5': '101', 'R6': '110', 'FLAGS': '111'}
# registers is a dictionary containing addresses of all registers

l1 = []
# l1 contains all the instructions

with open('binary.txt', 'w') as f2:
    for i in l1:

        if len(i) == 2:
            if i[0] in ['jmp', 'jlt', 'jgt', 'je']:
                string = opCodes[i[0]]+'0000'+f'{(labels[i[1]]):07b}'+'\n'
                f2.write(string)
        elif len(i) == 3:
            if i[2][0] == "$":
                string = opCodes[i[0]][0]+'0' + \
                    registers[i[1]]+f'{int(i[2][1:]):07b}'+'\n'
                f2.write(string)
