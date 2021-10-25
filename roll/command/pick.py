from random import random

# This function selects an activity at random from the list
def pick(node, last_title):

    print(node.title)

    c = [child for child in node.children
         if child.status and child.title != last_title]
    if not c:
        return node
    
    return pick(c[scale([child.priority for child in c])], last_title)

def scale(nums):

    powers = [1.1 ** num for num in nums]
    s = sum(powers)
    props = [pow / s for pow in powers]

    x = random()
    i = 0
    y = props[i]
    while y < x:
        i += 1
        y += props[i]
    return i