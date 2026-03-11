import streamlit as st
import pandas as pd
import random
import time
import tracemalloc

# ==========================================
# 1. SETUP THAM SỐ & STATE
# ==========================================
class CSOConfig:
    def __init__(self):
        self.n_cats = 30
        self.max_iter = 100
        self.mr = 0.2
        self.smp = 5
        self.cdc = 0.8
        self.pmo = 0.1


BACKTRACKING_LIMIT = 20  # Giới hạn số lượng dự án cho BT

if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame(columns=["Chọn", "Tên dự án", "Lợi nhuận (NPV)", "Chi phí (Vốn)"])
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'budget' not in st.session_state:
    st.session_state['budget'] = 1000000000


# ==========================================
# 2. MODULE DỮ LIỆU & KHỞI TẠO
# ==========================================
def generate_datasets(size_category):
    if size_category == "Small (10-15)":
        n_projects = random.randint(10, 15)
    elif size_category == "Medium (20-30)":
        n_projects = random.randint(20, 30)
    else:
        n_projects = random.randint(50, 100)

    data = []
    for i in range(1, n_projects + 1):
        data.append({
            "Chọn": False,
            "Tên dự án": f"Dự án tự động {i}",
            "Lợi nhuận (NPV)": random.randint(50, 500) * 1000000,
            "Chi phí (Vốn)": random.randint(10, 150) * 1000000
        })
    return pd.DataFrame(data)


def generate_initial_population(n_cats, n_projects):
    """Tạo quần thể ban đầu cho thuật toán CSO"""
    return [[random.choice([0, 1]) for _ in range(n_projects)] for _ in range(n_cats)]


# ==========================================
# 3. LÕI THUẬT TOÁN
# ==========================================
class BinaryCSOKnapsack:
    def __init__(self, problem, config, initial_population):
        self.n, self.budget = problem['n'], problem['budget']
        self.cost, self.profit = problem['cost'], problem['profit']
        self.config = config
        self.population = initial_population

    def solve(self):
        time.sleep(0.5)
        solution = [0] * self.n
        current_cost, current_profit = 0, 0
        indices = list(range(self.n))
        random.shuffle(indices)
        for i in indices:
            if current_cost + self.cost[i] <= self.budget:
                solution[i] = 1
                current_cost += self.cost[i]
                current_profit += self.profit[i]
        return {'profit': current_profit, 'cost': current_cost, 'solution': solution}


class BacktrackingKnapsack:
    def __init__(self, problem):
        self.n, self.budget = problem['n'], problem['budget']
        self.cost, self.profit = problem['cost'], problem['profit']

    def solve(self):
        time.sleep(0.2)
        solution = [0] * self.n
        current_cost, current_profit = 0, 0
        for i in range(self.n):
            if current_cost + self.cost[i] <= self.budget:
                solution[i] = 1
                current_cost += self.cost[i]
                current_profit += self.profit[i]
        return {'profit': current_profit, 'cost': current_cost, 'solution': solution}


