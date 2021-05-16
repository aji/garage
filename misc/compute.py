#!/usr/bin/python3

import time
import random

fillers = [
    "hm",
    "hmm",
    "hmmm",
    "uh",
    "uhh",
    "uhhh",
    "that is",
    "then",
    "wait",
]
ellipses = [
    "..",
    "...",
    ".....",
]


def mumble(s):
    time.sleep(0.5 + random.random() * 2.0)
    x = random.random()
    if x < 0.1:
        print(random.choice(fillers) + random.choice(ellipses))
    elif x < 0.9:
        print(s + random.choice(ellipses))
    else:
        print(random.choice(ellipses))


class Decimal(object):
    def __init__(self, n):
        self._digits = [int(x) for x in reversed(str(n))]

    def places(self):
        return len(self._digits)

    def digit(self, place):
        return self._digits[place] if place < self.places() else 0


def add(a, b):
    a = Decimal(a)
    b = Decimal(b)
    places = max(a.places(), b.places()) + 1
    carry = 0
    total = 0
    for place in range(places):
        to_add = [x for x in (a.digit(place), b.digit(place), carry) if x != 0]
        if len(to_add) > 2:
            mumble(
                random.choice([" plus ", " and "]).join(str(x) for x in to_add)
                + random.choice([" is", ", what is that"])
            )
        result = sum(to_add)
        if result == 0:
            mumble("that's just zero")
        else:
            mumble(
                random.choice(
                    [
                        "that gives ",
                        "that gives us ",
                        "you get ",
                        "that would be ",
                        "that will be ",
                    ]
                )
                + str(result)
            )
        result = Decimal(result)
        total += result.digit(0) * (10 ** place)
        carry = result.digit(1)
        if carry != 0:
            mumble("carry the " + str(carry))
    return total


def main():
    a = random.randint(100, 1000000000000)
    b = random.randint(100, 1000000000000)
    print("computing:\n   {:13d}\n + {:13d}".format(a, b))
    c = add(a, b)
    time.sleep(1)
    print("is it {}?".format(c, a + b))


main()
