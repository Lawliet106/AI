"""
=============================================================================
  app.py — Giao diện chính Streamlit (File chạy chính)
  Môn: Phân tích Thuật toán
  Bài toán: Tối ưu hóa danh mục đầu tư (0/1 Knapsack)

  Cách chạy:
      streamlit run app.py

  Phụ thuộc:
      algorithms.py  — Lõi thuật toán CSO & Backtracking
      utils.py       — Hàm tiện ích, CSS, Session State
=============================================================================
"""

import streamlit as st
import pandas as pd
import random

# ── Import từ các module nội bộ ───────────────────────────────────────────────
from algorithms import BinaryCSOKnapsack, BacktrackingKnapsack
from utils import (
    inject_css,
    init_state,
    fmt_money,
    fmt_mem,
    df_hash,
)


# ─────────────────────────────────────────────────────────────────────────────
# 0. CẤU HÌNH TRANG — phải gọi TRƯỚC mọi st.* khác
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tối Ưu Đầu Tư",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Tiêm CSS toàn cục + meta tag chặn dịch tự động ───────────────────────────
inject_css()

# ── Khởi tạo session state (chỉ set nếu chưa tồn tại) ───────────────────────
init_state()


# ═════════════════════════════════════════════════════════════════════════════
# 1. SIDEBAR — CẤU HÌNH THAM SỐ
# ═════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Cấu hình tham số")
    st.markdown("---")

    # ── CSO Parameters ────────────────────────────────────────────────────────
    st.markdown("### CSO Parameters")
    n_cats   = st.slider("Số lượng mèo (n_cats)",  10,  100, 30,  step=5)
    max_iter = st.slider("Số vòng lặp (max_iter)", 10,  500, 100, step=10)
    MR       = st.slider("Tỉ lệ truy tìm (MR)",    0.0, 1.0, 0.3, step=0.05)
    SMP      = st.slider("Bộ nhớ tìm kiếm (SMP)",  1,   10,  5)

    st.markdown("---")

    # ── Backtracking — giới hạn n (demo bùng nổ tổ hợp) ─────────────────────
    st.markdown("### Backtracking")
    bt_limit = st.slider(
        "Giới hạn Backtracking (n dự án)",
        min_value=10, max_value=30, value=20, step=1,
    )

    # Cảnh báo đỏ khi người dùng kéo vượt ngưỡng nguy hiểm
    if bt_limit > 23:
        st.markdown(
            """
            <div style='background:#7f1d1d; border-radius:8px; padding:0.6rem 0.8rem;
                        font-size:0.82rem; color:#fecaca; margin-top:0.3rem;'>
            ⚠️ <b>Cảnh báo!</b> Với n &gt; 23, độ phức tạp O(2ⁿ) có thể khiến
            <b>hệ thống bị treo</b>. Hãy cân nhắc kỹ trước khi chạy.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem; color:#64748b; text-align:center;'>"
        "CSO luôn chạy · Backtracking chỉ chạy khi n ≤ giới hạn"
        "</div>",
        unsafe_allow_html=True,
    )


# ═════════════════════════════════════════════════════════════════════════════
# 2. TIÊU ĐỀ TRANG CHÍNH
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    "<div class='main-title'>💼 Tối Ưu Hóa Danh Mục Đầu Tư</div>"
    "<div class='main-subtitle'>So sánh hiệu năng: "
    "<b>Cat Swarm Optimization (CSO)</b> vs <b>Backtracking</b> · "
    "Bài toán cái túi 0/1 Knapsack</div>",
    unsafe_allow_html=True,
)
st.divider()


# ═════════════════════════════════════════════════════════════════════════════
# 3. BA CỘT CHÍNH
# ═════════════════════════════════════════════════════════════════════════════
col_input, col_data, col_result = st.columns([1.4, 1.6, 2.0], gap="large")


# ─────────────────────────────────────────────────────────────────────────────
# CỘT 1 — NHẬP DỮ LIỆU
# ─────────────────────────────────────────────────────────────────────────────
with col_input:
    st.markdown("<h3 class='section-title'>📥 Nhập dữ liệu</h3>", unsafe_allow_html=True)

    # ── Ngân sách đầu tư ─────────────────────────────────────────────────────
    budget = st.number_input(
        "💰 Ngân sách đầu tư (đồng)",
        min_value=10_000_000,
        max_value=100_000_000_000,
        value=1_000_000_000,
        step=10_000_000,
        format="%d",
        help="Tổng ngân sách tối đa cho danh mục đầu tư",
    )
    st.caption(f"Ngân sách: **{fmt_money(budget)}**")
    st.markdown("---")

    # ── 3 Tab nhập liệu ───────────────────────────────────────────────────────
    tab_auto, tab_csv, tab_manual = st.tabs(["🎲 Sinh tự động", "📁 Tải CSV", "✏️ Thêm thủ công"])

    # ── TAB 1: Sinh dữ liệu ngẫu nhiên ───────────────────────────────────────
    with tab_auto:
        size_option = st.selectbox(
            "Quy mô danh sách",
            ["Small (10–15 dự án)", "Medium (20–30 dự án)", "Large (50+ dự án)"],
        )
        size_map = {
            "Small (10–15 dự án)":  (10, 15),
            "Medium (20–30 dự án)": (20, 30),
            "Large (50+ dự án)":    (50, 70),
        }

        if st.button("🎲 Sinh dữ liệu ngẫu nhiên", use_container_width=True):
            lo, hi = size_map[size_option]
            n      = random.randint(lo, hi)
            rows   = [
                {
                    "Chọn":              False,
                    "Tên dự án":         f"Dự án {i:02d}",
                    "Lợi nhuận (đồng)":  random.randint(50_000_000, 500_000_000),
                    "Chi phí (đồng)":    random.randint(20_000_000, int(budget * 0.35)),
                }
                for i in range(1, n + 1)
            ]
            st.session_state["df_projects"]  = pd.DataFrame(rows)
            st.session_state["result_stale"] = True
            st.success(f"✅ Đã sinh {n} dự án ngẫu nhiên!")

    # ── TAB 2: Tải file CSV ───────────────────────────────────────────────────
    with tab_csv:
        st.caption("File CSV cần có các cột: `ten_du_an`, `loi_nhuan`, `chi_phi`")
        uploaded = st.file_uploader("Chọn file CSV", type=["csv"], label_visibility="collapsed")

        if uploaded:
            file_bytes = uploaded.getvalue()

            # Chỉ đọc lại nếu đây là file mới (tránh rerun gây đọc lặp)
            if st.session_state.get("last_uploaded_bytes") != file_bytes:
                try:
                    df_raw       = pd.read_csv(uploaded, sep=None, engine="python", encoding="utf-8-sig")
                    required_cols = {"ten_du_an", "loi_nhuan", "chi_phi"}
                    missing       = required_cols - set(df_raw.columns.str.lower().str.strip())

                    if missing:
                        st.error(
                            f"❌ File CSV thiếu cột: **{', '.join(missing)}**\n\n"
                            "Vui lòng kiểm tra lại định dạng file."
                        )
                    else:
                        df_raw.columns = df_raw.columns.str.lower().str.strip()
                        rows = []
                        for _, r in df_raw.iterrows():
                            try:
                                rows.append({
                                    "Chọn":              False,
                                    "Tên dự án":         str(r["ten_du_an"]),
                                    "Lợi nhuận (đồng)":  int(float(r["loi_nhuan"])),
                                    "Chi phí (đồng)":    int(float(r["chi_phi"])),
                                })
                            except (ValueError, KeyError):
                                continue

                        if not rows:
                            st.error("❌ Không đọc được dòng dữ liệu hợp lệ nào.")
                        else:
                            st.session_state["df_projects"]       = pd.DataFrame(rows)
                            st.session_state["result_stale"]      = True
                            st.session_state["last_uploaded_bytes"] = file_bytes
                            st.success(f"✅ Đã tải {len(rows)} dự án từ CSV!")

                except Exception as e:
                    st.error(f"❌ Lỗi đọc file: {e}")

    # ── TAB 3: Thêm dự án thủ công ───────────────────────────────────────────
    with tab_manual:
        with st.form("form_add_project", clear_on_submit=True):
            proj_name   = st.text_input("Tên dự án", placeholder="VD: Dự án Xanh")
            proj_profit = st.number_input(
                "Lợi nhuận kỳ vọng (đồng)",
                min_value=0, value=100_000_000, step=10_000_000, format="%d",
            )
            proj_cost = st.number_input(
                "Chi phí đầu tư (đồng)",
                min_value=0, value=50_000_000, step=10_000_000, format="%d",
            )
            submitted = st.form_submit_button("➕ Thêm dự án", use_container_width=True)

        if submitted:
            if not proj_name.strip():
                st.warning("⚠️ Vui lòng nhập tên dự án.")
            elif proj_cost <= 0:
                st.warning("⚠️ Chi phí phải lớn hơn 0.")
            else:
                new_row = pd.DataFrame([{
                    "Chọn":              False,
                    "Tên dự án":         proj_name.strip(),
                    "Lợi nhuận (đồng)":  int(proj_profit),
                    "Chi phí (đồng)":    int(proj_cost),
                }])
                st.session_state["df_projects"] = pd.concat(
                    [st.session_state["df_projects"], new_row], ignore_index=True
                )
                st.session_state["result_stale"] = True
                st.success(f"✅ Đã thêm **{proj_name.strip()}**!")


# ─────────────────────────────────────────────────────────────────────────────
# CỘT 2 — QUẢN LÝ DỮ LIỆU + NÚT CHẠY
# ─────────────────────────────────────────────────────────────────────────────
with col_data:
    st.markdown("<h3 class='section-title'>📋 Danh sách dự án</h3>", unsafe_allow_html=True)

    df         = st.session_state["df_projects"]
    n_projects = len(df)

    # ── Trường hợp chưa có dự án ──────────────────────────────────────────────
    if n_projects == 0:
        st.markdown(
            "<div class='info-box'>📭 Chưa có dự án nào. "
            "Hãy sinh tự động, tải CSV hoặc thêm thủ công ở cột bên trái.</div>",
            unsafe_allow_html=True,
        )
    else:
        st.caption(f"Tổng: **{n_projects}** dự án · Backtracking giới hạn: **{bt_limit}** dự án")

        # Đảm bảo cột Chọn tồn tại (phòng tải CSV thiếu cột này)
        if "Chọn" not in df.columns:
            df.insert(0, "Chọn", False)

        # ── Bảng dữ liệu có thể chỉnh sửa ────────────────────────────────────
        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            column_config={
                "Chọn":              st.column_config.CheckboxColumn("☑", width="small"),
                "Tên dự án":         st.column_config.TextColumn("Tên dự án", width="medium"),
                "Lợi nhuận (đồng)":  st.column_config.NumberColumn("Lợi nhuận (đ)", format="%d", width="medium"),
                "Chi phí (đồng)":    st.column_config.NumberColumn("Chi phí (đ)",   format="%d", width="medium"),
            },
            height=min(400, 80 + n_projects * 35),
            key="data_editor_main",
        )

        # ── Phát hiện thay đổi dữ liệu → đánh dấu stale ─────────────────────
        # Không lưu edited_df ngay — chỉ đọc để so hash, giữ delta nội bộ của data_editor.
        old_hash = st.session_state.get("last_data_hash")
        new_hash = df_hash(edited_df.drop(columns=["Chọn"], errors="ignore"))
        if old_hash and old_hash != new_hash and (
            st.session_state["cso_result"] or st.session_state["bt_result"]
        ):
            st.session_state["result_stale"] = True

        # ── Nút thao tác: Xóa đã chọn / Xóa tất cả ──────────────────────────
        btn_del, btn_clear = st.columns(2)

        with btn_del:
            if st.button("🗑️ Xóa đã chọn", use_container_width=True):
                mask  = edited_df["Chọn"] == True
                n_del = int(mask.sum())
                if n_del == 0:
                    st.warning("Chưa chọn dự án nào để xóa.")
                else:
                    new_df = edited_df[~mask].reset_index(drop=True)
                    new_df["Chọn"] = False
                    st.session_state["df_projects"]  = new_df
                    st.session_state["result_stale"] = True
                    st.rerun()

        with btn_clear:
            if st.button("🗑️ Xóa tất cả", use_container_width=True, type="secondary"):
                st.session_state["df_projects"]  = pd.DataFrame(
                    columns=["Chọn", "Tên dự án", "Lợi nhuận (đồng)", "Chi phí (đồng)"]
                )
                st.session_state["cso_result"]   = None
                st.session_state["bt_result"]    = None
                st.session_state["result_stale"] = False
                st.rerun()

        # ── Cảnh báo nếu n vượt giới hạn BT ──────────────────────────────────
        st.markdown("---")
        if n_projects > bt_limit:
            st.markdown(
                f"<div class='warn-box'>⚠️ Backtracking sẽ <b>bị bỏ qua</b> vì "
                f"n={n_projects} > giới hạn {bt_limit}. CSO vẫn chạy bình thường.</div>",
                unsafe_allow_html=True,
            )

        # ── Nút chạy thuật toán ───────────────────────────────────────────────
        run_btn = st.button(
            "🚀 Chạy so sánh thuật toán",
            use_container_width=True,
            type="primary",
            disabled=(n_projects == 0),
        )
        if n_projects == 0:
            st.caption("⬆️ Thêm dữ liệu để kích hoạt")

    # ── Xử lý khi người dùng nhấn nút chạy ───────────────────────────────────
    if n_projects > 0 and "run_btn" in dir() and run_btn:
        # Commit toàn bộ edited_df (kể cả mọi chỉnh sửa inline) làm nguồn chạy
        st.session_state["df_projects"] = edited_df
        df_run  = edited_df
        profits = df_run["Lợi nhuận (đồng)"].tolist()
        costs   = df_run["Chi phí (đồng)"].tolist()

        # ── Chạy CSO (luôn luôn) ──────────────────────────────────────────────
        with st.spinner("🐱 Đang chạy CSO..."):
            cso_algo = BinaryCSOKnapsack(n_cats=n_cats, max_iter=max_iter, MR=MR, SMP=SMP)
            st.session_state["cso_result"] = cso_algo.solve(profits, costs, int(budget))

        # ── Chạy Backtracking (chỉ khi n ≤ bt_limit) ─────────────────────────
        if n_projects <= bt_limit:
            with st.spinner("🔁 Đang chạy Backtracking (vét cạn)..."):
                bt_algo = BacktrackingKnapsack()
                st.session_state["bt_result"] = bt_algo.solve(profits, costs, int(budget))
        else:
            st.session_state["bt_result"] = None

        # Lưu hash hiện tại → kết quả khớp với dữ liệu
        st.session_state["last_data_hash"] = df_hash(
            df_run.drop(columns=["Chọn"], errors="ignore")
        )
        st.session_state["result_stale"] = False
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
# CỘT 3 — KẾT QUẢ & BÁO CÁO SO SÁNH
# ─────────────────────────────────────────────────────────────────────────────
with col_result:
    st.markdown("<h3 class='section-title'>📊 Kết quả & Báo cáo so sánh</h3>", unsafe_allow_html=True)

    cso_res = st.session_state.get("cso_result")
    bt_res  = st.session_state.get("bt_result")
    stale   = st.session_state.get("result_stale", False)

    # ── Trạng thái: dữ liệu thay đổi chưa chạy lại ───────────────────────────
    if stale and (cso_res or bt_res):
        st.markdown(
            "<div class='stale-banner'>"
            "⚠️ Dữ liệu đã thay đổi — kết quả bên dưới không còn chính xác.<br>"
            "Hãy nhấn <b>🚀 Chạy so sánh thuật toán</b> để cập nhật."
            "</div>",
            unsafe_allow_html=True,
        )

    # ── Trạng thái: chưa có kết quả nào ──────────────────────────────────────
    elif not cso_res and not bt_res:
        st.markdown(
            "<div class='info-box'>"
            "📌 Chưa có kết quả. Hãy nhập dữ liệu và nhấn "
            "<b>🚀 Chạy so sánh thuật toán</b>."
            "</div>",
            unsafe_allow_html=True,
        )

    # ── Hiển thị kết quả khi có và dữ liệu vẫn còn hợp lệ ───────────────────
    if (cso_res or bt_res) and not stale:
        df_disp = st.session_state["df_projects"]
        n_total = len(df_disp)

        # ════════════════════════════════════════════════════════════════════
        # A. KẾT QUẢ CSO
        # ════════════════════════════════════════════════════════════════════
        if cso_res:
            st.markdown("#### 🐱 Cat Swarm Optimization (CSO)")
            n_sel_cso = sum(cso_res["solution"])

            st.markdown("<div class='metric-cso'>", unsafe_allow_html=True)
            m1, m2 = st.columns(2)
            m1.metric("💰 Lợi nhuận", fmt_money(cso_res["profit"]))
            m2.metric("💸 Chi phí",   fmt_money(cso_res["cost"]))
            m3, m4 = st.columns(2)
            m3.metric("⏱️ Thời gian", f"{cso_res['time']:.2f}s")
            m4.metric("🧠 Memory",    fmt_mem(cso_res["memory"]))
            st.markdown("</div>", unsafe_allow_html=True)

            st.caption(f"📌 Chọn **{n_sel_cso}/{n_total}** dự án")

            if n_sel_cso > 0:
                idx_cso      = [i for i, s in enumerate(cso_res["solution"]) if s == 1]
                df_cso_detail = df_disp.iloc[idx_cso][
                    ["Tên dự án", "Lợi nhuận (đồng)", "Chi phí (đồng)"]
                ].reset_index(drop=True)
                with st.expander(f"📋 Chi tiết {n_sel_cso} dự án (CSO)", expanded=False):
                    st.dataframe(df_cso_detail, use_container_width=True, hide_index=True)

        st.markdown("---")

        # ════════════════════════════════════════════════════════════════════
        # B. KẾT QUẢ BACKTRACKING
        # ════════════════════════════════════════════════════════════════════
        if bt_res:
            st.markdown("#### 🔁 Backtracking (Vét cạn)")
            n_sel_bt = sum(bt_res["solution"])

            st.markdown("<div class='metric-bt'>", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            b1.metric("💰 Lợi nhuận", fmt_money(bt_res["profit"]))
            b2.metric("💸 Chi phí",   fmt_money(bt_res["cost"]))
            b3, b4 = st.columns(2)
            b3.metric("⏱️ Thời gian", f"{bt_res['time']:.2f}s")
            b4.metric("🧠 Memory",    fmt_mem(bt_res["memory"]))
            st.markdown("</div>", unsafe_allow_html=True)

            st.caption(f"📌 Chọn **{n_sel_bt}/{n_total}** dự án · Nghiệm tối ưu chính xác 100%")

            if n_sel_bt > 0:
                idx_bt       = [i for i, s in enumerate(bt_res["solution"]) if s == 1]
                df_bt_detail  = df_disp.iloc[idx_bt][
                    ["Tên dự án", "Lợi nhuận (đồng)", "Chi phí (đồng)"]
                ].reset_index(drop=True)
                with st.expander(f"📋 Chi tiết {n_sel_bt} dự án (Backtracking)", expanded=False):
                    st.dataframe(df_bt_detail, use_container_width=True, hide_index=True)

        # BT bị bỏ qua do vượt giới hạn
        elif cso_res and not bt_res:
            st.markdown("#### 🔁 Backtracking")
            st.markdown(
                f"<div class='warn-box'>"
                f"⛔ Backtracking không chạy vì số dự án (<b>{n_total}</b>) "
                f"vượt giới hạn (<b>{bt_limit}</b>).<br>"
                f"Độ phức tạp O(2<sup>{n_total}</sup>) có thể gây treo hệ thống."
                f"</div>",
                unsafe_allow_html=True,
            )

        # ════════════════════════════════════════════════════════════════════
        # C. BẢNG SO SÁNH TỔNG HỢP (chỉ khi cả 2 cùng chạy)
        # ════════════════════════════════════════════════════════════════════
        if cso_res and bt_res:
            st.markdown("---")
            st.markdown("#### 📊 Bảng so sánh tổng hợp")

            faster   = "CSO" if cso_res["time"]   < bt_res["time"]   else "Backtracking"
            mem_less = "CSO" if cso_res["memory"] < bt_res["memory"] else "Backtracking"
            gap_pct  = (
                abs(cso_res["profit"] - bt_res["profit"]) / bt_res["profit"] * 100
                if bt_res["profit"] > 0 else 0.0
            )

            df_compare = pd.DataFrame({
                "Tiêu chí": [
                    "Lợi nhuận tìm được",
                    "Chi phí sử dụng",
                    "Thời gian chạy",
                    "Bộ nhớ sử dụng",
                    "Số dự án chọn",
                    "Loại nghiệm",
                ],
                "CSO 🐱": [
                    fmt_money(cso_res["profit"]),
                    fmt_money(cso_res["cost"]),
                    f"{cso_res['time']:.2f}s",
                    fmt_mem(cso_res["memory"]),
                    f"{sum(cso_res['solution'])}/{n_total}",
                    "Xấp xỉ (heuristic)",
                ],
                "Backtracking 🔁": [
                    fmt_money(bt_res["profit"]),
                    fmt_money(bt_res["cost"]),
                    f"{bt_res['time']:.2f}s",
                    fmt_mem(bt_res["memory"]),
                    f"{sum(bt_res['solution'])}/{n_total}",
                    "Chính xác (exact)",
                ],
            })
            st.dataframe(df_compare, use_container_width=True, hide_index=True)

            st.markdown(
                f"<div class='info-box'>"
                f"🏎️ <b>{faster}</b> chạy nhanh hơn · "
                f"💾 <b>{mem_less}</b> ít bộ nhớ hơn · "
                f"📉 Độ lệch lợi nhuận CSO so với tối ưu: <b>{gap_pct:.2f}%</b>"
                f"</div>",
                unsafe_allow_html=True,
            )

        # ════════════════════════════════════════════════════════════════════
        # D. XUẤT BÁO CÁO CSV
        # ════════════════════════════════════════════════════════════════════
        st.markdown("---")
        st.markdown("#### 💾 Xuất báo cáo")

        export_rows = []
        if cso_res:
            export_rows.append({
                "Thuật toán":       "CSO",
                "Lợi nhuận (đồng)": cso_res["profit"],
                "Chi phí (đồng)":   cso_res["cost"],
                "Thời gian (s)":    round(cso_res["time"], 6),
                "Bộ nhớ (KB)":      round(cso_res["memory"], 2),
                "Số dự án chọn":    sum(cso_res["solution"]),
                "Tổng dự án":       n_total,
            })
        if bt_res:
            export_rows.append({
                "Thuật toán":       "Backtracking",
                "Lợi nhuận (đồng)": bt_res["profit"],
                "Chi phí (đồng)":   bt_res["cost"],
                "Thời gian (s)":    round(bt_res["time"], 6),
                "Bộ nhớ (KB)":      round(bt_res["memory"], 2),
                "Số dự án chọn":    sum(bt_res["solution"]),
                "Tổng dự án":       n_total,
            })

        if export_rows:
            csv_bytes = pd.DataFrame(export_rows).to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                label="📥 Tải báo cáo CSV",
                data=csv_bytes,
                file_name="bao_cao_so_sanh_thuat_toan.csv",
                mime="text/csv",
                use_container_width=True,
            )


# ═════════════════════════════════════════════════════════════════════════════
# 4. FOOTER
# ═════════════════════════════════════════════════════════════════════════════
st.divider()
st.markdown(
    "<div style='text-align:center; color:#94a3b8; font-size:0.78rem;'>"
    "💼 Tối Ưu Đầu Tư · Đồ án Phân tích Thuật toán · "
    "CSO (Metaheuristic) vs Backtracking (Exact) · "
    "Built with Streamlit 🚀"
    "</div>",
    unsafe_allow_html=True,
)
