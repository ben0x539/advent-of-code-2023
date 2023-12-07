import os

card_values = list(reversed("AKQJT98765432J"))

def get_type(cards):
    cards = list(cards)
    sorted_cards = sorted(cards, key=lambda c: (-cards.count(c), c))
    [a,b,c,d,e] = sorted_cards
    if a == b == c == d == e:
        return 7
    elif a == b == c == d != e:
        return 6
    elif a == b == c != d == e:
        return 5
    elif a == b == c != d != e:
        return 4
    elif a == b != c == d != e:
        return 3
    elif a == b != c != d != e:
        return 2
    else:
        return 1

def get_cards_values(cards):
    return [card_values.index(c) for c in cards]

def dejokerify(cards):
    cards_without_jokers = cards.replace("J", "")
    if len(cards_without_jokers) == 0:
        return cards
    best_card = max(cards_without_jokers, key=lambda c: cards_without_jokers.count(c))
    return cards.replace('J', best_card)

def run(input_file):
    with open(input_file) as f:
        lines = f.readlines()

    hands = [(cards, int(bid)) for (cards, bid) in map(str.split, lines)]
    for transform in [lambda x: x, dejokerify]:
        typed_hands = [(get_type(transform(cards)), cards, bid) for (cards, bid) in hands]
        typed_hands.sort(key=lambda h: (h[0], get_cards_values(h[1])))
        winnings = ((n+1) * bid for (n, (_, _, bid)) in enumerate(typed_hands))
        print(sum(winnings))


today = os.path.dirname(os.path.realpath(__file__)).rpartition('/')[2]
run(f"../inputs/sample-{today}.txt")
run(f"../inputs/input-{today}.txt")
