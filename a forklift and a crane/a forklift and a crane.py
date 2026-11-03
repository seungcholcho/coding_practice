'''
A 회사의 물류창고에는 알파벳 대문자로 종류를 구분하는 컨테이너가 세로로 n 줄, 가로로 m줄 총 n x m개 놓여 있습니다.
특정 종류 컨테이너의 출고 요청이 들어올 때마다 지게차로 창고에서 접근이 가능한 해당 종류의 컨테이너를 모두 꺼냅니다.
접근이 가능한 컨테이너란 4면 중 적어도 1면이 창고 외부와 연결된 컨테이너를 말합니다.
최근 이 물류 창고에서 창고 외부와 연결되지 않은 컨테이너도 꺼낼 수 있도록 크레인을 도입했습니다.
크레인을 사용하면 요청된 종류의 모든 컨테이너를 꺼냅니다.

위 그림처럼 세로로 4줄, 가로로 5줄이 놓인 창고를 예로 들어보겠습니다. 
이때 "A", "BB", "A" 순서대로 해당 종류의 컨테이너 출고 요청이 들어왔다고 가정하겠습니다.
“A”처럼 알파벳 하나로만 출고 요청이 들어올 경우 지게차를 사용해 출고 요청이 들어온 순간 접근 가능한 컨테이너를 꺼냅니다.
"BB"처럼 같은 알파벳이 두 번 반복된 경우는 크레인을 사용해 요청된 종류의 모든 컨테이너를 꺼냅니다.

위 그림처럼 컨테이너가 꺼내져 3번의 출고 요청 이후 남은 컨테이너는 11개입니다.
두 번째 요청은 크레인을 활용해 모든 B 컨테이너를 꺼냈음을 유의해 주세요.
세 번째 요청이 들어왔을 때 2행 2열의 A 컨테이너만 접근이 가능하고 2행 3열의 A 컨테이너는 접근이 불가능했음을 유의해 주세요.

처음 물류창고에 놓인 컨테이너의 정보를 담은 1차원 문자열 배열 storage와 출고할 컨테이너의 종류와 출고방법을 요청 순서대로 담은 1차원 문자열 배열 requests가 매개변수로 주어집니다.
이때 모든 요청을 순서대로 완료한 후 남은 컨테이너의 수를 return 하도록 solution 함수를 완성해 주세요.

제한사항
2 ≤ storage의 길이 = n ≤ 50
2 ≤ storage[i]의 길이 = m ≤ 50
storage[i][j]는 위에서 부터 i + 1번째 행 j + 1번째 열에 놓인 컨테이너의 종류를 의미합니다.
storage[i][j]는 알파벳 대문자입니다.
1 ≤ requests의 길이 ≤ 100
1 ≤ requests[i]의 길이 ≤ 2
requests[i]는 한 종류의 알파벳 대문자로 구성된 문자열입니다.
requests[i]의 길이가 1이면 지게차를 이용한 출고 요청을, 2이면 크레인을 이용한 출고 요청을 의미합니다.

테스트 케이스 구성 안내
아래는 테스트 케이스 구성을 나타냅니다. 각 그룹 내의 테스트 케이스를 모두 통과하면 해당 그룹에 할당된 점수를 획득할 수 있습니다.
그룹	총점	추가 제한 사항
#1	10%	requests에 크레인을 사용한 출고 요청만 존재합니다.
#2	15%	requests에 지게차를 사용한 출고 요청만 존재합니다.
#3	25%	requests에 컨테이너의 종류가 최대 한 번씩 등장합니다. 즉, 이전에 꺼낸 컨테이너 종류를 다시 꺼내지 않습니다.
#4	50%	제한사항 외 추가조건이 없습니다.


'''

'''
세로 n줄(행의 수) 가로 m줄(열의 수)
외부와 접근 가능한지 체크하기.
공백 패딩을 만들어야 함.
컨볼루션필터? 를 만들어서 해당 칸 상하좌우로 공백이 있으면 외부와 접근 가능 => 크레인으로 꺼낸 블럭은 탐지 안됨.
or 외곽선의 좌표를 저장하는 배열?
m*n의 가장 초기상태의 외곽선 좌표배열 outline
outline = [0,0]~[0,m], [0,0][n,0], [n,0][n,m], [0,m][n,m]


if len(requests[r]) == 1:   
    new_outline = []
    for(i,j) in outline:
        if storage[i][j] == requests[r]:
            new_outline.append([i-1,j], [i,j-1], [i+1, j], [i, j+1])
        
'''

