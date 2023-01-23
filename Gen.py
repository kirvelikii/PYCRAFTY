import random

def generate(x, y, n):
    g = open(n, mode='w')
    a = [[' ' for t in range(y)] for i in range(x)]
    a.append(['-' for _ in range(y)])
    k = x * 4 // 5
    for j in range(y):
        r = random.randint(0, 10)
        if k < 10:
            k = 7
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
        elif r == 8 and 3 <= j <= len(a[0]) - 3:
            ty = True
            k += random.randint(-1, 1)
        a[k][j] = '-'
        if ty and '|' not in a[k + 1 : k - 3][j - 3: j + 3]:
            we = k - random.randint(5, 8)
            for e in range(we, k):
                if k - e >= 3:
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
            try:
                a[we][j] = '*'
            except IndexError:
                pass
    for kk in range(len(a[0])):
        whi = False
        for i in range(len(a)):
            if whi:
                err = random.randint(i, 100)
                if err > 95:
                    a[i][kk] = 'R'
                elif err <= 60 and i < 60:
                    a[i][kk] = 'E'
                else:
                    a[i][kk] = 'S'
            if a[i][kk] == '-':
                whi = True

    for t in a:
        print(''.join(t), end='',  file=g)
        print(file=g)
generate(10, 50, 'level.txt')