'''

당신은 순서대로 n개의 퍼즐을 제한 시간 내에 풀어야 하는 퍼즐 게임을 하고 있습니다. 
각 퍼즐은 난이도와 소요 시간이 정해져 있습니다. 
당신의 숙련도에 따라 퍼즐을 풀 때 틀리는 횟수가 바뀌게 됩니다. 

현재 퍼즐의 난이도를 diff, 
현재 퍼즐의 소요 시간을 time_cur, 
이전 퍼즐의 소요 시간을 time_prev,
당신의 숙련도를 level이라 하면, 

게임은 다음과 같이 진행됩니다.
diff ≤ level이면 퍼즐을 틀리지 않고 time_cur만큼의 시간을 사용하여 해결합니다.
diff > level이면, 퍼즐을 총 diff - level번 틀립니다. 

퍼즐을 틀릴 때마다, time_cur만큼의 시간을 사용하며, 추가로 time_prev만큼의 시간을 사용해 이전 퍼즐을 다시 풀고 와야 합니다.
이전 퍼즐을 다시 풀 때는 이전 퍼즐의 난이도에 상관없이 틀리지 않습니다. 
diff - level번 틀린 이후에 다시 퍼즐을 풀면 time_cur만큼의 시간을 사용하여 퍼즐을 해결합니다.

예를 들어 diff = 3, time_cur = 2, time_prev = 4인 경우, level에 따라 퍼즐을 푸는데 걸리는 시간은 다음과 같습니다.
level = 1이면, 퍼즐을 3 - 1 = 2번 틀립니다.
한 번 틀릴 때마다 2 + 4 = 6의 시간을 사용하고, 다시 퍼즐을 푸는 데 2의 시간을 사용하므로 총 6 × 2 + 2 = 14의 시간을 사용하게 됩니다.

level = 2이면, 퍼즐을 3 - 2 = 1번 틀리므로, 6 + 2 = 8의 시간을 사용하게 됩니다.

level ≥ 3이면 퍼즐을 틀리지 않으며, 2의 시간을 사용하게 됩니다.
퍼즐 게임에는 전체 제한 시간 limit가 정해져 있습니다.
제한 시간 내에 퍼즐을 모두 해결하기 위한 숙련도의 최솟값을 구하려고 합니다.
난이도, 소요 시간은 모두 양의 정수며, 숙련도도 양의 정수여야 합니다.

퍼즐의 난이도를 순서대로 담은 1차원 정수 배열 diffs, 
퍼즐의 소요 시간을 순서대로 담은 1차원 정수 배열 times, 
전체 제한 시간 limit이 매개변수로 주어집니다.
제한 시간 내에 퍼즐을 *모두 해결*하기 위한 *숙련도의 최솟값*을 정수로 return 하도록 solution 함수를 완성해 주세요.
'''
'''
제한사항
1 ≤ diffs의 길이 = times의 길이 = n ≤ 300,000
diffs[i]는 i번째 퍼즐의 난이도, times[i]는 i번째 퍼즐의 소요 시간입니다.
diffs[0] = 1
1 ≤ diffs[i] ≤ 100,000
1 ≤ times[i] ≤ 10,000
1 ≤ limit ≤ 10^15
제한 시간 내에 퍼즐을 모두 해결할 수 있는 경우만 입력으로 주어집니다.
'''

def solution_ver1(diffs, times, limit): # 타임 오버. 1부터 올라가면 너무 늦음.
    level = 0
    elapsed_time = 0
    while(True):
        level += 1
        solved = 0
        elapsed_time = 0
        stop = 0
        for i in range(0,len(diffs)):
            if level >= diffs[i]:
                elapsed_time += times[i]
            else:
                elapsed_time += (diffs[i] - level) * (times[i-1] + times[i]) + times[i]
            if elapsed_time > limit:
                answer = level + 1
                stop = 1
                break
            else:
                solved +=1
        if stop == 1:
            break        
    return answer

def solve(diffs, times, limit, level):
    solved = False
    elapsed_time = 0
    for i in range(0, len(diffs)):
        if level >= diffs[i]:
            elapsed_time += times[i]
        else:
            elapsed_time += (diffs[i] - level) * (times[i-1] + times[i]) + times[i]
        if elapsed_time > limit:
            solved = False
            break
        else:
            solved = True
        #print(elapsed_time)
    return solved

def solution(diffs, times, limit): #이진 탐색. 업 다운 게임과 비슷함.
    max_level = max(diffs)
    min_level = 1
    level = max(diffs) // 2 + max(diffs) % 2
    from collections import deque
    levels_visited = deque()
    
    while(True):
        solved=solve(diffs,times,limit,level)
        if(solved): #level l 에서 풀 수 있으면 level을 낮추기
            max_level = level
            level -= (level - min_level) // 2 + (level - min_level) %2
        else: #풀 수 없으면 level을 높이기
            min_level = level
            level += (max_level - level) // 2 + (max_level - level) %2
        levels_visited.append(level)
        if(len(levels_visited)>2):
            temp = levels_visited.popleft()
            if(level == temp):
                answer = max_level
                break
        
    return answer


diffs = [1, 328, 467, 209, 54]	
times = [2, 7, 1, 4, 3]
limit = 1723

print(solution(diffs,times,limit))