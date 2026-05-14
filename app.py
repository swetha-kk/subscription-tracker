import streamlit as st
import pandas as pd

st.set_page_config(page_title="Subscription Waste Tracker", page_icon="💸", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0e0e0e;
        color: #f0f0f0;
    }
    h1, h2, h3 {
        font-family: 'Syne', sans-serif;
    }
    .stApp { background-color: #0e0e0e; }

    .big-title {
        font-family: 'Syne', sans-serif;
        font-size: 2.6rem;
        font-weight: 800;
        color: #f0f0f0;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #888;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #1a1a1a;
        border: 1px solid #2a2a2a;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 0.78rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-family: 'Syne', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        color: #f0f0f0;
    }
    .waste-value { color: #ff4d4d; }
    .save-value  { color: #39d98a; }
    .warn-box {
        background: #1f1010;
        border-left: 4px solid #ff4d4d;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        font-size: 0.95rem;
        color: #ffaaaa;
    }
    .good-box {
        background: #0f1f15;
        border-left: 4px solid #39d98a;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-top: 1rem;
        font-size: 0.95rem;
        color: #a0ffc8;
    }
    </style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────────────
st.markdown('<div class="big-title">💸 Subscription Waste Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Find out how much you\'re spending — and wasting — every month.</div>', unsafe_allow_html=True)

# ── Default subscriptions ────────────────────────────────────────────────────
DEFAULT_SUBS = [
    {"name": "Netflix",  "cost": 649.0,  "used": True},
    {"name": "Spotify",  "cost": 119.0,  "used": True},
    {"name": "Amazon Prime", "cost": 299.0, "used": True},
    {"name": "YouTube Premium", "cost": 189.0, "used": False},
    {"name": "Disney+", "cost": 299.0, "used": False},
]

# ── Session state ────────────────────────────────────────────────────────────
if "subscriptions" not in st.session_state:
    st.session_state.subscriptions = DEFAULT_SUBS.copy()

subs = st.session_state.subscriptions

# ── Add new subscription ─────────────────────────────────────────────────────
st.markdown("### ➕ Add a Subscription")
col1, col2, col3 = st.columns([3, 2, 1])
with col1:
    new_name = st.text_input("Service Name", placeholder="e.g. Hotstar, Canva...")
with col2:
    new_cost = st.number_input("Monthly Cost (₹)", min_value=0.0, step=10.0, value=0.0)
with col3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Add", use_container_width=True):
        if new_name.strip():
            subs.append({"name": new_name.strip(), "cost": new_cost, "used": True})
            st.success(f"Added {new_name}!")

st.divider()

# ── Edit subscriptions table ─────────────────────────────────────────────────
st.markdown("### 📋 Your Subscriptions")
st.caption("Uncheck 'Do you use it?' for subscriptions you barely use.")

to_delete = []
for i, sub in enumerate(subs):
    c1, c2, c3, c4 = st.columns([3, 2, 2, 1])
    with c1:
        subs[i]["name"] = st.text_input("Name", value=sub["name"], key=f"name_{i}", label_visibility="collapsed")
    with c2:
        subs[i]["cost"] = st.number_input("Cost", value=sub["cost"], min_value=0.0, step=10.0, key=f"cost_{i}", label_visibility="collapsed")
    with c3:
        subs[i]["used"] = st.checkbox("Do you use it?", value=sub["used"], key=f"used_{i}")
    with c4:
        if st.button("🗑️", key=f"del_{i}"):
            to_delete.append(i)

for i in reversed(to_delete):
    subs.pop(i)

st.divider()

# ── Calculations ─────────────────────────────────────────────────────────────
total_monthly  = sum(s["cost"] for s in subs)
total_yearly   = total_monthly * 12
wasted_monthly = sum(s["cost"] for s in subs if not s["used"])
wasted_yearly  = wasted_monthly * 12
used_monthly   = total_monthly - wasted_monthly

st.markdown("### 📊 Your Summary")

col_a, col_b = st.columns(2)
with col_a:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Monthly Spend</div>
        <div class="metric-value">₹{total_monthly:,.0f}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Yearly Spend</div>
        <div class="metric-value">₹{total_yearly:,.0f}</div>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Wasted Monthly</div>
        <div class="metric-value waste-value">₹{wasted_monthly:,.0f}</div>
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Wasted Yearly</div>
        <div class="metric-value waste-value">₹{wasted_yearly:,.0f}</div>
    </div>""", unsafe_allow_html=True)

# ── Insight message ──────────────────────────────────────────────────────────
if wasted_monthly > 0:
    unused_names = [s["name"] for s in subs if not s["used"]]
    st.markdown(f"""
    <div class="warn-box">
        🚨 You're wasting <strong>₹{wasted_monthly:,.0f}/month</strong> on unused subscriptions:
        {', '.join(unused_names)}.<br>
        Cancel them to save <strong>₹{wasted_yearly:,.0f} per year</strong>!
    </div>""", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="good-box">
        ✅ Great job! You're using all your subscriptions. No waste detected.
    </div>""", unsafe_allow_html=True)

# ── Bar chart ────────────────────────────────────────────────────────────────
st.divider()
st.markdown("### 📈 Spend Breakdown")

if subs:
    df = pd.DataFrame(subs)
    df["Status"] = df["used"].map({True: "✅ Used", False: "❌ Unused"})
    df = df.rename(columns={"name": "Service", "cost": "Monthly Cost (₹)"})
    chart_df = df.set_index("Service")[["Monthly Cost (₹)"]]
    st.bar_chart(chart_df)

    st.markdown("#### All Subscriptions")
    st.dataframe(
        df[["Service", "Monthly Cost (₹)", "Status"]],
        use_container_width=True,
        hide_index=True
    )
