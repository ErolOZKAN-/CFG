import random
from collections import OrderedDict


def get_rules(filename):
    '''Creates rules from file.'''
    rules = OrderedDict()
    with open(filename, "r") as file:
        lines = file.readlines()
        for line in lines:
            if line != "\n" and line[0] != "#":
                content = line.split("#")[0]
                content = content.replace("\n", "").split("\t")
                if rules.get(content[0]) == None:
                    rules[content[0]] = content[1]
                else:
                    rules[content[0]] = rules[content[0]] + "|" + content[1]
    return rules


def print_rules(rules):
    '''Prints rules.'''
    for rule in rules:
        print(rule, ":", rules[rule])


def print_to_file(generated_sentences, filename):
    '''Prints generated sentences to given filename.'''
    with open(filename, "w") as file:
        for sentence in generated_sentences:
            file.write(sentence + "\n")
    print("Printed to", filename)


def create_sentence(rules, start):
    '''Creates a new sentence from given rules and start symbol.'''
    crated_string = []

    def dfs(root):
        '''Depth first ramdom creation.'''
        prod = random.choice(rules[root].split('|')).split()
        for unit in prod:

            if unit in rules:
                dfs(unit)
            else:
                crated_string.append(unit)

    dfs(start)
    return " ".join(crated_string)


print("--------------------- RULES --------------------------")
rules = get_rules("../data/cfg.gr")
print_rules(rules)
print("------------------------------------------------------\n")
print("--------------------- SENTENCE GENERATION --------------------------")

generated_sentences = []
for i in range(0, 1000):
    sentence = create_sentence(rules, "ROOT")
    if len(sentence.split()) > 30:
        continue
    if len(generated_sentences) > 20:
        break
    generated_sentences.append(sentence)

print_to_file(generated_sentences, "../output/random-sentence.txt")
print("------------------------------------------------------")
