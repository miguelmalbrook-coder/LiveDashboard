import streamlit as st
import gspread
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from google.oauth2.service_account import Credentials

def load_data():
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)
    client = gspread.authorize(creds)

    spreadsheet = client.open("Bank Statement")
    sheet = spreadsheet.worksheet("Transactions")

    data = sheet.get_all_values()
    if not data or len(data) < 2:
        return pd.DataFrame()

    df = pd.DataFrame(data[1:], columns=data[0])
    return df

def clean_direction(series: pd.Series) -> pd.Series:
    return (
        series.astype(str)
        .str.replace("\xa0", " ", regex=False)
        .str.strip()
        .str.upper()
    )

def clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(",", "", regex=False).str.strip(),
        errors="coerce"
    )

st.set_page_config(
    page_title="Personal Finance Tracker",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    html {
        scroll-behavior: smooth;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(34,197,94,0.08), transparent 22%),
            radial-gradient(circle at 90% 10%, rgba(59,130,246,0.10), transparent 24%),
            radial-gradient(circle at 50% 100%, rgba(168,85,247,0.10), transparent 25%),
            linear-gradient(180deg, #08111f 0%, #0f172a 45%, #111827 100%);
        color: #f8fafc;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        color: #f8fafc !important;
        letter-spacing: 0.2px;
    }

    .hero {
        padding: 1.3rem 1.5rem;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(34,197,94,0.17), rgba(59,130,246,0.16), rgba(168,85,247,0.14));
        border: 1px solid rgba(255,255,255,0.10);
        box-shadow: 0 14px 40px rgba(0,0,0,0.28);
        animation: fadeUp 0.8s ease-out;
        margin-bottom: 1rem;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }

    .hero-sub {
        color: #cbd5e1;
        font-size: 0.98rem;
    }

    .jumpbar {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 1rem 0 1.2rem 0;
    }

    .jumpbar a {
        text-decoration: none;
        color: white;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
        padding: 10px 14px;
        border-radius: 999px;
        font-size: 0.92rem;
        transition: all 0.25s ease;
    }

    .jumpbar a:hover {
        background: linear-gradient(135deg, rgba(34,197,94,0.25), rgba(59,130,246,0.25));
        transform: translateY(-2px);
    }

    .glass {
        background: rgba(255,255,255,0.055);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 22px;
        padding: 1rem 1rem 0.7rem 1rem;
        box-shadow: 0 12px 30px rgba(0,0,0,0.22);
        animation: fadeUp 0.8s ease-out;
    }

    .section-anchor {
        position: relative;
        top: -10px;
    }

    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.55rem;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(255,255,255,0.09), rgba(255,255,255,0.045));
        border: 1px solid rgba(255,255,255,0.10);
        padding: 18px 16px;
        border-radius: 18px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.18);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 16px 35px rgba(0,0,0,0.28);
    }

    div[data-testid="stMetricLabel"] {
        color: #cbd5e1 !important;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
    }

    div[data-testid="stMetricDelta"] {
        color: #86efac !important;
    }

    div[data-testid="stExpander"] {
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.08);
        overflow: hidden;
    }

    .recent-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.07), rgba(255,255,255,0.04));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 14px 16px;
        margin-bottom: 10px;
        box-shadow: 0 8px 22px rgba(0,0,0,0.18);
    }

    .recent-top {
        display: flex;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
    }

    .recent-merchant {
        font-weight: 700;
        color: #f8fafc;
    }

    .recent-meta {
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-top: 4px;
    }

    .recent-amount-in {
        color: #86efac;
        font-weight: 800;
        font-size: 1.02rem;
    }

    .recent-amount-out {
        color: #fca5a5;
        font-weight: 800;
        font-size: 1.02rem;
    }

    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(12px); }
        to   { opacity: 1; transform: translateY(0px); }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <div class="hero-title">📊 Personal Finance Dashboard</div>
    <div class="hero-sub">
        Live spending, balance, merchant behaviour, and category trends from your synced bank sheet.
    </div>
</div>

<div class="jumpbar">
    <a href="#overview">Overview</a>
    <a href="#merchants">Merchants</a>
    <a href="#categories">Categories</a>
    <a href="#recent">Recent</a>
    <a href="#all-transactions">All Transactions</a>
