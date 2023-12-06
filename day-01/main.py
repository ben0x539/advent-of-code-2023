import re

calibration_value = 0

digit_words = [
    "one", "two", "three",
    "four", "five", "six",
    "seven", "eight", "nine",
]

with open("../inputs/input-day-01.txt", "r", encoding="utf-8") as f:
    for line in f:
        first, last = None, None
        replaced_line = ""
        i = 0
        while i < len(line):
            c = line[i]
            if not c.isdigit():
                for j in range(len(digit_words)):
                    w = digit_words[j]
                    if line[i:i+len(w)] == w:
                        c = str(j+1)
                        i += 1 #len(w)
                        break
                else:
                    i += 1
                    continue
            else:
                i += 1

            if first is None:
                first = c
            last = c
        print(line, first, last)
        calibration_value += int(first + last)

print(calibration_value)
