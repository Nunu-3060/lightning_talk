"""スライドで扱うセル・オートマトンのモデルをまとめたモジュール。

どのモデルも、格子の端は反対側の端とつながっている (周期境界条件) ものとし、
numpy の配列を 1 ステップずつ更新する関数として書いている。

* 基本セル・オートマトン (1 次元・2 状態・3 セル近傍)
* ライフゲーム
* ナーゲル・シュレッケンベルク・モデル (1 次元の交通流)
* BML 交通モデル (2 次元の交通流)
* 飛砂のモデル (Nishimori・Ouchi, 1993)

BML 交通モデルと飛砂のモデルは、sphinx_docs の
python_simulation_bml_traffic_model と python_simulation_sand の実装と同じ規則である。
"""
import numpy as np
import numpy.typing as npt

Cells = npt.NDArray[np.uint8]
Heights = npt.NDArray[np.float64]


# ---------------------------------------------------------------------------
# 基本セル・オートマトン
# ---------------------------------------------------------------------------
def rule_table(rule: int) -> Cells:
    """ルール番号を、近傍の番号 (0〜7) から次の状態を引く表に変換する。

    近傍 (左, 自分, 右) = (a, b, c) の番号は 4a + 2b + c で、
    その近傍に対する次の状態は、ルール番号を 2 進数で表したときの下から (4a + 2b + c) 桁目である。
    """
    return np.array([(rule >> i) & 1 for i in range(8)], dtype=np.uint8)


