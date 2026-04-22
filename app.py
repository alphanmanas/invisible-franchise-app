import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Invisible Hair Franchising Model v7.1",
    layout="wide"
)

# =========================================================
# STYLE
# =========================================================
st.markdown("""
<style>
    .main {
        background-color: #f6f8fc;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    .top-title {
        font-size: 34px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 0.2rem;
    }

    .top-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 1.2rem;
    }

    .section-card {
        background: #ffffff;
        padding: 18px 18px 14px 18px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
        margin-bottom: 16px;
    }

    .section-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 10px;
    }

    .metric-box {
        padding: 16px;
        border-radius: 16px;
        color: white;
        min-height: 110px;
        margin-bottom: 10px;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
    }

    .metric-label {
        font-size: 13px;
        opacity: 0.92;
        margin-bottom: 8px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 800;
        line-height: 1.15;
    }

    .metric-note {
        font-size: 12px;
        opacity: 0.88;
        margin-top: 8px;
    }

    .hero-kpi {
        background: #ffffff;
        padding: 18px 20px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05);
        min-height: 118px;
    }

    .hero-kpi-label {
        font-size: 13px;
        color: #475569;
        margin-bottom: 10px;
        font-weight: 600;
    }

    .hero-kpi-value {
        font-size: 28px;
        color: #0f172a;
        font-weight: 800;
        line-height: 1.1;
    }

    .hero-kpi-note {
        font-size: 11px;
        color: #64748b;
        margin-top: 8px;
    }

    .blue-box {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
    }

    .green-box {
        background: linear-gradient(135deg, #047857, #10b981);
    }

    .orange-box {
        background: linear-gradient(135deg, #c2410c, #f97316);
    }

    .purple-box {
        background: linear-gradient(135deg, #6d28d9, #8b5cf6);
    }

    .slate-box {
        background: linear-gradient(135deg, #334155, #475569);
    }

    .red-box {
        background: linear-gradient(135deg, #b91c1c, #ef4444);
    }

    .teal-box {
        background: linear-gradient(135deg, #0f766e, #14b8a6);
    }

    .small-note {
        font-size: 12px;
        color: #64748b;
        margin-top: 4px;
    }

    .status-good {
        color: #047857;
        font-weight: 700;
    }

    .status-bad {
        color: #b91c1c;
        font-weight: 700;
    }

    .status-neutral {
        color: #92400e;
        font-weight: 700;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: #e2e8f0;
        border-radius: 10px 10px 0 0;
        padding: 10px 16px;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0f172a !important;
        color: white !important;
    }

    .formula-box {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
        color: #334155;
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
def fmt_num(value):
    return f"{round(value):,}"

def fmt_usd(value):
    return f"${round(value):,}"

def fmt_pct(value):
    return f"{round(value)}%"

def fmt_months(value):
    if value is None:
        return "N/A"
    return f"{round(value):,}"

# =========================================================
# HEADER
# =========================================================
st.markdown('<div class="top-title">Invisible Hair Franchising Model</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="top-subtitle">v7.1 • Franchisee ROI and Franchisor profitability model • Integer display with thousand separators</div>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("Model Inputs")

with st.sidebar.expander("Store & Investment Inputs", expanded=True):
    store_size_m2 = st.number_input("Store Size (m2)", min_value=0.0, value=150.0, step=1.0)
    decoration_cost_per_m2 = st.number_input("Decoration Cost per m2 ($)", min_value=0.0, value=350.0, step=10.0)
    rent_per_m2 = st.number_input("Rent per m2 / Monthly ($)", min_value=0.0, value=20.0, step=1.0)
    franchise_fee_usd = st.number_input("Franchise Fee ($)", min_value=0.0, value=40000.0, step=1000.0)

with st.sidebar.expander("Commercial Inputs", expanded=True):
    dealer_discount_pct = st.number_input("Franchisee Discount (%)", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
    personnel_cost_monthly = st.number_input("Personnel + Side Costs / Monthly ($)", min_value=0.0, value=7000.0, step=100.0)

dealer_discount = dealer_discount_pct / 100

# =========================================================
# PRODUCTS
# =========================================================
products = [
    {"name": "Premium Wig - Short", "retail_price": 3000.0, "import_cost": 1250.0, "qty": 6.0},
    {"name": "Premium Wig - Medium", "retail_price": 3500.0, "import_cost": 1400.0, "qty": 5.0},
    {"name": "Premium Wig - Long", "retail_price": 4000.0, "import_cost": 1600.0, "qty": 4.0},
    {"name": "Topper - Small", "retail_price": 1800.0, "import_cost": 600.0, "qty": 4.0},
    {"name": "Topper - Medium", "retail_price": 2200.0, "import_cost": 750.0, "qty": 3.0},
]

for i, p in enumerate(products, start=1):
    if f"retail_{i}" not in st.session_state:
        st.session_state[f"retail_{i}"] = p["retail_price"]
    if f"import_{i}" not in st.session_state:
        st.session_state[f"import_{i}"] = p["import_cost"]
    if f"qty_{i}" not in st.session_state:
        st.session_state[f"qty_{i}"] = p["qty"]

# =========================================================
# PRODUCT DATA
# =========================================================
product_rows = []
for i, p in enumerate(products, start=1):
    retail_price = st.session_state[f"retail_{i}"]
    import_cost = st.session_state[f"import_{i}"]
    qty = st.session_state[f"qty_{i}"]

    franchisee_unit_cost = retail_price * (1 - dealer_discount)
    franchisee_revenue = retail_price * qty
    franchisee_product_cost = franchisee_unit_cost * qty
    franchisee_gross_profit = franchisee_revenue - franchisee_product_cost

    franchisor_revenue = franchisee_product_cost
    franchisor_product_cost = import_cost * qty
    franchisor_profit = franchisor_revenue - franchisor_product_cost

    product_rows.append({
        "Product": p["name"],
        "Retail Price ($)": retail_price,
        "Import Cost ($)": import_cost,
        "Monthly Units": qty,
        "Franchisee Unit Cost ($)": franchisee_unit_cost,
        "Monthly Revenue (Franchisee)": franchisee_revenue,
        "Monthly Cost (Franchisee)": franchisee_product_cost,
        "Monthly Gross Profit (Franchisee)": franchisee_gross_profit,
        "Monthly Revenue (Franchisor)": franchisor_revenue,
        "Monthly Cost (Franchisor)": franchisor_product_cost,
        "Monthly Profit (Franchisor)": franchisor_profit
    })

products_df = pd.DataFrame(product_rows)

# =========================================================
# CALCULATIONS
# =========================================================
monthly_revenue_franchisee = products_df["Monthly Revenue (Franchisee)"].sum()
monthly_cost_franchisee = products_df["Monthly Cost (Franchisee)"].sum()
monthly_rent_franchisee = store_size_m2 * rent_per_m2
monthly_profit_franchisee = monthly_revenue_franchisee - monthly_cost_franchisee - monthly_rent_franchisee - personnel_cost_monthly

monthly_revenue_franchisor = products_df["Monthly Revenue (Franchisor)"].sum()
monthly_cost_franchisor = products_df["Monthly Cost (Franchisor)"].sum()
monthly_profit_franchisor = products_df["Monthly Profit (Franchisor)"].sum()

decoration_total = store_size_m2 * decoration_cost_per_m2
total_investment = franchise_fee_usd + decoration_total

payback_months = None
if monthly_profit_franchisee > 0:
    payback_months = total_investment / monthly_profit_franchisee

if monthly_profit_franchisee > 0:
    franchisee_status = "Positive"
    franchisee_status_class = "status-good"
elif monthly_profit_franchisee == 0:
    franchisee_status = "Break-even"
    franchisee_status_class = "status-neutral"
else:
    franchisee_status = "Negative"
    franchisee_status_class = "status-bad"

if monthly_profit_franchisor > 0:
    franchisor_status = "Positive"
    franchisor_status_class = "status-good"
elif monthly_profit_franchisor == 0:
    franchisor_status = "Break-even"
    franchisor_status_class = "status-neutral"
else:
    franchisor_status = "Negative"
    franchisor_status_class = "status-bad"

# =========================================================
# TOP HERO KPI ROW (from screenshot logic)
# =========================================================
hero1, hero2, hero3, hero4 = st.columns(4)

with hero1:
    st.markdown(f"""
    <div class="hero-kpi">
        <div class="hero-kpi-label">Monthly Revenue</div>
        <div class="hero-kpi-value">{fmt_usd(monthly_revenue_franchisee)}</div>
        <div class="hero-kpi-note">Franchisee</div>
    </div>
    """, unsafe_allow_html=True)

with hero2:
    st.markdown(f"""
    <div class="hero-kpi">
        <div class="hero-kpi-label">Monthly Profit</div>
        <div class="hero-kpi-value">{fmt_usd(monthly_profit_franchisee)}</div>
        <div class="hero-kpi-note">Franchisee</div>
    </div>
    """, unsafe_allow_html=True)

with hero3:
    st.markdown(f"""
    <div class="hero-kpi">
        <div class="hero-kpi-label">Total Investment</div>
        <div class="hero-kpi-value">{fmt_usd(total_investment)}</div>
        <div class="hero-kpi-note">Franchisee</div>
    </div>
    """, unsafe_allow_html=True)

with hero4:
    st.markdown(f"""
    <div class="hero-kpi">
        <div class="hero-kpi-label">Payback (Months)</div>
        <div class="hero-kpi-value">{fmt_months(payback_months)}</div>
        <div class="hero-kpi-note">Franchisee</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# =========================================================
# KPI ROW 1 - FRANCHISEE
# =========================================================
st.markdown('<div class="section-card"><div class="section-title">Invisible Hair Franchising Model (Franchisee)</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-box blue-box">
        <div class="metric-label">Monthly Revenue (Franchisee)</div>
        <div class="metric-value">{fmt_usd(monthly_revenue_franchisee)}</div>
        <div class="metric-note">Retail sales to end customers</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-box orange-box">
        <div class="metric-label">Monthly Cost (Franchisee)</div>
        <div class="metric-value">{fmt_usd(monthly_cost_franchisee)}</div>
        <div class="metric-note">Discounted purchase cost from franchisor</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-box red-box">
        <div class="metric-label">Rent (Franchisee)</div>
        <div class="metric-value">{fmt_usd(monthly_rent_franchisee)}</div>
        <div class="metric-note">Store size × rent per m2</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-box slate-box">
        <div class="metric-label">Personnel (Franchisee)</div>
        <div class="metric-value">{fmt_usd(personnel_cost_monthly)}</div>
        <div class="metric-note">Personnel and side costs</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-box green-box">
        <div class="metric-label">Profit (Franchisee)</div>
        <div class="metric-value">{fmt_usd(monthly_profit_franchisee)}</div>
        <div class="metric-note">Net monthly profit</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    f'<div class="small-note">Franchisee Status: <span class="{franchisee_status_class}">{franchisee_status}</span></div>',
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# KPI ROW 2 - FRANCHISOR
# =========================================================
st.markdown('<div class="section-card"><div class="section-title">Invisible Hair Franchising Model (Franchisor)</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(f"""
    <div class="metric-box purple-box">
        <div class="metric-label">Monthly Revenue (Franchisor)</div>
        <div class="metric-value">{fmt_usd(monthly_revenue_franchisor)}</div>
        <div class="metric-note">Sales to franchisee after discount</div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown(f"""
    <div class="metric-box orange-box">
        <div class="metric-label">Monthly Cost (Franchisor)</div>
        <div class="metric-value">{fmt_usd(monthly_cost_franchisor)}</div>
        <div class="metric-note">Import cost of sold units</div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown(f"""
    <div class="metric-box teal-box">
        <div class="metric-label">Monthly Profit (Franchisor)</div>
        <div class="metric-value">{fmt_usd(monthly_profit_franchisor)}</div>
        <div class="metric-note">Revenue - product cost</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    f'<div class="small-note">Franchisor Status: <span class="{franchisor_status_class}">{franchisor_status}</span></div>',
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)

if monthly_profit_franchisee <= 0:
    st.warning("Franchisee profit is zero or negative. Payback cannot be calculated under current assumptions.")

st.divider()

# =========================================================
# TABS
# =========================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "Executive Dashboard",
    "Product Inputs",
    "Detailed Tables",
    "Calculation Logic"
])

# =========================================================
# TAB 1
# =========================================================
with tab1:
    left, right = st.columns([1.1, 1])

    with left:
        st.markdown('<div class="section-card"><div class="section-title">Investment Summary</div>', unsafe_allow_html=True)

        a1, a2 = st.columns(2)
        with a1:
            st.metric("Decoration Cost", fmt_usd(decoration_total))
            st.metric("Franchise Fee", fmt_usd(franchise_fee_usd))
            st.metric("Total Investment", fmt_usd(total_investment))

        with a2:
            st.metric("Franchisee Discount", fmt_pct(dealer_discount_pct))
            st.metric("Total Monthly Units", fmt_num(products_df["Monthly Units"].sum()))
            st.metric("Payback (Months)", fmt_months(payback_months))

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card"><div class="section-title">Monthly Overview</div>', unsafe_allow_html=True)

        monthly_overview_df = pd.DataFrame([
            ["Monthly Revenue (Franchisee)", monthly_revenue_franchisee],
            ["Monthly Cost (Franchisee)", monthly_cost_franchisee],
            ["Rent (Franchisee)", monthly_rent_franchisee],
            ["Personnel (Franchisee)", personnel_cost_monthly],
            ["Profit (Franchisee)", monthly_profit_franchisee],
            ["Monthly Revenue (Franchisor)", monthly_revenue_franchisor],
            ["Monthly Cost (Franchisor)", monthly_cost_franchisor],
            ["Monthly Profit (Franchisor)", monthly_profit_franchisor],
        ], columns=["Metric", "Value"])

        monthly_overview_display = monthly_overview_df.copy()
        monthly_overview_display["Value"] = monthly_overview_display["Value"].apply(fmt_usd)

        st.dataframe(monthly_overview_display, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2
# =========================================================
with tab2:
    st.markdown('<div class="section-card"><div class="section-title">Editable Product Inputs</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-note">Enter retail price, import cost and monthly units for each of the 5 products.</div>', unsafe_allow_html=True)

    for i, p in enumerate(products, start=1):
        st.markdown(f"**{p['name']}**")
        p1, p2, p3 = st.columns(3)

        with p1:
            st.session_state[f"retail_{i}"] = st.number_input(
                f"Retail Price ($) - {p['name']}",
                min_value=0.0,
                value=float(st.session_state[f"retail_{i}"]),
                step=10.0,
                key=f"retail_input_{i}"
            )

        with p2:
            st.session_state[f"import_{i}"] = st.number_input(
                f"Import Cost ($) - {p['name']}",
                min_value=0.0,
                value=float(st.session_state[f"import_{i}"]),
                step=10.0,
                key=f"import_input_{i}"
            )

        with p3:
            st.session_state[f"qty_{i}"] = st.number_input(
                f"Monthly Units - {p['name']}",
                min_value=0.0,
                value=float(st.session_state[f"qty_{i}"]),
                step=1.0,
                key=f"qty_input_{i}"
            )

        st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 3
# =========================================================
with tab3:
    left, right = st.columns(2)

    with left:
        st.markdown('<div class="section-card"><div class="section-title">Franchisee Product Economics</div>', unsafe_allow_html=True)

        franchisee_table = products_df[[
            "Product",
            "Retail Price ($)",
            "Monthly Units",
            "Franchisee Unit Cost ($)",
            "Monthly Revenue (Franchisee)",
            "Monthly Cost (Franchisee)",
            "Monthly Gross Profit (Franchisee)"
        ]].copy()

        for col in [
            "Retail Price ($)",
            "Franchisee Unit Cost ($)",
            "Monthly Revenue (Franchisee)",
            "Monthly Cost (Franchisee)",
            "Monthly Gross Profit (Franchisee)"
        ]:
            franchisee_table[col] = franchisee_table[col].apply(fmt_usd)

        franchisee_table["Monthly Units"] = franchisee_table["Monthly Units"].apply(fmt_num)

        st.dataframe(franchisee_table, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card"><div class="section-title">Franchisor Product Economics</div>', unsafe_allow_html=True)

        franchisor_table = products_df[[
            "Product",
            "Import Cost ($)",
            "Monthly Units",
            "Monthly Revenue (Franchisor)",
            "Monthly Cost (Franchisor)",
            "Monthly Profit (Franchisor)"
        ]].copy()

        for col in [
            "Import Cost ($)",
            "Monthly Revenue (Franchisor)",
            "Monthly Cost (Franchisor)",
            "Monthly Profit (Franchisor)"
        ]:
            franchisor_table[col] = franchisor_table[col].apply(fmt_usd)

        franchisor_table["Monthly Units"] = franchisor_table["Monthly Units"].apply(fmt_num)

        st.dataframe(franchisor_table, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 4
# =========================================================
with tab4:
    st.markdown('<div class="section-card"><div class="section-title">Calculation Logic</div>', unsafe_allow_html=True)

    st.markdown('<div class="formula-box"><b>Monthly Revenue</b><br>Sum of: Retail Price × Monthly Units</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Monthly Cost (Franchisee)</b><br>Sum of: Retail Price × (1 - Franchisee Discount) × Monthly Units</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Rent</b><br>Store Size × Rent per m2</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Personnel</b><br>Monthly personnel and side costs</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Monthly Profit (Franchisee)</b><br>Monthly Revenue - Monthly Cost (Franchisee) - Rent - Personnel</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Monthly Revenue (Franchisor)</b><br>Same as discounted sales to franchisee</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Monthly Cost (Franchisor)</b><br>Sum of: Import Cost × Monthly Units</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Monthly Profit (Franchisor)</b><br>Monthly Revenue (Franchisor) - Monthly Cost (Franchisor)</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Total Investment</b><br>Franchise Fee + Decoration Cost</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Payback (Months)</b><br>Total Investment / Monthly Profit (Franchisee)</div>', unsafe_allow_html=True)

    st.info("All outputs are displayed as integers with thousand separators. Example: 3,000")

    st.markdown("</div>", unsafe_allow_html=True)
