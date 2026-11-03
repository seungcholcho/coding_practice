# 지게차와 크레인 (프로그래머스)

## 풀이 기록 (삼세번)

| 회차 | 날짜 | 소요 시간 | 결과 |
|---|---|---|---|
| 1회차 | (기록 필요) | 약 4시간 | 정답 |
| 2회차 | | | |
| 3회차 | | | |

- 도움받은 부분: 문법 확인(문자열 수정, set에 좌표, 패딩, 큐), 그룹별 테스트 케이스와 "한 번 훑기" 반례
- 핵심 구멍(크레인이 만든 안쪽 빈칸)은 혼자 발견

## 문제 요약

n × m 창고에 알파벳 컨테이너가 있다. 요청이 순서대로 들어오는데,

- `"A"`처럼 한 글자: **지게차**. 그 순간 **창고 바깥과 이어진** A만 꺼낸다.
- `"AA"`처럼 두 글자: **크레인**. 위치와 상관없이 A를 **전부** 꺼낸다.

모든 요청 후 남은 컨테이너 수를 구한다.

- 2 ≤ n, m ≤ 50
- 요청 ≤ 100

---

## 풀이 흐름

### 1차 생각: "주변에 빈칸이 있으면 꺼낸다" → 틀림

크레인으로 **안쪽**에서 컨테이너를 빼면, 바깥과 이어지지 않은 빈칸이 생긴다. 그 옆 컨테이너는 주변에 빈칸이 있어도 지게차가 들어갈 수 없다. (문제 예시의 2행 3열 A)

빈칸은 두 종류다.

- **바깥과 이어진 빈칸:** 밖에서 빈칸만 밟고 걸어 들어올 수 있는 칸
- **안에 갇힌 빈칸:** 주변이 막혀서 밖에서 못 들어오는 칸

그리고 지게차로 바깥쪽을 꺼내면 갇혀 있던 빈칸이 **나중에 바깥과 이어질 수 있다.** → 요청마다 다시 계산해야 한다.

### 2차: 패딩 + 한 번 훑기 → 일부 틀림

- 창고 둘레에 빈칸(`'.'`) 테두리를 한 겹 둘러서, **바깥 전체를 하나의 이어진 빈칸 덩어리**로 만들었다.
- 위→아래, 왼→오른쪽으로 한 번 훑으며 "이웃이 바깥이면 나도 바깥"으로 표시했다.

제공된 테스트는 다 통과했지만 랜덤 비교에서 틀렸다. 바깥이 **아래나 오른쪽에서** 이어지는 통로는, 훑는 방향 때문에 위·왼쪽으로 퍼지지 못한다.

```
B B B B B
B C . C B
B C . C B      통로 입구는 맨 아래뿐
B C . C B      → 위에서부터 훑으면 통로 위쪽을 볼 때
B B . B B         아직 입구가 바깥으로 표시되기 전
```

배양체 감염 첫 시도의 "한 바퀴로는 연쇄가 덜 퍼진다"와 같은 문제.

### 3차: BFS로 바깥 찾기 → 정답

패딩 칸 `(0, 0)`에서 출발해 **빈칸만** 따라 BFS. 도착한 빈칸이 전부 "바깥과 이어진 빈칸"이다. 방향과 상관없이 끝까지 퍼진다. (패딩 칸들은 서로 이어져 있어서 출발점 하나면 충분)

요청마다:

1. 지게차면: 바깥과 이어진 빈칸 옆의 해당 컨테이너를 꺼낸다.
2. 크레인이면: 해당 컨테이너를 전부 꺼낸다.
3. 바깥을 BFS로 다시 계산한다.

### 시간

요청 100 × 격자 52 × 52 × (BFS + 훑기) ≈ 수십만 번. 충분하다.

---

## 코드

```python
from collections import deque

DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def outside_update(storage):
    H, W = len(storage), len(storage[0])
    visited = [[0] * W for _ in range(H)]
    que = deque([(0, 0)])
    visited[0][0] = 1                         # 넣을 때 표시
    while que:
        i, j = que.popleft()
        for dr, dc in DIRS:
            nr, nc = i + dr, j + dc
            if 0 <= nr < H and 0 <= nc < W:
                if storage[nr][nc] == '.' and visited[nr][nc] == 0:
                    visited[nr][nc] = 1       # 넣는 칸 = 표시하는 칸
                    que.append((nr, nc))
    return visited                            # 1 = 바깥과 이어진 빈칸

def forklift(storage, outside, letter):
    H, W = len(storage), len(storage[0])
    for i in range(H):
        for j in range(W):
            if storage[i][j] == letter:
                for dr, dc in DIRS:
                    nr, nc = i + dr, j + dc
                    if 0 <= nr < H and 0 <= nc < W and outside[nr][nc] == 1:
                        storage[i][j] = '.'
                        break

def crane(storage, letter):
    for row in storage:
        for j in range(len(row)):
            if row[j] == letter:
                row[j] = '.'

def solution(storage, requests):
    n, m = len(storage), len(storage[0])
    grid = [['.'] * (m + 2)]
    for row in storage:
        grid.append(['.'] + list(row) + ['.'])
    grid.append(['.'] * (m + 2))

    outside = outside_update(grid)
    for r in requests:
        if len(r) == 1:
            forklift(grid, outside, r)
        else:
            crane(grid, r[0])
        outside = outside_update(grid)

    return sum(1 for row in grid for x in row if x != '.')
```

