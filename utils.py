"""
=============================================================================
  utils.py — Hàm tiện ích, CSS toàn cục và khởi tạo Session State
  Chứa: fmt_money, fmt_mem, df_hash, mark_stale, init_state, inject_css
  Import vào app.py để sử dụng.
=============================================================================
"""

import streamlit as st
import pandas as pd


# ─────────────────────────────────────────────────────────────────────────────
# HẰNG SỐ: TOÀN BỘ CSS + META TAG
# ─────────────────────────────────────────────────────────────────────────────
_CSS_STYLES = """
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

/* ── Metric cards — style chung ── */
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

/* Fix metric value: thu nhỏ + chống cắt xén dấu "..." */
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

/* ── Metric CSO — màu xanh lá ── */
.metric-cso div[data-testid="metric-container"] {
    border-left-color: #10b981;
    background: #f0fdf8;
    border-color: #a7f3d0;
}
.metric-cso [data-testid="stMetricValue"],
.metric-cso [data-testid="stMetricValue"] > div {
    color: #065f46 !important;
}

/* ── Metric Backtracking — màu vàng cam ── */
.metric-bt div[data-testid="metric-container"] {
    border-left-color: #f59e0b;
    background: #fffbeb;
    border-color: #fde68a;
}
.metric-bt [data-testid="stMetricValue"],
.metric-bt [data-testid="stMetricValue"] > div {
    color: #92400e !important;
}

/* ── Hộp cảnh báo cam ── */
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

/* ── Hộp thông tin xanh dương ── */
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

/* ── Sidebar dark gradient ── */
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

/* ── Banner kết quả đã lỗi thời ── */
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
"""


# ─────────────────────────────────────────────────────────────────────────────
# HÀM: INJECT CSS VÀO TRANG
# ─────────────────────────────────────────────────────────────────────────────
def inject_css() -> None:
    """Tiêm toàn bộ CSS + meta tag vào trang Streamlit."""
    st.markdown(_CSS_STYLES, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HÀM: KHỞI TẠO SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
def init_state() -> None:
    """
    Khởi tạo các key trong st.session_state nếu chưa tồn tại.
    Gọi một lần duy nhất ở đầu app.py.

    Keys:
        df_projects       : DataFrame chứa danh sách dự án
        cso_result        : Kết quả CSO (dict) hoặc None
        bt_result         : Kết quả Backtracking (dict) hoặc None
        result_stale      : True nếu dữ liệu thay đổi mà chưa chạy lại
        last_data_hash    : Hash của dữ liệu tại lần chạy gần nhất
        last_uploaded_bytes: Bytes của file CSV đã đọc, tránh đọc lại
    """
    defaults = {
        "df_projects": pd.DataFrame(
            columns=["Chọn", "Tên dự án", "Lợi nhuận (đồng)", "Chi phí (đồng)"]
        ),
        "cso_result":          None,
        "bt_result":           None,
        "result_stale":        False,
        "last_data_hash":      None,
        "last_uploaded_bytes": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ─────────────────────────────────────────────────────────────────────────────
# HÀM TIỆN ÍCH — FORMAT DỮ LIỆU
# ─────────────────────────────────────────────────────────────────────────────
def fmt_money(value: float) -> str:
    """
    Format số tiền theo chuẩn Việt Nam.
    Ví dụ: 1_000_000_000 → '1.000.000.000 đồng'
    """
    return f"{int(value):,} đồng".replace(",", ".")


def fmt_mem(kb: float) -> str:
    """
    Format dung lượng bộ nhớ.
    Dưới 1024 KB → hiển thị KB, ngược lại → hiển thị MB.
    """
    if kb < 1024:
        return f"{kb:.1f} KB"
    return f"{kb / 1024:.2f} MB"


# ─────────────────────────────────────────────────────────────────────────────
# HÀM TIỆN ÍCH — PHÁT HIỆN THAY ĐỔI DỮ LIỆU
# ─────────────────────────────────────────────────────────────────────────────
def df_hash(df: pd.DataFrame) -> str:
    """
    Tính hash nhẹ của DataFrame để phát hiện thay đổi dữ liệu.
    Dùng pd.util.hash_pandas_object; fallback về len(df) nếu lỗi.
    """
    try:
        return str(pd.util.hash_pandas_object(df).sum())
    except Exception:
        return str(len(df))


def mark_stale() -> None:
    """
    Đánh dấu kết quả cũ là 'lỗi thời' (stale) nếu dữ liệu hiện tại
    khác với dữ liệu tại lần chạy thuật toán gần nhất.

    Chỉ đánh dấu khi đã từng có kết quả (tránh false-positive lúc khởi động).
    """
    current_hash = df_hash(st.session_state["df_projects"])
    has_results  = st.session_state.get("cso_result") or st.session_state.get("bt_result")
    last_hash    = st.session_state.get("last_data_hash")

    if last_hash is not None and current_hash != last_hash and has_results:
        st.session_state["result_stale"] = True
