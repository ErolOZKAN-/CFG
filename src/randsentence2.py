import random
from collections import OrderedDict


class CFG(OrderedDict):
    def __init__(self, *args):
        super().__init__(map(lambda s: s.replace(' ', '').split('->'), args))

    def getProductions(self, symbol):
        return self[symbol].split('|')


# Depth-first walk through tree, selecting random productions
def generateSentence(cfg, start='S'):
    string = []

    def dfs(root):
        local_str = ''
        prod = random.choice(cfg.getProductions(root))
        for char in prod:
            if char in cfg:
                result = dfs(char)
                if result:
                    string.append(result)
            else:
                local_str += char
        return local_str

    dfs(start)
    return ' '.join(string[:-1]).capitalize() + string[-1]


if __name__ == "__main__":
    # Example CFG found online
    L = [
        'S -> NP VP ENDP erol',
        'NP -> DET ADJ_L NOUN',
        'VP -> VERB | VERB ADV | VP CONJ VP',
        'ADJ_L -> ADJ | ADJ_L ADJ',
        'NOUN -> "butterflies" | "flowers" | "days" | "moons" | "waves" | "kisses" | "sighs" | "ideas" | "winds"',
        'ADJ -> "painful" | "yellow" | "lonely" | "beautiful" | "colorless"',
        'DET -> "the" | "some" | "many" | "these" | "those"',
        'VERB -> "die" | "wither" | "sleep" | "wilt" | "disappear"',
        'ADV -> "woefully" | "pointlessly" | "slowly" | "selflessly" | "graciously"',
        'CONJ -> "and" | "but" | "or"',
        'ENDP -> "." | "!" | ". . ."'
    ]

    # Replacing variable names for simpler parsing
    table = OrderedDict([
        ('NP', 'A'),
        ('VP', 'B'),
        ('ADJ_L', 'C'),
        ('NOUN', 'D'),
        ('ADJ', 'E'),
        ('DET', 'F'),
        ('VERB', 'G'),
        ('ADV', 'H'),
        ('CONJ', 'I'),
        ('ENDP', 'J')
    ])

    for i in range(len(L)):
        L[i] = L[i].replace('\"', '')
        for key in table:
            L[i] = L[i].replace(key, table[key])

    cfg = CFG(*L)
    for _ in range(20):
        print(generateSentence(cfg))