(제출한 코드를 정리한 버전. `outside`는 요청 처리 중에는 바뀌지 않으므로, 같은 요청 안에서 꺼낸 칸 때문에 연쇄로 더 꺼내지 않는다.)

---

## 테스트 케이스

```python
tests = [
    # 그룹 1: 크레인만
    (["ABCCC", "AACCC", "BCCCB", "CBAAC"], ["AA", "CC"], 4),
    (["AACAD", "ADCBD", "CCCDA", "CACCD", "BCACC"], ["DD", "AA", "DD"], 13),
    # 그룹 2: 지게차만
    (["BBABBA", "BBBBBB", "AAAAAB", "BABAAB", "BBBBBB"], ["A", "A", "B", "A"], 4),
    (["BABBAA", "ACCBCB", "BABCBB", "CBBCCA", "BBBABC", "CCBBAB"], ["C", "B", "C", "A"], 8),
    # 그룹 3: 종류마다 한 번 (크레인이 만든 안쪽 빈칸)
    (["AAAAAAAA", "ABBBBBBA", "ABCCCCBA", "ABCCCCBA",
      "ABCCCCAA", "ABBBBBBA", "AAAAAAAA"], ["BB", "A", "C"], 3),
    (["DACDC", "ABDBD", "AAADE", "EAEBB", "AEAEC"], ["E", "BB", "A", "D"], 6),
    # 그룹 4: 제한 없음
    (["AZWQY", "CAABX", "BBDDA", "ACACA"], ["A", "BB", "A"], 11),
    (["AAAAA", "ABBBA", "ABABA", "ABBBA", "AAAAA"], ["A", "B", "A"], 0),
    # 한 번 훑기가 놓치는 통로
    (["BBBBB", "BCACB", "BCACB", "BCACB", "BBABB"], ["AA", "C"], 15),
    (["BBBBB", "BCCCB", "BAAAA", "BCCCB", "BBBBB"], ["AA", "C"], 15),
    (["BBBBBB", "BAAAAB", "BCCCAB", "BCCCAB", "BBBBAB"], ["AA", "C"], 19),
    (["BBABAB", "BBBABB", "BBBABA", "BBBAAA"], ["AA", "B"], 2),
]
```

---

## 회고

### 핵심

- **"외곽"은 공식이 아니라 연결이다.** 행·열 번호로 판단할 수 없고, "밖에서 빈칸만 밟고 걸어 들어올 수 있는가"를 확인해야 한다.
- **패딩**으로 바깥을 하나의 빈칸 덩어리로 만들면, 출발점 하나로 BFS가 된다.
- 바깥은 요청마다 바뀔 수 있다 → 요청마다 다시 계산.

### 막혔던 것

- **패딩 만들기:** 패딩 문자를 `"-1"`(두 글자)로 씀, 문자열과 리스트를 더함, 위아래 줄 길이를 행 수로 계산, `outside` 크기가 창고와 안 맞음. → `len(arr)`(행)과 `len(arr[0])`(열)을 찍어보며 맞춤.
- **한 번 훑기의 한계:** 테스트는 통과했지만 랜덤 비교에서 38개 틀림. 반례를 손으로 따라가서 원인을 찾음.
- **BFS 시간 초과:** 방문 표시를 꺼낼 때 하거나, 넣는 칸이 아닌 지금 칸에 표시함. → **넣는 칸과 표시하는 칸이 같아야** 한 칸이 큐에 한 번만 들어간다. 배양체 감염 때의 "방문 표시와 넣기는 한 쌍"이 두 번째로 나옴.
- 범위 확인 `nr <= len(storage)` → `<` (인덱스는 `len - 1`까지)

### 처음 써본 것 / 다시 확인한 것

- 문자열은 수정 불가 → `[list(row) for row in storage]`로 문자 리스트로 바꾸기
- set에 좌표는 튜플 `(r, c)`로, 순서가 필요하면 리스트 + set 또는 dict
- 리스트 중복 제거: `set`, 순서 유지는 `dict.fromkeys`
- 격자 이웃: `for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]`
