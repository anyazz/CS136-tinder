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
discount = 1.0

def run_round(i):
    candidates = {}
    user_ids = set(i for i in range(len(users)))
    for user in users:
        sample = user_ids - set([user.id]) - set(user.seen)
        x = random.choice(tuple(sample))
        candidates[user.id] = x
        user.seen.add(x)

    # print(candidates)
    for user_id, cand_id in candidates.items():
        user = users[user_id]
        cand = users[cand_id]
        diff = user.swipe(cand, discount, isTraining=True)
        user.history.append((i, cand_id, round(user.r_hat,2), round(user.p_hat,2), diff))

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

def tinder(n, rounds):
    global users, discount
    discount = .1 ** (1/(2*rounds))

    # initialize users
    users = []
    for i in range(n):
        user = User(i)
        users.append(User(i))

    # train predictions using random pairs of candidates
    for i in range(rounds):
        run_round(i)

    # calculate RMSE
    real_r, pred_r, real_p, pred_p = [], [], [], []
    for user in users:
        real_r.append(user.r)
        real_p.append(user.p)
        pred_r.append(user.r_hat)
        pred_p.append(user.p_hat)
        print(user)
        # print("History: " + str(user.history))
        # print("Delta: " + str(user.delta))
    return (rmse(np.array(real_r), np.array(pred_r)), rmse(np.array(real_p), np.array(pred_p)))

    # simulate actual Tinder, calculating total utility
    # utility = 0
    # for user in users:
    #     candidates = [x for x in users if x.r >= user.p and user.r >= x.p]
    #     for candidate in candidates:
    #         user.swipe(candidate, isTraining=false)
    #     utility += user.utility
    # print("TOTAL U", utility)

sum_rmse_r, sum_rmse_p = 0.0,0.0
for i in range(10):
    print("****TEST {}****".format(i))
    rmse_r, rmse_p = tinder(300, 200)
    sum_rmse_r += rmse_r
    sum_rmse_p += rmse_p
print(sum_rmse_r/10, sum_rmse_p/10)


