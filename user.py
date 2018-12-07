# User class

# ATTRIBUTES
# user id
# true values for rating and pickiness, all i.i.d Unif(0, 5) 
# predicted values for rating and pickiness, init to 2.5

# METHODS
# swipe - takes other User object, returns 1 for swipe right and 0 for swipe left
# 		  (possibly nondeterministic --> p of not defecting = abs(rating - threshold)/5)	
# get_utility - calculates utility to user
# update_predictions - based on outcome of swipe, update r_hat and p_hat
