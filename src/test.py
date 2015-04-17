__author__ = 'jaejun'

import itertools

deck = [x for x in range(9)]

n1 = 3
n2 = 2
n = 5
for dealt_cards in itertools.combinations(deck, n):
    for hand1 in itertools.combinations(dealt_cards, n1):
        hand2 = tuple(card for card in dealt_cards if card not in hand1)
        # print dealt_cards, hand1, hand2

dd = itertools.combinations(deck, n)
for a in dd:
    pass
print list(dd)

