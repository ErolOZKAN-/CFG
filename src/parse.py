from collections import defaultdict
import itertools
import re

GRAMMAR_RULES = "../data/cfg_changed.gr"
SENTENCES = "../data/sentence.txt"
OUTPUT_PATH = "../output/parse_results"


def read_lines(filename):
    all_lines = list()
    with open(filename, "r") as file:
        for line in file.readlines():
            all_lines.append(line.replace("\n", ""))
    return all_lines


def print_to_file(sentence, table, file):
    number_of_parses = (len([p for p in table[0][len(table) - 1] if p == 'ROOT']))
    if number_of_parses > 0:
        file.write("TRUE")
    else:
        file.write("FALSE")
    file.write("\t" + sentence + "\n")


def print_table(table):
    print('\n\n\nTABLE:')
    for row in range(len(table)):
        for col in range(row, len(table)):
            contents = '-' if not table[row][col] else ' '.join(sorted(table[row][col]))
            print('  TABLE[{},{}]: {}'.format(row + 1, col + 1, contents))


class Rule(object):
    def __init__(self, line):
        matches = re.match(r'([^\s]+)\s+([^\s]+)(?:\s+([^\s]+))?', line)
        if matches:
            self.terminal = False if matches.group(3) else True
            self.left = matches.group(1)

            if self.terminal:
                self.right = matches.group(2)
            else:
                self.right = (matches.group(2), matches.group(3))


class Grammar(object):
    def __init__(self, lines):
        super(Grammar, self).__init__()
        self.lines = lines
        self.rules = defaultdict(lambda: [])

        for line in lines:
            if line == "\r" or line == '' or line[0] == '#':
                continue
            rule = Rule(line)
            self.rules[rule.left].append(rule.right)

    def __str__(self):
        return_string = ""
        for elem in self.rules.keys():
            return_string += elem + " -> " + str(self.rules[elem]) + "\n"
        return return_string


def find_matches(grammar, word, right1, right2):
    matches = []

    def search_rules(right):
        for left in grammar.rules:
            for rule in grammar.rules[left]:
                if rule == (word or non_terminal):
                    matches.append(left)

    if word:
        search_rules(word)
    else:
        for non_terminal in itertools.product(right1, right2):
            search_rules(non_terminal)

    return matches


def parse(sentence, grammar):
    words = sentence.split()
    table = []
    for x in range(len(words)):
        table.append([])
        for y in range(len(words)):
            table[x].append([])
    for column in range(len(words)):
        table[column][column] = find_matches(grammar, words[column], None, None)
        for row in reversed(range(column + 1)):
            for s in range(row + 1, column + 1):
                table[row][column].extend(find_matches(grammar, None, table[row][s - 1], table[s][column]))
    return table


def main():
    print("Parsing...")
    grammar = read_lines(GRAMMAR_RULES)
    sentences = read_lines(SENTENCES)

    grammar = Grammar(grammar)
    # print grammar

    with open(OUTPUT_PATH, "w") as file:
        for sentence in sentences:
            parse_table = parse(sentence, grammar)
            print_to_file(sentence, parse_table, file)
            # print_table(parse_table)

    print("Parsed sentences in", SENTENCES, "successfully")
    print("Please check",OUTPUT_PATH, "to see these sentences are grammatically correct or not")


if __name__ == '__main__':
    main()
