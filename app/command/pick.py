from random import random

import db.helpers.past_activities as pa

# This function selects an activity at random from the list
def pick(session, node, last_title):

    if len(node.children) == 1 and node.children[0].title == last_title:
        return pick(session, ancestor_with_siblings(node), last_title)

    print(node.title)

    c = [child for child in node.children
         if child.status and child.title != last_title]
    if not c:
        return node

    if node.ordered:
        lsi = pa.last_seq_index(session, node.id)
        c.sort(key=lambda child: child.order_index)
        if lsi is not None:
            if max([child.order_index for child in c]) > lsi:
                c = [child for child in c if child.order_index > lsi]
        return pick(session, c[0], last_title)

    return pick(
        session,
        c[scale([child.priority * pa.time_of_day_weight(session, child.id)
                 for child in c])],
        last_title
    )

# return the first ancestor with non-zero siblings
def ancestor_with_siblings(node):
    if len(node.children) > 1:
        return node
    return ancestor_with_siblings(node.parent)

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