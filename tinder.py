# initialize n users w/ id, true/pred values
# intelligently choose subsets of users & run simulation
# options: 
# 1. attempt to handle matches sequentially like Tinder
# 2. run algorithm once w/ random subsets to get predictions, 
#	 use predictions to choose new subsets, calculate utilities


from user import User
import random
users = []

def init_users(n):
	global users
	for i in range(n):
		users.append(User(i))

def run_round(isRandom):
	sorted_users = users
	candidates = {}
	if not isRandom:
		sorted_users.sort(key=lambda x: x.p_hat, reverse=True)		
	for user in sorted_users:	
		if user.id not in candidates:
			user_ids = set(i for i in range(len(users)))
			if not isRandom: 
				#TODO 
				pass
			sample = user_ids - user.seen - set([user.id]) - set(candidates.keys())
			x = random.sample(sample, 1)[0]
			candidates[user.id] = x
			candidates[x] = user.id
			user.seen.add(x)
			users[x].seen.add(user.id)
	print candidates

init_users(6)
for i in range(5):
	run_round(True)