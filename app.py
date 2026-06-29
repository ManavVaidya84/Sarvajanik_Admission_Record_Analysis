import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Sarvajanik University Analytics",
    layout="wide",
    page_icon="🎓",
    initial_sidebar_state="expanded"
)

# ====================== PREMIUM GLASSMORPHISM CSS ======================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

    /* ── Root & Background ── */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #020818 0%, #0b1437 40%, #0e1f3d 70%, #071426 100%) !important;
        min-height: 100vh;
    }
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed; inset: 0; z-index: 0;
        background:
            radial-gradient(ellipse 800px 600px at 15% 20%, rgba(56,132,255,0.12) 0%, transparent 70%),
            radial-gradient(ellipse 600px 500px at 85% 75%, rgba(139,92,246,0.10) 0%, transparent 70%),
            radial-gradient(ellipse 500px 400px at 50% 50%, rgba(20,184,166,0.05) 0%, transparent 60%);
        pointer-events: none;
    }
    [data-testid="stAppViewContainer"] > .main { background: transparent !important; }
    .main .block-container {
        padding: 2rem 2.5rem 3rem;
        max-width: 1400px;
        position: relative; z-index: 1;
    }

    /* ── Global Typography ── */
    * { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; font-weight: 700; }
    h1 {
        background: linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #34d399 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 2.4rem; letter-spacing: -0.5px; line-height: 1.2;
        margin-bottom: 0.3rem;
    }
    h2 { color: #94a3b8; font-size: 1.1rem; font-weight: 400; }
    /* Only color text nodes that aren't already styled */
    .stMarkdown p, .stText { color: #cbd5e1; }

    /* ── Sidebar always visible ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #060e24 0%, #0a1628 100%) !important;
        backdrop-filter: blur(24px) saturate(180%);
        border-right: 1px solid rgba(96,165,250,0.18) !important;
        min-width: 240px !important;
        width: 240px !important;
    }
    [data-testid="stSidebar"] > div:first-child { padding-top: 0 !important; }

    /* ── Kill EVERY variant of the collapse/expand toggle ── */
    [data-testid="collapsedControl"]          { display: none !important; visibility: hidden !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; visibility: hidden !important; }
    button[kind="header"]                     { display: none !important; }
    /* The floating arrow button that Streamlit renders outside the sidebar */
    .st-emotion-cache-1egp75o,
    .st-emotion-cache-1li7dat,
    .st-emotion-cache-po3384,
    [class*="collapsedControl"]               { display: none !important; }
    /* Catch-all for any top-left button containing a Material icon */
    body > div > div > section:first-of-type ~ div > button,
    [data-testid="stAppViewContainer"] > div > button { display: none !important; }

    section[data-testid="stSidebar"] { transform: none !important; visibility: visible !important; }

    /* ── Radio nav items ── */
    .stRadio > div { gap: 4px !important; }
    .stRadio > div > label {
        display: flex !important;
        align-items: center !important;
        color: #94a3b8 !important;
        padding: 11px 16px !important;
        border-radius: 12px !important;
        transition: all 0.2s ease !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        cursor: pointer !important;
        border: 1px solid transparent !important;
        width: 100% !important;
    }
    .stRadio > div > label:hover {
        background: rgba(96,165,250,0.10) !important;
        color: #e2e8f0 !important;
        border-color: rgba(96,165,250,0.15) !important;
    }
    /* Selected radio item */
    .stRadio > div > label[data-baseweb="radio"]:has(input:checked),
    .stRadio > div > label:has(> div > input:checked) {
        background: rgba(96,165,250,0.15) !important;
        color: #60a5fa !important;
        border-color: rgba(96,165,250,0.3) !important;
    }
    /* Hide the radio dot itself */
    .stRadio > div > label > div:first-child { display: none !important; }
    .stRadio [data-testid="stMarkdownContainer"] p { color: inherit !important; margin: 0 !important; font-size: inherit !important; }

    /* ── Glass Cards ── */
    .glass-card {
        background: rgba(255,255,255,0.04);
        backdrop-filter: blur(24px) saturate(160%);
        -webkit-backdrop-filter: blur(24px) saturate(160%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 20px;
        padding: 28px 22px 24px;
        box-shadow:
            0 4px 24px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.06);
        transition: transform 0.35s cubic-bezier(.22,.68,0,1.2), box-shadow 0.35s ease, border-color 0.3s ease;
        text-align: center;
        position: relative; overflow: hidden;
    }
    .glass-card::before {
        content: '';
        position: absolute; top: 0; left: 0; right: 0; height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.15), transparent);
    }
    .glass-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 0 1px rgba(96,165,250,0.2), inset 0 1px 0 rgba(255,255,255,0.1);
        border-color: rgba(96,165,250,0.25);
    }
    .glass-card .card-label {
        font-size: 0.75rem; font-weight: 600; letter-spacing: 0.1em;
        text-transform: uppercase; color: #64748b; margin-bottom: 10px;
    }
    .glass-card .card-value {
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 2.4rem; font-weight: 800; line-height: 1.1;
        letter-spacing: -1px;
    }
    .glass-card .card-sub {
        font-size: 0.78rem; color: #475569; margin-top: 6px;
    }

    /* ── Accent Colors per Card ── */
    .card-blue  .card-value { color: #60a5fa; text-shadow: 0 0 30px rgba(96,165,250,0.5); }
    .card-green .card-value { color: #34d399; text-shadow: 0 0 30px rgba(52,211,153,0.5); }
    .card-amber .card-value { color: #fbbf24; text-shadow: 0 0 30px rgba(251,191,36,0.5); }
    .card-violet .card-value { color: #a78bfa; text-shadow: 0 0 30px rgba(167,139,250,0.5); }

    /* ── Section Headers ── */
    .section-label {
        font-size: 0.72rem; font-weight: 700; letter-spacing: 0.14em;
        text-transform: uppercase; color: #60a5fa;
        margin-bottom: 6px; display: block;
    }
    .divider {
        height: 1px;
        background: linear-gradient(90deg, rgba(96,165,250,0.4), rgba(167,139,250,0.3), transparent);
        margin: 28px 0;
        border: none;
    }

    /* ── Plotly Chart Wrapper ── */
    .chart-glass {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 20px;
        padding: 6px;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        overflow: hidden;
    }

    /* ── Streamlit overrides ── */
    .stSuccess {
        background: rgba(52,211,153,0.08) !important;
        border: 1px solid rgba(52,211,153,0.25) !important;
        border-radius: 14px !important;
        color: #34d399 !important;
    }
    .stInfo {
        background: rgba(96,165,250,0.08) !important;
        border: 1px solid rgba(96,165,250,0.2) !important;
        border-radius: 14px !important;
        color: #93c5fd !important;
    }
    .stMetric {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 16px !important;
        padding: 18px 22px !important;
    }
    .stMetric label { color: #64748b !important; font-size: 0.78rem !important; font-weight: 600 !important; text-transform: uppercase; letter-spacing: 0.08em; }
    .stMetric [data-testid="stMetricValue"] { color: #e2e8f0 !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 800 !important; }

    .stSlider > label { color: #94a3b8 !important; font-weight: 500 !important; }
    .stSlider [data-baseweb="slider"] > div { background: rgba(96,165,250,0.2) !important; }

    /* Hide default Streamlit elements */
    #MainMenu, footer, header { visibility: hidden; height: 0 !important; }
    .stDeployButton { display: none !important; }

    /* ── Nuclear hide: the keyboard_double_arrow sidebar toggle ── */
    /* Target by every known selector variant */
    [data-testid="collapsedControl"]          { display: none !important; opacity: 0 !important; pointer-events: none !important; width: 0 !important; height: 0 !important; }
    [data-testid="stSidebarCollapsedControl"] { display: none !important; opacity: 0 !important; pointer-events: none !important; }
    button[aria-label="Close sidebar"]        { display: none !important; }
    button[aria-label="Open sidebar"]         { display: none !important; }
    button[aria-label="collapse sidebar"]     { display: none !important; }
    button[aria-label="expand sidebar"]       { display: none !important; }
    /* The floating button Streamlit places at top-left outside the sidebar */
    .st-emotion-cache-1egp75o { display: none !important; }
    .st-emotion-cache-1li7dat  { display: none !important; }
    .st-emotion-cache-po3384   { display: none !important; }
    .st-emotion-cache-czk5ss   { display: none !important; }
    [class*="collapsedControl"] { display: none !important; }
    /* Hide the Material icon span specifically */
    .material-symbols-rounded  { display: none !important; font-size: 0 !important; }
    span[data-testid="stIconMaterial"] { display: none !important; }
    /* Hide the entire top-bar area that holds the button */
    [data-testid="stAppViewContainer"] > div:first-child > button { display: none !important; }
    header[data-testid="stHeader"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# Remove the sidebar collapse button from the DOM via JS
st.markdown("""
<script>
(function nukeSidebarToggle() {
    function hide(el) {
        el.style.cssText += 'display:none!important;visibility:hidden!important;width:0!important;height:0!important;opacity:0!important;pointer-events:none!important;';
    }
    function nuke() {
        // 1. Any button containing "keyboard_double" text
        document.querySelectorAll('button').forEach(btn => {
            const txt = (btn.innerText || btn.textContent || '');
            if (txt.includes('keyboard_double') || txt.trim() === 'keyboard_double_arrow_left' || txt.trim() === 'keyboard_double_arrow_right') {
                hide(btn);
            }
        });
        // 2. By data-testid
        ['collapsedControl','stSidebarCollapsedControl','stHeader'].forEach(id => {
            document.querySelectorAll('[data-testid="' + id + '"]').forEach(hide);
        });
        // 3. By aria-label
        ['Close sidebar','Open sidebar','collapse sidebar','expand sidebar'].forEach(label => {
            document.querySelectorAll('button[aria-label="' + label + '"]').forEach(hide);
        });
        // 4. Any span whose text is the raw material icon name
        document.querySelectorAll('span').forEach(span => {
            const txt = (span.innerText || span.textContent || '').trim();
            if (txt === 'keyboard_double_arrow_left' || txt === 'keyboard_double_arrow_right' || txt.startsWith('keyboard_double')) {
                hide(span);
                if (span.parentElement) hide(span.parentElement);
            }
        });
    }
    nuke();
    setTimeout(nuke, 100);
    setTimeout(nuke, 500);
    setTimeout(nuke, 1500);
    new MutationObserver(nuke).observe(document.documentElement, {childList: true, subtree: true});
})();
</script>
""", unsafe_allow_html=True)
_AXIS_STYLE = dict(
    gridcolor='rgba(255,255,255,0.05)',
    linecolor='rgba(255,255,255,0.1)',
    tickcolor='rgba(255,255,255,0.1)',
)
# Base layout — NO xaxis/yaxis keys so callers can pass their own without collision
_LAYOUT_BASE = dict(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family='Inter', color='#94a3b8', size=12),
    title_font=dict(family='Space Grotesk', color='#e2e8f0', size=16),
    legend=dict(bgcolor='rgba(255,255,255,0.04)', bordercolor='rgba(255,255,255,0.08)', borderwidth=1),
    margin=dict(l=16, r=16, t=48, b=16),
    hoverlabel=dict(bgcolor='rgba(15,23,42,0.95)', bordercolor='rgba(96,165,250,0.3)', font_color='#e2e8f0'),
)
COLORS = ['#60a5fa', '#a78bfa', '#34d399', '#fbbf24', '#f472b6', '#38bdf8', '#fb923c', '#4ade80']


def apply_layout(fig, height=500, xaxis_extra=None, yaxis_extra=None):
    """Apply shared dark theme. Axis overrides are deep-merged to avoid duplicate-kwarg errors."""
    xaxis = {**_AXIS_STYLE, **(xaxis_extra or {})}
    yaxis = {**_AXIS_STYLE, **(yaxis_extra or {})}
    fig.update_layout(height=height, xaxis=xaxis, yaxis=yaxis, **_LAYOUT_BASE)

# ====================== DATA LOADING ======================
@st.cache_data(show_spinner=False)
def load_all_data():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    files = [
        (os.path.join(BASE_DIR, "20260106153152255_Admission 2023 24.xls"), "2023"),
        (os.path.join(BASE_DIR, "20260106153439552_Admission 2024 25.xls"), "2024"),
        (os.path.join(BASE_DIR, "20260106153808096_Admission 2025 26.xls"), "2025"),
        (os.path.join(BASE_DIR, "20260106153841088_Admission 2026 27.xls"), "2026"),
    ]
    dfs = []
    for path, year in files:
        if os.path.exists(path):
            try:
                df_temp = pd.read_excel(path, header=3, engine='xlrd')
                df_temp['Year'] = year
                dfs.append(df_temp)
            except Exception:
                pass
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True, copy=False)


@st.cache_data(show_spinner=False)
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return df
    df = df.copy()
    if 'City' in df.columns:
        df['City'] = df['City'].astype(str).str.strip().str.title()
        df['City'] = df['City'].replace(
            {'Suart': 'Surat', 'SURAT': 'Surat', 'surat': 'Surat', 'Suarat': 'Surat', 'Surat City': 'Surat'}
        )
    if 'Status' in df.columns:
        df['Status'] = df['Status'].fillna('Inquiry').astype(str)
    return df


@st.cache_data(show_spinner=False)
def compute_kpis(df: pd.DataFrame):
    if df.empty:
        return 0, 0, 0
    total = len(df)
    submitted = df['Status'].str.contains('Submitted|Submit', na=False, case=False).sum() if 'Status' in df.columns else 0
    confirmed = get_confirmed_count(df)
    return total, int(submitted), int(confirmed)


@st.cache_data(show_spinner=False)
def get_confirmed_count(df: pd.DataFrame) -> int:
    if df.empty:
        return 0
    if 'Confirmed' in df.columns:
        return int(df['Confirmed'].astype(str).str.contains('Yes|True|1', na=False, case=False).sum())
    if 'Confirmation Date' in df.columns:
        return int(df['Confirmation Date'].notna().sum())
    if 'Status' in df.columns:
        return int(df['Status'].str.contains('Confirmed|Confirm|Admitted', na=False, case=False).sum())
    return 0


def wrap_chart(fig, height=500, xaxis_extra=None, yaxis_extra=None):
    """Apply shared dark theme + wrap in glass div."""
    apply_layout(fig, height=height, xaxis_extra=xaxis_extra, yaxis_extra=yaxis_extra)
    st.markdown('<div class="chart-glass">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)


# ====================== LOAD & CLEAN ======================
with st.spinner("Loading data…"):
    raw_df = load_all_data()
    df = clean_data(raw_df)

# ====================== SIDEBAR ======================
with st.sidebar:
    st.markdown(f"""
    <div style="padding:24px 16px 20px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:16px;">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,#3b82f6,#8b5cf6);
                        display:flex;align-items:center;justify-content:center;font-size:1.1rem;flex-shrink:0;">🎓</div>
            <div>
                <div style="font-size:0.65rem;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#3b82f6;">Sarvajanik</div>
                <div style="font-size:0.9rem;font-weight:700;color:#e2e8f0;line-height:1.2;">University</div>
            </div>
        </div>
        <div style="padding:12px 14px;background:rgba(96,165,250,0.07);border:1px solid rgba(96,165,250,0.18);
                    border-radius:12px;margin-bottom:4px;">
            <div style="font-size:0.65rem;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:.1em;margin-bottom:4px;">Total Records</div>
            <div style="font-size:1.6rem;font-weight:800;color:#60a5fa;letter-spacing:-0.5px;">{len(df):,}</div>
        </div>
    </div>
    <div style="padding:0 16px 8px;">
        <div style="font-size:0.65rem;font-weight:700;letter-spacing:.14em;text-transform:uppercase;
                    color:#475569;margin-bottom:8px;padding-left:4px;">Navigate</div>
    </div>
    """, unsafe_allow_html=True)

    NAV_ITEMS = [
        "🏠 Home Overview",
        "📈 Inquiry Funnel",
        "🏆 Program Popularity",
        "🗺️ Geographic Analysis",
        "👥 Gender Analysis",
        "📚 Board & Stream",
        "🔮 Advanced Analytics",
    ]

    # Initialise session state
    if "page" not in st.session_state:
        st.session_state["page"] = NAV_ITEMS[0]

    for item in NAV_ITEMS:
        is_active = st.session_state["page"] == item
        active_style = (
            "background:rgba(96,165,250,0.15);color:#60a5fa;border:1px solid rgba(96,165,250,0.3);"
            if is_active else
            "background:transparent;color:#94a3b8;border:1px solid transparent;"
        )
        if st.button(
            item,
            key=f"nav_{item}",
            use_container_width=True,
            help=item,
        ):
            st.session_state["page"] = item
            st.rerun()

    # Build active-item highlight CSS (targets the nth button in sidebar)
    active_idx = NAV_ITEMS.index(st.session_state["page"])
    active_css = f"""
    <style>
        /* Base nav button style */
        [data-testid="stSidebar"] .stButton > button {{
            background: transparent !important;
            border: 1px solid transparent !important;
            border-radius: 12px !important;
            color: #94a3b8 !important;
            font-size: 0.92rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            padding: 10px 14px !important;
            margin-bottom: 3px !important;
            transition: all 0.2s ease !important;
            width: 100% !important;
            justify-content: flex-start !important;
        }}
        [data-testid="stSidebar"] .stButton > button:hover {{
            background: rgba(96,165,250,0.10) !important;
            color: #e2e8f0 !important;
            border-color: rgba(96,165,250,0.15) !important;
        }}
        [data-testid="stSidebar"] .stButton > button:focus {{
            box-shadow: none !important;
            outline: none !important;
        }}
        /* Active item highlight */
        [data-testid="stSidebar"] .stButton:nth-of-type({active_idx + 1}) > button {{
            background: rgba(96,165,250,0.15) !important;
            color: #60a5fa !important;
            border-color: rgba(96,165,250,0.3) !important;
            font-weight: 600 !important;
        }}
    </style>
    """
    st.markdown(active_css, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style="padding:0 16px 20px;margin-top:auto;">
        <div style="padding:10px 12px;background:rgba(52,211,153,0.06);border:1px solid rgba(52,211,153,0.15);
                    border-radius:10px;font-size:0.72rem;color:#64748b;text-align:center;">
            📊 Analytics Dashboard v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.get("page", NAV_ITEMS[0])

# ====================== PAGES ======================

if page == "🏠 Home Overview":
    st.markdown('<span class="section-label">Dashboard</span>', unsafe_allow_html=True)
    st.title("Admission Analytics")
    st.markdown('<h2>2023 – 2027 · Sarvajanik University</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    total, submitted, confirmed = compute_kpis(df)
    conv = round(confirmed / total * 100, 1) if total > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "card-blue",   "Total Inquiries",       f"{total:,}",     "All-time records"),
        (c2, "card-green",  "Submitted",             f"{submitted:,}", "Applications filed"),
        (c3, "card-amber",  "Confirmed Admissions",  f"{confirmed:,}", "Seat confirmed"),
        (c4, "card-violet", "Conversion Rate",       f"{conv}%",       "Inquiry → Admit"),
    ]
    for col, cls, label, value, sub in cards:
        with col:
            st.markdown(f"""
            <div class="glass-card {cls}">
                <div class="card-label">{label}</div>
                <div class="card-value">{value}</div>
                <div class="card-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty and 'Program_Select_1' in df.columns:
        top10 = df['Program_Select_1'].value_counts().head(10)
        fig = px.bar(top10, text_auto=True, title="Top 10 Most Applied Programs",
                     color_discrete_sequence=COLORS)
        fig.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
        wrap_chart(fig)

elif page == "📈 Inquiry Funnel":
    st.markdown('<span class="section-label">Conversion</span>', unsafe_allow_html=True)
    st.title("Inquiry Funnel")
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty:
        total, submitted, confirmed = compute_kpis(df)
        fig = go.Figure(go.Funnel(
            y=['Total Inquiries', 'Submitted', 'Confirmed'],
            x=[total, submitted, confirmed],
            textinfo="value+percent initial",
            marker=dict(color=['#60a5fa', '#34d399', '#fbbf24'],
                        line=dict(color='rgba(0,0,0,0.2)', width=1)),
            connector=dict(line=dict(color='rgba(255,255,255,0.06)', width=2))
        ))
        fig.update_layout(title="Admission Conversion Funnel")
        wrap_chart(fig, height=550)

        # Mini KPI row
        rate_sub = round(submitted / total * 100, 1) if total else 0
        rate_con = round(confirmed / total * 100, 1) if total else 0
        c1, c2, c3 = st.columns(3)
        for col, label, val, cls in [
            (c1, "Inquiry → Submit", f"{rate_sub}%", "card-green"),
            (c2, "Inquiry → Confirm", f"{rate_con}%", "card-amber"),
            (c3, "Drop-off Rate", f"{round(100-rate_sub,1)}%", "card-violet"),
        ]:
            with col:
                st.markdown(f'<div class="glass-card {cls}"><div class="card-label">{label}</div><div class="card-value">{val}</div></div>', unsafe_allow_html=True)

elif page == "🏆 Program Popularity":
    st.markdown('<span class="section-label">Programs</span>', unsafe_allow_html=True)
    st.title("Program Popularity")
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty and 'Program_Select_1' in df.columns:
        top15 = df['Program_Select_1'].value_counts().head(15).reset_index()
        top15.columns = ['Program', 'Count']
        fig = px.bar(top15, x='Count', y='Program', orientation='h',
                     text_auto=True, title="Top 15 Programs by Demand",
                     color='Count', color_continuous_scale='Blues')
        fig.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
        wrap_chart(fig, height=560, yaxis_extra={'categoryorder': 'total ascending'})

elif page == "🗺️ Geographic Analysis":
    st.markdown('<span class="section-label">Geography</span>', unsafe_allow_html=True)
    st.title("Geographic Analysis")
    st.markdown('<h2>Surat & South Gujarat focus</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty and 'City' in df.columns:
        c1, c2 = st.columns([3, 2])
        with c1:
            city_count = df['City'].value_counts().head(15).reset_index()
            city_count.columns = ['City', 'Count']
            fig1 = px.bar(city_count, x='Count', y='City', orientation='h',
                          text_auto=True, title="Top 15 Cities by Inquiries",
                          color='Count', color_continuous_scale='Blues')
            wrap_chart(fig1, height=480, yaxis_extra={'categoryorder': 'total ascending'})
        with c2:
            surat_count = (df['City'] == 'Surat').sum()
            other_count = len(df) - surat_count
            fig2 = px.pie(
                values=[surat_count, other_count],
                names=['Surat', 'Other Regions'],
                title="Surat vs Rest", hole=0.55,
                color_discrete_sequence=['#60a5fa', '#1e3a5f']
            )
            fig2.update_traces(textfont_color='#e2e8f0', marker_line_color='rgba(0,0,0,0.2)')
            wrap_chart(fig2, height=480)

elif page == "👥 Gender Analysis":
    st.markdown('<span class="section-label">Demographics</span>', unsafe_allow_html=True)
    st.title("Gender Analysis")
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty and 'Gender' in df.columns and 'Program_Select_1' in df.columns:
        c1, c2 = st.columns([2, 3])
        with c1:
            gender_dist = df['Gender'].value_counts()
            fig1 = px.pie(names=gender_dist.index, values=gender_dist.values,
                          title="Gender Distribution", hole=0.5,
                          color_discrete_sequence=['#60a5fa', '#f472b6', '#a78bfa'])
            fig1.update_traces(textfont_color='#e2e8f0', marker_line_color='rgba(0,0,0,0)')
            wrap_chart(fig1, height=380)
        with c2:
            top_progs = df['Program_Select_1'].value_counts().head(8).index
            gp = (df[df['Program_Select_1'].isin(top_progs)]
                  .groupby(['Gender', 'Program_Select_1'], observed=True)
                  .size().reset_index(name='Count'))
            fig2 = px.bar(gp, x='Program_Select_1', y='Count', color='Gender',
                          title="Program Preference by Gender", barmode='group',
                          color_discrete_sequence=['#60a5fa', '#f472b6', '#a78bfa'])
            wrap_chart(fig2, height=380, xaxis_extra={'tickangle': -30})

        st.markdown('<hr class="divider"/>', unsafe_allow_html=True)
        gender_stats = (
            df.groupby('Gender', observed=True)['Status']
            .agg(
                Total='count',
                Submitted=lambda x: x.str.contains('Submitted|Submit', na=False, case=False).sum(),
                Confirmed=lambda x: x.str.contains('Confirmed|Confirm|Admitted', na=False, case=False).sum()
            )
            .reset_index()
        )
        gender_stats['Conversion_%'] = (gender_stats['Confirmed'] / gender_stats['Total'] * 100).round(1).fillna(0)
        fig3 = px.bar(gender_stats, x='Gender', y='Conversion_%', text_auto=True,
                      title="Conversion Rate by Gender (%)",
                      color_discrete_sequence=['#a78bfa'])
        fig3.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
        wrap_chart(fig3)

elif page == "📚 Board & Stream":
    st.markdown('<span class="section-label">Academic Background</span>', unsafe_allow_html=True)
    st.title("Board & Stream Analysis")
    st.markdown('<h2>GSEB · CBSE · ICSE &nbsp;·&nbsp; Science · Commerce · Arts</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty:
        # Vectorised board detection — scan entire row as one string
        combined = df.astype(str).agg(' '.join, axis=1).str.upper()
        gseb_count = int(combined.str.contains('GSEB').sum())
        cbse_count = int(combined.str.contains('CBSE').sum())
        icse_count = int(combined.str.contains('ICSE').sum())
        other_count = max(0, len(df) - gseb_count - cbse_count - icse_count)

        board_df = pd.DataFrame({
            'Board':  ['GSEB', 'CBSE', 'ICSE', 'Other'],
            'Count':  [gseb_count, cbse_count, icse_count, other_count],
        })
        # Drop boards with 0 students
        board_df = board_df[board_df['Count'] > 0].reset_index(drop=True)

        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.bar(
                board_df, x='Board', y='Count', text_auto=True,
                title="Students by Board",
                color='Board',
                color_discrete_map={'GSEB': '#60a5fa', 'CBSE': '#34d399', 'ICSE': '#fbbf24', 'Other': '#64748b'},
            )
            fig1.update_traces(marker_line_width=0, textfont_color='#e2e8f0')
            wrap_chart(fig1, height=420)

        with c2:
            fig2 = px.pie(
                board_df, names='Board', values='Count',
                title="Board Distribution", hole=0.48,
                color='Board',
                color_discrete_map={'GSEB': '#60a5fa', 'CBSE': '#34d399', 'ICSE': '#fbbf24', 'Other': '#64748b'},
            )
            fig2.update_traces(
                textfont_color='#e2e8f0',
                textinfo='label+percent',
                marker_line_color='rgba(0,0,0,0.15)',
                marker_line_width=2,
                pull=[0.04, 0.04, 0.04, 0],
            )
            wrap_chart(fig2, height=420)

        # ── end of Board & Stream page ──

elif page == "🔮 Advanced Analytics":
    st.markdown('<span class="section-label">Intelligence</span>', unsafe_allow_html=True)
    st.title("Advanced Analytics")
    st.markdown('<h2>Trends, Forecasts & Recommendations</h2>', unsafe_allow_html=True)
    st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

    if not df.empty:
        c1, c2 = st.columns(2)
        with c1:
            if 'Year' in df.columns and 'Status' in df.columns:
                yearly = (
                    df.groupby('Year')['Status']
                    .agg(
                        Total='count',
                        Confirmed=lambda x: x.str.contains('Confirmed|Confirm|Admitted', na=False, case=False).sum()
                    )
                    .reset_index()
                )
                yearly['Conversion_%'] = (yearly['Confirmed'] / yearly['Total'] * 100).round(1)
                fig1 = px.line(yearly, x='Year', y='Conversion_%', markers=True,
                               title="Year-wise Conversion Rate Trend",
                               color_discrete_sequence=['#60a5fa'])
                fig1.update_traces(line_width=3, marker_size=8, marker_color='#a78bfa')
                wrap_chart(fig1)

        with c2:
            st.markdown("**🎯 Program Recommendation**")
            marks = st.slider("Your 12th Grade Percentage", 40, 100, 75)
            if marks >= 85:
                rec, icon = "B.Tech / B.Sc. (IT) / Biotechnology", "🥇"
            elif marks >= 70:
                rec, icon = "BBA / B.Com / B.Sc. Programs", "🥈"
            elif marks >= 60:
                rec, icon = "B.A. / General Undergraduate", "🥉"
            else:
                rec, icon = "Diploma / Foundation Courses", "📘"
            st.markdown(f"**{icon} Recommended:** {rec}")

        st.markdown('<hr class="divider"/>', unsafe_allow_html=True)

        total, _, confirmed = compute_kpis(df)
        occ_rate = round(confirmed / max(total, 1) * 100, 1)
        c3, c4, c5 = st.columns(3)
        with c3: st.metric("Seat Occupancy Rate", f"{occ_rate}%")
        with c4: st.metric("Total Records", f"{total:,}")
        with c5: st.metric("Confirmed Admissions", f"{confirmed:,}")

        st.info("**Roadmap** · ML-based admission forecasting · AI chatbot for student queries · Personalised program recommendation engine")

# ====================== FOOTER ======================
st.markdown('<hr class="divider"/>', unsafe_allow_html=True)
st.success("✅ Dashboard loaded successfully")
