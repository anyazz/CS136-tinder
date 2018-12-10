import random

# USER CLASS
class User:

    def __init__(self, id):
        # unique integer ID of user
        self.id = id
        # true rating: implicit "attractiveness" rating perceived by other users
        self.r = round(random.uniform(0.0, 5.0), 1)
        # true pickiness: implicit rating threshold for right swipe
        self.p = round(random.uniform(max(self.r - 1.5, 0), min(self.r + 1.5, 5.0)), 1)
        # predicted rating
        self.r_hat = 2.5
        # predicted pickiness
        self.p_hat = 2.5
        # set of users seen while training
        self.seen = set()
        # number of right swipes
        self.swipes = 0
        # set of matches
        self.matches = set()
        # discount factor
        self.delta = 1.0
        # records evolution of predictions over time
        self.history = []
        # user utility
        self.utility = 0

    def __str__(self):
        string = "User {}: \n    true: {}, {}\n    pred: {}, {}\n    matches: {}\n    utility: {}"
        return string.format(self.id, self.r, self.p, self.r_hat, 
            self.p_hat, len(self.matches), round(self.utility, 2))


    # swipe function for training
    def swipe_train(self, other, discount):
        # calculate magnitude of difference between rating and pickiness
        diff = abs(self.p_hat - other.r_hat) 

        # multiply by appropriate delta factor for user
        self_diff = max(diff, 1) * self.delta
        other_diff = max(diff, 1) * other.delta

        # if behavior does not match expected, update predictions by diff, 
        # ensuring that new values don't go outside [0,5] range
        if self.p <= other.r and self.p_hat > other.r_hat:
            # true swipe right, expected swipe left --> decrease pickiness
            # and increase rating
            self.p_hat = round(max(self.p_hat - self_diff, 0.0), 2)
            other.r_hat = round(min(other.r_hat + other_diff, 5.0), 2)

        elif self.p > other.r and self.p_hat <= other.r_hat:
            # true swipe left, expected swipe right --> increase pickiness
            # and decrease rating
            self.p_hat = round(min(self.p_hat + self_diff, 5.0), 2)
            other.r_hat = round(max(other.r_hat - other_diff, 0.0), 2)
       
        # update delta factors by discount
        self.delta = self.delta * discount
        other.delta = other.delta * discount

    # swipe function for simulation
    def swipe_actual(self, other):
        if self.p <= other.r:
            # observe swipe right
            self.swipes += 1
            if other.p <= self.r:
                # match
                self.matches.add(other)
                self.utility += other.r - self.p + 2
            else:
                self.utility += min(0, other.r - self.p - 2)
        else:
            # observe swipe left
            if other.p <= self.r:
                self.utility += 0.5
            else:
                self.utility += 0
        return