def print_list(arr):
    for row in arr:
        print(row)

from collections import deque
def outside_update(storage,outside):
    n, m = len(storage), len(storage[0])
    visited = [[0]* (m+2) for _ in range(n+2)]
    que = deque()
    que.append([0,0])
    while que:
        i, j = que.popleft()
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = i + dr, j + dc
            if(0 <= nr and nr <len(storage) and 0<=nc and nc<len(storage[0])):
                visited[nr][nc]=1  
                if(storage[nr][nc] == '.' and visited[nr][nc]==0):
                    que.append([nr,nc])        
    return visited
            
            
    '''
    for i in range(0,len(storage)):
        for j in range(0,len(storage[0])):
            if storage[i][j] == '.' and outside[i][j] != 1:
                for dr, dc in [(-1,0),(1,0),(0,1),(0,-1)]:
                        nr, nc = i + dr, j + dc
                        if(0 <= nr and nr <= len(storage) and 0<=nc and nc<=len(storage[0])):
                            if outside[nr][nc] == 1:
                                new_outside[i][j] = 1
    '''                          
    
def forklift(storage, outside, letter):
    new_storage = storage
    for i in range(0,len(storage)):
        for j in range(0,len(storage[0])):
            if(storage[i][j] == letter[0]):
                for dr, dc in [(-1,0),(1,0),(0,1),(0,-1)]:
                    nr, nc = i + dr, j + dc
                    if(0 <= nr and nr <= len(storage) and 0<=nc and nc<=len(storage[0])):
                        if(outside[nr][nc]==1):
                            new_storage[i][j] = '.'
    return new_storage

def crane(storage, letter):
    for i in range(0,len(storage)):
            for j in range(0,len(storage[0])):
                if(storage[i][j] == letter[0]):
                    storage[i][j] = '.'
    return storage

def solution(storage, requests):
    n, m = len(storage), len(storage[0])
    outside = [[0]* (m+2) for _ in range(n+2)]
    temp = [list(row) for row in storage]
    
    pad = ['.']
    storage = [pad * (m+2)]
    for row in temp:
        storage.append(pad + row + pad)
    storage.append(pad * (m+2))
    
    for i in range(0,n+2):
        for j in range(0,m+2):
            if i == 0 or j == 0 or i == n+1  or j == m+1:
                outside[i][j] = 1
    for r in requests:
        if len(r) == 1:
            storage = forklift(storage,outside,r)
            outside = outside_update(storage,outside)
        else:
            storage = crane(storage,r)
            outside = outside_update(storage,outside)
    answer = 0
    
    for row in storage:
        for col in row:
            if col != '.':
                answer +=1
    
    return answer

storage = ["HAH", "HBH", "HHH", "HAH", "HBH"]
requests = ["C", "B", "B", "B", "B", "H"]

print('answer is:' , solution(storage, requests))

tests = [
    # 1. 아래에서 위로 뚫린 통로
    (["BBBBB",
      "BCACB",
      "BCACB",
      "BCACB",
      "BBABB"], ["AA", "C"], 15),     # 지금 코드: 21

    # 2. 오른쪽에서 왼쪽으로 뚫린 통로
    (["BBBBB",
      "BCCCB",
      "BAAAA",
      "BCCCB",
      "BBBBB"], ["AA", "C"], 15),     # 지금 코드: 21

    # 3. 아래에서 위로, 다시 왼쪽으로 꺾이는 통로
    (["BBBBBB",
      "BAAAAB",
      "BCCCAB",
      "BCCCAB",
      "BBBBAB"], ["AA", "C"], 19),    # 지금 코드: 23

    # 4. 랜덤 비교에서 찾은 반례
    (["BBABAB",
      "BBBABB",
      "BBBABA",
      "BBBAAA"], ["AA", "B"], 2),     # 지금 코드: 3
]

for storage, requests, expected in tests:
    result = solution(storage, requests)
    print("OK" if result == expected else "FAIL", result, expected, requests)