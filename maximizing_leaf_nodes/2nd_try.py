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
분배도 제한의 의미:
분배도를 2와 3으로 인수분해. 2**i * 3**j * k(나머지) 에서 최대 i + j층 까지 쌓을 수 있음.

1. 2**i * 3**j <= split_limit인 (i,j) 구하기

combination = []
while(i)




트리를 표현 하는 방법
주어지는 것은 최대 분배 노드의 수, 분배도의 제한.


Depth dist_nodes leaf_nodes childs dist_nodes_left
0

dist_node = 3


'''
def printlist(arr):
    for r in arr:
        print(r)
    print("-------------")
def solution(dist_limit, split_limit):
    i,j = 0, 0
    combinatinon = []
    while(2**i<=split_limit):
        while(3**j<=split_limit):
            if(2**i*3**j<=split_limit): 
                combinatinon.append([i,j])
            j+=1
        j=0    
        i+=1
    
    leaf_list = []

    for c in range(0,len(combinatinon)):
        depth, dist_node_left = 0, dist_limit
        i, j = combinatinon[c][0], combinatinon[c][1] #child가 2인 층을 i개, 3인 층을 j개.
        tree = []
        total_leaf_nodes = 0
        if(dist_limit>0):
            tree.append([0,1,0,1])
        else:
            tree.append([0,0,0,1])
            
        if tree[-1][1] == 0 & tree[-1][2] == 0:
            leaf_list.append(1)
            break
        
        for i in range(i):
            depth+=1
            nodes = tree[-1][3] * tree[-1][1]
            if dist_node_left - nodes >= 0:
                dist_node = nodes
                dist_node_left -= dist_node
                leaf_node = nodes - dist_node
            elif dist_node_left - nodes < 0:
                dist_node = dist_node_left
                leaf_node = nodes - dist_node
                dist_node_left = 0
            child=2
            total_leaf_nodes +=leaf_node
            tree.append([depth, dist_node, leaf_node, child])
            
        for j in range(j):
            depth+=1
            nodes = tree[-1][3] * tree[-1][1]
            if dist_node_left - nodes >= 0:
                dist_node = nodes
                dist_node_left -= dist_node
                leaf_node = nodes - dist_node
            elif dist_node_left - nodes < 0:
                dist_node = dist_node_left
                leaf_node = nodes - dist_node
                dist_node_left = 0
            child=3
            total_leaf_nodes +=leaf_node
            tree.append([depth, dist_node, leaf_node, child])
        total_leaf_nodes += tree[-1][3] * tree[-1][1]
        leaf_list.append(total_leaf_nodes)
 
            
    answer = min(leaf_list)
    return answer


dist_limit = 2
split_limit = 6

solution(dist_limit,split_limit)
