with open("assembly.txt") as f:
    l=f.read().splitlines()
    print(l)
for i in range(len(l)):
    if l[i]=="hlt":
        n=i+1

vars=["var1","var2","var3","var3","var4","var5"]
val=[]

for j in range(len(vars)):
    nb='{0:07b}'.format(n)
    val.append(nb)
    n+=1
print(val)


def load():
    ld_out=''
    for i in range(len(l)):
        l2=l[i].split() 
        for j in range(len(l2)):
            if l2[j]=="ld":
                ld_out+="001000"
                for k in range(len(l2)):
                    if l2[k]=="R0":
                        ld_out+="000"
                    elif l2[k]=="R1":
                        ld_out+="001"
                    elif l2[k]=="R2":
                        ld_out+="010"
                    elif l2[k]=="R3":
                        ld_out+="011"
                    elif l2[k]=="R4":
                        ld_out+="100"
                    elif l2[k]=="R5":
                        ld_out+="101"
                    elif l2[k]=="R6":
                        ld_out+="110"
                    elif k==len(l2)-1:
                        for x in range(len(vars)):
                            if x==0:
                                ld_out+=val[x]
                                val.pop(0)
                                vars.pop(0)
                
                    
                    
    print(ld_out)

load()

def store():
    st_out=''
    for i in range(len(l)):
        l2=l[i].split()
        for j in range(len(l2)):
            if l2[j]=="st":
                st_out+="001010"
                for k in range(len(l2)):
                    if l2[k]=="R0":
                        st_out+="000"
                    elif l2[k]=="R1":
                        st_out+="001"
                    elif l2[k]=="R2":
                        st_out+="010"
                    elif l2[k]=="R3":
                        st_out+="011"
                    elif l2[k]=="R4":
                        st_out+="100"
                    elif l2[k]=="R5":
                        st_out+="101"
                    elif l2[k]=="R6":
                        st_out+="110"
                    elif k==len(l2)-1:
                        for x in range(len(vars)):
                            if x==0:
                                st_out+=val[x]
                                val.pop(0)
                                vars.pop(0)
                
    print(st_out)

store()
