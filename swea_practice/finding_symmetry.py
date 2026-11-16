
import sys
sys.stdin = open("input.txt", "r")

def is_symmetric(d,grid,N):
    for i in range(N):
        for j in range(i, N):
            if (grid[i][(j+d)%N] != grid[j][(i+d)%N]):
                return False
    return True

T = int(input())
# 여러개의 테스트 케이스가 주어지므로, 각각을 처리합니다.
for test_case in range(1, T + 1):
    # ///////////////////////////////////////////////////////////////////////////////////
    N = int(input())
    first_grid = [list(input()) for _ in range(N)]
    symmetry_count = 0
    for d in range(0,N):
        if is_symmetric(d,first_grid,N):
            symmetry_count += N
    print(symmetry_count)
    # ///////////////////////////////////////////////////////////////////////////////////
