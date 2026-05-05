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
        font-size: 2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.15rem;
    }
    .main-subtitle {
        font-size: 0.95rem;
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


    /* ── Metric cards ── */
    div[data-testid="metric-container"] {
        background: #f8faff;
        border: 1px solid #c7d7f7;
        border-left: 4px solid #3b82f6;
        border-radius: 10px;
        padding: 0.65rem 1rem;
        box-shadow: 0 1px 4px rgba(59,130,246,0.07);
    }
    div[data-testid="metric-container"] label {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }
    /* ── Fix metric value: thu nhỏ + chống cắt xén dấu "..." ── */
    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] > div {
        font-size: 1rem !important;          /* bằng cỡ chữ văn bản thường */
        font-weight: 700 !important;
        color: #1e40af !important;
        white-space: normal !important;      /* cho phép xuống dòng thay vì bị cắt */
        overflow: visible !important;        /* không ẩn nội dung tràn */
        text-overflow: clip !important;      /* tuyệt đối không dùng dấu "..." */
        word-break: break-word !important;   /* phòng trường hợp chuỗi quá dài */
        line-height: 1.3 !important;
    }
    
    /* Override màu riêng cho từng loại, giữ nguyên các màu cũ */
    .metric-cso [data-testid="stMetricValue"],
    .metric-cso [data-testid="stMetricValue"] > div {
        color: #065f46 !important;
    }
    .metric-bt [data-testid="stMetricValue"],
    .metric-bt [data-testid="stMetricValue"] > div {
        color: #92400e !important;
    }

    /* ── Metric CSO ── */
    .metric-cso div[data-testid="metric-container"] {
        border-left-color: #10b981;
        background: #f0fdf8;
        border-color: #a7f3d0;
    }
    .metric-cso div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #065f46 !important;
    }


    /* ── Metric BT ── */
    .metric-bt div[data-testid="metric-container"] {
        border-left-color: #f59e0b;
        background: #fffbeb;
        border-color: #fde68a;
    }
    .metric-bt div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #92400e !important;
    }


    /* ── Warning box ── */
    .warn-box {
        background: #fff7ed;
        border: 1px solid #fed7aa;
        border-left: 4px solid #f97316;
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        font-size: 0.88rem;
        color: #9a3412;
        margin: 0.5rem 0;
    }


    /* ── Info box ── */
    .info-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 0.6rem 0.9rem;
        font-size: 0.88rem;
        color: #1e40af;
        margin: 0.5rem 0;
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
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        color: #991b1b;
        font-weight: 600;
        font-size: 0.95rem;
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


        # 🔁 Vòng lặp chính
        for _ in range(self.max_iter):
            for i in range(self.n_cats):


                if random.random() < self.MR:
                    # =======================
                    # 🔎 SEEKING MODE
                    # =======================
                    candidates = []


                    for _ in range(self.SMP):
                        candidate = cats[i][:]
                        idx = random.randint(0, n - 1)
                        candidate[idx] = 1 - candidate[idx]  # flip bit
                        candidates.append(candidate)


                    # chọn candidate tốt nhất
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


                        # sigmoid → nhị phân
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
            "memory": peak / 1024  # KB
        }






class BacktrackingKnapsack:
    """
    Thuật toán Backtracking thật sự — O(2^n).
    Đệ quy phân nhánh: chọn hoặc không chọn từng dự án.
    """
    def __init__(self):
        self._best_profit   = 0
        self._best_solution = []


    def _backtrack(self, idx: int, profits: list, costs: list,
                   budget: int, current_profit: int, current_cost: int,
                   current_sol: list):
        n = len(profits)
        # Cập nhật nghiệm tốt nhất
        if current_profit > self._best_profit:
            self._best_profit   = current_profit
            self._best_solution = current_sol[:]


        if idx == n:
            return


        # Nhánh 1: KHÔNG chọn dự án idx
        current_sol.append(0)
        self._backtrack(idx + 1, profits, costs, budget,
                        current_profit, current_cost, current_sol)
        current_sol.pop()


        # Nhánh 2: CHỌN dự án idx (nếu còn đủ ngân sách)
        if current_cost + costs[idx] <= budget:
            current_sol.append(1)
            self._backtrack(idx + 1, profits, costs, budget,
                            current_profit + profits[idx],
                            current_cost  + costs[idx],
                            current_sol)
            current_sol.pop()


    def solve(self, profits: list, costs: list, budget: int) -> dict:
        """Chạy backtracking thật, đo time và memory."""
        self._best_profit   = 0
        self._best_solution = []


        tracemalloc.start()
        t0 = time.time()
        self._backtrack(0, profits, costs, budget, 0, 0, [])
        elapsed = time.time() - t0
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()


        sol = self._best_solution
        if len(sol) < len(profits):
            sol = sol + [0] * (len(profits) - len(sol))


        total_cost = sum(c * s for c, s in zip(costs, sol))
        return {
            "profit":   self._best_profit,
            "cost":     total_cost,
            "solution": sol,
            "time":     elapsed,
            "memory":   peak / 1024,  # KB
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
        # D. XUẤT BÁO CÁO CSV
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