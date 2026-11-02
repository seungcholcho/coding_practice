from collections import deque

def sliding_min(list, w):
    dq = deque()
    min_list = []
    for i in range(len(list)):
        while(dq and (list[i] <= list[dq[-1]])):
            dq.pop()
        dq.append(i)
        if(i - dq[0] >= w):
            dq.popleft()
        if (i >= w-1):
            min_list.append(list[dq[0]])
    return(min_list)

def list_transition(arr):
    list_t = [[0] * len(arr) for _ in range(len(arr[0]))]
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            list_t[j][i] = arr[i][j]
    return list_t

def find_max(arr):
    max = 0
    cur_val = 0
    x, y = -1, -1
    for i in range(0,len(arr)):
        for j in range(0,len(arr[0])):
            cur_val = arr[i][j]
            if cur_val > max:
                max = cur_val
                x, y = i, j
    return([x, y])

def solution(m, n, h, w, drops):
    field = [[len(drops)+1] * n for _ in range(m)]
    seq = 1

    for d in drops:
        x, y = d[0], d[1]
        field[x][y] = seq
        seq += 1
    min_field = []
    for row in field:
        min_field.append(sliding_min(row, w))

    #transition to get col min
    temp = list_transition(min_field) # copy to temp
    min_field = [] # empty min_field
    for col in temp:
        min_field.append(sliding_min(col, h))
    
    min_field = list_transition(min_field)
    
    for f in min_field:
        print (f)         
    answer = find_max(min_field)
    
    print(answer)
    return answer

m=3
n=3 
h=1 
w=1 
drops = [[0, 0], [0, 1], [0, 2], [1, 0]]

solution(m,n,h,w,drops)