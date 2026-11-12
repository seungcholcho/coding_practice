# 충돌위험 찾기 (프로그래머스)

## 풀이 기록 (삼세번)

| 회차 | 날짜 | 소요 시간 | 결과 |
|---|---|---|---|
| 1회차 | (기록 필요) | 약 2시간 | 정답 |
| 2회차 | | | |
| 3회차 | | | |

- 도움받은 부분: `routes`의 의미 해석(좌표가 아니라 포인트 번호), 문법 확인(2차원 리스트, 리스트·튜플·딕셔너리 메서드)
- 최단 경로 로직과 전체 코드는 혼자 완성

## 문제 요약

n개의 포인트가 좌표로 주어지고, 로봇 x대가 각자 정해진 포인트 순서대로 이동한다. 로봇은 1초에 r 또는 c를 1만큼 움직이며, 최단 경로로 가되 **r을 먼저, c를 나중에** 바꾼다. 같은 시간에 같은 좌표에 로봇이 2대 이상 있으면 위험 상황이다. 모든 로봇이 끝날 때까지 위험 상황의 총 횟수를 구한다.

- 포인트 ≤ 100, 로봇 ≤ 100, 경로의 포인트 수 ≤ 100, 좌표 1 ~ 100

### 문제 표현 주의

`routes[i][j]`는 **좌표가 아니라 포인트 번호**다. 좌표는 `points[번호 - 1]` (번호는 1부터, 인덱스는 0부터).

---

## 풀이

### 1. 두 포인트 사이의 최단 경로

- 한 번에 r이나 c 중 하나만 1칸 → 걸리는 시간은 `|Δr| + |Δc|` (맨해튼 거리)
- **r을 먼저** 같아질 때까지, 그다음 c를 같아질 때까지 한 칸씩
- 한 칸에 +1인지 -1인지는 목표 좌표가 더 큰지 작은지로 정함

순서가 바뀌면 지나가는 칸이 달라진다.

```
(5, 6) → (2, 4)
r 먼저: (5,6) (4,6) (3,6) (2,6) (2,5) (2,4)
c 먼저: (5,6) (5,5) (5,4) (4,4) (3,4) (2,4)
```

### 2. 로봇마다 "몇 초에 어디 있는지" 목록 만들기

- `navigate`는 출발 칸을 **빼고** 도착 칸까지 돌려준다.
- 로봇 경로의 맨 처음에만 출발 칸을 한 번 넣는다. 그러면 구간이 이어질 때 중간 포인트가 두 번 들어가지 않는다.
- 이렇게 만든 목록에서 `path[t]`가 t초의 위치다.

### 3. 시간마다 같은 좌표에 몇 대인지 세기

- 그 시간에 아직 운송 중인 로봇만 위치를 모은다 (끝난 로봇은 물류 센터를 벗어남).
- 좌표를 튜플로 만들어 딕셔너리로 개수를 센다.
- 개수가 2 이상인 **좌표 하나당 1번**. 같은 칸에 3대가 모여도 그 좌표는 1번이다.

### 시간

로봇 100대 × 경로 길이 최대 약 2만 칸(포인트 100개 × 구간 최대 약 200칸). 최악 입력에서 약 0.5초.

---

## 코드

```python
def navigate(a, b, points):
    point_a, point_b = points[a-1], points[b-1]
    cur_r, cur_c = point_a[0], point_a[1]
    route = []
    while cur_r != point_b[0]:              # r 먼저
        if point_b[0] - cur_r > 0:
            cur_r += 1
        else:
            cur_r -= 1
        route.append([cur_r, cur_c])
    while cur_c != point_b[1]:              # 그다음 c
        if point_b[1] - cur_c > 0:
            cur_c += 1
        else:
            cur_c -= 1
        route.append([cur_r, cur_c])
    return route                            # 출발 칸 제외, 도착 칸 포함

def solution(points, routes):
    robot_path = []
    for route in routes:
        path = []
        for i in range(len(route) - 1):
            if not path:                    # 맨 처음 출발 칸만 한 번
                path.append([points[route[i]-1][0], points[route[i]-1][1]])
            path.extend(navigate(route[i], route[i+1], points))
        robot_path.append(path)

    max_time = max(len(r) for r in robot_path)
    threat = 0
    for time in range(max_time):
        count = {}
        for r in robot_path:
            if time < len(r):               # 아직 운송 중인 로봇만
                p = (r[time][0], r[time][1])
                count[p] = count.get(p, 0) + 1
        for k in count.values():
            if k >= 2:                      # 좌표 하나당 1번
                threat += 1
    return threat
```

(제출 코드에서 `while time < max(time_cost)`를 `for time in range(max_time)`으로, `if ... pass / else`를 `if time < len(r)`로 정리. `max`를 매 바퀴 다시 계산하지 않음. 동작은 같음.)

---

## 테스트

```python
print(solution([[3,2],[6,4],[4,7],[1,4]], [[4,2],[1,3],[2,4]]))           # 1
print(solution([[3,2],[6,4],[4,7],[1,4]], [[4,2],[1,3],[4,2],[4,3]]))     # 9
print(solution([[2,2],[2,3],[2,7],[6,6],[5,2]], [[2,3,4,5],[1,3,4,5]]))   # 0
```

---

## 회고

### 혼자 해낸 것

- 이동 거리 = r 차이 + c 차이 (맨해튼 거리)를 스스로 떠올림
- 구간을 이어 붙일 때 중간 포인트를 두 번 세지 않도록 `navigate`에서 출발 칸을 빼고, 첫 구간에서만 넣음
- 좌표를 튜플로 만들어 딕셔너리로 세기 (두 도둑의 set + 튜플을 응용)

### 다시 짚은 것

- `routes`가 좌표가 아니라 **포인트 번호** (번호와 인덱스 차이, 비밀 코드·퍼즐 게임과 같은 종류)
- 처음엔 "c를 먼저"로 생각함 → 문제 문장은 **r 먼저**. 순서가 바뀌면 지나가는 칸이 달라진다
- 튜플 자체는 중복을 없애지 않는다. 중복 제거는 set, 개수 세기는 dict

### 처음 써본 것 / 다시 확인한 것

- 딕셔너리로 개수 세기: `count[k] = count.get(k, 0) + 1`
- `collections.Counter`, `defaultdict(int)`도 같은 일을 함
- 튜플은 set·dict의 키가 될 수 있고, 리스트는 안 됨
