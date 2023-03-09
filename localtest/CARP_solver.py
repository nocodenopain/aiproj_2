import argparse
import math
import random
import threading
import time
from multiprocessing import Process


# INF = 0x3f3f3f3f
# start_time = 200
# end_time = 250
# n = 0
# depot = 1
# require_edge = 0
# not_require_edge = 0
# # vehicles = 0
# capacity = 0
# # total_cost = 0
# graph = [[]]
# dis = []
# edges = []
# tasks = []
# task_set = []
# thread_test = []
# ans = []


def OpenFile():
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


def readData(file_str: str):
    global n, depot, require_edge, not_require_edge, capacity
    global dis
    global tasks
    with open(file_str, 'r') as f:
        inputData = []
        for i in range(8):
            inputData.append(f.readline().split(':')[1])
        # n, depot, require_edge, not_require_edge, capacity = int(buf[1]), int(buf[2]), int(buf[3]), int(buf[3]) + int(
        #     buf[4]), int(buf[6])
        n = int(inputData[1])
        depot = int(inputData[2])
        require_edge = int(inputData[3])
        not_require_edge = int(inputData[4])
        capacity = int(inputData[6])
        dis = [[INF] * (n + 5) for i in range(n + 5)]
        f.readline()
        edge_line = f.readlines()
        # cnt = 0
        for tmp in edge_line:
            # cnt += 1
            # if cnt == 11:
            #     break
            if tmp == 'END':
                break
            edge = tuple(map(int, tmp.split()))
            edges.append(edge)
            u, v, c, d = edge
            dis[u][v] = dis[v][u] = c
            if edge[3]:
                tasks.append(edge)


def floyd():
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                dis[j][k] = min(dis[j][i] + dis[i][k], dis[j][k])

    for i in range(1, n + 1):
        dis[i][i] = 0


def calculate_cost(buf):
    cur, last = depot, capacity
    ans = 0
    for u, v, w, d in buf:
        if last < d:
            last = capacity
            ans += dis[cur][depot]
            cur = depot
        last -= d
        fir = dis[cur][v] + w
        sec = dis[cur][u] + w
        if fir < sec:
            cur = u
            ans += fir
        else:
            cur = v
            ans += sec
    ans += dis[cur][depot]
    return ans


# def cal_cost(task):
#     global capacity
#     global depot
#     node = depot
#     tmp = capacity
#     # road = task.copy()
#     cost = 0
#     for edge in task:
#         if edge[3] > capacity:
#             cost += dis[node][depot]
#             node = depot
#             tmp = capacity
#         if dis[node][edge[0]] < dis[node][edge[1]]:
#             cost += dis[node][edge[0]]
#             cost += edge[2]
#             node = edge[1]
#             tmp -= edge[3]
#         else:
#             cost += dis[node][edge[1]]
#             cost += edge[2]
#             node = edge[0]
#             tmp -= edge[3]
#     cost += dis[node][depot]
#     return cost

INF = 0x3f3f3f3f

start_time = 200
end_time = 250
n = 0
depot = 1
require_edge = 0
not_require_edge = 0
# vehicles = 0
capacity = 0
# total_cost = 0
graph = [[]]
dis = []
edges = []
tasks = []
task_set = []
thread_test = []
ans = []


def flip(t):
    global tasks
    mutation = t.copy()
    r1 = random.randint(0, len(tasks) - 1)
    r2 = random.randint(0, len(tasks) - 1)
    while r1 == r2:
        r2 = random.randint(0, len(tasks) - 1)
    tmp = mutation[r1]
    mutation[r1] = mutation[r2]
    mutation[r2] = tmp
    return mutation


def single_insert(t):
    global tasks
    mutation = t.copy()
    r1 = random.randint(0, len(tasks) - 1)
    e = mutation[r1]
    mutation.remove(e)
    r2 = random.randint(0, len(tasks))
    mutation.insert(r2, e)
    return mutation


def double_insert(t):
    global tasks
    mutation = t.copy()
    r1 = random.randint(0, len(tasks) - 2)
    e1 = mutation[r1]
    e2 = mutation[r1 + 1]
    mutation.remove(e1)
    mutation.remove(e2)
    r2 = random.randint(0, len(tasks))
    mutation.insert(r2, e1)
    mutation.insert(r2 + 1, e2)
    return mutation


def find_edge(free, cur):
    e = free[0]
    list = []
    d = dis[cur][e[0]]
    for edge in free:
        dtmp = dis[cur][edge[0]]
        if dtmp < d:
            d = dtmp
    for edge in free:
        dtmp = dis[cur][edge[0]]
        if dtmp == d:
            list.append(edge)
    return list


