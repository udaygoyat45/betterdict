all_words = []
fin = open("flaskapp/static/words/corncob_lowercase.txt")
all_words = fin.readlines()
all_words = list(map(lambda x: x.strip(), all_words))

def compareStrings (x, y):
    r = min(len(x), len(y))
    x = list(x)
    y = list(y)
    count = 0
    for i in range(r):
        if (x[i] == y[i]):
            count += 1

    return count


def topPriority (word):
    from itertools import permutations
    global all_words
    words = []
    for each in permutations(word):
        p = "".join(each)
        if (p in all_words):
            words.append(p)
    return words


def possibilties (word):
    global all_words
    order = [[] for i in range(len(all_words))]
    for i in range(len(all_words)):
        order[i] = [compareStrings(all_words[i], word), all_words[i]]

    order.sort(reverse=True)
    final_list = topPriority(word)
    for i in range(7):
        final_list.append(order[i][1])

    return final_list
