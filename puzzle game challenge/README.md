# 퍼즐 게임 챌린지 (프로그래머스)

## 풀이 기록 (삼세번)

| 회차 | 날짜 | 소요 시간 | 결과 |
|---|---|---|---|
| 1회차 | (기록 필요) | 약 2시간 | 정답 |
| 2회차 | | | |
| 3회차 | | | |

- 도움받은 부분: 문제의 인덱스 표현 해석(0부터 센 "i번째" vs 1부터 센 입출력 예), 끝나는 조건의 반례
- 이진 탐색 아이디어와 코드는 혼자 완성

## 문제 요약

n개의 퍼즐을 순서대로 푼다. 숙련도 level이 난이도 diff보다 낮으면 diff - level번 틀리고, 틀릴 때마다 현재 퍼즐 시간과 이전 퍼즐 시간을 다시 쓴다. 전체 제한 시간 안에 모두 풀 수 있는 **숙련도의 최솟값**을 구한다.

- n ≤ 300,000
- 난이도 ≤ 100,000, 시간 ≤ 10,000
- limit ≤ 10^15

### 문제 표현 주의

설명의 "`diffs[i]`는 i번째 퍼즐"은 **0부터** 센 번호, 입출력 예의 "1번째 퍼즐"은 **1부터** 센 번호다. 입출력 예의 1번째 퍼즐은 `diffs[0] = 1`, `times[0] = 2`.

---

## 풀이 흐름

### 1차: 숙련도를 1부터 하나씩 올리기 → 시간 초과 (+ 논리 오류)

숙련도 후보 최대 100,000 × 퍼즐 300,000 = 최악 300억 번. 시간 초과.

게다가 처음 **실패**한 순간 `level + 1`을 돌려줘서, 처음 **성공**하는 숙련도를 찾는 문제와 반대였다.

### 2차: 이진 탐색 ("업다운 게임")

이진 탐색을 쓸 수 있는 이유: **숙련도가 높아질수록 걸리는 시간은 절대 늘지 않는다.** 그래서 어떤 숙련도에서 풀리면 그보다 높은 숙련도에서도 항상 풀린다.

```
숙련도:  1  2  3  4  5
풀림?    ✗  ✗  ✓  ✓  ✓     ← 경계(처음 ✓)를 찾는 문제
```

- 풀리면 → 더 낮은 쪽을 탐색 (`max_level = level`)
- 안 풀리면 → 더 높은 쪽을 탐색 (`min_level = level`)

### 시간

탐색 약 17번(log₂ 100,000) × 퍼즐 300,000 ≈ 500만 번. 최대 입력에서 약 0.4초.

### 막힌 곳: 끝나는 순간 답이 1씩 틀림

`levels_visited`로 "같은 숙련도가 다시 나오면 멈추고 `level + 1`을 돌려준다"로 했더니, 작은 랜덤 입력 5,000개 중 3,221개에서 정답보다 **정확히 1 크게** 나왔다.

```
diffs = [1, 4], times = [4, 3], limit = 16   → 정답 3, 내 답 4

level 2 ✗ → level 3 ✓ → level 2 ✗ → 3이 다시 나와서 멈춤 → 3 + 1 = 4
```

멈추는 순간 `level`이 **풀리는 쪽**에 있는지 **안 풀리는 쪽**에 있는지에 따라 답이 달라진다.

### 해결: `max_level`이 무엇을 보장하는지

`max_level`은 탐색 내내 **"이 값에서는 풀린다"가 보장된 값**이다. 그래서 멈출 때 `level + 1` 대신 `max_level`을 돌려주면 된다.

- 처음 `max_level = max(diffs)`는 확인하지 않은 값이지만, 가장 높은 난이도 이상이면 하나도 틀리지 않아 시간이 가장 적게 들고, 문제가 "풀 수 있는 입력만 준다"고 보장하므로 항상 풀린다.

---

## 코드

```python
def solve(diffs, times, limit, level):
    elapsed_time = 0
    for i in range(len(diffs)):
        if level >= diffs[i]:
            elapsed_time += times[i]
        else:
            elapsed_time += (diffs[i] - level) * (times[i-1] + times[i]) + times[i]
        if elapsed_time > limit:
            return False
    return True

def solution(diffs, times, limit):  # 이진 탐색. 업다운 게임과 비슷함.
    from collections import deque
    max_level = max(diffs)          # 풀리는 게 보장된 값
    min_level = 1
    level = max(diffs) // 2 + max(diffs) % 2
    levels_visited = deque()

    while True:
        if solve(diffs, times, limit, level):   # 풀리면 낮추기
            max_level = level
            level -= (level - min_level) // 2 + (level - min_level) % 2
        else:                                    # 안 풀리면 높이기
            min_level = level
            level += (max_level - level) // 2 + (max_level - level) % 2
        levels_visited.append(level)
        if len(levels_visited) > 2:
            if level == levels_visited.popleft():
                return max_level
```

(제출 코드에서 `solve`의 `solved` 변수를 바로 `return`으로 바꾸는 정리만 함. 동작은 같음. 작은 랜덤 입력 25,000개로 브루트포스와 비교해 전부 일치.)

`diffs[0] = 1`이 보장되어 있어서, 첫 퍼즐에서 `times[i-1]`(= `times[-1]`)을 쓸 일이 없다.

---

## 회고

### 배운 것

- **이진 탐색을 쓸 수 있는 조건:** "숙련도가 높을수록 시간이 줄거나 같다"처럼 답이 한쪽 방향으로만 바뀔 때.
- **경계를 찾는 이진 탐색에서는 두 변수의 의미를 먼저 정한다.** `max_level` = 풀리는 게 확인된 값. 무엇을 돌려줄지가 여기서 정해진다.
- 1부터 올리는 브루트포스는 시간 초과와 별개로, "처음 실패"와 "처음 성공"을 헷갈려 답도 틀렸다.

### 2회차에서 해볼 것

`levels_visited` 없이, `min_level`과 `max_level`이 만나면 멈추는 일반적인 이진 탐색 모양으로 다시 짜기.

### 반복된 실수 패턴

- **하나 차이:** 끝날 때 `level + 1`
- **문제의 인덱스 표현:** "i번째"(0부터)와 "1번째"(1부터) 혼동. 비밀 코드 문제의 `ans[i]`와 같은 종류