def single_seed(width: int) -> Cells:
    """中央の 1 セルだけが 1 の初期配置を作る。"""
    cells = np.zeros(width, dtype=np.uint8)
    cells[width // 2] = 1
    return cells


def random_cells(width: int, density: float, seed: int) -> Cells:
    """各セルが確率 density で 1 になる初期配置を作る。"""
    rng = np.random.default_rng(seed)
    return (rng.random(width) < density).astype(np.uint8)


def eca_evolve(rule: int, initial: Cells, steps: int) -> Cells:
    """時空図 (1 行が 1 時刻、形は (steps + 1, 幅)) を計算する。"""
    table = rule_table(rule)
    history = np.empty((steps + 1, initial.size), dtype=np.uint8)
    history[0] = initial
    cells = initial
    for t in range(1, steps + 1):
        left = np.roll(cells, 1)
        right = np.roll(cells, -1)
        cells = table[4 * left + 2 * cells + right]
        history[t] = cells
    return history


# ---------------------------------------------------------------------------
# ライフゲーム
# ---------------------------------------------------------------------------
GLIDER = [
    ".O.",
    "..O",
    "OOO",
]

GOSPER_GLIDER_GUN = [
    "........................O...........",
    "......................O.O...........",
    "............OO......OO............OO",
    "...........O...O....OO............OO",
    "OO........O.....O...OO..............",
    "OO........O...O.OO....O.O...........",
    "..........O.....O.......O...........",
    "...........O...O....................",
    "............OO......................",
]


def place(pattern: list[str], shape: tuple[int, int], top: int, left: int) -> Cells:
    """文字列で書いたパターン (O が生きたセル) を、空の盤面の指定位置に置く。"""
    grid = np.zeros(shape, dtype=np.uint8)
    for i, row in enumerate(pattern):
        for j, char in enumerate(row):
            if char == "O":
                grid[top + i, left + j] = 1
    return grid


def count_neighbors(grid: Cells) -> npt.NDArray[np.int64]:
    """各セルの周囲 8 セルのうち、生きているセルの数を数える。"""
    total = np.zeros(grid.shape, dtype=np.int64)
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if (di, dj) != (0, 0):
                total += np.roll(grid, shift=(di, dj), axis=(0, 1))
    return total


def life_step(grid: Cells) -> Cells:
    """ライフゲームの規則 (周りが 3 個なら誕生、2〜3 個なら生存) で 1 世代進める。"""
    n = count_neighbors(grid)
    born = (grid == 0) & (n == 3)
    survive = (grid == 1) & ((n == 2) | (n == 3))
    alive: Cells = (born | survive).astype(np.uint8)
    return alive


# ---------------------------------------------------------------------------
# ナーゲル・シュレッケンベルク・モデル
# ---------------------------------------------------------------------------
def nasch_evolve(length: int, density: float, v_max: int, p: float, steps: int, seed: int) -> Cells:
    """周回道路の時空図 (車が居るセルが 1、形は (steps + 1, length)) を計算する。

    各ステップで全車に次の 4 つの規則を順に適用する。

    1. 加速: v ← min(v + 1, v_max)
    2. 減速: v ← min(v, 前の車までの空きセル数)
    3. ランダムな減速: 確率 p で v ← max(v - 1, 0)
    4. 移動: 車を v セル前 (右) に進める
    """
    rng = np.random.default_rng(seed)
    n_cars = round(density * length)
    positions = np.sort(rng.choice(length, size=n_cars, replace=False)).astype(np.int64)
    velocities = np.zeros(n_cars, dtype=np.int64)
    history = np.zeros((steps + 1, length), dtype=np.uint8)
    history[0, positions] = 1
    for t in range(1, steps + 1):
        # 車は追い越さないので、配列の次の要素が前の車である
        gaps = (np.roll(positions, -1) - positions - 1) % length
        velocities = np.minimum(velocities + 1, v_max)
        velocities = np.minimum(velocities, gaps)
        slow_down = rng.random(n_cars) < p
        velocities = np.where(slow_down, np.maximum(velocities - 1, 0), velocities)
        positions = (positions + velocities) % length
        history[t, positions] = 1
    return history


# ---------------------------------------------------------------------------
# BML 交通モデル
# ---------------------------------------------------------------------------
EMPTY = 0
NORTH_CAR = 1  # 北 (上) へ進む車
EAST_CAR = 2  # 東 (右) へ進む車


def bml_initial(size: int, density: float, seed: int) -> Cells:
    """密度 density で、北向きと東向きの車を半分ずつ置いた盤面を作る。"""
    rng = np.random.default_rng(seed)
    p = rng.random((size, size))
    lattice = np.full((size, size), EMPTY, dtype=np.uint8)
    lattice[p < density] = NORTH_CAR
    lattice[p < density / 2] = EAST_CAR
    return lattice


def bml_step(lattice: Cells) -> tuple[Cells, int]:
    """北向きの車、東向きの車の順に、前が空いていれば 1 マス進める。

    戻り値は、更新後の盤面と、このステップで動いた車の台数である。
    """
    # 北向きの車: 自分の北 (1 行上) が空いていれば進む
    can_move = (lattice == NORTH_CAR) & (np.roll(lattice == EMPTY, 1, axis=0))
    moved_north = int(can_move.sum())
    after_north = lattice.copy()
    after_north[can_move] = EMPTY
    after_north[np.roll(can_move, -1, axis=0)] = NORTH_CAR
    # 東向きの車: 自分の東 (1 列右) が空いていれば進む
    can_move = (after_north == EAST_CAR) & (np.roll(after_north == EMPTY, -1, axis=1))
    moved_east = int(can_move.sum())
    after_east = after_north.copy()
    after_east[can_move] = EMPTY
    after_east[np.roll(can_move, 1, axis=1)] = EAST_CAR
    return after_east, moved_north + moved_east


# ---------------------------------------------------------------------------
# 飛砂のモデル
# ---------------------------------------------------------------------------
def sand_initial(size: int, seed: int) -> Heights:
    """各セルの砂の高さを 0 以上 1 未満の一様乱数で決める。"""
    rng = np.random.default_rng(seed)
    return rng.random((size, size))


def sand_step(height: Heights, l0: float = 2, b: float = 4, q: float = 0.1, d: float = 0.2) -> Heights:
    """飛砂のモデルで 1 ステップ進める。

    1. 輸送: 各セルは量 q の砂を、round(l0 + b × 高さ) セルだけ風下 (左) へ飛ばす。
       高い所ほど遠くへ飛ぶ。
    2. 拡散: 周囲 8 セルとの重み付き平均で、地形を少し均す。

    どちらの段階も砂の総量を変えない。
    """
    rows, cols = height.shape
    hop = np.round(l0 + b * height).astype(np.int64)
    destination = (np.arange(cols)[None, :] - hop) % cols
    change = np.full(height.shape, -q)
    row_index = np.repeat(np.arange(rows), cols)
    np.add.at(change, (row_index, destination.ravel()), q)
    h = height + change

    def shifted(di: int, dj: int) -> Heights:
        return np.roll(h, shift=(di, dj), axis=(0, 1))

    side = shifted(1, 0) + shifted(-1, 0) + shifted(0, 1) + shifted(0, -1)
    corner = shifted(1, 1) + shifted(1, -1) + shifted(-1, 1) + shifted(-1, -1)
    smoothed: Heights = h * (1 - d) + side * d / 6 + corner * d / 12
    return smoothed
