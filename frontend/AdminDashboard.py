import streamlit as st
import pandas as pd
import plotly.graph_objects as go

try:
    from frontend.components.cards import render_banner
    from frontend.services.admin_service import (
        get_admin_dashboard_stats,
        get_all_users,
        update_user_by_admin,
        delete_user_by_admin,
        get_admin_activity_logs,
        get_pending_loan_requests,
        approve_loan_request,
        reject_loan_request
    )
except ModuleNotFoundError:
    from components.cards import render_banner
    from services.admin_service import (
        get_admin_dashboard_stats,
        get_all_users,
        update_user_by_admin,
        delete_user_by_admin,
        get_admin_activity_logs,
        get_pending_loan_requests,
        approve_loan_request,
        reject_loan_request
    )


def render():
    user = st.session_state.get("user")
    role_session = (st.session_state.get("role") or (user.get("role") if user else "") or "").lower()

    # Strict Role Guard: Only admins can view AdminDashboard
    if role_session != "admin" and user and user.get("role") != "admin":
        st.error("🛡️ Access Denied: Administrator privileges required to view this page.")
        if st.button("🔑 Sign In as Admin", key="admin_guard_login_btn", use_container_width=True):
            st.session_state["current_page"] = "Login"
            st.rerun()
        return

    is_dark = st.session_state.get("theme", "light") == "dark"
    card_bg = "#161F2E" if is_dark else "#FFFFFF"
    border_c = "#233148" if is_dark else "#CBD5E1"
    text_color = "#FFFFFF" if is_dark else "#0F172A"
    sub_color = "#94A3B8" if is_dark else "#475569"

    # Header Banner
    render_banner(
        title="Admin Control Operations & Diagnostics",
        subtitle="Real-time MongoDB Atlas analytics, user management, loan request approvals, and activity trends.",
        icon="🛡️"
    )

    # Fetch Real MongoDB Data via admin service
    _, dash_data, _ = get_admin_dashboard_stats()
    _, users_list, _ = get_all_users()
    _, activity_logs, _ = get_admin_activity_logs()
    _, pending_requests, _ = get_pending_loan_requests()

    total_users = dash_data.get("totalUsers", len(users_list))
    active_users = dash_data.get("activeUsers", len([u for u in users_list if u.get("isActive", True)]))
    pending_cnt = dash_data.get("pendingCount", len(pending_requests))
    inactive_users = dash_data.get("inactiveUsers", total_users - active_users)
    locked_users = dash_data.get("userStatusBreakdown", {}).get("Locked", 0)

    # Tabs for Admin Workflow
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Dashboard Overview",
        "👥 User Management",
        "📋 Loan Requests",
        "📜 Activity & System Logs"
    ])

    # TAB 1: Dashboard Overview (Matching Image 1 layout)
    with tab1:
        g1, g2 = st.columns([1, 1.3], gap="medium")

        # Donut Chart - User Base Overview
        with g1:
            st.markdown(
                f"""
                <div style="background:{card_bg};border:1.5px solid {border_c};border-radius:14px;padding:18px 22px;height:100%;">
                    <div style="font-size:0.95rem;font-weight:800;letter-spacing:0.05em;color:{text_color} !important;margin-bottom:12px;">
                        USER BASE OVERVIEW
                    </div>
                """,
                unsafe_allow_html=True
            )

            if total_users > 0:
                fig_donut = go.Figure(data=[go.Pie(
                    labels=["Active", "Pending Request", "Inactive", "Locked"],
                    values=[active_users, pending_cnt, inactive_users, locked_users],
                    hole=0.6,
                    marker_colors=["#2563EB", "#EAB308", "#64748B", "#EF4444"],
                    textinfo="value",
                    textfont=dict(size=13, color="#FFFFFF"),
                )])
                fig_donut.update_layout(
                    annotations=[dict(text=f"<b>Total Users:</b><br>{total_users:,}", x=0.5, y=0.5, font_size=15, font_color=text_color, showarrow=False)],
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=text_color),
                    showlegend=True,
                    height=260,
                    margin=dict(l=10, r=10, t=10, b=10),
                )
                st.plotly_chart(fig_donut, use_container_width=True)
            else:
                st.info("No users found.")

            st.markdown("</div>", unsafe_allow_html=True)

        # Line Chart - User Activity Trends (Last 30 Days)
        with g2:
            st.markdown(
                f"""
                <div style="background:{card_bg};border:1.5px solid {border_c};border-radius:14px;padding:18px 22px;height:100%;">
                    <div style="font-size:0.95rem;font-weight:800;letter-spacing:0.05em;color:{text_color} !important;margin-bottom:12px;">
                        USER ACTIVITY TRENDS (Last 30 Days)
                    </div>
                """,
                unsafe_allow_html=True
            )

            daily_trends = dash_data.get("dailyTrends", [])
            if daily_trends:
                df_trends = pd.DataFrame(daily_trends)
                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(x=df_trends["date"], y=df_trends["logins"], mode="lines", name="Daily Logins", line=dict(color="#3B82F6", width=2.5)))
                fig_line.add_trace(go.Scatter(x=df_trends["date"], y=df_trends["applications"], mode="lines", name="Loan Applications", line=dict(color="#10B981", width=2.5)))
                fig_line.add_trace(go.Scatter(x=df_trends["date"], y=df_trends["logs"], mode="lines", name="System Logs", line=dict(color="#94A3B8", width=2)))

                fig_line.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color=text_color),
                    height=260,
                    margin=dict(l=10, r=10, t=10, b=30),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                )
                st.plotly_chart(fig_line, use_container_width=True)
            else:
                st.info("No activity trends data available.")

            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Admin Watchlist & Pending Actions
        m1, m2 = st.columns([0.8, 1.5], gap="medium")
        with m1:
            st.markdown(
                f"""
                <div style="background:{card_bg};border:1.5px solid {border_c};border-radius:14px;padding:20px;">
                    <div style="font-size:1rem;font-weight:800;color:{text_color} !important;margin-bottom:8px;">Loan Management</div>
                    <div style="font-size:0.85rem;color:{sub_color} !important;">Credit Assessment Module</div>
                    <div style="font-size:0.85rem;color:{sub_color} !important;margin-bottom:12px;">Active Model: <b>Gradient Boosting</b></div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button("Assess Credit Risk", key="overview_assess_risk_btn", use_container_width=True):
                st.session_state["current_page"] = "LoanPrediction"
                st.rerun()

        with m2:
            st.markdown(
                f"""
                <div style="background:{card_bg};border:1.5px solid {border_c};border-radius:14px;padding:18px 22px;">
                    <div style="font-size:0.95rem;font-weight:800;color:{text_color} !important;margin-bottom:12px;">
                        ADMIN WATCHLIST: RECENT USER ACTIVITIES
                    </div>
                """,
                unsafe_allow_html=True
            )
            if activity_logs:
                act_df = pd.DataFrame([
                    {
                        "User": log.get("user", "User"),
                        "Activity Type": log.get("activityType", "Activity"),
                        "Timestamp": str(log.get("timestamp", ""))[:16],
                        "Details": str(log.get("details", ""))[:30]
                    }
                    for log in activity_logs[:5]
                ])
                st.dataframe(act_df, use_container_width=True, height=180)
            else:
                st.info("No user activity found.")
            st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: User Management
    with tab2:
        st.markdown(f"<h3 style='color:{text_color} !important;'>👥 System Users Directory</h3>", unsafe_allow_html=True)

        if not users_list:
            st.info("No users found.")
        else:
            u_col1, u_col2 = st.columns([1, 2])
            with u_col1:
                role_filter = st.selectbox("Filter Role", ["All Roles", "user", "admin"])
            with u_col2:
                search_user = st.text_input("Search Users by Name or Email", "")

            filtered_users = users_list
            if role_filter != "All Roles":
                filtered_users = [u for u in filtered_users if u.get("role") == role_filter]
            if search_user:
                q = search_user.lower()
                filtered_users = [u for u in filtered_users if q in str(u.get("name", "")).lower() or q in str(u.get("email", "")).lower()]

            u_rows = []
            for u in filtered_users:
                u_rows.append({
                    "User ID": str(u.get("id") or u.get("_id")),
                    "Name": u.get("name", "N/A"),
                    "Email": u.get("email", "N/A"),
                    "Role": u.get("role", "user"),
                    "Status": "🟢 Active" if u.get("isActive", True) else "🔴 Disabled",
                    "Joined": str(u.get("createdAt", ""))[:10]
                })

            st.dataframe(pd.DataFrame(u_rows), use_container_width=True)

            st.markdown("---")
            st.markdown(f"<h4 style='color:{text_color} !important;'>⚙️ Manage Selected User</h4>", unsafe_allow_html=True)

            user_options = {f"{u.get('name')} ({u.get('email')})": str(u.get('id') or u.get('_id')) for u in filtered_users}
            if user_options:
                selected_label = st.selectbox("Select User to Manage", list(user_options.keys()))
                sel_user_id = user_options[selected_label]
                sel_user_obj = next((u for u in filtered_users if str(u.get('id') or u.get('_id')) == sel_user_id), {})

                a_col1, a_col2, a_col3, a_col4 = st.columns(4)
                with a_col1:
                    new_role = st.selectbox("Change Role", ["user", "admin"], index=0 if sel_user_obj.get("role") == "user" else 1, key=f"role_{sel_user_id}")
                    if st.button("Save Role", key=f"btn_role_{sel_user_id}", use_container_width=True):
                        ok, res, err = update_user_by_admin(sel_user_id, {"role": new_role})
                        if ok: st.toast("✅ Role updated!", icon="✅"); st.rerun()
                        else: st.error(f"Error: {err}")

                with a_col2:
                    current_active = sel_user_obj.get("isActive", True)
                    target_active = not current_active
                    btn_label = "Disable Account 🔴" if current_active else "Enable Account 🟢"
                    if st.button(btn_label, key=f"btn_act_{sel_user_id}", use_container_width=True):
                        ok, res, err = update_user_by_admin(sel_user_id, {"isActive": target_active})
                        if ok: st.toast("✅ User status updated!", icon="✅"); st.rerun()
                        else: st.error(f"Error: {err}")

                with a_col3:
                    reset_pass = st.text_input("New Password", type="password", key=f"pass_{sel_user_id}", placeholder="Reset password")
                    if st.button("Reset Password", key=f"btn_pass_{sel_user_id}", use_container_width=True):
                        if reset_pass:
                            ok, res, err = update_user_by_admin(sel_user_id, {"password": reset_pass})
                            if ok: st.toast("✅ Password reset successfully!", icon="🔑"); st.rerun()
                            else: st.error(f"Error: {err}")
                        else:
                            st.warning("Please enter a new password.")

                with a_col4:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("Delete User 🗑️", key=f"btn_del_{sel_user_id}", use_container_width=True):
                        ok, res, err = delete_user_by_admin(sel_user_id)
                        if ok: st.toast("🗑️ User deleted!", icon="🗑️"); st.rerun()
                        else: st.error(f"Error: {err}")

    # TAB 3: Loan Requests
    with tab3:
        st.markdown(f"<h3 style='color:{text_color} !important;'>📋 Pending Loan Requests</h3>", unsafe_allow_html=True)

        if not pending_requests:
            st.info("No pending loan requests.")
        else:
            for req in pending_requests:
                req_id = req.get("id") or req.get("_id")
                applicant = req.get("user", "Applicant")
                l_type = req.get("loanType", "Personal Loan")
                amt = req.get("amount", 0)
                dt_str = str(req.get("date", ""))[:16]

                r1, r2, r3, r4 = st.columns([1.5, 2, 2, 2])
                with r1: st.markdown(f"**Request #{str(req_id)[-4:]}**")
                with r2: st.markdown(f"👤 **{applicant}** ({l_type})")
                with r3: st.markdown(f"Amount: **₹{float(amt):,.0f}** | Date: {dt_str}")
                with r4:
                    b1, b2 = st.columns(2)
                    with b1:
                        if st.button("Approve ✅", key=f"tab3_app_{req_id}", use_container_width=True):
                            ok, res, err = approve_loan_request(req_id)
                            if ok: st.toast("✅ Loan Approved!", icon="✅"); st.rerun()
                            else: st.error(f"Error: {err}")
                    with b2:
                        if st.button("Reject ❌", key=f"tab3_rej_{req_id}", use_container_width=True):
                            ok, res, err = reject_loan_request(req_id)
                            if ok: st.toast("❌ Loan Rejected.", icon="❌"); st.rerun()
                            else: st.error(f"Error: {err}")
                st.markdown("---")

    # TAB 4: Activity & System Logs
    with tab4:
        st.markdown(f"<h3 style='color:{text_color} !important;'>📜 Audit & Activity Trail</h3>", unsafe_allow_html=True)
        if activity_logs:
            log_df = pd.DataFrame([
                {
                    "Log ID": str(log.get("id") or log.get("_id")),
                    "User": log.get("user", "System"),
                    "Action / Event": log.get("activityType", "Activity"),
                    "Loan Type": log.get("loanType", "N/A"),
                    "Details": str(log.get("details", "")),
                    "Timestamp": str(log.get("timestamp", ""))[:19]
                }
                for log in activity_logs
            ])
            st.dataframe(log_df, use_container_width=True)
        else:
            st.info("No activity logs recorded yet.")
