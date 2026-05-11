"""
=============================================================================
  algorithms.py — Lõi thuật toán tối ưu hóa danh mục đầu tư
  Chứa: BinaryCSOKnapsack (CSO) và BacktrackingKnapsack (Vét cạn)
  Import vào app.py để sử dụng.
=============================================================================
"""

import random
import time
import tracemalloc
import math


# ─────────────────────────────────────────────────────────────────────────────
# THUẬT TOÁN 1: CAT SWARM OPTIMIZATION — Binary 0/1 Knapsack
# ─────────────────────────────────────────────────────────────────────────────
class BinaryCSOKnapsack:
    """
    Cat Swarm Optimization (CSO) — Binary version cho bài toán 0/1 Knapsack.

    Tham số:
        n_cats   : Số lượng mèo trong quần thể (population size)
        max_iter : Số vòng lặp tối đa
        MR       : Mixture Ratio — tỉ lệ mèo ở Seeking Mode (0.0 → 1.0)
        SMP      : Seeking Memory Pool — số ứng viên sinh ra trong Seeking Mode

    Chiến lược:
        - Seeking Mode  : Mèo đứng yên, thám hiểm vùng lân cận bằng cách
                          flip bit ngẫu nhiên rồi chọn ứng viên tốt nhất.
        - Tracing Mode  : Mèo di chuyển về phía nghiệm tốt nhất toàn cục,
                          dùng hàm sigmoid để chuyển vận tốc → xác suất → bit nhị phân.
    """

    def __init__(self, n_cats: int, max_iter: int, MR: float, SMP: int):
        self.n_cats   = n_cats
        self.max_iter = max_iter
        self.MR       = MR
        self.SMP      = SMP

    # ── Hàm fitness: lợi nhuận hợp lệ hoặc -1 nếu vượt ngân sách ────────────
    def _fitness(self, sol: list, profits: list, costs: list, budget: int) -> int:
        total_cost   = sum(c * s for c, s in zip(costs, sol))
        total_profit = sum(p * s for p, s in zip(profits, sol))
        if total_cost > budget:
            return -1   # nghiệm không hợp lệ
        return total_profit

    # ── Vòng lặp chính ────────────────────────────────────────────────────────
    def solve(self, profits: list, costs: list, budget: int) -> dict:
        """
        Chạy CSO thật, đo thời gian và bộ nhớ.

        Returns:
            dict với các key: profit, cost, solution, time, memory(KB)
        """
        n = len(profits)

        tracemalloc.start()
        t0 = time.time()

        # ── Khởi tạo quần thể ngẫu nhiên ─────────────────────────────────────
        cats       = [[random.randint(0, 1) for _ in range(n)] for _ in range(self.n_cats)]
        velocities = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(self.n_cats)]

        best_solution = [0] * n
        best_profit   = 0
        best_cost     = 0

        # ── Vòng lặp chính: max_iter thế hệ ──────────────────────────────────
        for _ in range(self.max_iter):
            for i in range(self.n_cats):

                if random.random() < self.MR:
                    # ════════════════════════════════
                    # 🔎 SEEKING MODE
                    # Sinh SMP ứng viên bằng flip bit,
                    # chọn ứng viên có fitness cao nhất.
                    # ════════════════════════════════
                    candidates = []
                    for _ in range(self.SMP):
                        candidate = cats[i][:]
                        flip_idx  = random.randint(0, n - 1)
                        candidate[flip_idx] = 1 - candidate[flip_idx]
                        candidates.append(candidate)

                    # Chọn ứng viên tốt nhất trong pool
                    cats[i] = max(
                        candidates,
                        key=lambda sol: self._fitness(sol, profits, costs, budget),
                    )

                else:
                    # ════════════════════════════════
                    # 🚀 TRACING MODE
                    # Cập nhật vận tốc hướng về best,
                    # dùng sigmoid → xác suất → bit.
                    # ════════════════════════════════
                    for d in range(n):
                        velocities[i][d] += random.random() * (best_solution[d] - cats[i][d])
                        # Sigmoid chuyển vận tốc → xác suất
                        prob       = 1 / (1 + math.exp(-velocities[i][d]))
                        cats[i][d] = 1 if random.random() < prob else 0

                # ── Cập nhật global best sau mỗi con mèo ──────────────────────
                total_cost   = sum(c * s for c, s in zip(costs, cats[i]))
                total_profit = sum(p * s for p, s in zip(profits, cats[i]))

                if total_cost <= budget and total_profit > best_profit:
                    best_profit   = total_profit
                    best_cost     = total_cost
                    best_solution = cats[i][:]

        elapsed = time.time() - t0
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "profit":   best_profit,
            "cost":     best_cost,
            "solution": best_solution,
            "time":     elapsed,
            "memory":   peak / 1024,    # → KB
        }


