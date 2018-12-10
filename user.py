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
        self.discount = 0.01

# METHODS
# swipe - takes other User object, returns 1 for swipe right and 0 for swipe left
# 		  (possibly nondeterministic --> p of not defecting = abs(rating - threshold)/5)
# get_utility - calculates utility to user
# update_predictions - based on outcome of swipe, update r_hat and p_hat
    def swipe(self, user):
		diff = (self.p_hat - user.r_hat) * discount
		if self.p <= user.r:
			if self.p_hat > user.r_hat:
				self.p_hat -= diff
				user.r_hat += diff
		else:
			if self.p_hat <= user.r_hat:
				self.p_hat -= diff
				user.r_hat += diff
		return