</div>
""", unsafe_allow_html=True)

try:
    df = load_data()

    if df.empty:
        st.warning("The 'Transactions' tab is empty.")
    else:
        df.columns = df.columns.str.strip().str.lower()

        required_cols = ["txn_date", "amount", "direction", "merchant", "balance_after", "category"]
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            st.error(f"Missing required columns: {missing_cols}")
            st.stop()

        df["amount"] = clean_numeric(df["amount"])
        df["balance_after"] = clean_numeric(df["balance_after"])
        df["txn_date"] = pd.to_datetime(df["txn_date"], errors="coerce")
        df["direction"] = clean_direction(df["direction"])
        df["merchant"] = df["merchant"].astype(str).str.strip()
        df["category"] = df["category"].astype(str).str.strip()

        df = df.dropna(subset=["txn_date", "amount"]).copy()
        df = df.sort_values(by="txn_date").reset_index(drop=True)

        expenses = df[df["direction"] == "OUT"].copy()
        income = df[df["direction"] == "IN"].copy()

        total_income = income["amount"].sum()
        total_expense = expenses["amount"].sum()

        balance_series = df["balance_after"].dropna()
        current_balance = balance_series.iloc[-1] if not balance_series.empty else 0

        # ---------- METRICS ----------
        st.markdown('<div id="overview" class="section-anchor"></div>', unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Income (IN)", f"SCR {total_income:,.2f}")
        m2.metric("Total Expenses (OUT)", f"SCR {total_expense:,.2f}")
        m3.metric(
            "Current Bank Balance",
            f"SCR {current_balance:,.2f}",
            delta=f"{total_income - total_expense:,.2f}"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------- BALANCE + INCOME ----------
        left, right = st.columns([1.45, 1])

        with left:
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📈 Account Balance Over Time</div>', unsafe_allow_html=True)

            balance_plot_df = df.dropna(subset=["balance_after"]).copy()

            if not balance_plot_df.empty:
                fig_balance = go.Figure()

                fig_balance.add_trace(
                    go.Scatter(
                        x=balance_plot_df["txn_date"],
                        y=balance_plot_df["balance_after"],
                        mode="lines+markers",
                        name="Balance",
                        line=dict(color="#60a5fa", width=4, shape="spline", smoothing=1.2),
                        marker=dict(size=7, color="#93c5fd"),
                        fill="tozeroy",
                        fillcolor="rgba(96,165,250,0.16)",
                        hovertemplate="<b>%{x}</b><br>Balance: SCR %{y:,.2f}<extra></extra>"
                    )
                )

                fig_balance.add_trace(
                    go.Scatter(
                        x=balance_plot_df["txn_date"],
                        y=balance_plot_df["balance_after"],
                        mode="lines",
                        line=dict(color="rgba(34,197,94,0.22)", width=10, shape="spline", smoothing=1.2),
                        hoverinfo="skip",
                        showlegend=False
                    )
                )

                fig_balance.update_layout(
                    template="plotly_dark",
                    height=500,
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor="rgba(8,15,30,0.45)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#f8fafc"),
                    hovermode="x unified",
                    transition_duration=900,
                    legend=dict(orientation="h", y=1.05, x=0.01),
                    xaxis=dict(
                        showgrid=False,
                        zeroline=False,
                        showline=False
                    ),
                    yaxis=dict(
                        title="SCR",
                        gridcolor="rgba(255,255,255,0.08)",
                        zeroline=False
                    )
                )

                st.plotly_chart(fig_balance, use_container_width=True)
            else:
                st.info("No balance data available to plot.")
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">💰 Income Over Time</div>', unsafe_allow_html=True)

            if not income.empty:
                income_daily = income.groupby(income["txn_date"].dt.date)["amount"].sum().reset_index()
                fig_income = px.bar(
                    income_daily,
                    x="txn_date",
                    y="amount",
                    template="plotly_dark",
                    text_auto=".2s"
                )
                fig_income.update_traces(
                    marker_color="#22c55e",
                    hovertemplate="<b>%{x}</b><br>Income: SCR %{y:,.2f}<extra></extra>"
                )
                fig_income.update_layout(
                    height=500,
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor="rgba(8,15,30,0.45)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#f8fafc"),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.08)"),
                    transition_duration=900
                )
                st.plotly_chart(fig_income, use_container_width=True)
            else:
                st.info("No income rows found where direction = IN.")
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------- MERCHANTS ----------
        st.markdown('<div id="merchants" class="section-anchor"></div>', unsafe_allow_html=True)
        col_m1, col_m2 = st.columns(2)

        with col_m1:
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🏪 Top 10 Merchants by Total Spend</div>', unsafe_allow_html=True)
            if not expenses.empty:
                top_spend = (
                    expenses.groupby("merchant", dropna=False)["amount"]
                    .sum()
                    .sort_values(ascending=False)
                    .head(10)
                    .reset_index()
                    .sort_values("amount", ascending=True)
                )
                fig_spend = px.bar(
                    top_spend,
                    x="amount",
                    y="merchant",
                    orientation="h",
                    color="amount",
                    color_continuous_scale="Reds",
                    template="plotly_dark",
                    text_auto=".2s"
                )
                fig_spend.update_layout(
                    height=500,
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor="rgba(8,15,30,0.45)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#f8fafc"),
                    yaxis=dict(title=""),
                    xaxis=dict(title="SCR", gridcolor="rgba(255,255,255,0.08)"),
                    transition_duration=900
                )
                fig_spend.update_traces(
                    hovertemplate="<b>%{y}</b><br>Spend: SCR %{x:,.2f}<extra></extra>"
                )
                st.plotly_chart(fig_spend, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_m2:
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🔁 Most Frequent Merchants</div>', unsafe_allow_html=True)
            if not expenses.empty:
                top_freq = expenses["merchant"].value_counts().head(10).reset_index()
                top_freq.columns = ["merchant", "visit_count"]
                top_freq = top_freq.sort_values("visit_count", ascending=True)
                fig_freq = px.bar(
                    top_freq,
                    x="visit_count",
                    y="merchant",
                    orientation="h",
                    color="visit_count",
                    color_continuous_scale="Blues",
                    template="plotly_dark",
                    text_auto=True
                )
                fig_freq.update_layout(
                    height=500,
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor="rgba(8,15,30,0.45)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#f8fafc"),
                    yaxis=dict(title=""),
                    xaxis=dict(title="Visits", gridcolor="rgba(255,255,255,0.08)"),
                    transition_duration=900
                )
                fig_freq.update_traces(
                    hovertemplate="<b>%{y}</b><br>Visits: %{x}<extra></extra>"
                )
                st.plotly_chart(fig_freq, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------- CATEGORIES ----------
        st.markdown('<div id="categories" class="section-anchor"></div>', unsafe_allow_html=True)
        col_left, col_right = st.columns([1.35, 1])

        with col_left:
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">🥧 Expenses by Category</div>', unsafe_allow_html=True)
            if not expenses.empty:
                category_summary = expenses.groupby("category", dropna=False)["amount"].sum().reset_index()

                fig_pie = px.pie(
                    category_summary,
                    values="amount",
                    names="category",
                    hole=0.38,
                    template="plotly_dark"
                )
                fig_pie.update_traces(
                    textposition="inside",
                    textinfo="percent+label",
                    hovertemplate="<b>%{label}</b><br>SCR %{value:,.2f}<br>%{percent}<extra></extra>"
                )
                fig_pie.update_layout(
                    height=720,
                    margin=dict(l=20, r=180, t=20, b=20),
                    plot_bgcolor="rgba(8,15,30,0.45)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#f8fafc", size=14),
                    legend=dict(
                        orientation="v",
                        yanchor="top",
                        y=1,
                        xanchor="left",
                        x=1.02,
                        bgcolor="rgba(255,255,255,0.03)"
                    ),
                    transition_duration=900
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_right:
            st.markdown('<div class="glass">', unsafe_allow_html=True)
            st.markdown('<div class="section-title">📉 Daily Spending Spikes</div>', unsafe_allow_html=True)
            if not expenses.empty:
                daily = expenses.groupby(expenses["txn_date"].dt.date)["amount"].sum().reset_index()
                fig_bar = px.bar(
                    daily,
                    x="txn_date",
                    y="amount",
                    template="plotly_dark",
                    text_auto=".2s"
                )
                fig_bar.update_traces(
                    marker_color="#ef4444",
                    hovertemplate="<b>%{x}</b><br>Spent: SCR %{y:,.2f}<extra></extra>"
                )
                fig_bar.update_layout(
                    height=720,
                    margin=dict(l=10, r=10, t=20, b=10),
                    plot_bgcolor="rgba(8,15,30,0.45)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#f8fafc"),
                    xaxis=dict(showgrid=False),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.08)", title="SCR"),
                    transition_duration=900
                )
                st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------- RECENT ----------
        st.markdown('<div id="recent" class="section-anchor"></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">🕒 Last 5 Recent Transactions</div>', unsafe_allow_html=True)

        recent_df = df.sort_values("txn_date", ascending=False).head(5).copy()
        for _, row in recent_df.iterrows():
            amount_class = "recent-amount-in" if row["direction"] == "IN" else "recent-amount-out"
            sign = "+" if row["direction"] == "IN" else "-"
            st.markdown(f"""
            <div class="recent-card">
                <div class="recent-top">
                    <div>
                        <div class="recent-merchant">{row["merchant"]}</div>
                        <div class="recent-meta">
                            {row["txn_date"].strftime("%d %b %Y, %H:%M:%S")} · {row["direction"]} · {row["category"]}
                        </div>
                    </div>
                    <div class="{amount_class}">
                        {sign} SCR {row["amount"]:,.2f}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------- ALL TRANSACTIONS ----------
        st.markdown('<div id="all-transactions" class="section-anchor"></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">📋 All Transactions</div>', unsafe_allow_html=True)

        display_df = df[
            ["txn_date", "merchant", "amount", "direction", "balance_after", "category"]
        ].sort_values(by="txn_date", ascending=False)

        st.dataframe(
            display_df,
            use_container_width=True,
            height=600
        )

        st.markdown('</div>', unsafe_allow_html=True)

        with st.expander("Debug direction values"):
            st.write("Unique direction values found:")
            st.write(df["direction"].value_counts(dropna=False))

            st.write("Rows counted as IN:")
            st.dataframe(
                income[["txn_date", "merchant", "amount", "direction", "balance_after"]]
                .sort_values(by="txn_date", ascending=False),
                use_container_width=True
            )

except Exception as e:
    st.error(f"Error: {e}")
