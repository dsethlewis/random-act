class Item:
    def __init__(self, do, children):
        self.do = do
        self.children = children

i1 = Item("Read", [])

print(i1.do)
print(i1.children)

i1.do = "Rest"

print(i1.do)

tree = [
    Item("Read", []),
    Item("Workout", [])
]

print(tree[0].do)