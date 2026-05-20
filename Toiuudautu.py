"""
=============================================================================
  TỐI ƯU ĐẦU TƯ — Ứng dụng So sánh Thuật toán CSO vs Backtracking
  Môn: Phân tích Thuật toán
  Người 1: UI / Dữ liệu / Báo cáo so sánh hiệu năng
=============================================================================
"""


import streamlit as st
import pandas as pd
import random
import time
import tracemalloc
import io
import math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from matplotlib.patches import FancyBboxPatch
import networkx as nx


# ─────────────────────────────────────────────────────────────────────────────
# 0. CẤU HÌNH TRANG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tối Ưu Đầu Tư",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ─────────────────────────────────────────────────────────────────────────────
# 1. INJECT META TAG + CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    """
    <!-- Chặn Google Chrome tự động dịch trang -->
    <meta name="google" content="notranslate">
    <meta http-equiv="Content-Language" content="vi">


    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Be Vietnam Pro', sans-serif;
    }

    /* ── Tiêu đề app ── */
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.15rem;
        letter-spacing: -0.01em;
    }
    .main-subtitle {
        font-size: 0.97rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }

    /* ── Căn giữa tiêu đề bảng ── */
    .section-title {
        text-align: center;
        font-size: 1.05rem;
        font-weight: 600;
        color: #1e293b;
        margin: 0.6rem 0 0.5rem 0;
        padding: 0.4rem 0;
        border-bottom: 2px solid #e2e8f0;
    }

    /* ── Metric cards — nổi khối 3D nhẹ ── */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #f0f7ff 0%, #e8f2ff 100%);
        border: 1px solid #c7d7f7;
        border-left: 5px solid #3b82f6;
        border-radius: 14px;
        padding: 0.8rem 1.1rem;
        box-shadow:
            0 4px 12px rgba(59,130,246,0.10),
            0 1px 3px rgba(59,130,246,0.06),
            inset 0 1px 0 rgba(255,255,255,0.8);
        transition: box-shadow 0.2s ease;
    }
    div[data-testid="metric-container"]:hover {
        box-shadow:
            0 8px 24px rgba(59,130,246,0.16),
            0 2px 6px rgba(59,130,246,0.10),
            inset 0 1px 0 rgba(255,255,255,0.9);
    }
    div[data-testid="metric-container"] label {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    /* ── Fix metric value ── */
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] > div {
        font-size: 1rem !important;
        font-weight: 700 !important;
        color: #1e40af !important;
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        word-break: break-word !important;
        line-height: 1.3 !important;
    }

    /* Override màu riêng cho từng loại */
    .metric-cso [data-testid="stMetricValue"],
    .metric-cso [data-testid="stMetricValue"] > div {
        color: #065f46 !important;
    }
    .metric-bt [data-testid="stMetricValue"],
    .metric-bt [data-testid="stMetricValue"] > div {
        color: #92400e !important;
    }

    /* ── Metric CSO — pastel teal ── */
    .metric-cso div[data-testid="metric-container"] {
        border-left-color: #10b981;
        background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
        border-color: #a7f3d0;
        box-shadow:
            0 4px 14px rgba(16,185,129,0.12),
            0 1px 3px rgba(16,185,129,0.07),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    .metric-cso div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #065f46 !important;
    }

    /* ── Metric BT — pastel amber ── */
    .metric-bt div[data-testid="metric-container"] {
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-color: #fde68a;
        box-shadow:
            0 4px 14px rgba(245,158,11,0.12),
            0 1px 3px rgba(245,158,11,0.07),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    .metric-bt div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #92400e !important;
    }

    /* ── Warning box — pastel orange ── */
    .warn-box {
        background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
        border: 1px solid #fed7aa;
        border-left: 5px solid #f97316;
        border-radius: 12px;
        padding: 0.75rem 1.1rem;
        font-size: 0.88rem;
        color: #9a3412;
        margin: 0.6rem 0;
        box-shadow:
            0 3px 10px rgba(249,115,22,0.10),
            inset 0 1px 0 rgba(255,255,255,0.7);
    }

    /* ── Info box — pastel blue ── */
    .info-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border: 1px solid #bfdbfe;
        border-left: 5px solid #3b82f6;
        border-radius: 12px;
        padding: 0.75rem 1.1rem;
        font-size: 0.88rem;
        color: #1e40af;
        margin: 0.6rem 0;
        box-shadow:
            0 3px 10px rgba(59,130,246,0.10),
            inset 0 1px 0 rgba(255,255,255,0.7);
    }

    /* ── Chart section wrapper ── */
    .chart-section {
        background: linear-gradient(135deg, #f8faff 0%, #f0f4ff 100%);
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 1.5rem 1.5rem 1rem 1.5rem;
        margin: 1rem 0;
        box-shadow:
            0 6px 20px rgba(15,23,42,0.06),
            0 2px 6px rgba(15,23,42,0.04),
            inset 0 1px 0 rgba(255,255,255,0.9);
    }
    .chart-caption {
        background: linear-gradient(135deg, #f1f5f9 0%, #e8edf5 100%);
        border-left: 4px solid #6366f1;
        border-radius: 8px;
        padding: 0.55rem 0.9rem;
        font-size: 0.85rem;
        color: #475569;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(99,102,241,0.08);
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stSidebar"] .stSlider > label,
    [data-testid="stSidebar"] .stNumberInput > label,
    [data-testid="stSidebar"] .stSelectbox > label {
        color: #94a3b8 !important;
        font-size: 0.82rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ── Divider ── */
    hr { border-color: #e2e8f0; }

    /* ── Stale result banner ── */
    .stale-banner {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        text-align: center;
        color: #991b1b;
        font-weight: 600;
        font-size: 0.95rem;
        box-shadow: 0 4px 14px rgba(239,68,68,0.12);
    }

    /* ── Tab biểu đồ ── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 6px;
        background: #f1f5f9;
        border-radius: 12px;
        padding: 4px 6px;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        border-radius: 9px !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        padding: 0.4rem 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# 2. KHỞI TẠO SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "df_projects": pd.DataFrame(columns=["Chọn", "Tên dự án", "Lợi nhuận (đồng)", "Chi phí (đồng)"]),
        "cso_result":  None,   # dict: profit, cost, solution, time, memory
        "bt_result":   None,
        "result_stale": False, # True nếu dữ liệu thay đổi mà chưa chạy lại
        "last_data_hash": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()


# ─────────────────────────────────────────────────────────────────────────────
# 3. HÀM TIỆN ÍCH
# ─────────────────────────────────────────────────────────────────────────────
def fmt_money(value: float) -> str:
    """Format số tiền dạng 1.000.000.000 đồng"""
    return f"{int(value):,} đồng".replace(",", ".")


def fmt_mem(kb: float) -> str:
    if kb < 1024:
        return f"{kb:.1f} KB"
    return f"{kb/1024:.2f} MB"


# ─────────────────────────────────────────────────────────────────────────────
# BIỂU ĐỒ 1: CSO Scatter Plot — phân bố không gian nghiệm qua PCA
# ─────────────────────────────────────────────────────────────────────────────
def render_cso_scatter(snapshots: dict, n_items: int):
    """Vẽ Scatter Plot 2D (PCA) cho 3 mốc thời gian của CSO."""
    if not snapshots or n_items < 2:
        st.info("Cần ít nhất 2 dự án để vẽ biểu đồ phân bố không gian nghiệm.")
        return

    labels = list(snapshots.keys())
    n_cols = len(labels)

    # ── Kích thước lớn hơn để dễ nhìn ────────────────────────────────────
    fig, axes = plt.subplots(1, n_cols, figsize=(7 * n_cols, 6))
    fig.patch.set_facecolor("#0f172a")
    if n_cols == 1:
        axes = [axes]

    for ax, label in zip(axes, labels):
        snap = snapshots[label]
        X = np.array(snap["positions"], dtype=float)  # shape (n_cats, n_items)
        fits = np.array(snap["fitness"], dtype=float)

        # ── PCA thủ công (không cần sklearn) ──────────────────────────────
        if X.shape[1] >= 2:
            X_centered = X - X.mean(axis=0)
            cov = np.cov(X_centered.T)
            if cov.ndim == 2:
                try:
                    vals, vecs = np.linalg.eigh(cov)
                    idx_sort = np.argsort(vals)[::-1]
                    pc = vecs[:, idx_sort[:2]]
                    X_2d = X_centered @ pc
                except Exception:
                    X_2d = X_centered[:, :2]
            else:
                X_2d = X_centered[:, :2] if X_centered.shape[1] >= 2 else np.zeros((len(X), 2))
        else:
            X_2d = np.zeros((len(X), 2))

        # ── Màu theo fitness ───────────────────────────────────────────────
        max_f = fits.max() if fits.max() > 0 else 1
        norm_fits = fits / max_f

        ax.set_facecolor("#1e293b")

        # Grid mờ để dễ gióng tọa độ
        ax.grid(True, color="#334155", linewidth=0.6, linestyle="--", alpha=0.5, zorder=0)
        ax.set_axisbelow(True)

        sc = ax.scatter(
            X_2d[:, 0], X_2d[:, 1],
            c=norm_fits,
            cmap="YlOrRd",
            s=130,           # phóng to điểm dữ liệu
            alpha=0.88,
            edgecolors="#ffffff55",
            linewidths=0.8,
            zorder=2,
        )

        # Đánh dấu con mèo tốt nhất — ngôi sao lớn hơn
        best_idx = int(np.argmax(fits))
        ax.scatter(
            X_2d[best_idx, 0], X_2d[best_idx, 1],
            marker="*", s=340, color="#fbbf24",
            edgecolors="#f59e0b", linewidths=1.0,
            zorder=5, label="Best cat ⭐"
        )

        ax.set_title(label, color="white", fontsize=12, fontweight="bold", pad=10)
        ax.tick_params(colors="#94a3b8", labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor("#334155")
        ax.set_xlabel("PC 1", color="#94a3b8", fontsize=11)
        ax.set_ylabel("PC 2", color="#94a3b8", fontsize=11)
        ax.legend(fontsize=9, facecolor="#1e293b", labelcolor="white", framealpha=0.8,
                  edgecolor="#475569")

    # Colorbar chung - Gắn vào đồ thị cuối cùng và đẩy ra lề phải
    last_ax = axes[-1] if isinstance(axes, (list, tuple, np.ndarray)) else axes
    cbar = fig.colorbar(sc, ax=last_ax, shrink=0.8, pad=0.08, aspect=25)
    cbar.set_label("Fitness (chuẩn hóa)", color="#94a3b8", fontsize=10)
    cbar.ax.yaxis.set_tick_params(color="#94a3b8", labelsize=9)
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color="#94a3b8")

    fig.suptitle(
        "Phân bố không gian nghiệm CSO — PCA 2D",
        color="white", fontsize=14, fontweight="bold", y=1.02
    )
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# BIỂU ĐỒ 2: Backtracking — Cây quyết định (nhỏ) hoặc Depth Density (lớn)
# ─────────────────────────────────────────────────────────────────────────────
def render_bt_tree(bt_res: dict):
    """
    Nếu n_items <= 15: vẽ cây trạng thái (networkx).
    Nếu n_items > 15:  vẽ Depth Density Chart.
    """
    tree_nodes  = bt_res.get("tree_nodes", [])
    depth_hits  = bt_res.get("depth_hits", {})
    total_nodes = bt_res.get("total_nodes", 0)
    n_items     = bt_res.get("n_items", 0)

    if not tree_nodes and not depth_hits:
        st.info("Không có dữ liệu cây để hiển thị.")
        return

    COLOR_MAP = {
        "explore":       "#3b82f6",   # xanh dương — đang duyệt
        "valid":         "#10b981",   # xanh lá — lá hợp lệ
        "best":          "#fbbf24",   # vàng — nghiệm tốt nhất
        "pruned_bound":  "#ef4444",   # đỏ — cắt do bound
        "pruned_weight": "#f97316",   # cam — cắt do vượt ngân sách
    }
    LEGEND_LABELS = {
        "explore":       "Đang duyệt",
        "valid":         "Lá hợp lệ",
        "best":          "Nghiệm tốt nhất",
        "pruned_bound":  "Cắt (Bound)",
        "pruned_weight": "Cắt (Vượt ngân sách)",
    }

    # ── Nếu nhỏ: vẽ cây ────────────────────────────────────────────────────
    if n_items <= 15 and tree_nodes:
        G = nx.DiGraph()
        node_colors = []
        node_labels = {}

        for nd in tree_nodes:
            nid  = nd["id"]
            stat = nd["status"]
            G.add_node(nid)
            node_colors.append(COLOR_MAP.get(stat, "#64748b"))
            # Nhãn ngắn: idx dự án đang xét
            item_label = f"P{nd['idx']}" if nd["idx"] < n_items else "✓"
            node_labels[nid] = item_label

        for nd in tree_nodes:
            if nd["parent"] >= 0 and nd["parent"] in G.nodes:
                G.add_edge(nd["parent"], nd["id"])

        # Layout theo tầng (hierarchical)
        depth_groups = {}
        for nd in tree_nodes:
            d = nd["depth"]
            depth_groups.setdefault(d, []).append(nd["id"])

        pos = {}
        for d, nodes_at_d in depth_groups.items():
            width = len(nodes_at_d)
            for i, nid in enumerate(nodes_at_d):
                pos[nid] = ((i - width / 2) * 1.6, -d * 1.4)

        fig, ax = plt.subplots(figsize=(max(14, len(tree_nodes) * 0.4), 10))
        fig.patch.set_facecolor("#0f172a")
        ax.set_facecolor("#0f172a")

        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#475569",
                               arrows=True, arrowsize=12, width=1.1, alpha=0.75)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors,
                               node_size=600, alpha=0.96)
        nx.draw_networkx_labels(G, pos, labels=node_labels, ax=ax,
                                font_size=9, font_color="white", font_weight="bold")

        # Legend
        from matplotlib.lines import Line2D
        legend_handles = [
            Line2D([0], [0], marker="o", color="w",
                   markerfacecolor=COLOR_MAP[k], markersize=11, label=LEGEND_LABELS[k])
            for k in COLOR_MAP
        ]
        ax.legend(handles=legend_handles, loc="upper right",
                  facecolor="#1e293b", labelcolor="white",
                  fontsize=10, framealpha=0.9, edgecolor="#475569")

        ax.set_title(
            f"Cây Không Gian Trạng Thái Backtracking  "
            f"(hiển thị {len(tree_nodes)}/{total_nodes} nút)",
            color="white", fontsize=13, fontweight="bold", pad=12
        )
        ax.axis("off")
        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)

    else:
        # ── Nếu lớn: Depth Density Chart ───────────────────────────────────
        if not depth_hits:
            st.info("Không có dữ liệu độ sâu.")
            return

        depths  = sorted(depth_hits.keys())
        counts  = [depth_hits[d] for d in depths]
        max_c   = max(counts) if counts else 1
        norm_c  = [c / max_c for c in counts]

        fig, ax = plt.subplots(figsize=(14, 7))
        fig.patch.set_facecolor("#0f172a")
        ax.set_facecolor("#1e293b")

        bars = ax.barh(depths, counts, color=[
            plt.cm.RdYlGn(1 - nc) for nc in norm_c
        ], edgecolor="#0f172a", linewidth=0.8, height=0.72)

        # Ghi số lên mỗi bar — font lớn hơn
        for bar, cnt in zip(bars, counts):
            ax.text(bar.get_width() + max_c * 0.008, bar.get_y() + bar.get_height() / 2,
                    f"{cnt:,}", va="center", ha="left", fontsize=10, color="#cbd5e1",
                    fontweight="600")

        ax.set_xlabel("Số nút được duyệt", color="#94a3b8", fontsize=12)
        ax.set_ylabel("Độ sâu (Depth)", color="#94a3b8", fontsize=12)
        ax.set_title(
            f"Mật Độ Độ Sâu Cây Backtracking  "
            f"(Tổng {total_nodes:,} nút · n={n_items} dự án)",
            color="white", fontsize=13, fontweight="bold", pad=12
        )
        ax.tick_params(colors="#94a3b8", labelsize=10)
        ax.set_yticks(depths)
        for spine in ax.spines.values():
            spine.set_edgecolor("#334155")
        ax.invert_yaxis()

        # Chú thích: Tầng cắt nhiều nhất
        max_depth = depths[counts.index(max(counts))]
        ax.axhline(max_depth, color="#fbbf24", linewidth=1.5, linestyle="--", alpha=0.85)
        ax.text(max_c * 0.5, max_depth - 0.4,
                f" Tầng cắt nhiều nhất: {max_depth}",
                color="#fbbf24", fontsize=10, fontweight="600")

        plt.tight_layout()
        st.pyplot(fig, use_container_width=True)
        plt.close(fig)


def df_hash(df: pd.DataFrame) -> str:
    """Hash nhẹ để phát hiện thay đổi dữ liệu"""
    try:
        return str(pd.util.hash_pandas_object(df).sum())
    except Exception:
        return str(len(df))


def mark_stale():
    """Đánh dấu kết quả cũ đã lỗi thời"""
    current_hash = df_hash(st.session_state["df_projects"])
    if (
        st.session_state["last_data_hash"] is not None
        and current_hash != st.session_state["last_data_hash"]
        and (st.session_state["cso_result"] or st.session_state["bt_result"])
    ):
        st.session_state["result_stale"] = True


# ─────────────────────────────────────────────────────────────────────────────
# 4. LÕI THUẬT TOÁN
# ─────────────────────────────────────────────────────────────────────────────


class BinaryCSOKnapsack:
    """
    Cat Swarm Optimization (CSO) — Binary version cho bài toán 0/1 Knapsack.
    """


    def __init__(self, n_cats: int, max_iter: int, MR: float, SMP: int):
        self.n_cats = n_cats
        self.max_iter = max_iter
        self.MR = MR      # Mixture Ratio
        self.SMP = SMP    # Seeking Memory Pool


    def _fitness(self, sol, profits, costs, budget):
        total_cost = sum(c * s for c, s in zip(costs, sol))
        total_profit = sum(p * s for p, s in zip(profits, sol))


        if total_cost > budget:
            return -1  # loại nghiệm không hợp lệ
        return total_profit


    def solve(self, profits: list, costs: list, budget: int) -> dict:
        n = len(profits)

        tracemalloc.start()
        t0 = time.time()

        # 🔹 Khởi tạo quần thể
        cats = [[random.randint(0, 1) for _ in range(n)] for _ in range(self.n_cats)]
        velocities = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(self.n_cats)]

        best_solution = [0] * n
        best_profit = 0
        best_cost = 0

        # ── Snapshots cho Scatter Plot ──────────────────────────────────────
        snapshots = {}   # {label: {"positions": list[list], "fitness": list[float]}}
        snap_iters = {
            0: "Vòng 1 (Khởi đầu)",
            self.max_iter // 2: f"Vòng {self.max_iter // 2} (Giữa)",
            self.max_iter - 1: f"Vòng {self.max_iter} (Cuối)",
        }

        def _take_snapshot(label):
            fits = [max(0, self._fitness(c, profits, costs, budget)) for c in cats]
            snapshots[label] = {
                "positions": [c[:] for c in cats],
                "fitness": fits,
            }

        # 🔁 Vòng lặp chính
        for it in range(self.max_iter):
            if it in snap_iters:
                _take_snapshot(snap_iters[it])

            for i in range(self.n_cats):
                if random.random() < self.MR:
                    # =======================
                    # 🔎 SEEKING MODE
                    # =======================
                    candidates = []
                    for _ in range(self.SMP):
                        candidate = cats[i][:]
                        idx = random.randint(0, n - 1)
                        candidate[idx] = 1 - candidate[idx]
                        candidates.append(candidate)

                    best_local = max(
                        candidates,
                        key=lambda sol: self._fitness(sol, profits, costs, budget)
                    )
                    cats[i] = best_local
                else:
                    # =======================
                    # 🚀 TRACING MODE
                    # =======================
                    for d in range(n):
                        velocities[i][d] += random.random() * (best_solution[d] - cats[i][d])
                        prob = 1 / (1 + math.exp(-velocities[i][d]))
                        cats[i][d] = 1 if random.random() < prob else 0

                # =======================
                # 📊 Cập nhật global best
                # =======================
                total_cost = sum(c * s for c, s in zip(costs, cats[i]))
                total_profit = sum(p * s for p, s in zip(profits, cats[i]))

                if total_cost <= budget and total_profit > best_profit:
                    best_profit = total_profit
                    best_cost = total_cost
                    best_solution = cats[i][:]

        elapsed = time.time() - t0
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            "profit": best_profit,
            "cost": best_cost,
            "solution": best_solution,
            "time": elapsed,
            "memory": peak / 1024,  # KB
            "snapshots": snapshots,
        }






class BacktrackingKnapsack:
    """
    Thuật toán Backtracking thật sự — O(2^n).
    Đệ quy phân nhánh: chọn hoặc không chọn từng dự án.
    """
    # Giới hạn node lưu cho cây (tránh bùng nổ bộ nhớ khi n lớn)
    MAX_TREE_NODES = 500

    def __init__(self):
        self._best_profit   = 0
        self._best_solution = []
        # Tree tracking
        self._node_id    = 0
        self._tree_nodes = []   # list of dicts
        self._depth_hits = {}   # depth → count (cho depth density chart)

    def _upper_bound(self, idx, profits, costs, budget, current_profit, remaining_budget):
        """Fractional knapsack bound (greedy) để cắt nhánh."""
        bound = current_profit
        cap   = remaining_budget
        n     = len(profits)
        # sắp xếp theo tỉ lệ profit/cost giảm dần (chỉ từ idx)
        items = sorted(
            [(profits[j] / costs[j] if costs[j] > 0 else 0, profits[j], costs[j])
             for j in range(idx, n)],
            reverse=True
        )
        for ratio, p, c in items:
            if cap <= 0:
                break
            if c <= cap:
                bound += p
                cap   -= c
            else:
                bound += ratio * cap
                cap    = 0
        return bound

    def _backtrack(self, idx: int, profits: list, costs: list,
                   budget: int, current_profit: int, current_cost: int,
                   current_sol: list, parent_id: int, depth: int):
        n = len(profits)
        remaining = budget - current_cost

        # Ghi nhận depth hit
        self._depth_hits[depth] = self._depth_hits.get(depth, 0) + 1

        # ── Lưu node vào tree (nếu còn dưới giới hạn) ──────────────────────
        nid = self._node_id
        self._node_id += 1
        track = len(self._tree_nodes) < self.MAX_TREE_NODES

        if track:
            self._tree_nodes.append({
                "id":     nid,
                "parent": parent_id,
                "depth":  depth,
                "profit": current_profit,
                "cost":   current_cost,
                "idx":    idx,
                "status": "explore",   # sẽ được ghi đè khi rõ hơn
            })

        # Cập nhật nghiệm tốt nhất
        if current_profit > self._best_profit:
            self._best_profit   = current_profit
            self._best_solution = current_sol[:]
            if track:
                self._tree_nodes[-1]["status"] = "best"

        if idx == n:
            if track:
                self._tree_nodes[-1]["status"] = "valid"
            return

        # ── Cắt nhánh: upper bound ──────────────────────────────────────────
        ub = self._upper_bound(idx, profits, costs, budget,
                               current_profit, remaining)
        if ub <= self._best_profit:
            if track:
                self._tree_nodes[-1]["status"] = "pruned_bound"
            return

        # Nhánh 1: KHÔNG chọn dự án idx
        current_sol.append(0)
        self._backtrack(idx + 1, profits, costs, budget,
                        current_profit, current_cost, current_sol, nid, depth + 1)
        current_sol.pop()

        # Nhánh 2: CHỌN dự án idx (nếu còn đủ ngân sách)
        if current_cost + costs[idx] <= budget:
            current_sol.append(1)
            self._backtrack(idx + 1, profits, costs, budget,
                            current_profit + profits[idx],
                            current_cost  + costs[idx],
                            current_sol, nid, depth + 1)
            current_sol.pop()
        else:
            # Ghi nhận nút bị cắt vì vượt ngân sách
            pruned_id = self._node_id
            self._node_id += 1
            self._depth_hits[depth + 1] = self._depth_hits.get(depth + 1, 0) + 1
            if len(self._tree_nodes) < self.MAX_TREE_NODES:
                self._tree_nodes.append({
                    "id":     pruned_id,
                    "parent": nid,
                    "depth":  depth + 1,
                    "profit": current_profit + profits[idx],
                    "cost":   current_cost  + costs[idx],
                    "idx":    idx,
                    "status": "pruned_weight",
                })

    def solve(self, profits: list, costs: list, budget: int) -> dict:
        """Chạy backtracking thật, đo time và memory."""
        self._best_profit   = 0
        self._best_solution = []
        self._node_id       = 0
        self._tree_nodes    = []
        self._depth_hits    = {}

        tracemalloc.start()
        t0 = time.time()
        self._backtrack(0, profits, costs, budget, 0, 0, [], -1, 0)
        elapsed = time.time() - t0
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        sol = self._best_solution
        if len(sol) < len(profits):
            sol = sol + [0] * (len(profits) - len(sol))

        total_cost = sum(c * s for c, s in zip(costs, sol))
        return {
            "profit":      self._best_profit,
            "cost":        total_cost,
            "solution":    sol,
            "time":        elapsed,
            "memory":      peak / 1024,  # KB
            "tree_nodes":  self._tree_nodes,
            "depth_hits":  self._depth_hits,
            "total_nodes": self._node_id,
            "n_items":     len(profits),
        }


# ─────────────────────────────────────────────────────────────────────────────
# 5. SIDEBAR — CẤU HÌNH THAM SỐ
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Cấu hình tham số")
    st.markdown("---")


    # ── CSO ──────────────────────────────────────────────────────────────────
    st.markdown("### CSO Parameters")
    n_cats   = st.slider("Số lượng mèo (n_cats)",   10,  100, 30, step=5)
    max_iter = st.slider("Số vòng lặp (max_iter)",  10,  500, 100, step=10)
    MR       = st.slider("Tỉ lệ truy tìm (MR)",     0.0, 1.0, 0.3, step=0.05)
    SMP      = st.slider("Bộ nhớ tìm kiếm (SMP)",   1,   10,  5)


    st.markdown("---")


    # ── Backtracking giới hạn (demo bùng nổ tổ hợp) ──────────────────────
    st.markdown("### Backtracking")
    bt_limit = st.slider(
        "Giới hạn Backtracking (n dự án)",
        min_value=10, max_value=30, value=20, step=1,
    )
    if bt_limit > 23:
        st.markdown(
            """
            <div style='background:#7f1d1d;border-radius:8px;padding:0.6rem 0.8rem;
                        font-size:0.82rem;color:#fecaca;margin-top:0.3rem;'>
             <b>Cảnh báo!</b> Với n &gt; 23, độ phức tạp O(2ⁿ) có thể khiến
            <b>hệ thống bị treo</b>. Hãy cân nhắc kỹ trước khi chạy.
            </div>
            """,
            unsafe_allow_html=True,
        )


    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem;color:#64748b;text-align:center;'>"
        "CSO luôn chạy · Backtracking chỉ chạy khi n ≤ giới hạn"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# 6. TIÊU ĐỀ APP
# ─────────────────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='main-title'>Tối Ưu Hóa Danh Mục Đầu Tư</div>"
    "<div class='main-subtitle'>So sánh hiệu năng: "
    "<b>Cat Swarm Optimization (CSO)</b> vs <b>Backtracking</b> · "
    "Bài toán cái túi 0/1 Knapsack</div>",
    unsafe_allow_html=True,
)
st.divider()


# ─────────────────────────────────────────────────────────────────────────────
# 7. BA CỘT CHÍNH
# ─────────────────────────────────────────────────────────────────────────────
col_input, col_data, col_result = st.columns([1.4, 1.6, 2.0], gap="large")


# ═════════════════════════════════════════════════════════════════════════════
# CỘT 1 — NHẬP DỮ LIỆU
# ═════════════════════════════════════════════════════════════════════════════
with col_input:
    st.markdown("<h3 class='section-title'> Nhập dữ liệu</h3>", unsafe_allow_html=True)


    # ── Ngân sách ──────────────────────────────────────────────────────────
    budget = st.number_input(
        "Ngân sách đầu tư (đồng)",
        min_value=10_000_000,
        max_value=100_000_000_000,
        value=1_000_000_000,
        step=10_000_000,
        format="%d",
        help="Tổng ngân sách tối đa cho danh mục đầu tư",
    )
    st.caption(f"Ngân sách: **{fmt_money(budget)}**")


    st.markdown("---")


    # ── Tabs nhập liệu ─────────────────────────────────────────────────────
    tab_auto, tab_csv, tab_manual = st.tabs(["Sinh tự động", "Tải CSV", "Thêm thủ công"])


    # ── TAB 1: Sinh tự động ────────────────────────────────────────────────
    with tab_auto:
        size_option = st.selectbox(
            "Quy mô danh sách",
            ["Small (10–15 dự án)", "Medium (20–30 dự án)", "Large (50+ dự án)"],
        )
        size_map = {
            "Small (10–15 dự án)":   (10, 15),
            "Medium (20–30 dự án)":  (20, 30),
            "Large (50+ dự án)":     (50, 70),
        }


        if st.button("Sinh dữ liệu ngẫu nhiên", use_container_width=True):
            lo, hi = size_map[size_option]
            n = random.randint(lo, hi)
            rows = []
            for i in range(1, n + 1):
                profit = random.randint(50_000_000, 500_000_000)
                cost   = random.randint(20_000_000, int(budget * 0.35))
                rows.append({
                    "Chọn": False,
                    "Tên dự án":        f"Dự án {i:02d}",
                    "Lợi nhuận (đồng)": profit,
                    "Chi phí (đồng)":   cost,
                })
            st.session_state["df_projects"] = pd.DataFrame(rows)
            st.session_state["result_stale"] = True
            st.success(f"Đã sinh {n} dự án ngẫu nhiên!")


    # ── TAB 2: Tải CSV ─────────────────────────────────────────────────────
    with tab_csv:
        st.caption(
            "File CSV cần có các cột: `ten_du_an`, `loi_nhuan`, `chi_phi`"
        )
        uploaded = st.file_uploader("Chọn file CSV", type=["csv"], label_visibility="collapsed")


        if uploaded:
            # Lấy nội dung file để kiểm tra xem đã đọc file này chưa
            file_bytes = uploaded.getvalue()


            # CHỈ ĐỌC LẠI NẾU ĐÂY LÀ FILE MỚI HOÀN TOÀN
            if st.session_state.get("last_uploaded_bytes") != file_bytes:
                try:
                    df_raw = pd.read_csv(uploaded, sep=None, engine='python', encoding='utf-8-sig')
                    required_cols = {"ten_du_an", "loi_nhuan", "chi_phi"}
                    missing = required_cols - set(df_raw.columns.str.lower().str.strip())


                    if missing:
                        st.error(
                            f"File CSV thiếu cột: **{', '.join(missing)}**\n\n"
                            "Vui lòng kiểm tra lại định dạng file."
                        )
                    else:
                        df_raw.columns = df_raw.columns.str.lower().str.strip()
                        rows = []
                        for _, r in df_raw.iterrows():
                            try:
                                rows.append({
                                    "Chọn": False,
                                    "Tên dự án": str(r["ten_du_an"]),
                                    "Lợi nhuận (đồng)": int(float(r["loi_nhuan"])),
                                    "Chi phí (đồng)": int(float(r["chi_phi"])),
                                })
                            except (ValueError, KeyError):
                                continue


                        if not rows:
                            st.error("Không đọc được dòng dữ liệu hợp lệ nào.")
                        else:
                            st.session_state["df_projects"] = pd.DataFrame(rows)
                            st.session_state["result_stale"] = True


                            # Ghi nhớ rằng file này đã được đọc xong
                            st.session_state["last_uploaded_bytes"] = file_bytes


                            st.success(f"Đã tải {len(rows)} dự án từ CSV!")
                except Exception as e:
                    st.error(f"Lỗi đọc file: {e}")


    # ── TAB 3: Thêm thủ công ───────────────────────────────────────────────
    with tab_manual:
        with st.form("form_add_project", clear_on_submit=True):
            proj_name   = st.text_input("Tên dự án", placeholder="VD: Dự án Xanh")
            proj_profit = st.number_input(
                "Lợi nhuận kỳ vọng (đồng)",
                min_value=0, value=100_000_000, step=10_000_000, format="%d"
            )
            proj_cost   = st.number_input(
                "Chi phí đầu tư (đồng)",
                min_value=0, value=50_000_000, step=10_000_000, format="%d"
            )
            submitted = st.form_submit_button("Thêm dự án", use_container_width=True)


        if submitted:
            if not proj_name.strip():
                st.warning("Vui lòng nhập tên dự án.")
            elif proj_cost <= 0:
                st.warning("Chi phí phải lớn hơn 0.")
            else:
                new_row = pd.DataFrame([{
                    "Chọn": False,
                    "Tên dự án":        proj_name.strip(),
                    "Lợi nhuận (đồng)": int(proj_profit),
                    "Chi phí (đồng)":   int(proj_cost),
                }])
                st.session_state["df_projects"] = pd.concat(
                    [st.session_state["df_projects"], new_row], ignore_index=True
                )
                st.session_state["result_stale"] = True
                st.success(f"Đã thêm **{proj_name.strip()}**!")


# ═════════════════════════════════════════════════════════════════════════════
# CỘT 2 — QUẢN LÝ DỮ LIỆU
# ═════════════════════════════════════════════════════════════════════════════
with col_data:
    st.markdown("<h3 class='section-title'>Danh sách dự án</h3>", unsafe_allow_html=True)

    df = st.session_state["df_projects"]
    n_projects = len(df)

    if n_projects == 0:
        st.markdown(
            "<div class='info-box'>Chưa có dự án nào. "
            "Hãy sinh tự động, tải CSV hoặc thêm thủ công ở cột bên trái.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.caption(f"Tổng: **{n_projects}** dự án · Backtracking giới hạn: **{bt_limit}** dự án")

        if "Chọn" not in df.columns:
            df.insert(0, "Chọn", False)

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            column_config={
                "Chọn": st.column_config.CheckboxColumn("☑", width="small"),
                "Tên dự án": st.column_config.TextColumn("Tên dự án", width="medium"),
                "Lợi nhuận (đồng)": st.column_config.NumberColumn(
                    "Lợi nhuận (đ)", format="%d", width="medium"
                ),
                "Chi phí (đồng)": st.column_config.NumberColumn(
                    "Chi phí (đ)", format="%d", width="medium"
                ),
            },
            height=min(400, 80 + n_projects * 35),
            key="data_editor_main",
        )

        # ✅ FIX: KHÔNG lưu edited_df về session_state sau mỗi lần rerun.
        # Chỉ đọc để kiểm tra stale — base df phải ổn định giữa các rerun
        # để data_editor giữ được delta nội bộ (checkbox state).
        old_hash = st.session_state.get("last_data_hash")
        new_hash = df_hash(edited_df.drop(columns=["Chọn"], errors="ignore"))
        if old_hash and old_hash != new_hash and (
            st.session_state["cso_result"] or st.session_state["bt_result"]
        ):
            st.session_state["result_stale"] = True

        # ── Nút thao tác ────────────────────────────────────────────────────
        btn_del, btn_clear = st.columns(2)

        with btn_del:
            if st.button("Xóa đã chọn", use_container_width=True):
                mask = edited_df["Chọn"] == True
                n_del = int(mask.sum())
                if n_del == 0:
                    st.warning("Chưa chọn dự án nào để xóa.")
                else:
                    # ✅ Commit edited_df (với mọi edit hiện tại), xóa hàng đã chọn,
                    #    reset checkbox, lưu làm base mới → rerun sạch.
                    new_df = edited_df[~mask].reset_index(drop=True)
                    new_df["Chọn"] = False
                    st.session_state["df_projects"] = new_df
                    st.session_state["result_stale"] = True
                    st.rerun()

        with btn_clear:
            if st.button("Xóa tất cả", use_container_width=True, type="secondary"):
                st.session_state["df_projects"] = pd.DataFrame(
                    columns=["Chọn", "Tên dự án", "Lợi nhuận (đồng)", "Chi phí (đồng)"]
                )
                st.session_state["cso_result"]   = None
                st.session_state["bt_result"]    = None
                st.session_state["result_stale"] = False
                st.rerun()

        # ── Nút chạy thuật toán ─────────────────────────────────────────────
        st.markdown("---")
        run_disabled = n_projects == 0

        if n_projects > bt_limit and n_projects > 0:
            st.markdown(
                f"<div class='warn-box'>Backtracking sẽ <b>bị bỏ qua</b> vì n={n_projects} "
                f"> giới hạn {bt_limit}. CSO vẫn chạy bình thường.</div>",
                unsafe_allow_html=True,
            )

        run_btn = st.button(
            "Chạy so sánh thuật toán",
            use_container_width=True,
            type="primary",
            disabled=run_disabled,
        )

        if run_disabled:
            st.caption("⬆Thêm dữ liệu để kích hoạt")

    # ─────────────────────────────────────────────────────────────────────
    # XỬ LÝ CHẠY THUẬT TOÁN
    # ─────────────────────────────────────────────────────────────────────
    if n_projects > 0 and "run_btn" in dir() and run_btn:
        st.session_state["df_projects"] = edited_df
        df_run = edited_df

        profits = df_run["Lợi nhuận (đồng)"].tolist()
        costs   = df_run["Chi phí (đồng)"].tolist()

        with st.spinner("Đang chạy CSO..."):
            cso = BinaryCSOKnapsack(n_cats=n_cats, max_iter=max_iter, MR=MR, SMP=SMP)
            st.session_state["cso_result"] = cso.solve(profits, costs, int(budget))

        if n_projects <= bt_limit:
            with st.spinner("Đang chạy Backtracking..."):
                bt = BacktrackingKnapsack()
                st.session_state["bt_result"] = bt.solve(profits, costs, int(budget))
        else:
            st.session_state["bt_result"] = None

        st.session_state["last_data_hash"] = df_hash(
            df_run.drop(columns=["Chọn"], errors="ignore")
        )
        st.session_state["result_stale"] = False
        st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# CỘT 3 — KẾT QUẢ / BÁO CÁO
# ═════════════════════════════════════════════════════════════════════════════
with col_result:
    st.markdown("<h3 class='section-title'>Kết quả & Báo cáo so sánh</h3>", unsafe_allow_html=True)


    cso_res = st.session_state.get("cso_result")
    bt_res  = st.session_state.get("bt_result")
    stale   = st.session_state.get("result_stale", False)


    # ── Kiểm tra stale ────────────────────────────────────────────────────
    if stale and (cso_res or bt_res):
        st.markdown(
            "<div class='stale-banner'>"
            "Dữ liệu đã thay đổi — kết quả bên dưới không còn chính xác.<br>"
            "Hãy nhấn <b>Chạy so sánh thuật toán</b> để cập nhật."
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("")
    elif not cso_res and not bt_res:
        st.markdown(
            "<div class='info-box'>"
            "Chưa có kết quả. Hãy nhập dữ liệu và nhấn <b>Chạy so sánh thuật toán</b>."
            "</div>",
            unsafe_allow_html=True,
        )


    # ── Hiển thị kết quả nếu có và không stale ────────────────────────────
    if (cso_res or bt_res) and not stale:
        df_disp = st.session_state["df_projects"]
        n_total = len(df_disp)


        # ================================================================
        # A. KẾT QUẢ CSO
        # ================================================================
        if cso_res:
            st.markdown("#### Cat Swarm Optimization (CSO)")
            n_sel_cso = sum(cso_res["solution"])


            with st.container():
                st.markdown("<div class='metric-cso'>", unsafe_allow_html=True)
                m1, m2 = st.columns(2)
                m1.metric("Lợi nhuận", fmt_money(cso_res["profit"]))
                m2.metric("Chi phí", fmt_money(cso_res["cost"]))

                m3, m4 = st.columns(2)
                m3.metric("Thời gian", f"{cso_res['time']:.2f}s")
                m4.metric("Memory", fmt_mem(cso_res["memory"]))


            st.caption(f"Chọn **{n_sel_cso}/{n_total}** dự án")


            if n_sel_cso > 0:
                idx_sel = [i for i, s in enumerate(cso_res["solution"]) if s == 1]
                df_cso_detail = df_disp.iloc[idx_sel][
                    ["Tên dự án", "Lợi nhuận (đồng)", "Chi phí (đồng)"]
                ].copy().reset_index(drop=True)
                with st.expander(f"Chi tiết {n_sel_cso} dự án được chọn (CSO)", expanded=False):
                    st.dataframe(df_cso_detail, use_container_width=True, hide_index=True)


        st.markdown("---")


        # ================================================================
        # B. KẾT QUẢ BACKTRACKING
        # ================================================================
        if bt_res:
            st.markdown("#### Backtracking")
            n_sel_bt = sum(bt_res["solution"])


            with st.container():
                st.markdown("<div class='metric-bt'>", unsafe_allow_html=True)
                b1, b2 = st.columns(2)
                b1.metric("Lợi nhuận", fmt_money(bt_res["profit"]))
                b2.metric("Chi phí", fmt_money(bt_res["cost"]))

                b3, b4 = st.columns(2)
                b3.metric("Thời gian", f"{bt_res['time']:.2f}s")
                b4.metric("Memory", fmt_mem(bt_res["memory"]))
                st.markdown("</div>", unsafe_allow_html=True)


            st.caption(f"Chọn **{n_sel_bt}/{n_total}** dự án · Nghiệm tối ưu chính xác 100%")


            if n_sel_bt > 0:
                idx_sel_bt = [i for i, s in enumerate(bt_res["solution"]) if s == 1]
                df_bt_detail = df_disp.iloc[idx_sel_bt][
                    ["Tên dự án", "Lợi nhuận (đồng)", "Chi phí (đồng)"]
                ].copy().reset_index(drop=True)
                with st.expander(f"Chi tiết {n_sel_bt} dự án được chọn (Backtracking)", expanded=False):
                    st.dataframe(df_bt_detail, use_container_width=True, hide_index=True)


        elif cso_res and not bt_res:
            st.markdown("####" \
            " Backtracking")
            st.markdown(
                f"<div class='warn-box'>"
                f" Backtracking không chạy vì số dự án hiện tại (<b>{n_total}</b>) "
                f"vượt giới hạn cho phép (<b>{bt_limit}</b>).<br>"
                f"Độ phức tạp O(2<sup>{n_total}</sup>) có thể gây treo hệ thống."
                f"</div>",
                unsafe_allow_html=True,
            )


        # ================================================================
        # C. BẢNG SO SÁNH TỔNG HỢP
        # ================================================================
        if cso_res and bt_res:
            st.markdown("---")
            st.markdown("#### Bảng so sánh tổng hợp")


            faster    = "CSO" if cso_res["time"] < bt_res["time"] else "Backtracking"
            mem_less  = "CSO" if cso_res["memory"] < bt_res["memory"] else "Backtracking"
            gap_pct   = 0.0
            if bt_res["profit"] > 0:
                gap_pct = abs(cso_res["profit"] - bt_res["profit"]) / bt_res["profit"] * 100


            compare_data = {
                "Tiêu chí": [
                    "Lợi nhuận tìm được",
                    "Chi phí sử dụng",
                    "Thời gian chạy",
                    "Bộ nhớ sử dụng",
                    "Số dự án được chọn",
                    "Loại nghiệm",
                ],
                "CSO": [
                    fmt_money(cso_res["profit"]),
                    fmt_money(cso_res["cost"]),
                    f"{cso_res['time']:.2f}s",
                    fmt_mem(cso_res["memory"]),
                    f"{sum(cso_res['solution'])}/{n_total}",
                    "Xấp xỉ (heuristic)",
                ],
                "Backtracking": [
                    fmt_money(bt_res["profit"]),
                    fmt_money(bt_res["cost"]),
                    f"{bt_res['time']:.2f}s",
                    fmt_mem(bt_res["memory"]),
                    f"{sum(bt_res['solution'])}/{n_total}",
                    "Chính xác (exact)",
                ],
            }
            df_compare = pd.DataFrame(compare_data)
            st.dataframe(df_compare, use_container_width=True, hide_index=True)


            # Nhận xét nhanh
            st.markdown(
                f"<div class='info-box'>"
                f"<b>{faster}</b> chạy nhanh hơn · "
                f"<b>{mem_less}</b> ít bộ nhớ hơn · "
                f"Độ lệch lợi nhuận CSO so với tối ưu: <b>{gap_pct:.2f}%</b>"
                f"</div>",
                unsafe_allow_html=True,
            )

        # ================================================================
        # XUẤT BÁO CÁO CSV (giữ trong cột kết quả)
        # ================================================================
        st.markdown("---")
        st.markdown("#### Xuất báo cáo")


        export_rows = []
        if cso_res:
            export_rows.append({
                "Thuật toán": "CSO",
                "Lợi nhuận (đồng)": cso_res["profit"],
                "Chi phí (đồng)":   cso_res["cost"],
                "Thời gian (s)":    round(cso_res["time"], 6),
                "Bộ nhớ (KB)":      round(cso_res["memory"], 2),
                "Số dự án chọn":    sum(cso_res["solution"]),
                "Tổng dự án":       n_total,
            })
        if bt_res:
            export_rows.append({
                "Thuật toán": "Backtracking",
                "Lợi nhuận (đồng)": bt_res["profit"],
                "Chi phí (đồng)":   bt_res["cost"],
                "Thời gian (s)":    round(bt_res["time"], 6),
                "Bộ nhớ (KB)":      round(bt_res["memory"], 2),
                "Số dự án chọn":    sum(bt_res["solution"]),
                "Tổng dự án":       n_total,
            })


        if export_rows:
            df_export = pd.DataFrame(export_rows)
            csv_bytes  = df_export.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="📥 Tải báo cáo CSV",
                data=csv_bytes,
                file_name="bao_cao_so_sanh_thuat_toan.csv",
                mime="text/csv",
                use_container_width=True,
            )


# ═════════════════════════════════════════════════════════════════════════════
# PHẦN BIỂU ĐỒ — TOÀN CHIỀU RỘNG TRANG (bên ngoài cột hẹp)
# ═════════════════════════════════════════════════════════════════════════════
_cso_res = st.session_state.get("cso_result")
_bt_res  = st.session_state.get("bt_result")
_stale   = st.session_state.get("result_stale", False)
_n_total = len(st.session_state["df_projects"])

if (_cso_res or _bt_res) and not _stale:
    has_cso_chart = _cso_res and _cso_res.get("snapshots")
    has_bt_chart  = _bt_res and (_bt_res.get("tree_nodes") or _bt_res.get("depth_hits"))

    if has_cso_chart or has_bt_chart:
        st.divider()
        st.markdown(
            "<h2 style='text-align:center;color:#1e293b;font-size:1.35rem;"
            "font-weight:700;margin-bottom:0.3rem;'>📊 Phân tích trực quan — Biểu đồ chi tiết</h2>",
            unsafe_allow_html=True,
        )

        # Xây dựng danh sách tab
        tab_names = []
        if has_cso_chart:
            tab_names.append("CSO — Phân bố không gian nghiệm")
        if has_bt_chart:
            n_it = _bt_res.get("n_items", _n_total)
            if n_it <= 15:
                tab_names.append("Backtracking — Cây trạng thái")
            else:
                tab_names.append("Backtracking — Mật độ độ sâu")

        tabs = st.tabs(tab_names)
        tab_idx = 0

        # ── Tab CSO Scatter ─────────────────────────────────────────────
        if has_cso_chart:
            with tabs[tab_idx]:
                st.markdown(
                    "<div class='chart-caption'>"
                    "Mỗi chấm là một chú mèo. Màu <b>vàng/đỏ</b> = fitness cao, "
                    "màu <b>trắng/vàng nhạt</b> = fitness thấp. ⭐ = mèo tốt nhất tại mốc đó."
                    "</div>",
                    unsafe_allow_html=True,
                )
                with st.container():
                    render_cso_scatter(_cso_res["snapshots"], _n_total)
            tab_idx += 1

        # ── Tab Backtracking ─────────────────────────────────────────────
        if has_bt_chart:
            with tabs[tab_idx]:
                n_it = _bt_res.get("n_items", _n_total)
                if n_it <= 15:
                    cap = (
                        "🔵 Đang duyệt · 🟢 Lá hợp lệ · ⭐ Nghiệm tốt nhất · "
                        "🔴 Cắt (Bound) · 🟠 Cắt (Vượt ngân sách)"
                    )
                else:
                    cap = (
                        f"Với n={n_it} dự án, cây có {_bt_res.get('total_nodes', '?'):,} nút — "
                        "quá lớn để vẽ toàn bộ. Biểu đồ hiển thị số nút được duyệt theo từng tầng."
                    )
                st.markdown(
                    f"<div class='chart-caption'>{cap}</div>",
                    unsafe_allow_html=True,
                )
                with st.container():
                    render_bt_tree(_bt_res)


# ─────────────────────────────────────────────────────────────────────────────
# 8. FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center;color:#94a3b8;font-size:0.78rem;'>"
    "Tối Ưu Đầu Tư · Đồ án Phân tích Thuật toán · "
    "CSO (Metaheuristic) vs Backtracking (Exact) · "
    "Built with Streamlit"
    "</div>",
    unsafe_allow_html=True,
)
