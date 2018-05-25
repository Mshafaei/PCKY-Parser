import sys
# Global dictionary used for storing the rules.
RULE_DICT = {}


def read_grammar(grammar_file):
    #read CFG rules and splits it into separate lists for each rule.
    with open(grammar_file) as cfg:
        lines = cfg.readlines()
    return [x.replace("->", "").split() for x in lines]


def add_rule(rule):
    global RULE_DICT
    
    if rule[0] not in RULE_DICT:
        RULE_DICT[rule[0]] = set()
    my_tuple = ' '.join(rule[1:])
    RULE_DICT[rule[0]].add(my_tuple)




def convert_grammar(grammar):

    #Converts a context-free grammar in the form of
       
    
    # Remove all the productions of the type
    #A -> X B C
        #A->A|X_B,C
        #A|X_B-> X B
    # A -> B a
        # A-> B A0
        # A0->a
    global RULE_DICT
    unit_productions = []
    processed_unit=set()
    result = set()
    res_append = result.add
    index = 0
    cou=0
    for rule in grammar:
        new_rules = []
        if len(rule) == 2 and rule[1][0] != "'":
            # Rule is in form A -> X, reserve rule to handle it
            unit_productions.append(rule)
        elif len(rule) > 2:
            # Rule is in form A -> X B C or A -> X a
            terminals = [(item, i) for i, item in enumerate(rule) if item[0] == "'"]
            if terminals:
                for item in terminals:
                    print item[0]
                    rule[item[1]] = "<{}>".format(item[0].replace("'",""),)
                    new_rules.append(["<{}>".format(item[0].replace("'","")), item[0]])
                index += 1
            while len(rule) > 3:
                rule_1=rule[1]
                rule_2=rule[2]
                if(len(rule[1].split("|"))>1):
                    rule_1=rule[1].split("|")[1]
                if(len(rule[2].split("|"))>1):
                    rule_2=rule[2].split("|")[1]
                new_rules.append(["{}|{}_{}".format(rule[0], rule_1, rule_2 ), rule[1], rule[2]])
                rule = [rule[0]] + ["{}|{}_{}".format(rule[0], rule_1, rule_2 )] + rule[3:]
                index += 1
        # Adds the modified or unmodified (in case of A -> x i.e.) rules.

        add_rule(rule)
        my_tuple = ' '.join(rule)
        res_append(my_tuple)
        for n in new_rules:
            my_tuple = ' '.join(n)
            res_append(my_tuple)


    return result

f = open("CNF_with_unit.txt", 'w')
res=convert_grammar(read_grammar("cfg_grammar.txt"))
s=""
print ("++++++++++==")
for r in res:
    b= str(r).split()
    for i in range(1,len(b)):
        s=s+b[i]+" "
    f.write(b[0]+" -> "+s)
    f.write("\n")
    s=""

#print res
