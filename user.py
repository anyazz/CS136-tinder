# User class

# ATTRIBUTES
# user id
# true values for rating and pickiness, all i.i.d Unif(0, 5)
# predicted values for rating and pickiness, init to 2.5
import random

class User:

    def __init__(self, id):
        self.id = id
        self.r = round(random.uniform(0.0, 5.0), 1)
        self.p = round(random.uniform(0.0, 5.0), 1)
        self.r_hat = 2.5
        self.p_hat = 2.5
        self.seen = set()
        self.matches = set()
        self.discount = 0.3
        self.history = []

    def __str__(self):
        string = "User {}: \n    true: {}, {}\n    pred: {}, {}"
        return string.format(self.id, self.r, self.p, self.r_hat, self.p_hat)

# METHODS
# swipe - takes other User object, returns 1 for swipe right and 0 for swipe left
#         (possibly nondeterministic --> p of not defecting = abs(rating - threshold)/5)
# get_utility - calculates utility to user
# update_predictions - based on outcome of swipe, update r_hat and p_hat
    def swipe(self, user):
        diff = abs(self.p_hat - user.r_hat) * self.discount
        diff = max(diff, self.discount)
        if self.p <= user.r:
            # print("User {} swiped right on user {}".format(self.id, user.id))
            if self.p_hat > user.r_hat:
                self.p_hat = round(max(self.p_hat - diff, 0.0), 1)
                user.r_hat = round(min(user.r_hat + diff, 5.0), 1)
        else:
            # print("User {} swiped left on user {}".format(self.id, user.id))
            if self.p_hat <= user.r_hat:
                self.p_hat = round(min(self.p_hat + diff, 5.0), 1)
                user.r_hat = round(max(user.r_hat - diff, 0.0), 1)
        return
