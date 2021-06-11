#ba ham fekrie yazdane seyedi : 96521299
import numpy as np
from ple import PLE
from ple.games.snake import Snake

gama = 0.9
alfa = 0.1
Q_list=[]
for i in range(256):
    Q_list.append([])
    for j in range(256):
        Q_list[i].append([0,0,0,0])

def Q_list_update(state, action, reward):
    X_head = state.getGameState()['snake_head_x']
    Y_head = state.getGameState()['snake_head_y']

    if X_head > 255:
        X_head = 255
    if Y_head > 255:
        Y_head = 255
    if X_head < 0:
        X_head = 0
    if Y_head < 0:
        Y_head = 0

    next_Q = Q_list[int(X_head)][int(Y_head)]
    max_q = max(next_Q[0], next_Q[1], next_Q[2], next_Q[3])
    sample = reward + gama * max_q 
    pre_state = state.getGameState()['snake_body_pos'][1]

    if pre_state[0] > 255:
        pre_state[0] = 255
    if pre_state[1] > 255:
        pre_state[1] = 255
    if pre_state[0] < 0:
        pre_state[0] = 0
    if pre_state[1] < 0:
        pre_state[1] = 0

    if action == 119:
        Q_list[int(pre_state[0])][int(pre_state[1])][0] = (1 - alfa) * Q_list[int(pre_state[0])][int(pre_state[1])][0] + alfa * sample
    elif action == 100:
        Q_list[int(pre_state[0])][int(pre_state[1])][1] = (1 - alfa) * Q_list[int(pre_state[0])][int(pre_state[1])][1] + alfa * sample
    elif action == 115:
        Q_list[int(pre_state[0])][int(pre_state[1])][2] = (1 - alfa) * Q_list[int(pre_state[0])][int(pre_state[1])][2] + alfa * sample
    elif action == 97:
        Q_list[int(pre_state[0])][int(pre_state[1])][3] = (1 - alfa) * Q_list[int(pre_state[0])][int(pre_state[1])][3] + alfa * sample 



"""def Q_Learning_temp(state, action, W_food, W_body):
    X_head = state.getGameState()['snake_head_x']
    Y_head = state.getGameState()['snake_head_y']
    X_food = state.getGameState()['food_x']
    Y_food = state.getGameState()['food_y']
    list_snakeBody = state.getGameState()['snake_body']
    for s in list_snakeBody:
        if s < 13.0:
            F_body = -1000
            break
    F_food = 1000 / (manhatan_distance(X_head, Y_head, X_food, Y_food))
    return (W_food * F_food + W_body * F_body)
"""
agent = Snake(width=256, height=256)

env = PLE(agent, fps=15, force_fps=False, display_screen=True)

env.init()
actions = env.getActionSet()
while True:
    if env.game_over():
        env.reset_game()

    X_head = agent.getGameState()['snake_head_x']
    Y_head = agent.getGameState()['snake_head_y']

    if X_head > 255:
        X_head = 255
    if Y_head > 255:
        Y_head = 255
    if X_head < 0:
        X_head = 0
    if Y_head < 0:
        Y_head = 0
    state_now = Q_list[int(X_head)][int(Y_head)]
    max_q = max(state_now[0], state_now[1], state_now[2], state_now[3])
    
    counter = 0
    list_q_index = []
    if max_q == state_now[0]:
        counter += 1
        action = 119
        list_q_index.append(119)
    if max_q == state_now[1]:
        counter += 1
        action = 100
        list_q_index.append(100)
    if max_q == state_now[2]:
        counter += 1
        action = 115
        list_q_index.append(115)
    if max_q == state_now[3]:
        counter += 1
        action = 97
        list_q_index.append(97)
    if counter >= 2:
        action = list_q_index[np.random.randint(0, len(list_q_index))]
    
    #action = actions[np.random.randint(0, len(actions))]
    reward = env.act(action)
    Q_list_update(agent, action, reward)
