from collections import defaultdict
import itertools
import re

GRAMMAR_RULES = "../data/cfg_changed.gr"
SENTENCES = "../data/sentence.txt"
OUTPUT_PATH = "../output/parse_results"


def read_lines(filename):
    '''Reads lines.'''
    all_lines = list()
    with open(filename, "r") as file:
        for line in file.readlines():
            all_lines.append(line.replace("\n", ""))
    return all_lines


def init_table(words):
    '''Initilizes empty table.'''
    table = []
    for x in range(len(words)):
        table.append([])
        for y in range(len(words)):
            table[x].append([])
    return table


def print_to_file(sentence, table, file):
    '''Prints sentences and their parse results.'''
    print('\n\n\nSENTENCE:', sentence)

    number_of_parses = (len([p for p in table[0][len(table) - 1] if p == 'ROOT']))
    print("Number of parses: ", number_of_parses, end="\t\t")
    if number_of_parses > 0:
        print("CORRECT")
        file.write("CORRECT")
    else:
        print("NOT CORRECT")
        file.write("NOT CORRECT")
    file.write("\t" + sentence + "\n")


def print_table(sentence, table):
    '''Prints given table.'''
    print()
    for row in range(len(table)):
        for col in range(row, len(table)):
            print(table[row][col], end="")
        print()


class Rule:
    '''Rule class.'''

    def __init__(self, line):
        '''Constructor for Rule class, parses line, creates left and right nodes. Decides if it as terminal or not.'''
        matches = re.match(r'([^\s]+)\s+([^\s]+)(?:\s+([^\s]+))?', line)
        if matches:
            'If third string can be parse, then it is not a terminal'
            self.terminal = False if matches.group(3) else True
            self.left = matches.group(1)

            if self.terminal:
                self.right = matches.group(2)
            else:
                self.right = (matches.group(2), matches.group(3))


class Grammar:
    '''Grammar class.'''

    def __init__(self, lines):
        '''Constructor for grammar class. Initializes grammar rules.'''
        super(Grammar, self).__init__()
        self.lines = lines
        self.rules = defaultdict(lambda: [])

        for line in lines:
            if line == "\r" or line == '' or line[0] == '#':
                continue
            rule = Rule(line)
            self.rules[rule.left].append(rule.right)

    def __str__(self):
        '''To string method of grammar class. '''
        return_string = ""
        for elem in self.rules.keys():
            return_string += elem + " -> " + str(self.rules[elem]) + "\n"
        return return_string


def find_matches(grammar, word, right1, right2):
    '''Searches possible rules given word or non_terminal.'''
    matches = []

    def search_rules(right):
        '''Compares rules with given word or non_terminal '''
        for left in grammar.rules:
            for rule in grammar.rules[left]:
                if rule == (word or non_terminal):
                    # print(rule, print(left))
                    matches.append(left)

    if word:
        search_rules(word)
    else:
        for non_terminal in itertools.product(right1, right2):
            search_rules(non_terminal)

    return matches


def parse(sentence, grammar):
    '''Parses given sentences given grammar rules.'''
    words = sentence.split()
    table = init_table(words)  # Inits empty table.
    for column in range(len(words)):
        '# Fill bottom values . Important: Matrix is transposed. So, it fills diagonally.'
        table[column][column] = find_matches(grammar, words[column], None, None)
        for row in reversed(range(column + 1)):
            for s in range(row + 1, column + 1):
                table[row][column].extend(find_matches(grammar, None, table[row][s - 1], table[s][column]))
        # print_table(table)
    return table


print("Parsing...")
grammar = read_lines(GRAMMAR_RULES)
sentences = read_lines(SENTENCES)

grammar = Grammar(grammar)
# print grammar

with open(OUTPUT_PATH, "w") as file:
    for sentence in sentences:
        parse_table = parse(sentence, grammar)
        print_to_file(sentence, parse_table, file)
        print_table(sentence, parse_table)

print("\n\n\nParsed sentences in", SENTENCES, "successfully")
print("Please check", OUTPUT_PATH, "to see these sentences are grammatically correct or not")
