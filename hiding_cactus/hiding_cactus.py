"""
선인장 숨기기

m개의 행과 n개의 열로 구성된 격자가 주어지며, 이는 사막 지도를 나타냅니다.
사막 지도의 가장 왼쪽 위칸 좌표는 (0, 0), 오른쪽 아래칸 좌표는 (m-1, n-1)입니다. 
이 사막 어딘가에 가로 w, 세로 h 크기의 선인장구역을 조성하려 합니다. 
선인장 구역은 격자 축에 맞춘 연속된 w × h 크기의 부분 격자이며, 회전할 수 없습니다.

비구름은 미리 정해진 순서대로 격자의 여러 칸에 비를 뿌립니다. 
이때 빗방울이 처음으로 선인장 구역에 포함된 칸에 떨어졌을 때, 그 시점을 선인장이 처음으로 비를 맞는 순간으로 기록합니다.
당신은 선인장이 가능한 한 늦게 비를 맞도록, 선인장 구역의 위치를 정하려고 합니다.
    선인장이 비를 맞지 않도록 선인장 구역의 위치를 정할 수 있다면 해당 위치가 가장 우선됩니다.
    가능한 늦게 비를 맞는 선인장 구역 후보가 여러 개라면 그중 가장 위쪽 행, 그래도 여러 개면 가장 왼쪽 열에 위치한 구역을 선택합니다.
    
격자의 세로 길이와 가로 길이를 나타내는 정수 m, n, 선인장 구역의 세로 길이와 가로 길이를 나타내는 정수 h, w, 
그리고 빗방울이 떨어지는 순서대로 칸의 좌표를 담은 2차원 정수 배열 drops가 매개변수로 주어집니다. 
주어진 조건을 만족하는 선인장 구역에 포함된 가장 왼쪽 위칸의 좌표를 정수 배열로 return 하도록 solution 함수를 완성해 주세요.

제한사항
1 ≤ m, n ≤ 500,000
1 ≤ m x n ≤ 500,000
1 ≤ h ≤ m
1 ≤ w ≤ n
1 ≤ drops의 길이 ≤ m x n
drops[i]는 [r, c] 형태입니다.
drops[i]는 i + 1번째로 떨어진 빗방울의 좌표를 의미합니다.
0 ≤ r < m
0 ≤ c < n
drops의 모든 원소는 서로 다른 칸을 나타냅니다.

"""
'''
문제분해

1. m * n 구역 내, h * w 크기의 선인장이 존재할 수 있는 위치 중, 비를 가장 늦게 맞는 곳 찾기
2. 선인장의 좌상단 좌표 [i,j] 기준, 선인장 구역 내 빗방울의 최소값 구하기
    - [0,0]에 위치했을 때, 비를 가장 먼저 맞는 시간(구역내 drops의 최소값) t1
    - [0,1]에 위치했을 때, 비를 가장 먼저 맞는 시간(구역내 drops의 최소값) t2
    - ...
    - [i,j]에 위치했을 때, 비를 가장 먼저 맞는 시간(구역내 drops의 최소값) tn
2.1. 특정 구역 내 최소값을 구하는 방법
    - 완전 탐색
    - 슬라이딩 윈도우 최솟값
3. tn이 최대값인 곳이 정답.
'''

'''
pseudo code

1. m * n의 행렬에 drop 순서 저장, 비가 내리지 않는 곳은 0.
    field = [[len(drops)+1] * n for _ in range(m)]
    for idx, (r, c) in enumerate(drops):
        field[r][c] = idx + 1

2. m * n의 행렬 위에 h * w의 컨볼루션 서치 필터 생성

3. 필터의 위치별 필터 범위 내의 최소값 저장.
    sets = []
    for i in range(m-h+1):
        for j in range(n-w+1):
            cur_min = field[i][j]
            for a in range(h):
                for b in range(w):
                    temp = field[i+a][j+b]
                    if temp < cur_min:
                        cur_min = temp
            sets.append([i,j,cur_min])
4. sets의 cur_min의 최대값을 가진 좌표가 정답.
    results = max(sets, key = lambda x:[2])
    answer = results[0:2]
'''

