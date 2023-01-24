import gensim
import ast
import json

sent=open('GeneralClass_SW.txt')
mylist=sent.read()
sent.close()
mylist=ast.literal_eval(mylist)
print(mylist)

#mylist=json.load(mylist)
newlist=list()
for i in mylist:
    for n in mylist.get(i):
        if n not in newlist:
            newlist.append(n)
file=open('General_SW.txt','+a')
file.write(newlist.__str__())
