import argparse
import math
import random
import time
import CARP_solver

INF = 0x3f3f3f3f
n, S, taskCnt, m, lim = 0, 0, 0, 0, 0
edges, tasks = [], []
dis = []
start_time, end_time = 0, 0
online_judge = False


def readData(file_str: str):
    global n, S, taskCnt, m, lim
    global dis
    with open(file_str, 'r') as f:
        buf = []
        for i in range(8):
            buf.append(f.readline().split(':')[1])
        n, S, taskCnt, m, lim = int(buf[1]), int(buf[2]), int(buf[3]), int(buf[3]) + int(buf[4]), int(buf[6])
        dis = [[INF] * (n + 5) for i in range(n + 5)]
        f.readline()
        es = f.readlines()
        for tmp in es:
            if tmp == 'END':
                break
            edge = tuple(map(int, tmp.split()))
            edges.append(edge)
            u, v, c, d = edge
            dis[u][v] = dis[v][u] = c
            if edge[3]:
                tasks.append(edge)


def Floyd():
    for i in range(1, n + 1):
        dis[i][i] = 0
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j])


def cal_cost(buf):
    cur, last = S, lim
    res = 0
    for u, v, w, d in buf:
        if last < d:
            last = lim
            res += dis[cur][S]
            cur = S
        last -= d
        fir = dis[cur][v] + w
        sec = dis[cur][u] + w
        if fir < sec:
            cur = u
            res += fir
        else:
            cur = v
            res += sec
    res += dis[cur][S]
    return res


def anneal():
    buf = tasks.copy()
    # random.shuffle(buf)
    temperature = 1e4
    rate = 0.9998
    # rate = 0.99
    while temperature > 1e-4:
        temperature *= rate
        pre_val = cal_cost(buf)
        fir, sec = random.randint(0, taskCnt - 1), random.randint(0, taskCnt - 1)
        buf[fir], buf[sec] = buf[sec], buf[fir]
        new_val = cal_cost(buf)
        delta = (new_val - pre_val) / pre_val
        if delta == 0:
            continue
        exp_val = -delta / temperature
        if exp_val > 0:
            continue
        if math.exp(exp_val) < random.random():
            buf[fir], buf[sec] = buf[sec], buf[fir]

    return buf, cal_cost(buf)


def printDet(buf):
    cur, last = S, lim
    b, res = [], []
    for u, v, w, d in buf:
        if last < d:
            last = lim
            cur = S
            if b:
                res.append(b.copy())
            b.clear()
        last -= d
        fir = dis[cur][v] + w
        sec = dis[cur][u] + w
        if fir < sec:
            cur = u
            b.append((v, u))
        else:
            cur = v
            b.append((u, v))

    if b:
        res.append(b.copy())

    print('s ', end='')
    for i in range(len(res)):
        print('0,', end='')
        for u, v in res[i]:
            print(f'({u},{v}),', end='')
        print('0', end='')
        if i != len(res) - 1:
            print(',', end='')
    print('')
    print(f'q {cal_cost(buf)}')


def preWork():
    global tasks
    cnt, cost = 100, INF
    while cnt:
        cnt -= 1
        buf = tasks.copy()
        random.shuffle(buf)
        new_val = cal_cost(buf)
        if new_val < cost:
            cost = new_val
            tasks = buf.copy()
    print(cost)


def solve():
    Floyd()
    preWork()
    # path_scanning()
    res, cost = [], INF

    global tasks
    # path_scanning()
    if online_judge:
        while time.time() + 5 < end_time:
            cur_det, new_cost = anneal()
            if new_cost < cost:
                cost = new_cost
                res = cur_det
    else:
        for i in range(5):
            cur_det, new_cost = anneal()
            if new_cost < cost:
                cost = new_cost
                res = cur_det

    printDet(res)


def OnlineJudge():
    # Command:
    # python CARP_solver.py ./CARP_samples/val1A.dat -t 10 -s 0
    global start_time, end_time
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    parser.add_argument('-t', type=float)
    parser.add_argument('-s', type=float)
    args = parser.parse_args()
    end_time = start_time + args.t
    random.seed(args.s)
    return args.file


if __name__ == '__main__':
    online_judge = False
    # online_judge = True
    if online_judge:
        readData(OnlineJudge())
    else:
        # file_str = 'val1A.dat'
        # file_str = 'val4A.dat'
        # file_str = 'egl-s1-A.dat'
        file_str = 'gdb10.dat'
        # file_str = 'byMe1.dat'
        # file_str = 'val7A.dat'
        readData('./CARP_samples/' + file_str)
    # Floyd()
    # print(tasks)
    # print(cal_cost(tasks))
    solve()
    # Floyd()
    # printDet(tasks)
    # print(cal_cost(tasks))
