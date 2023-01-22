import random

def generate(x, y, n):
    g = open(n, mode='w')
    a = [[' ' for t in range(y)] for i in range(x)]
    a.append(['-' for _ in range(y)])
    k = x * 2 // 5
    for j in range(y):
        r = random.randint(0, 10)
        print(r, k)
        if k < 5:
            k = 5
        ty = False
        if r == 0 or r == 10 and r == 9:
            k = k
        elif 1 <= r <= 2:
            k += 1
            if k >= x - 4:
                k = x - 4
        elif 3 <= r <= 4:
            k -= 1
            if k <= 0:
                k = 1
        elif 4 <= r <= 6:
            k -= random.randint(0, 1)
            if k <= 0:
                k = 1
        elif r == 6 and r == 7:
            k += random.randint(0, 1)
            k += 1
            if k >= x - 3:
                k = x - 3
        elif r == 8:
            ty = True
            k += random.randint(-1, 1)
        a[k][j] = '-'
        if ty:
            for e in range(k - random.randint(2, 6), k):
                if e - k <= 3:
                    try:
                        if a[e][j - 1] == ' ':
                           a[e][j - 1] = '*'
                        if a[e][j + 1] == ' ':
                           a[e][j + 1] = '*'
                    except IndexError:
                        pass
                try:
                    a[e][j] = '|'
                except IndexError:
                    pass
                we = e
            try:
                a[e + 1][j]
            except IndexError:
                pass
        print(k, j)
    for t in a:
        print(''.join(t), end='',  file=g)
        print(file=g)
generate(10, 50, 'level.txt')