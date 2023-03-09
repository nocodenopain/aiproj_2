# # import random
# # import threading
# #
# # ans = 0
# #
# #
# # def test(a):
# #     tmp = random.randint(1, 100)
# #     if tmp > a:
# #         a = tmp
# #
# #
# # thread1 = threading.Thread(name='t1', target=test, args=ans)
# # thread2 = threading.Thread(name='t2', target=test, args=ans)
# # thread1.start()
# # thread2.start()
#
# import threading
#
# ans = 0
#
#
# def test(x, y):
#     global ans
#     for i in range(x, y):
#         if ans < i:
#             ans = i
#
#
# thread1 = threading.Thread(name='t1', target=test, args=(1, 1000))
# thread2 = threading.Thread(name='t2', target=test, args=(11, 2000))
# thread1.start()  # 启动线程1
# thread2.start()  # 启动线程2
# print(ans)

list = [1, 3, 5, 7]
list.insert(4, 4)
for i in range(-5, -1):
    print(list[i])
