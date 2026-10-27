# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         Kennyson Le 
# Section:      567
# Assignment:   THE ASSIGNMENT NUMBER (e.g. Lab 1b-2)
# Date:         27 11 2026
#

# ENGR 102 - Chocolate Boxes
# Team members: Add all contributing team members here.
"""Arrange chocolate truffles in boxes of four under all the rules."""

import random
from itertools import combinations


def _compatible(a, b):
    if a == b:
        return False
    if {a[2], b[2]} in ({'caramel', 'vanilla'}, {'toffee', 'coconut'}):
        return False
    if {a[3], b[3]} in ({'nuts', 'sprinkles'},
                         {'white chocolate drizzle', 'dark chocolate drizzle'}):
        return False
    if {a[1], b[1]} in ({'square', 'rectangle'}, {'round', 'heart'}):
        return False
    return True


def make_boxes(chocolates):
    """Return valid boxes of four IDs, or [] if no arrangement is found."""
    ids = list(chocolates)
    if len(ids) % 4:
        return []
    if not ids:
        return []

    values = [chocolates[t] for t in ids]
    n = len(ids)
    dark = [v[0] == 'dark' for v in values]
    white = [v[0] == 'white' for v in values]
    neighbors = [set() for _ in ids]
    for i, j in combinations(range(n), 2):
        if _compatible(values[i], values[j]):
            neighbors[i].add(j)
            neighbors[j].add(i)

    randomizer = random.Random(102)

    def search(node_limit):
        calls = 0
        result = []
        # Remember states proved impossible in this search, to avoid revisiting them.
        rejected = set()

        def solve(remaining):
            nonlocal calls
            if not remaining:
                return True
            if remaining in rejected:
                return False
            calls += 1
            if calls > node_limit:
                return False

            m = len(remaining) // 4
            nd = sum(dark[i] for i in remaining)
            nw = sum(white[i] for i in remaining)
            if nd == 1 or nw == 1 or nd > 3*m or nw > 3*m:
                rejected.add(remaining)
                return False

            # Find the item with the fewest potentially usable partners.
            best = None
            partners = None
            for i in remaining:
                p = neighbors[i].intersection(remaining)
                if len(p) < 3:
                    rejected.add(remaining)
                    return False
                if partners is None or len(p) < len(partners):
                    best, partners = i, p

            others = list(partners)
            randomizer.shuffle(others)
            # Form possible boxes in randomized order. Test counts before recursing.
            for a, b, c in combinations(others, 3):
                if b not in neighbors[a] or c not in neighbors[a] or c not in neighbors[b]:
                    continue
                d = dark[best] + dark[a] + dark[b] + dark[c]
                w = white[best] + white[a] + white[b] + white[c]
                if d not in (0, 2, 3) or w not in (0, 2, 3):
                    continue
                box = (best, a, b, c)
                result.append(box)
                if solve(remaining.difference(box)):
                    return True
                result.pop()
                if calls > node_limit:
                    return False
            rejected.add(remaining)
            return False

        if solve(frozenset(range(n))):
            return [[ids[i] for i in box] for box in result]
        return None

    # Multiple differently ordered searches help avoid unlucky backtracking paths.
    # Larger limits make a difficult but valid dataset less likely to return [].
    for limit in ([2000]*12 + [10000]*25 + [40000]*15):
        answer = search(limit)
        if answer is not None:
            return answer
    return []


if __name__ == '__main__':
    chocolates = {
        1: ['white', 'round', 'caramel', 'none'],
        2: ['white', 'round', 'toffee', 'nuts'],
        3: ['dark', 'round', 'strawberry', 'none'],
        4: ['dark', 'round', 'caramel', 'nuts'],
        5: ['milk', 'heart', 'vanilla', 'none'],
        6: ['milk', 'heart', 'strawberry', 'sprinkles'],
        7: ['dark', 'heart', 'vanilla', 'white chocolate drizzle'],
        8: ['dark', 'heart', 'strawberry', 'sprinkles'],
    }
    print(make_boxes(chocolates))
