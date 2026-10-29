'''
A도둑과 B도둑이 팀을 이루어 모든 물건을 훔치려고 합니다. 
단, 각 도둑이 물건을 훔칠 때 남기는 흔적이 누적되면 경찰에 붙잡히기 때문에, 두 도둑 중 누구도 경찰에 붙잡히지 않도록 흔적을 최소화해야 합니다.

물건을 훔칠 때 조건은 아래와 같습니다.
- 물건 i를 훔칠 때,
    A도둑이 훔치면 info[i][0]개의 A에 대한 흔적을 남깁니다.
    B도둑이 훔치면 info[i][1]개의 B에 대한 흔적을 남깁니다.

- 각 물건에 대해 A도둑과 B도둑이 남기는 흔적의 개수는 1 이상 3 이하입니다.

경찰에 붙잡히는 조건은 아래와 같습니다.
- A도둑은 자신이 남긴 흔적의 누적 개수가 n개 이상이면 경찰에 붙잡힙니다.
- B도둑은 자신이 남긴 흔적의 누적 개수가 m개 이상이면 경찰에 붙잡힙니다.

각 물건을 훔칠 때 생기는 흔적에 대한 정보를 담은 2차원 정수 배열 info, 
A도둑이 경찰에 붙잡히는 최소 흔적 개수를 나타내는 정수 n, 
B도둑이 경찰에 붙잡히는 최소 흔적 개수를 나타내는 정수 m이 매개변수로 주어집니다. 

두 도둑 모두 경찰에 붙잡히지 않도록 모든 물건을 훔쳤을 때, 
A도둑이 남긴 흔적의 누적 개수의 최솟값을 return 하도록 solution 함수를 완성해 주세요. 

만약 어떠한 방법으로도 두 도둑 모두 경찰에 붙잡히지 않게 할 수 없다면 -1을 return해 주세요.

제한사항
1 ≤ info의 길이 ≤ 40
    - info[i]는 물건 i를 훔칠 때 생기는 흔적의 개수를 나타내며, [A에 대한 흔적 개수, B에 대한 흔적 개수]의 형태입니다.
    - 1 ≤ 흔적 개수 ≤ 3
1 ≤ n ≤ 120
1 ≤ m ≤ 120

'''

'''
생각해보기

물건 info[i]를 A가 훔치면 
A_evidence += info[i][0]
물건 info[i]를 B가 훔치면 
B_evidence += info[i][1]

if (A_evidence >= n):
    A = 체포됨

if (B_evidence >= m):
    B = 체포됨
    
if A 체포됨 or B 체포됨 in every case:
    return -1

A_evidence < n and B_evidence < m 인 A_evidence의 최소값을 구하기.

every case의 최대, 최소 개수

len(info)개를 A 혹은 B가 가져감.

every case = 2 ** len(info) 만큼.
최소 2, 최대 1,099,511,627,776  ==> brute force는 not a good idea.

n과 m이 120보다 작은 이유는
info의 최대 길이는 40 -> 각 info의 최대값은 3. 

1 * len(info) <= sum(info[][0]) <= 3 *len(info)
1 * len(info) <= sum(info[][1]) <= 3 *len(info)

모든 경우의 수를 찾지 않고 구할 수 있나..?
정보를 압축..?

최소로 추정하고 A의 개수를 늘려간다.
'''

info = [[2, 1], [2, 3], [1, 1], [3, 1], [2, 3],
        [1, 3], [1, 1], [1, 2], [2, 1], [1, 1],
        [3, 2], [1, 3], [1, 1], [3, 3], [3, 1]]
n = 1
m = 1

def solution(info,n,m):
    branch = set()
    branch.add((0,0))
    add_a = 1
    for item in info:
        temp = set()   
        for current_a, currnet_b in branch:
            for i in range(2):
                a,b = current_a, currnet_b
                if(add_a == 1):
                    if(item[i]+a>=n):
                        add_a=0
                        pass
                    else:
                        a+=item[i]
                        add_a=0
                        temp.add((a,b))
                elif(add_a ==0):
                    if(item[i]+b>=m):
                        add_a=1
                        pass
                    else:
                        b += item[i]
                        add_a=1
                        temp.add((a,b))
        branch = temp
    if branch:
        a, b = min(branch)
        return a
    else:
        return -1

answer = solution(info,n,m)
print(answer)    


'''
info.sort()

cases = []

for c in range(2**len(info)):
    binary = []
    temp = c
    for j in range(len(info)):
        binary.append(temp%2)
        temp = temp // 2
    cases.append(binary)
    
minimum_list = []
    
for c in cases:
    print('trying cases: ', c)
    print(info)
    A_evidence = 0
    B_evidence = 0
    A_caught = False
    B_caught = False
    
    for i in range(0,len(c)):       
        if c[i] == 0:
            print('adding',info[i][1],'to B_evidence')
            B_evidence += info[i][1]
        else:
            print('adding',info[i][0],'to A_evidence')
            A_evidence += info[i][0]
            
    print('A_sum:',A_evidence,'B_sum:',B_evidence)       
    if B_evidence >= m:
        B_caught = True
    if A_evidence >= n:
        A_caught = True
    print(A_caught,B_caught)
    if A_caught and B_caught:
        print('hello!')
        minimum_list.append(4)
    if not A_caught and not B_caught:
        minimum_list.append(A_evidence)   

print(min(minimum_list))
'''