def path_scanning():
    global tasks, depot, capacity, dis
    free = tasks.copy()
    ans = []
    tmp = capacity
    cur = depot
    while len(free) > 0:
        list = find_edge(free, cur)
        e = list[random.randint(0, len(list) - 1)]
        if e[3] > tmp:
            tmp = capacity
            cur = depot
            list = find_edge(free, cur)
            e = list[random.randint(0, len(list) - 1)]
        free.remove(e)
        ans.append(e)
        tmp -= e[3]
        cur = e[1]
    return ans


def basic_cost():
    c = 0
    tmp = capacity
    cur = depot
    for e in tasks:
        if tmp < e[3]:
            tmp = capacity
            c += dis[cur][depot]
            cur = depot
        tmp -= e[3]
        c += dis[cur][e[0]]
        c += e[2]
        cur = e[1]
        # c += dis[cur][e[1]]
    c += dis[cur][depot]
    return c


def printData(buf):
    cur, last = depot, capacity
    b, res = [], []
    for u, v, w, d in buf:
        if last < d:
            last = capacity
            cur = depot
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
    print(f'q {calculate_cost(buf)}')


def mutate(t):
    r = random.randint(0, 3)
    if r == 0:
        return flip(t)
    elif r == 1:
        return single_insert(t)
    else:
        return double_insert(t)


def big_mutate():
    ans = tasks.copy()
    for i in range(0, 3):
        ans = mutate(ans)
    return ans


def t_mutate(buf, t_a):
    t = time.time()
    cost = calculate_cost(buf)
    while time.time() - t < t_a:
        new = mutate(buf)
        t_c = calculate_cost(new)
        if t_c < cost:
            cost = t_c
            buf = new
    ans.append(buf)


if __name__ == "__main__":
    readData(OpenFile())
    # floyd()
    # path_scanning()
    # print_ans()
    # file_str = 'egl-s1-A.dat'
    # readData(file_str)
    floyd()
    t = time.time()
    cost = calculate_cost(tasks)
    while time.time() - t < 10:
        tmp = path_scanning()
        temp = calculate_cost(tmp)
        if temp < cost:
            tasks = tmp
            cost = temp
            task_set.append(tmp)
            # print(cost)
        # path_scanning()
        # print("?")
    while len(task_set) < 8:
        m = path_scanning()
        task_set.append(m)

    for i in range(-8, 0):
        thread_test.append(task_set[i])
    # print(time.time())
    t = end_time - start_time - 15
    t /= 8
    # thread1 = threading.Thread(name='t1', target=t_mutate(thread_test[0], t))
    # thread2 = threading.Thread(name='t2', target=t_mutate(thread_test[1], t))
    # thread3 = threading.Thread(name='t3', target=t_mutate(thread_test[2], t))
    # thread4 = threading.Thread(name='t4', target=t_mutate(thread_test[3], t))
    # thread5 = threading.Thread(name='t5', target=t_mutate(thread_test[4], t))
    # thread6 = threading.Thread(name='t6', target=t_mutate(thread_test[5], t))
    # thread7 = threading.Thread(name='t7', target=t_mutate(thread_test[6], t))
    # thread8 = threading.Thread(name='t8', target=t_mutate(thread_test[7], t))
    p1 = Process(target=t_mutate(thread_test[0], t))
    p2 = Process(target=t_mutate(thread_test[1], t))
    p3 = Process(target=t_mutate(thread_test[2], t))
    p4 = Process(target=t_mutate(thread_test[3], t))
    p5 = Process(target=t_mutate(thread_test[4], t))
    p6 = Process(target=t_mutate(thread_test[5], t))
    p7 = Process(target=t_mutate(thread_test[6], t))
    p8 = Process(target=t_mutate(thread_test[7], t))
    # print(time.time())
    # thread1.start()
    # thread2.start()
    # thread3.start()
    # thread4.start()
    # thread5.start()
    # thread6.start()
    # thread7.start()
    # thread8.start()
    # print(cost)
    cost = calculate_cost(ans[0])
    tasks = ans[0]
    for i in range(1, len(ans)):
        tmp = calculate_cost(ans[i])
        # print(tmp)
        if tmp < cost:
            cost = tmp
            tasks = ans[i]
    # print_()
    # print(tasks)
    # print(cal_cost(tasks))
    # random_run()

    # path_scanning()
    # print_ans()
    # print(tasks)
    # printDet(tasks)
    # print(tasks)
    # print(capacity)
    # basic_cost()
    printData(tasks)
