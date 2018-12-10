# other class

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
        self.delta = 1.0
        self.history = []
        self.utility = 0
        self.discount = 1.0

    def __str__(self):
        string = "User {}: \n    true: {}, {}\n    pred: {}, {}"
        return string.format(self.id, self.r, self.p, self.r_hat, self.p_hat)

# METHODS
# swipe - takes other User object, returns 1 for swipe right and 0 for swipe left
#         (possibly nondeterministic --> p of not defecting = abs(rating - threshold)/5)
# get_utility - calculates utility to other
# update_predictions - based on outcome of swipe, update r_hat and p_hat
    def swipe(self, other, discount, isTraining):
        if isTraining:
            diff = self.train(other, discount)
        else:
            self.get_utility(other)
        return 
        
    def train(self, other, discount):
        diff = abs(self.p_hat - other.r_hat) 
        self_diff = max(diff, 1) * self.delta
        other_diff = max(diff, 1) * other.delta

        if self.p <= other.r and self.p_hat > other.r_hat:
            self.p_hat = round(max(self.p_hat - self_diff, 0.0), 2)
            other.r_hat = round(min(other.r_hat + other_diff, 5.0), 2)
        elif self.p > other.r and self.p_hat <= other.r_hat:
            self.p_hat = round(min(self.p_hat + self_diff, 5.0), 2)
            other.r_hat = round(max(other.r_hat - other_diff, 0.0), 2)
        self.delta = self.delta * discount
        other.delta = other.delta * discount
        return self_diff

    def get_utility(self, other):
        if self.p <= other.r:
            # swipe right
            if other.p <= self.r:
                # match
                self.utility += max(0, other.r - self.r) + 1
            else:
                self.utility += min(0, other.r - self.r) - 1
        else:
            # swipe left
            if other.p <= self.r:
                self.utility += 0.5
            else:
                self.utility += 0
        return

