from random import choice, random
from math import log, ceil

# This function selects an activity at random from the list
def pick(node):
    print(node.title)
    c = [child for child in node.children if child.status]
    if not c:
        return node
    return pick(choice(c))

# def pos_int(nums):

#     powers = [2 ** num for num in nums]

#     s = sum(powers)
#     props = [pow / s for pow in powers]

#     d = 10 ** ceil(-log(min(props), 10))
#     return [round(prop * d) for prop in props]

def scale(nums):

    powers = [2 ** num for num in nums]
    s = sum(powers)
    props = [pow / s for pow in powers]

    x = random()
    i = 0
    y = props[i]
    while y < x:
        i += 1
        y += props[i]
    return i