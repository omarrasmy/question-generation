import gensim
s=list()
n=list()
for line in open('omar1.txt'):
    # assume there's one document per line, tokens separated by whitespace
    line=line.lower()
    gensim.utils.simple_preprocess(line)
    line=line.replace(",","")
    line=line.replace("(","")
    line=line.replace("'","")
    line = line.replace(".", "")
    line = line.replace("!", "")
    line = line.replace(")", "")
    line = line.replace(":", "")
    line=line.split()
    s.append(line)

    for line1 in line:
        if line1.__contains__("_"):
            if line1 not in n:
                n.append(line1)

print(s)
print(n)
file1=open('Sentence.txt','a+')
file1.write(s.__str__())
file1.close()

file=open('Keyword.txt','a+')
file.write(n.__str__())
file.close()
