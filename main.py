
f3 = open("result.txt", 'w')
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

def makeTree(i1,i2,start_symbol,p_table, words):
    max=0
    finalkey=""
    if i2==i1+1:
        termx="'"+words[i1]+"'"
        if start_symbol in all_cnf_rules_reverse[tuple([termx,])]:
            tree ="({} {})".format(start_symbol,words[i1])
        else:
            if tuple([start_symbol,]) in all_unit:
                for key in all_unit[tuple([start_symbol,])]:
                    termx="'"+words[i1]+"'"
                    if key[0] in all_cnf_rules_reverse[tuple([termx,])]:
                        if all_unit[tuple([start_symbol,])][key]>max:
                            max=all_unit[tuple([start_symbol,])][key]
                            finalkey=key
                if finalkey !="" and max>0:
                    tree ="({} ({} {}))".format(start_symbol,finalkey[0],words[i1])
                else:
                    tree ="({} {})".format(start_symbol,words[i1])
            else:
                tree ="({} {})".format(start_symbol,words[i1])
    else:
        children=index_table[i1][i2][start_symbol]
        j=children[0]
        k=children[1]
        first=children[2]
        i=children[3]
        second=children[4]
        t1=makeTree(j,k,first,p_table,words)
        t2=makeTree(k,i,second,p_table,words)
        if len(start_symbol.split("_"))>=2:
            tree = "{} {}".format(t1,t2)
        else:
            
            if tuple([first,second]) in all_cnf_rules_reverse and start_symbol in all_cnf_rules_reverse[tuple([first,second])]:
                tree = "({} {} {})".format(start_symbol,t1,t2)
            else:
                if tuple([start_symbol,]) in all_unit:
                    for key in all_unit[tuple([start_symbol,])]:
                        if tuple([first,second]) in all_cnf_rules_reverse:
                            if key[0] in all_cnf_rules_reverse[tuple([first,second])]:
                                max=all_unit[tuple([start_symbol,])][key]
                                finalkey=key
                    if finalkey !="" and max>0:
                        tree = "({} ({} {} {}))".format(start_symbol,finalkey[0],t1,t2)
                    else:
                        tree = "({} {} {})".format(start_symbol,t1,t2)
                else:
                    tree = "({} {} {})".format(start_symbol,t1,t2)

    return tree

f2 = open("cnfRules.txt", 'r')
content2=f2.readlines()
cnf_rules_reverse={}
    
for line in content2:
    data2=line.strip().replace("->","").split()
    
    if(len(data2)==3):
        token=tuple([data2[1],])
    else:
        token=tuple([data2[1],data2[2]])
    if token in cnf_rules_reverse:
        cnf_rules_reverse[token][data2[0]]=data2[-1].replace("[","").replace("]","")
    else:
        temp={}
        temp[data2[0]]=data2[-1].replace("[","").replace("]","")
        cnf_rules_reverse[token]=temp


#allCNFRules
f5 = open("CNF_with_unit_sorted.txt", 'r')
content5=f5.readlines()
all_cnf_rules_reverse={}

for line in content5:
    data5=line.strip().replace("->","").split()

    if(len(data5)==2):
        token=tuple([data5[1],])
    else:
        token=tuple([data5[1],data5[2]])
    if token in all_cnf_rules_reverse:
        all_cnf_rules_reverse[token].append(data5[0])
    else:
        temp=[]
        temp.append(data5[0])
        all_cnf_rules_reverse[token]=temp

#unit
f6 = open("unit_productions.txt", 'r')
content6=f6.readlines()
all_unit={}

for line in content6:
    data6=line.strip().replace("->","").split()
    token=tuple([data6[0],])
    if token in all_unit:
        token2=tuple([data6[1],])
        all_unit[token][token2]=data6[-1].replace("[","").replace("]","")
    else:
        token2=tuple([data6[1],])
        all_unit[token]={}
        all_unit[token][token2]=data6[-1].replace("[","").replace("]","")



f = open("test.txt", 'r')

content=f.readlines()

for lineindex, line in enumerate(content):
    words=[]
    print "---------------"
    data=line.strip().split()
    for word in data:
        words.append(word)
    print words

    prods={}
    temp2=[]
    length=len(words)+1
    p_table = [[{} for x in range(length)] for y in range(length - 1)]
    index_table = [[{} for x in range(length)] for y in range(length - 1)]
    for i in range(1,length):
        hasValue=False
        term="'"+words[i-1]+"'"
        tok=tuple([term,])
        for key in cnf_rules_reverse:
                if key==tok:
                    hasValue=True
                    for st in cnf_rules_reverse[key]:
                        p_table[i-1][i][st]=cnf_rules_reverse[key][st]
        if not hasValue:
            print tok
            term2="'"+words[i-1].lower()+"'"
            tok2=tuple([term2,])
            for key in cnf_rules_reverse:
                if key==tok2:
                    hasValue=True
                    for st in cnf_rules_reverse[key]:
                        p_table[i-1][i][st]=cnf_rules_reverse[key][st]
            if not hasValue:
                if hasNumbers(term2):
                    p_table[i-1][i]["CD"]=1
                else:
                    if (words[i-1].endswith("able") or words[i-1].endswith("ly")):
                        p_table[i-1][i]["PP"]=1
                    else:
                        p_table[i-1][i]["NNP"]=1

    for i in range(2, length):
        for j in range(i - 2, -1, -1):
            for k in range(j + 1, i):
                #if (j, k) not in prods:
                prods[j, k] = [node for node in p_table[j][k]]
                prod1 = prods[j, k]

#if (k, i) not in prods:
                prods[k, i] = [node for node in p_table[k][i]]
                prod2 = prods[k, i]
                for first in prod1:
                    for second in prod2:
                        key=tuple([first,second])
                        if key in cnf_rules_reverse:
                            arrrule=cnf_rules_reverse[key]
                            for ru in arrrule:
                                pp=float(cnf_rules_reverse[key][ru])*float(p_table[j][k][first])*float(p_table[k][i][second])
                                if ru in p_table[j][i]:
                                    if pp > p_table[j][i][ru]:
                                        p_table[j][i][ru]=pp
                                        index_table[j][i][ru]=[j,k,first,i,second]
                            
                                else:
                                    p_table[j][i][ru]=pp
                                    index_table[j][i][ru]=[j,k,first,i,second]

                                    if (j, i) not in prods:
                                        prods[j, i] ={}
                                    prods[j, i][ru]=pp

    start_symbol_index=-1
    for item in p_table[0][len(words)]:
        if item =="S":
            start_symbol_index=0
            stri=makeTree(0,len(words),item,p_table,words)
            f3.write(stri)
            f3.write("\n")
            break
    if start_symbol_index==-1:
        print "Unresolve:"
        print lineindex
        tempstr=""
        for t in range(len(words)-1,-1,-1):
            tempstr="(NP"+" "+words[t]+") "+tempstr
        tree ="(S"+tempstr+")"
        f3.write(tree)
        f3.write("\n")








