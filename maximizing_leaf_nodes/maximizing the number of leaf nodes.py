'''
문제 설명

루트 노드, 리프 노드, 분배 노드로 구성되는 트리가 있습니다. 
루트 노드는 자식 노드를 하나만 가지며, 루트 노드가 아닌 노드는 자식 노드를 2개, 3개 또는 0개를 가질 수 있습니다. 
자식 노드가 0개인 노드는 리프 노드입니다. 

당신은 제한된 조건 하에서 트리를 하나 구성하여 리프 노드를 가능한 한 많이 만들려고 합니다.

트리를 구성하는 규칙은 아래와 같습니다.

1.  루트 노드와 리프 노드를 제외한 나머지 노드를 분배 노드라고 하며, 분배 노드는 자식 노드를 2개 또는 3개를 갖습니다.
2.  분배 노드는 최대 dist_limit개 존재할 수 있습니다.
3.  트리에서 같은 깊이에 있는 분배 노드의 자식 노드 수는 모두 같아야 합니다. 노드의 깊이는 루트 노드부터 해당 노드까지의 최단 경로 길이와 같습니다.
4.  모든 리프 노드는 분배도라는 값을 갖습니다.
    분배도는 해당 리프 노드의 부모 노드에서 루트 노드까지의 최단 경로 상에 있는 모든 노드의 자식 노드 개수의 곱과 같습니다. 
    예를 들어 아래 그림과 같이 트리가 주어진 경우, 1번 리프 노드의 분배도는 3 × 1 = 3이며,
    2번 리프 노드의 분배도는 2 × 3 × 3 × 1 = 18입니다.
5.  모든 리프 노드의 분배도는 split_limit보다 작거나 같아야 합니다.

최대 몇 개의 분배 노드를 놓을 수 있는지 나타내는 정수 dist_limit, 분배도의 최댓값을 나타내는 정수 split_limit가 매개변수로 주어집니다. 
주어진 조건 하에서 만들 수 있는 트리의 리프 노드 수의 최댓값을 return 하도록 solution 함수를 완성해 주세요.

제한사항
0 ≤ dist_limit ≤ 109
1 ≤ split_limit ≤ 109

'''
'''
문제 정리

루트 노드 root_node : 자식이 하나인 노드
분배 노드 dist_node : 자식 노드가 2개 or 3개인 노드
리프 노드 leaf_node : 자식이 없는 노드

dist_limit: 분배 노드의 최대 개수
분배도: 해당 리프의 부모 노드에서 루트 노드까지의 최단 경로 상에 있는 모든 노드의 자식 노드 개수의 곱.    
분배도 <= split limit

depth = 트리의 깊이
depth 가 같은 dist_node 의 children의 수는 같음.

            0
        0       0
    0       0       0
0   0   0   0   0   0   0                    

split limit = 8
depth   D   L   C
1       1   0   2
2       2   0   2
3       4   0   2
4       0   8   0

1       1   0   3
2       3   0   2
3       0   6   0

1       1   0   2
2       2   0   3
3       0   6   0

1       0   1   0

1       1   0   2
2       0   2   0

1       1   0   3
2       0   3   0     

1       1   0   2
2       2   0   2
3       0   4   0



'''


def solution(dist_limit, split_limit):
    combination = []
    a, b = 0, 0
    while (2 ** a) <= split_limit:
        while (2 ** a) *  (3 ** b) <= split_limit:
            combination.append([a,b])
            b+=1
        a+=1
        b=0
    tree = []
    for a, b in combination:
        temp = []    
        for i in range(a):
            temp.append(2)
        for i in range(b):
            temp.append(3)
        tree.append(temp)    
    total_leaf = []
    for t in tree:
        if dist_limit == 0:
            total_leaf.append(1)
            break
        if len(t) == 0:
            total_leaf.append(1)
        elif len(t) == 1:
            total_leaf.append(t[0])
        else:
            left_dist_node = dist_limit
            nxt_nodes = 0
            D = 1
            L = 0
            for C in t:
                left_dist_node -= D
                nxt_nodes = D * C
                
                if left_dist_node >= nxt_nodes: #충분할 때
                    D = nxt_nodes
                    L += 0
                elif left_dist_node < nxt_nodes: #부족할 때
                    D = left_dist_node
                    L += nxt_nodes - left_dist_node
            L+=D
            total_leaf.append(L)
    answer = max(total_leaf)
    return answer