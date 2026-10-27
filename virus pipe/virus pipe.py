'''

문제 설명

1번부터 n번까지 번호가 붙은 n개의 배양체를 n-1개의 파이프로 이어 하나의 트리 모양을 만들었습니다. 
각 파이프는 A,B,C 3개의 종류 중 하나로 초기에 모든 파이프는 닫혀있습니다.

배양체 중 하나가 바이러스에 감염되어 있습니다. 
바이러스에 감염된 배양체는 열린 파이프를 통해 연결된 다른 인접한 배양체를 감염시킵니다.

당신은 종류가 같은 파이프를 한꺼번에 모두 열었다가 닫을 수 있습니다. 

단, 한 종류의 파이프를 연 후 다시 닫기 전에 다른 종류의 파이프를 열 수 없습니다. 
파이프를 열었다 닫는 행동을 최대 k번 반복해 최대한 많은 배양체에 바이러스를 감염시키려고 합니다.

배양체의 개수를 나타내는 정수 n, 
감염된 배양체의 노드 번호를 나타내는 정수 infection, 
파이프의 정보를 나타내는 2차원 정수 배열 edges, 
최대 행동 수를 나타내는 정수 k가 매개변수로 주어집니다. 

최대 k번 파이프를 열었다 닫은 후,
감염된 배양체 개수의 최댓값을 return 하도록 solution 함수를 완성해 주세요.

제한사항

2 ≤ n ≤ 100
1 ≤ infection ≤ n
edges의 길이 = n-1
edges[i]는 [x, y, type]의 형태로 x번 노드의 배양체와 y번 노드의 배양체 사이가 type 종류의 파이프로 연결되어 있음을 의미합니다.
1 ≤ x < y ≤ n
1 ≤ type ≤ 3
1은 A, 2는 B, 3은 C 를 나타냅니다.
1 ≤ k ≤ 10

'''
'''
문제 분해

- 감염된 노드 기록. is_infected = [] or edges[i][4]에 0,1 추가
- 감염 알고리즘.
    - 문을 열고 닫는 법 만들어야 함.
    - 열리고 닫혔던 문들을 기록 해야 함.
        - brute force?
        - k 길이의 문 열고 닫는 경우의 수. gate_combination
            - 같은 문을 두 번 열었다 닫았다 할 필요 없음.
            - gate_combination[k] != gate_combination[k-1]
            - 문 종류 A, B, C 중 같은게 중복되지 않게 k번
    - 노드를 순회. 
        for i in range(0, len(edges)):
            if edges[i][4] = 1 

'''

#solution1
def solution1(n, infection, edges, k):
    gate_combination_with_repeat = []
    gate_combination = []

    for c in range(3 ** k):
        combination = []
        temp = c
        for i in range(k):
            combination.append(temp % 3 + 1)
            temp = temp // 3
        gate_combination_with_repeat.append(combination)

    for c in range(0,len(gate_combination_with_repeat)):
        is_repeating = False
        temp = gate_combination_with_repeat[c]
        for i in range(len(temp)-1):
            if temp[i] == temp[i+1]:
                is_repeating = True
        if is_repeating == False:
            gate_combination.append(temp)
        is_repeating = False

    infected_combination = []

    for combination in gate_combination:
        is_infected = [0] * (n+1)
        is_infected[infection] = 1
        for gate_opened in combination:
            for edge in edges:
                current_node_number = edge[0]
                if gate_opened == edge[2] and is_infected[current_node_number] == 1:
                    is_infected[edge[1]] = 1       
        infected_combination.append(is_infected)  

    total = []
    for i in infected_combination:
        sum = 0
        for j in i:
            sum += j    
        total.append(sum)           
    answer = max(total)
    
    return answer


n = 10
infection = 1
edges = [[1, 2, 1], [1, 3, 1], [1, 4, 3], [1, 5, 2], [5, 6, 1], [5, 7, 1], [2, 8, 3], [2, 9, 2], [9, 10, 1]]
k = 2

gate_combination_with_repeat = []
gate_combination = []

for c in range(3 ** k):
    combination = []
    temp = c
    for i in range(k):
        combination.append(temp % 3 + 1)
        temp = temp // 3
    gate_combination_with_repeat.append(combination)

for c in range(0,len(gate_combination_with_repeat)):
    is_repeating = False
    temp = gate_combination_with_repeat[c]
    for i in range(len(temp)-1):
        if temp[i] == temp[i+1]:
            is_repeating = True
    if is_repeating == False:
        gate_combination.append(temp)
    is_repeating = False


graph = [[] for _ in range(n + 1)]
for x, y, t in edges:
    graph[x].append((y,t))
    graph[y].append((x,t))
    

from collections import deque


total_list = []

for combination in gate_combination:
    print('door open', combination)
   
    is_infected = [0] * (n+1)
    is_infected[infection] = 1  
        
    q = deque([infection])
    visited = [False] * (n+1)
    
    #시작 노드 설정

    #문 열기
    for opened_gate in combination:
        for i in range(0,len(is_infected)):
            if is_infected[i] == 1:
                visited[i] = True
                q.append(i)
                
        while q:
            node = q.popleft()
            is_infected[node] = 1
            for nxt, gate_type in graph[node]:
                if (visited[nxt] != True) and (gate_type == opened_gate):
                    visited[nxt] = True
                    q.append(nxt)
        total_list.append(sum(is_infected))
print(max(total_list))