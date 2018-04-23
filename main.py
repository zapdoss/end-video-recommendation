import sys
from sequential import tags
import fromKenlists import fromKenlists
import tags import sequential


if __name__ == '__main__':

    rule_1 = []
    rule_2 = []
    rule_3 = []

    id = raw_input()

    rule_1 = tags(id)
    rule_2 = fromKenlists(id)
    rule_3 = sequential(id)

    print rule_1, rule_2, rule_3
