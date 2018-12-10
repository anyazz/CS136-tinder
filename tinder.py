from user import User
import numpy as np
import random

# globals and constants
users = []
discount = 1.0
utility = 0
swipe_limit = 50
trials = 10

# main logic, runs multiple trials and aggregates statistics
def main():
    sum_rmse_r, sum_rmse_p, sum_utility = 0.0, 0.0, 0.0
    for i in range(trials):
        print("****TRIAL {}****".format(i))

        # call tinder function
        tinder(300, 250)

        # calculate statistics
        rmse_r, rmse_p = get_rmse()
        sum_rmse_r += rmse_r
        sum_rmse_p += rmse_p
        sum_utility += utility
        users.sort(key=lambda x: x.utility)
        for user in users:
            print(user)
    print("FINAL STATISTICS:")
    print("r error: " + str(sum_rmse_r/10)) 
    print("p error: " + str(sum_rmse_p/10)) 
    print("total utility: " + str(round(sum_utility/10, 2)))

# tinder function - runs 1 set of predictions and 1 simulation
def tinder(n, training_rounds):
    global users, discount, utility
    discount = .1 ** (1/(2*training_rounds))

    # initialize users
    users, i = [], 0
    for i in range(n):
        user = User(i)
        users.append(user)


    # train predictions using [training_rounds] rounds
    for i in range(training_rounds):
        run_training_round(i)

    # simulate actual Tinder behavior, calculating total utility
    utility = run_simulation(users)
    

# run 1 round of updating predictions
def run_training_round(i):
    # initialize map from each user to candidate
    candidates = {}
    user_ids = set(i for i in range(len(users)))

    # randomly allocate each user a new (unseen) candidate 
    for user in users:
        sample = user_ids - set([user.id]) - set(user.seen)
        x = random.choice(tuple(sample))
        candidates[user.id] = x
        user.seen.add(x)

    # for each (user, candidate) pair, call swipe for training and add to history
    for user_id, cand_id in candidates.items():
        user = users[user_id]
        cand = users[cand_id]
        user.swipe_train(cand, discount)
        user.history.append((i, cand_id, round(user.r_hat,2), round(user.p_hat,2)))

# run actual simulation
def run_simulation(users):
    utility = 0
    # filter candidates by stable match criteria
    for user in users:
        candidates = [x for x in users if x.r_hat >= user.p_hat and user.r_hat >= x.p_hat]
        for candidate in candidates:
            # allow only swipe_limit swipes
            if user.swipes >= swipe_limit:
                break
            user.swipe_actual(candidate)
        utility += user.utility
    return utility

# calculate RMSE for predictions
def get_rmse(): 
    real_r, pred_r, real_p, pred_p = [], [], [], []
    for user in users:
        real_r.append(user.r)
        real_p.append(user.p)
        pred_r.append(user.r_hat)
        pred_p.append(user.p_hat)
        print(user)
    return (rmse(np.array(real_r), np.array(pred_r)), rmse(np.array(real_p), np.array(pred_p)))

# general RMSE function
def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

main()


