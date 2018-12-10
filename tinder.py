# initialize n users w/ id, true/pred values
# intelligently choose subsets of users & run simulation
# options:
# 1. attempt to handle matches sequentially like Tinder
# 2. run algorithm once w/ random subsets to get predictions,
#    use predictions to choose new subsets, calculate utilities

from user import User
import numpy as np
import random
users = []

def init_users(n):
    global users
    for i in range(n):
        users.append(User(i))

def run_round(i, isRandom):
    flag = False
    sorted_users = users
    candidates = {}
    if not isRandom:
        sorted_users.sort(key=lambda x: x.p_hat, reverse=True)
    for user in sorted_users:
        if user.id not in candidates:
            user_ids = set(i for i in range(len(users)))
            if not isRandom:
                pass
            sample = user_ids - user.seen - set([user.id]) - set(candidates.keys())
            x = random.sample(sample, 1)[0]
            candidates[user.id] = x
            candidates[x] = user.id
            user.seen.add(x)
            users[x].seen.add(user.id)
    for user_id, cand_id in candidates.items():
        user = users[user_id]
        cand = users[cand_id]
        user.swipe(cand)
        user.history.append((i, cand_id, user.r_hat, user.p_hat))
        # print(users[user_id])

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

init_users(500)
for i in range(200):
    while True:
        try:
            run_round(i, (True))
            break
        except:
            pass

real_r, pred_r, real_p, pred_p = [], [], [], []
for user in users:
    real_r.append(user.r)
    real_p.append(user.p)
    pred_r.append(user.r_hat)
    pred_p.append(user.p_hat)
    print(user)
    # print("History: " + str(user.history))
print("Delta: " + str(users[0].delta))
print(rmse(np.array(real_r), np.array(pred_r)))
print(rmse(np.array(real_p), np.array(pred_p)))
