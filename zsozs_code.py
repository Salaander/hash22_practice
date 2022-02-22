from collections import defaultdict

class Person:
    def __init__(self, likes, dislikes):
        self.likes = likes
        self.dislikes = dislikes

    def __str__(self):
        return str(self.likes) + " " + str(self.dislikes)

class PizzaShop:
    def __init__(self):
        self.customers = []
        self.likes = defaultdict(int)
        self.dislikes = defaultdict(int)
        self.ingredients = []

    def read(self, filename):
        with open(filename, 'r') as file:
            lineno, likes, dislikes = 0, [], []
            for l in file.readlines():
                if lineno == 0:
                    pass
                else:
                    l = l.strip().split()[1:]
                    if lineno % 2 == 1:
                        likes = l
                    else:
                        dislikes = l
                        self.add_customer(likes, dislikes)
                lineno += 1

    def write(self, filename):
        with open(filename, 'w') as file:
            file.write(' '.join([str(len(self.ingredients))] + self.ingredients))

    def add_customer(self, likes, dislikes):
        self.customers.append(Person(likes, dislikes))

    def print(self, verbose=False):
        if verbose:
            for i, c in enumerate(self.customers):
                print(i, c)
        print("Likes:", dict(self.likes))
        print("Dislikes:", dict(self.dislikes))
        print("Num of all customers:", len(self.customers))

    def calculate_like_dislike_dict(self):
        for c in self.customers:
            for ingredient in c.likes:
                self.likes[ingredient] += 1
            for ingredient in c.dislikes:
                self.dislikes[ingredient] += 1

    def get_ingredients(self, limit):
        self.ingredients = []
        for ingredient in self.likes.keys():
            if self.dislikes[ingredient] < limit:
                self.ingredients.append(ingredient)

    def get_score(self):
        score = 0
        for c in self.customers:
            if all([(i in self.ingredients) for i in c.likes]) and \
                    not any([(i in self.ingredients) for i in c.dislikes]):
                score += 1
        return score

for filename in ["a_an_example", "b_basic", "c_coarse", "d_difficult", "e_elaborate"]:
    shop = PizzaShop()
    shop.read(filename + ".in.txt")
    shop.print()
    shop.calculate_like_dislike_dict()
    best = 0
    for i in range(max(100, len(shop.likes))):
        shop.get_ingredients(i)
        score = shop.get_score()
        if score > best:
            best = score
            shop.write(filename + ".out.txt")
            print(best)