def solution1(m, n, h, w, drops):
    field = [[len(drops)+1] * n for _ in range(m)]
    for idx, (r, c) in enumerate(drops):
        field[r][c] = idx + 1
    sets = []
    for i in range(m-h+1):
        for j in range(n-w+1):
            cur_min = field[i][j]
            for a in range(h):
                for b in range(w):
                    temp = field[i+a][j+b]
                    if temp < cur_min:
                        cur_min = temp
            sets.append([i,j,cur_min])
    results = max(sets, key = lambda x:x[2])
    answer = results[0:2]
    return answer


"""
처음 써본 것:
- 특정 값으로 채워진 n*m 크기의 행렬 생성
    field = [[len(drops)+1] * n for _ in range(m)]
    for i(dx, (r, c) in enumerate(drops):
        field[r][c] = idx + 1
        
- 여러개의 인자를 가진 행렬의 특정 인자의 최대값구하는 법
    results = max(sets, key = lambda x:x[2]) 
        
- 컨볼루션 필터 만들기
    for i in range(m-h+1):
        for j in range(n-w+1):
            cur_min = field[i][j]
            for a in range(h):
                for b in range(w):
                    temp = field[i+a][j+b]
                    if temp < cur_min:
                        cur_min = temp

한계:
1. 시간복잡도: 정답은 맞추나 컨볼루션 필터의 4중 포문, 연산량이 어마어마함.
    -> 최소값을 구할 때 sliding window와 deque을 사용할 것.
    -> field의 각 행에 길이 w의 슬라이딩 윈도우로 각 행의 구역별 최소값 표 min_row 구하기
    -> min_row의 각 열에 길이 h의 슬라이딩 윈도우로 각 열의 구역별 최소값 표 min_list 구하기
    -> min_list의 [i][j]가 최대값인 곳 찾기
    -> 최대값이 두 개가 있다면, 좌상단에 위치한 좌표 선정

"""


from collections import deque

def sliding_min(arr, w):
    window = []
    min_list = []
    for i in range(len(arr)):
        window.append(arr[i])
        if (len(window)>=w):
            min_list.append(min(window))
            window.pop(0)
    return min_list
    
def solution2(m, n, h, w, drops):
    field = [[len(drops)+1] * n for _ in range(m)]
    temp = []
    temp2 = []
    min_list = []
    for idx, (r, c) in enumerate(drops):
        field[r][c] = idx + 1
    
    for row in field:
        temp.append(sliding_min(row,w))
    
    for col in zip(*temp):
        temp2.append(sliding_min(col,h))
    
    for col in zip(*temp2):
        min_list.append(col)
    
    max_val = max(map(max,min_list))
    
    answer = []
    for i in range(len(min_list)):
        for j in range(len(min_list[0])):
            if min_list[i][j] == max_val:
                answer = [i,j]
                return answer
    return answer

'''
solution2의 개선점:
콘볼루션 필터 연산을 슬라이딩 윈도우로 대체해서 연산량 감소.

solution2의 한계점:
구간내 최소값을 구할 때 여전히 연산량이 많음. 줄여야함.

해결방안:
최소값을 구할 때, 덱을 사용해서 연산량 감소시키기.

- deque 만들기
field의 row를 하나씩 받아옴.
덱 dq에 row의 i번째 값이 들어올 때:
    1. while row[dq[-1]]의 마지막 값 > row[i], dq.pop()
    2. dq.append(i)
    3. i - dq[0] >= w, popleft()
    4. i >= w, min_list.append(row[dq[0]])



'''

from collections import deque

def sliding_min2(arr, w):
    dq = deque()
    min_list = []
    
    for i in range(len(arr)):
        while dq and arr[dq[-1]] > arr[i]:
            dq.pop()
        dq.append(i)
        if i -dq[0] >= w:
            dq.popleft()
        if i>= w-1:
            min_list.append(arr[dq[0]])
    
    return min_list
    
def solution3(m, n, h, w, drops):
    field = [[len(drops)+1] * n for _ in range(m)]
    temp = []
    temp2 = []
    min_list = []
    for idx, (r, c) in enumerate(drops):
        field[r][c] = idx + 1
    
    for row in field:
        temp.append(sliding_min2(row,w))
    
    for col in zip(*temp):
        temp2.append(sliding_min2(col,h))
    
    for col in zip(*temp2):
        min_list.append(col)
    
    max_val = max(map(max,min_list))
    
    answer = []
    for i in range(len(min_list)):
        for j in range(len(min_list[0])):
            if min_list[i][j] == max_val:
                answer = [i,j]
                return answer
    
    return answer