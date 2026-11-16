

import sys
from itertools import combinations

sys.stdin = open("input.txt", "r")

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    # ///////////////////////////////////////////////////////////////////////////////////
    ingredient_kinds, calorie_limit = list(map(int, input().split()))
    ingredients = [list(map(int,input().split())) for _ in range(ingredient_kinds)]
    best_burger_nominee = []
    for i in range(ingredient_kinds+1):
        for combo in combinations(ingredients, i):
            current_calorie = 0
            taste = 0
            if combo:
                for c in combo:
                    taste += c[0]      
                    current_calorie += c[1]
                if current_calorie <= calorie_limit:
                    best_burger_nominee.append(taste)     
    answer = max(best_burger_nominee)
    print(f'#{test_case} {answer}' )    
    # ///////////////////////////////////////////////////////////////////////////////////

