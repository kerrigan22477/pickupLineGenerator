import numpy as np
import re
import string

# read in pickup lines, add * to end of pickup lines (terminal char)
pickup_lines = []
file = open('pickup.txt', 'r')
for line in file:
    line.strip('\n')
    # remove all punctuation
    line = line.translate(str.maketrans('', '', string.punctuation))
    line_words = re.findall(r"[\w']+|[.,!?;]", line)
    line_words = [str(w).lower() for w in line_words if not w.isupper() and not w.isdigit()]
    line_words.append('*')
    if len(line_words) != 1:
        pickup_lines.extend(line_words)


class FirstOrderMarkovModel(object):
    terminal_char = '*'

    def __init__(self, lines):
        self.order = 1
        self.lines = lines
        # first dict, k=word, v=count
        # second dict, k=word, v={k=nextword, v=count}
        self.transitions = [{}]
        for i in range(self.order):
            self.transitions.append({})

    def build_transition_matrices(self):
        # count num times each word appears
        for i in range(len(self.lines)):
            word = self.lines[i]
            if word in self.transitions[0]:
                self.transitions[0][word] += 1
            else:
                self.transitions[0][word] = 1

        # normalize and convert to probabilites
        # add total num transitions
        transition_sum = float(sum(self.transitions[0].values()))
        # for first dict
        for k, v in self.transitions[0].items():
            # divide word count by total num transitions
            self.transitions[0][k] = v / transition_sum

        # track transitions
        for i in range(len(self.lines) - 1):
            word = self.lines[i]
            next_word = self.lines[i + 1]
            # if word second dict
            if word in self.transitions[1]:
                # if 2nd word in word's transition dict
                # increase count by 1
                if next_word in self.transitions[1][word]:
                    self.transitions[1][word][next_word] += 1
                else:
                    self.transitions[1][word][next_word] = 1
            # add new transition
            # increase count for new transition by 1
            else:
                self.transitions[1][word] = {}
                self.transitions[1][word][next_word] = 1

        # normalize and convert to probabilites
        for word, transdict in self.transitions[1].items():
            # total num transitions for word
            key_sum = float(sum(self.transitions[1][word].values()))
            for next_word, count in transdict.items():
                # divide specific transition count by
                # total num transitions for word
                self.transitions[1][word][next_word] = count / key_sum

    def generate_pickup_line(self):
        word = '*'
        while word == '*':
            # (all words, replace, p=prob of word at all)
            word = np.random.choice([*self.transitions[0].keys()], replace=True, p=[*self.transitions[0].values()])
            phrase = word + ' '
        while word != '*':
            # (all transition options, replace, p=transition probs)
            word = np.random.choice([*self.transitions[1][word].keys()], replace=True,
                                    p=[*self.transitions[1][word].values()])
            phrase += word + ' '

        return phrase[:len(phrase) - 2]


mm_pickup = FirstOrderMarkovModel(pickup_lines)
mm_pickup.build_transition_matrices()
for i in range(3):
    print(str(i + 1) + ') ' + mm_pickup.generate_pickup_line())