# ─────────────────────────────────────────────────────────────────────────────
# THUẬT TOÁN 2: BACKTRACKING — Vét cạn đệ quy O(2^n)
# ─────────────────────────────────────────────────────────────────────────────
class BacktrackingKnapsack:
    """
    Thuật toán Backtracking (Vét cạn) thật sự — độ phức tạp O(2^n).

    Chiến lược đệ quy phân nhánh tại mỗi dự án idx:
        - Nhánh 0 : KHÔNG chọn dự án idx  (luôn thực hiện)
        - Nhánh 1 : CHỌN dự án idx        (chỉ khi còn đủ ngân sách)

    Đảm bảo tìm được nghiệm tối ưu chính xác (exact solution).
    """

    def __init__(self):
        self._best_profit   = 0
        self._best_solution = []

    # ── Hàm đệ quy vét cạn ───────────────────────────────────────────────────
    def _backtrack(
        self,
        idx:            int,
        profits:        list,
        costs:          list,
        budget:         int,
        current_profit: int,
        current_cost:   int,
        current_sol:    list,
    ):
        # Cập nhật nghiệm tốt nhất nếu lợi nhuận hiện tại cao hơn
        if current_profit > self._best_profit:
            self._best_profit   = current_profit
            self._best_solution = current_sol[:]

        # Điều kiện dừng: đã xét hết tất cả dự án
        if idx == len(profits):
            return

        # ── Nhánh 0: KHÔNG chọn dự án idx ────────────────────────────────────
        current_sol.append(0)
        self._backtrack(
            idx + 1, profits, costs, budget,
            current_profit, current_cost, current_sol,
        )
        current_sol.pop()

        # ── Nhánh 1: CHỌN dự án idx (chỉ khi không vượt ngân sách) ──────────
        if current_cost + costs[idx] <= budget:
            current_sol.append(1)
            self._backtrack(
                idx + 1, profits, costs, budget,
                current_profit + profits[idx],
                current_cost   + costs[idx],
                current_sol,
            )
            current_sol.pop()

    # ── Hàm gọi ngoài ─────────────────────────────────────────────────────────
    def solve(self, profits: list, costs: list, budget: int) -> dict:
        """
        Chạy Backtracking thật, đo thời gian và bộ nhớ.

        Returns:
            dict với các key: profit, cost, solution, time, memory(KB)
        """
        # Reset trạng thái trước mỗi lần chạy
        self._best_profit   = 0
        self._best_solution = []

        tracemalloc.start()
        t0 = time.time()

        self._backtrack(0, profits, costs, budget, 0, 0, [])

        elapsed = time.time() - t0
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        # Pad nghiệm nếu dừng sớm ở nhánh không hợp lệ nào
        sol = self._best_solution
        if len(sol) < len(profits):
            sol = sol + [0] * (len(profits) - len(sol))

        total_cost = sum(c * s for c, s in zip(costs, sol))

        return {
            "profit":   self._best_profit,
            "cost":     total_cost,
            "solution": sol,
            "time":     elapsed,
            "memory":   peak / 1024,    # → KB
        }
