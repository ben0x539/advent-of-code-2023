import re
from dataclasses import dataclass

@dataclass
class Hand:
    red: int
    green: int
    blue: int

@dataclass
class Game:
    id: int
    hands: list[Hand]

hand_color_re = re.compile(r"(\d+) (red|green|blue)")

def parse_game(line: str) -> Game:
    game_id, _, hands = line.partition(": ")
    if game_id[:5] != "Game ":
        raise Exception("this line looks weird: " + line)
    game = Game(id=int(game_id[5:]), hands=[])
    hands = hands.split("; ")
    for hand_str in hands:
        hand = Hand(0, 0, 0)
        for (n, color) in re.findall(hand_color_re, hand_str):
            match color:
                case 'red':
                    hand.red += int(n)
                case 'green':
                    hand.green += int(n)
                case 'blue':
                    hand.blue += int(n)
        game.hands.append(hand)
    return game
        
def get_min_hand(game):
    min_hand = Hand(0, 0, 0)
    for hand in game.hands:
        min_hand.red = max(min_hand.red, hand.red)
        min_hand.green = max(min_hand.green, hand.green)
        min_hand.blue = max(min_hand.blue, hand.blue)
    return min_hand

pieces = Hand(12, 13, 14)
id_sum = 0
power_sum = 0
#with open("../inputs/sample-day-02.txt", "r", encoding="utf-8") as f:
with open("../inputs/day-02-input.txt", "r", encoding="utf-8") as f:
    for line in f:
        game = parse_game(line)
        min_hand = get_min_hand(game)
        print(game, min_hand)
        
        if min_hand.red <= pieces.red and min_hand.green <= pieces.green and min_hand.blue <= pieces.blue:
            id_sum += game.id
        power_sum += min_hand.red * min_hand.green * min_hand.blue

print(id_sum)
print(power_sum)