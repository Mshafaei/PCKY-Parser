#generate cfg grammer from WSJ dataset
import re
from nltk.corpus import ptb
from pythonds.basic.stack import Stack
import os
rules={}
singleWords=set([","])
punc=set([":","#","-LRB-","CD","TO","``","S","''","$","NP","IN","-RRB-",",","."])
punc2=set([":","#","``","''","$",",","."])
i=0
# I read all files then I will go thorugh all lines in each file and I used stack to extract the grammers.
#for each ')' I pop from stack until I face '(' so I generate rule and push back the last item in the stack for a next rule.

for o in os.listdir('wsj'):
    if (os.path.isdir(os.path.join('wsj',o))):
        for filename in os.listdir(os.path.join('wsj',o)):
            i=i+1
            print i
            if filename.endswith(".mrg"):
                path='wsj/'+o+'/'+filename
              
                singleWords=set(ptb.words(path))| singleWords
                pranthesis=Stack()
                words=Stack()
                f=open(path,'r')
                content=f.readlines()
                allWords=[]
                for line in content:
                    for l in line.strip().split():
                        # with regular expression we break each line to: words '('  ')'
                        result=re.findall("[)]|[(]|[^\)\(]*",l.strip())
                        for r in result:
                            if r !="":
                                allWords.append(r)

                buffer=[]
                for word in allWords:
                    if (word=="("):
                        words.push(tuple(["(","F"]))
                    elif (word==")"):
                        temp=words.pop()
                        while(temp[0]!="("):
                            buffer.append(temp)
                            temp=words.pop()
                        parent=buffer.pop()
                        parent=tuple([parent[0],"T"])
                        words.push(parent)
                        if parent in rules:
                            if buffer:
                                rules[parent].append(buffer)
                        else:
                            arr=[]
                            arr.append(buffer)
                            rules[parent]=arr
                    else:

                        if word!="" and word!=" ":
                            words.push(tuple([word,"F"]))
                    buffer=[]


f = open("cfg_grammar.txt", 'w')
for key in rules:
    b_set = set(map(tuple,rules[key])) #need to convert the inner lists to tuples so they are hashable
    b = map(list,b_set) #Now convert tuples back into lists
    for rule in b:
        for index,j in enumerate(rule):
            if j[1]=="T":
                rule[index]=j[0]
            if j[1]=="F":
                rule[index]="'"+j[0]+"'"

            
        st=" ".join(reversed(rule))
        f.write(key[0]+" -> "+st)
        f.write("\n")



