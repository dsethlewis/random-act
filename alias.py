# simple function that creates a list of initial substrings for a word
# e.g., aliases("word") -> ["w", "wo", "wor", "word"]
def alias(word: str):
    return [word[0:x] for x in range(1, len(word)+1)]

def aliases(words: list, blank: bool=False):
    s = set()
    if blank : s.add("")
    for word in words:
        for a in alias(word):
            s.add(a)
    return s

# create lists of options for each command
all_aliases = {
    "next": aliases(["next", "continue", "go", "activity"], blank=True),
    "quit": aliases(["quit", "exit", "leave"]),

    "do": aliases(["do"], blank=True),
    "pass": alias(["pass", "skip"]),

    "yes": alias(["yes", "yeah", "yep"]),
    "no": alias(["no", "nah", "nope", "nay"])
    }