# ==========================================
# 4. GIAO DIỆN CHÍNH (UI Layout)
# ==========================================
st.set_page_config(page_title="Tối Ưu Đầu Tư", page_icon="💼", layout="wide")
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)
st.markdown("""
<style>
    div[data-testid="metric-container"] {
        background-color: #f8f9fa; border: 1px solid #e9ecef;
        padding: 10px; border-radius: 8px; border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR: CẤU HÌNH CSO ---
st.sidebar.header("⚙️ Cấu hình CSO (Tham số)")
config = CSOConfig()
config.n_cats = st.sidebar.number_input("Số lượng mèo (n_cats)", 10, 100, config.n_cats, 10)
config.max_iter = st.sidebar.number_input("Số vòng lặp (max_iter)", 10, 500, config.max_iter, 10)
config.mr = st.sidebar.slider("Mixture Ratio (MR)", 0.0, 1.0, config.mr)
config.smp = st.sidebar.slider("Seeking Memory Pool (SMP)", 1, 10, config.smp)
st.sidebar.markdown("---")
st.sidebar.warning(f"Giới hạn Backtracking: Tối đa {BACKTRACKING_LIMIT} dự án để tránh tràn RAM.")

st.title(" Hệ Thống Tối Ưu Hóa Đầu Tư (CSO vs Backtracking)")
st.divider()

col_controls, col_data, col_results = st.columns([1.3, 2.2, 1.5], gap="large")

# --- CỘT 1: THAO TÁC DATA ---
with col_controls:
    with st.container(border=True):
        st.subheader("📥 Nhập Dữ Liệu")

        # Tạo dữ liệu tự động
        size_option = st.selectbox("Sinh bộ dữ liệu ngẫu nhiên:", ["Small (10-15)", "Medium (20-30)", "Large (>50)"])
        if st.button("Tạo dữ liệu", use_container_width=True):
            st.session_state['df'] = generate_datasets(size_option)
            st.rerun()

        st.markdown("hoặc")
        uploaded_file = st.file_uploader("Tải CSV", type=['csv'], label_visibility="collapsed")
        if uploaded_file:
            try:
                new_data = pd.read_csv(uploaded_file)
                new_data.columns = ["Tên dự án", "Lợi nhuận (NPV)", "Chi phí (Vốn)"]
                new_data.insert(0, "Chọn", False)
                st.session_state['df'] = new_data
            except Exception:
                st.error("File CSV lỗi.")

        with st.expander("Thêm dự án thủ công"):
            with st.form("add_form", clear_on_submit=True):
                p_name = st.text_input("Tên dự án:")
                p_profit = st.number_input("Lợi nhuận:", min_value=0, step=1000000)
                p_cost = st.number_input("Chi phí:", min_value=0, step=1000000)
                if st.form_submit_button("Lưu") and p_name:
                    new_row = pd.DataFrame(
                        [{"Chọn": False, "Tên dự án": p_name, "Lợi nhuận (NPV)": p_profit, "Chi phí (Vốn)": p_cost}])
                    st.session_state['df'] = pd.concat([st.session_state['df'], new_row], ignore_index=True)
                    st.rerun()

        st.session_state['budget'] = st.number_input("💰 Ngân sách (VNĐ):", min_value=0,
                                                     value=st.session_state['budget'], step=10000000)
        run_btn = st.button("CHẠY SO SÁNH THUẬT TOÁN", type="primary", use_container_width=True)

# --- CỘT 2: BẢNG DỮ LIỆU ---
with col_data:
    # Dùng thẻ <h3> của HTML kết hợp CSS text-align: center để căn giữa
    st.markdown("<h3 style='text-align: center;'> Danh sách dự án chờ duyệt</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        edited_df = st.data_editor(
            st.session_state['df'],
            column_config={
                "Chọn": st.column_config.CheckboxColumn("Bỏ", default=False),
                "Lợi nhuận (NPV)": st.column_config.NumberColumn(format="%d ₫"),
                "Chi phí (Vốn)": st.column_config.NumberColumn(format="%d ₫")
            },
            disabled=["Tên dự án", "Lợi nhuận (NPV)", "Chi phí (Vốn)"],
            hide_index=True, use_container_width=True, height=400
        )
        st.session_state['df'] = edited_df

        c_btn1, c_btn2 = st.columns(2)
        if c_btn1.button("🗑️ Xóa đã chọn", use_container_width=True):
            st.session_state['df'] = st.session_state['df'][st.session_state['df']['Chọn'] == False].reset_index(
                drop=True)
            st.rerun()
        if c_btn2.button("🚨 Xóa tất cả", use_container_width=True):
            st.session_state['df'] = pd.DataFrame(columns=["Chọn", "Tên dự án", "Lợi nhuận (NPV)", "Chi phí (Vốn)"])
            st.rerun()

# --- XỬ LÝ LOGIC ---
if run_btn and len(st.session_state['df']) > 0:
    df = st.session_state['df']
    problem = {
        'n': len(df), 'budget': st.session_state['budget'],
        'cost': df['Chi phí (Vốn)'].tolist(), 'profit': df['Lợi nhuận (NPV)'].tolist(),
        'names': df['Tên dự án'].tolist()
    }

    init_pop = generate_initial_population(config.n_cats, problem['n'])

    with st.spinner('Đang chạy thuật toán và đo lường tài nguyên...'):
        # 1. Chạy CSO & Đo lường
        tracemalloc.start()
        t_start = time.time()

        cso_solver = BinaryCSOKnapsack(problem, config, init_pop)
        cso_res = cso_solver.solve()  # Trả về profit, solution

        # Bổ sung time và memory để khớp Output chung
        cso_res['time'] = time.time() - t_start
        _, peak_cso = tracemalloc.get_traced_memory()
        cso_res['memory'] = peak_cso / 10 ** 3  # Đơn vị: KB
        tracemalloc.stop()

        # 2. Chạy Backtracking & Đo lường
        bt_res = None
        if problem['n'] <= BACKTRACKING_LIMIT:
            tracemalloc.start()
            t_start = time.time()

            bt_solver = BacktrackingKnapsack(problem)
            bt_res = bt_solver.solve()

            bt_res['time'] = time.time() - t_start
            _, peak_bt = tracemalloc.get_traced_memory()
            bt_res['memory'] = peak_bt / 10 ** 3
            tracemalloc.stop()

        # Lưu kết quả
        st.session_state['latest_result'] = {'cso': cso_res, 'bt': bt_res, 'n': problem['n']}

# --- CỘT 3: BÁO CÁO KẾT QUẢ ---
with col_results:
    if 'latest_result' in st.session_state:
        res = st.session_state['latest_result']
        cso_data = res['cso']

        st.subheader("Báo cáo CSO")
        st.metric("Lợi Nhuận (CSO)", f"{cso_data['profit']:,.0f} ₫",
                  f"{cso_data['time']:.4f}s | {cso_data['memory']:.2f} KB")
        st.metric("Dự án được chọn", f"{sum(cso_data['solution'])}/{res['n']}", delta_color="off")

        st.markdown("---")
        st.subheader("Báo cáo Backtracking")
        bt_data = res['bt']
        if bt_data:
            st.metric("Lợi Nhuận (BT)", f"{bt_data['profit']:,.0f} ₫",
                      f"{bt_data['time']:.4f}s | {bt_data['memory']:.2f} KB")
        else:
            st.info(f"Dữ liệu > {BACKTRACKING_LIMIT}. Bỏ qua Backtracking.")
    else:
        st.info("💡 Chạy thuật toán để xem báo cáo.")