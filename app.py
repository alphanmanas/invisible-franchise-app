import re
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Invisible Hair Franchising Model v7.2",
    layout="wide"
)

# =========================================================
# BRAND / STYLE
# Brand guide reference:
# - Page 1: logo composition
# - Page 2: K100 black, Pantone 871 C, Chronicle Display, Chronica Pro
# =========================================================
BRAND_BLACK = "#231F20"
BRAND_GOLD = "#9A8457"
BG = "#F7F6F3"
CARD_BG = "#FFFFFF"
BORDER = "#E7E3DB"
TEXT_MUTED = "#6B7280"
SUCCESS = "#0F766E"
DANGER = "#B91C1C"
WARNING = "#A16207"

st.markdown(f"""
<style>
    .main {{
        background-color: {BG};
    }}

    .block-container {{
        max-width: 1600px;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }}

    .brand-header {{
        background: linear-gradient(180deg, #ffffff 0%, #fcfbf8 100%);
        border: 1px solid {BORDER};
        border-radius: 22px;
        padding: 24px 28px 22px 28px;
        margin-bottom: 18px;
        box-shadow: 0 8px 26px rgba(35, 31, 32, 0.05);
    }}

    .brand-top {{
        display: flex;
        align-items: center;
        gap: 18px;
        margin-bottom: 8px;
    }}

    .brand-title {{
        font-family: Georgia, "Times New Roman", serif;
        color: {BRAND_BLACK};
        font-size: 38px;
        line-height: 1.05;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin: 0;
    }}

    .brand-subtitle {{
        color: {TEXT_MUTED};
        font-size: 13px;
        margin-top: 6px;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
    }}

    .brand-tagline {{
        color: {BRAND_GOLD};
        font-size: 14px;
        margin-top: 10px;
        font-family: Georgia, "Times New Roman", serif;
        letter-spacing: 0.04em;
    }}

    .hero-kpi {{
        background: {CARD_BG};
        padding: 18px 20px;
        border-radius: 18px;
        border: 1px solid {BORDER};
        box-shadow: 0 4px 14px rgba(35, 31, 32, 0.05);
        min-height: 118px;
    }}

    .hero-kpi-label {{
        font-size: 13px;
        color: #475569;
        margin-bottom: 10px;
        font-weight: 600;
    }}

    .hero-kpi-value {{
        font-size: 30px;
        color: {BRAND_BLACK};
        font-weight: 800;
        line-height: 1.1;
        font-family: Georgia, "Times New Roman", serif;
    }}

    .hero-kpi-note {{
        font-size: 11px;
        color: {TEXT_MUTED};
        margin-top: 8px;
    }}

    .section-card {{
        background: {CARD_BG};
        padding: 18px 18px 14px 18px;
        border-radius: 18px;
        border: 1px solid {BORDER};
        box-shadow: 0 4px 14px rgba(35, 31, 32, 0.04);
        margin-bottom: 16px;
    }}

    .section-title {{
        font-size: 18px;
        font-weight: 700;
        color: {BRAND_BLACK};
        margin-bottom: 10px;
    }}

    .metric-box {{
        padding: 16px;
        border-radius: 16px;
        color: white;
        min-height: 112px;
        margin-bottom: 10px;
        box-shadow: 0 8px 18px rgba(35, 31, 32, 0.08);
    }}

    .metric-label {{
        font-size: 13px;
        opacity: 0.94;
        margin-bottom: 8px;
        font-weight: 600;
    }}

    .metric-value {{
        font-size: 28px;
        font-weight: 800;
        line-height: 1.15;
        font-family: Georgia, "Times New Roman", serif;
    }}

    .metric-note {{
        font-size: 12px;
        opacity: 0.9;
        margin-top: 8px;
    }}

    .gold-box {{
        background: linear-gradient(135deg, #8C7447, #B59B69);
    }}

    .black-box {{
        background: linear-gradient(135deg, #1F1B1C, #3A3234);
    }}

    .green-box {{
        background: linear-gradient(135deg, #0F766E, #14B8A6);
    }}

    .red-box {{
        background: linear-gradient(135deg, #991B1B, #DC2626);
    }}

    .slate-box {{
        background: linear-gradient(135deg, #334155, #475569);
    }}

    .purple-box {{
        background: linear-gradient(135deg, #6D28D9, #8B5CF6);
    }}

    .small-note {{
        font-size: 12px;
        color: {TEXT_MUTED};
        margin-top: 4px;
    }}

    .status-good {{
        color: {SUCCESS};
        font-weight: 700;
    }}

    .status-bad {{
        color: {DANGER};
        font-weight: 700;
    }}

    .status-neutral {{
        color: {WARNING};
        font-weight: 700;
    }}

    .formula-box {{
        background: #FCFBF8;
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
        color: #334155;
        font-size: 14px;
    }}

    div[data-testid="stDataFrame"] {{
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }}

    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background-color: #ECE8DF;
        border-radius: 10px 10px 0 0;
        padding: 10px 16px;
        font-weight: 700;
        color: {BRAND_BLACK};
    }}

    .stTabs [aria-selected="true"] {{
        background-color: {BRAND_BLACK} !important;
        color: white !important;
    }}

    .input-note {{
        font-size: 11px;
        color: {TEXT_MUTED};
        margin-top: -4px;
        margin-bottom: 10px;
    }}

    .stTextInput label, .stNumberInput label, .stSelectbox label {{
        font-weight: 600 !important;
    }}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HELPERS
# =========================================================
def fmt_tr_num(value) -> str:
    return f"{int(round(value)):,}".replace(",", ".")

def fmt_tr_usd(value) -> str:
    return f"${fmt_tr_num(value)}"

def fmt_pct(value) -> str:
    return f"%{int(round(value))}"

def fmt_months(value):
    if value is None:
        return "N/A"
    return fmt_tr_num(value)

def parse_tr_int(text: str, default: int = 0) -> int:
    if text is None:
        return int(default)
    cleaned = re.sub(r"[^\d]", "", str(text))
    if cleaned == "":
        return int(default)
    return int(cleaned)

def formatted_text_input(label: str, storage_key: str, default_value: int, help_text: str = "") -> int:
    display_key = f"display_{storage_key}"
    if display_key not in st.session_state:
        st.session_state[display_key] = fmt_tr_num(default_value)

    raw = st.text_input(
        label,
        value=st.session_state[display_key],
        key=display_key,
        help=help_text
    )
    value = parse_tr_int(raw, default_value)
    return value

def status_of(value: float):
    if value > 0:
        return "Positive", "status-good"
    if value == 0:
        return "Break-even", "status-neutral"
    return "Negative", "status-bad"

# =========================================================
# HEADER / BRAND BLOCK
# =========================================================
logo_svg = f"""
<svg width="78" height="104" viewBox="0 0 78 104" xmlns="http://www.w3.org/2000/svg">
  <ellipse cx="39" cy="52" rx="31" ry="45" fill="none" stroke="{BRAND_BLACK}" stroke-width="3"/>
  <text x="39" y="66" text-anchor="middle" font-family="Georgia, Times New Roman, serif"
        font-size="44" fill="{BRAND_BLACK}" font-weight="700">IH</text>
</svg>
"""

st.markdown(f"""
<div class="brand-header">
    <div class="brand-top">
        <div>{logo_svg}</div>
        <div>
            <div class="brand-title">Invisible Hair Franchising Model</div>
            <div class="brand-subtitle">v7.2 • Franchisee ROI and Franchisor Profitability Model</div>
            <div class="brand-tagline">Hair is the most beautiful makeup of a human</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR INPUTS
# =========================================================
st.sidebar.title("Model Inputs")
st.sidebar.markdown("**Format:** no decimals, thousand separator as dot.")
st.sidebar.markdown('<div class="input-note">Example: 3.000</div>', unsafe_allow_html=True)

with st.sidebar.expander("Store & Investment Inputs", expanded=True):
    store_size_m2 = formatted_text_input("Store Size (m2)", "store_size_m2", 150)
    decoration_cost_per_m2 = formatted_text_input("Decoration Cost per m2 ($)", "decoration_cost_per_m2", 350)
    rent_per_m2 = formatted_text_input("Rent per m2 / Monthly ($)", "rent_per_m2", 20)
    franchise_fee_usd = formatted_text_input("Franchise Fee ($)", "franchise_fee_usd", 40000)

with st.sidebar.expander("Commercial Inputs", expanded=True):
    dealer_discount_pct = formatted_text_input("Franchisee Discount (%)", "dealer_discount_pct", 30)
    personnel_cost_monthly = formatted_text_input("Personnel + Side Costs / Monthly ($)", "personnel_cost_monthly", 7000)

dealer_discount = dealer_discount_pct / 100

# =========================================================
# PRODUCTS
# =========================================================
products = [
    {"name": "Premium Wig - Short", "retail_price": 3000, "import_cost": 1250, "qty": 6},
    {"name": "Premium Wig - Medium", "retail_price": 3500, "import_cost": 1400, "qty": 5},
    {"name": "Premium Wig - Long", "retail_price": 4000, "import_cost": 1600, "qty": 4},
    {"name": "Topper - Small", "retail_price": 1800, "import_cost": 600, "qty": 4},
    {"name": "Topper - Medium", "retail_price": 2200, "import_cost": 750, "qty": 3},
]

for i, p in enumerate(products, start=1):
    if f"retail_{i}" not in st.session_state:
        st.session_state[f"retail_{i}"] = p["retail_price"]
    if f"import_{i}" not in st.session_state:
        st.session_state[f"import_{i}"] = p["import_cost"]
    if f"qty_{i}" not in st.session_state:
        st.session_state[f"qty_{i}"] = p["qty"]

# =========================================================
# INPUT COLLECTION
# =========================================================
for i, _p in enumerate(products, start=1):
    st.session_state[f"retail_{i}"] = int(st.session_state.get(f"retail_{i}", products[i-1]["retail_price"]))
    st.session_state[f"import_{i}"] = int(st.session_state.get(f"import_{i}", products[i-1]["import_cost"]))
    st.session_state[f"qty_{i}"] = int(st.session_state.get(f"qty_{i}", products[i-1]["qty"]))

# =========================================================
# CALCULATIONS
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

monthly_revenue_franchisee = products_df["Monthly Revenue (Franchisee)"].sum()
monthly_cost_franchisee = products_df["Monthly Cost (Franchisee)"].sum()
monthly_rent_franchisee = store_size_m2 * rent_per_m2
monthly_profit_franchisee = (
    monthly_revenue_franchisee
    - monthly_cost_franchisee
    - monthly_rent_franchisee
    - personnel_cost_monthly
)

monthly_revenue_franchisor = products_df["Monthly Revenue (Franchisor)"].sum()
monthly_cost_franchisor = products_df["Monthly Cost (Franchisor)"].sum()
monthly_profit_franchisor = products_df["Monthly Profit (Franchisor)"].sum()

decoration_total = store_size_m2 * decoration_cost_per_m2
total_investment = franchise_fee_usd + decoration_total

payback_months = None
if monthly_profit_franchisee > 0:
    payback_months = total_investment / monthly_profit_franchisee

franchisee_status, franchisee_status_class = status_of(monthly_profit_franchisee)
franchisor_status, franchisor_status_class = status_of(monthly_profit_franchisor)

# =========================================================
# HERO KPI ROW
# =========================================================
hero1, hero2, hero3, hero4 = st.columns(4)

with hero1:
    st.markdown(f"""
    <div class="hero-kpi">
        <div class="hero-kpi-label">Monthly Revenue</div>
        <div class="hero-kpi-value">{fmt_tr_usd(monthly_revenue_franchisee)}</div>
        <div class="hero-kpi-note">Franchisee</div>
    </div>
    """, unsafe_allow_html=True)

with hero2:
    st.markdown(f"""
    <div class="hero-kpi">
        <div class="hero-kpi-label">Monthly Profit</div>
        <div class="hero-kpi-value">{fmt_tr_usd(monthly_profit_franchisee)}</div>
        <div class="hero-kpi-note">Franchisee</div>
    </div>
    """, unsafe_allow_html=True)

with hero3:
    st.markdown(f"""
    <div class="hero-kpi">
        <div class="hero-kpi-label">Total Investment</div>
        <div class="hero-kpi-value">{fmt_tr_usd(total_investment)}</div>
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
# FRANCHISEE KPI ROW
# =========================================================
st.markdown('<div class="section-card"><div class="section-title">Invisible Hair Franchising Model (Franchisee)</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-box gold-box">
        <div class="metric-label">Monthly Revenue (Franchisee)</div>
        <div class="metric-value">{fmt_tr_usd(monthly_revenue_franchisee)}</div>
        <div class="metric-note">Retail sales to end customers</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-box black-box">
        <div class="metric-label">Monthly Cost (Franchisee)</div>
        <div class="metric-value">{fmt_tr_usd(monthly_cost_franchisee)}</div>
        <div class="metric-note">Discounted purchase cost from franchisor</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-box red-box">
        <div class="metric-label">Rent (Franchisee)</div>
        <div class="metric-value">{fmt_tr_usd(monthly_rent_franchisee)}</div>
        <div class="metric-note">Store size × rent per m2</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-box slate-box">
        <div class="metric-label">Personnel (Franchisee)</div>
        <div class="metric-value">{fmt_tr_usd(personnel_cost_monthly)}</div>
        <div class="metric-note">Personnel and side costs</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-box green-box">
        <div class="metric-label">Monthly Profit (Franchisee)</div>
        <div class="metric-value">{fmt_tr_usd(monthly_profit_franchisee)}</div>
        <div class="metric-note">Net monthly profit</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(
    f'<div class="small-note">Franchisee Status: <span class="{franchisee_status_class}">{franchisee_status}</span></div>',
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FRANCHISOR KPI ROW
# =========================================================
st.markdown('<div class="section-card"><div class="section-title">Invisible Hair Franchising Model (Franchisor)</div>', unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(f"""
    <div class="metric-box purple-box">
        <div class="metric-label">Monthly Revenue (Franchisor)</div>
        <div class="metric-value">{fmt_tr_usd(monthly_revenue_franchisor)}</div>
        <div class="metric-note">Sales to franchisee after discount</div>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown(f"""
    <div class="metric-box black-box">
        <div class="metric-label">Monthly Cost (Franchisor)</div>
        <div class="metric-value">{fmt_tr_usd(monthly_cost_franchisor)}</div>
        <div class="metric-note">Import cost of sold units</div>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown(f"""
    <div class="metric-box gold-box">
        <div class="metric-label">Monthly Profit (Franchisor)</div>
        <div class="metric-value">{fmt_tr_usd(monthly_profit_franchisor)}</div>
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
            st.metric("Decoration Cost", fmt_tr_usd(decoration_total))
            st.metric("Franchise Fee", fmt_tr_usd(franchise_fee_usd))
            st.metric("Total Investment", fmt_tr_usd(total_investment))

        with a2:
            st.metric("Franchisee Discount", fmt_pct(dealer_discount_pct))
            st.metric("Total Monthly Units", fmt_tr_num(products_df["Monthly Units"].sum()))
            st.metric("Payback (Months)", fmt_months(payback_months))

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="section-card"><div class="section-title">Monthly Overview</div>', unsafe_allow_html=True)

        monthly_overview_df = pd.DataFrame([
            ["Monthly Revenue (Franchisee)", monthly_revenue_franchisee],
            ["Monthly Cost (Franchisee)", monthly_cost_franchisee],
            ["Rent (Franchisee)", monthly_rent_franchisee],
            ["Personnel (Franchisee)", personnel_cost_monthly],
            ["Monthly Profit (Franchisee)", monthly_profit_franchisee],
            ["Monthly Revenue (Franchisor)", monthly_revenue_franchisor],
            ["Monthly Cost (Franchisor)", monthly_cost_franchisor],
            ["Monthly Profit (Franchisor)", monthly_profit_franchisor],
        ], columns=["Metric", "Value"])

        monthly_overview_display = monthly_overview_df.copy()
        monthly_overview_display["Value"] = monthly_overview_display["Value"].apply(fmt_tr_usd)

        st.dataframe(monthly_overview_display, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# TAB 2
# =========================================================
with tab2:
    st.markdown('<div class="section-card"><div class="section-title">Editable Product Inputs</div>', unsafe_allow_html=True)
    st.markdown('<div class="small-note">All fields use no decimals and dot thousand separator. Example: 3.000</div>', unsafe_allow_html=True)

    for i, p in enumerate(products, start=1):
        st.markdown(f"**{p['name']}**")
        p1, p2, p3 = st.columns(3)

        with p1:
            st.session_state[f"retail_{i}"] = formatted_text_input(
                f"Retail Price ($) - {p['name']}",
                f"retail_{i}",
                products[i-1]["retail_price"]
            )

        with p2:
            st.session_state[f"import_{i}"] = formatted_text_input(
                f"Import Cost ($) - {p['name']}",
                f"import_{i}",
                products[i-1]["import_cost"]
            )

        with p3:
            st.session_state[f"qty_{i}"] = formatted_text_input(
                f"Monthly Units - {p['name']}",
                f"qty_{i}",
                products[i-1]["qty"]
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
            franchisee_table[col] = franchisee_table[col].apply(fmt_tr_usd)

        franchisee_table["Monthly Units"] = franchisee_table["Monthly Units"].apply(fmt_tr_num)

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
            franchisor_table[col] = franchisor_table[col].apply(fmt_tr_usd)

        franchisor_table["Monthly Units"] = franchisor_table["Monthly Units"].apply(fmt_tr_num)

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
    st.markdown('<div class="formula-box"><b>Monthly Revenue (Franchisor)</b><br>Discounted sales total billed to franchisee</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Monthly Cost (Franchisor)</b><br>Sum of: Import Cost × Monthly Units</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Monthly Profit (Franchisor)</b><br>Monthly Revenue (Franchisor) - Monthly Cost (Franchisor)</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Total Investment</b><br>Franchise Fee + Decoration Cost</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box"><b>Payback (Months)</b><br>Total Investment / Monthly Profit (Franchisee)</div>', unsafe_allow_html=True)

    st.info("All input and output displays use no decimals and dot thousand separator. Example: 3.000")

    st.markdown("</div>", unsafe_allow_html=True)
