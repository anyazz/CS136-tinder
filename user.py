# User class

# ATTRIBUTES
# user id
# true values for rating and pickiness, all i.i.d Unif(0, 5)
# predicted values for rating and pickiness, init to 2.5
class User:

    def __init__(self, id, r, p):
        self.id = id
        self.r = r
        self.p = p
        self.r_hat = 2.5
        self.p_hat = 2.5
        self.seen = set()
        self.matches = set()
        self.discount = 0.01

# METHODS
# swipe - takes other User object, returns 1 for swipe right and 0 for swipe left
# 		  (possibly nondeterministic --> p of not defecting = abs(rating - threshold)/5)
# get_utility - calculates utility to user
# update_predictions - based on outcome of swipe, update r_hat and p_hat
    def swipe(self, direction, user):
        if direction:
            self.pickiness -= user.rating * discount
        else:
            self.pickiness += user.rating * discount
        return

    def swiped(self, direction, user):
        if direction:
            self.rating += userPick * discount
        else:
            self.rating -= userPick * discount
        return
