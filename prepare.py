import random

f  = open("./data/example/raw/src-train.txt", "r") 
fl = f.readlines()
f.close()

f  = open("./data/example/raw/tgt-train.txt", "r") 
fl1 = f.readlines()
f.close()

lista_test_in = []
lista_test_out = []

for x in range(25):
    limite = len(fl)
    num = random.randint(1, limite)
    lista_test_in.append(fl[num])
    lista_test_out.append(fl1[num])
    del fl[num]
    del fl1[num]


f  = open("./data/example/raw/src-train.txt", "a") 
f.truncate(0)
for x in fl:
    f.write(x)
f.close()

f  = open("./data/example/raw/tgt-train.txt", "a") 
f.truncate(0)
for x in fl1:
    f.write(x)
f.close()

f  = open("./test/input.txt", "a") 
f.truncate(0)
for x in lista_test_in:
    f.write(x)
f.close()

f  = open("./test/output.txt", "a") 
f.truncate(0)
for x in lista_test_out:
    f.write(x)
f.close()
