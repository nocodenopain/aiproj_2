import argparse
import random
import time

INF = 0x3f3f3f3f
start_time = 0
end_time = 0
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
        buf = []
        for i in range(8):
            buf.append(f.readline().split(':')[1])
        n, depot, require_edge, not_require_edge, capacity = int(buf[1]), int(buf[2]), int(buf[3]), int(buf[3]) + int(
            buf[4]), int(buf[6])
        dis = [[INF] * (n + 5) for i in range(n + 5)]
        f.readline()
        es = f.readlines()
        # cnt = 0
        for tmp in es:
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


def cal_cost(buf):
    cur, last = depot, capacity
    res = 0
    for u, v, w, d in buf:
        if last < d:
            last = capacity
            res += dis[cur][depot]
            cur = depot
        last -= d
        fir = dis[cur][v] + w
        sec = dis[cur][u] + w
        if fir < sec:
            cur = u
            res += fir
        else:
            cur = v
            res += sec
    res += dis[cur][depot]
    return res


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


def print_ans():
    global capacity, tasks
    tmp = capacity
    cost = basic_cost()
    cnt = 0
    ans = [[]]
    for edge in tasks:
        if tmp < edge[3]:
            ans.append([])
            cnt += 1
            tmp = capacity
        ans[cnt].append((edge[0], edge[1]))
        tmp -= edge[3]
    # print(ans)
    print('s ', end='')
    for i in range(cnt + 1):
        print('0,', end='')
        for u, v in ans[i]:
            print(f'({u},{v}),', end='')
        print('0', end='')
        if i != cnt:
            print(',', end='')
    print('')
    print(f'q {cost}')


def print_():
    cost = basic_cost()
    ans = []
    for edge in tasks:
        ans.append([(edge[0], edge[1])])
    cnt = len(ans) - 1
    print('s ', end='')
    for i in range(cnt + 1):
        print('0,', end='')
        for u, v in ans[i]:
            print(f'({u},{v}),', end='')
        print('0', end='')
        if i != cnt:
            print(',', end='')
    print('')
    print(f'q {cost}')


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


def printDet(buf):
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
    print(f'q {cal_cost(buf)}')


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


if __name__ == "__main__":
    readData(OpenFile())
    # floyd()
    # path_scanning()
    # print_ans()
    # file_str = 'egl-s1-A.dat'
    # readData('./CARP_samples/' + file_str)
    floyd()
    t = time.time()
    cost = cal_cost(tasks)
    while time.time() - t < 5:
        tmp = path_scanning()
        temp = cal_cost(tmp)
        if temp < cost:
            tasks = tmp
            cost = temp
            # print(cost)
    # path_scanning()
    # print()
    cost = cal_cost(tasks)
    # print(cost)
    t = time.time()
    t_a = (end_time - start_time) / 8
    while time.time() - t < 3 * t_a:
        m = big_mutate()
        m_cost = cal_cost(m)
        if m_cost < cost:
            cost = m_cost
            # print(cost)
            tasks = m
    # print()
    t = time.time()
    while time.time() - t < 4 * t_a:
        m = mutate(tasks)
        m_cost = cal_cost(m)
        if m_cost < cost:
            cost = m_cost
            # print(cost)
            tasks = m
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
    printDet(tasks)
