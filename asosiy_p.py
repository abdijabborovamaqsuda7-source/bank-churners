import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────────
#  SAHIFA SOZLAMALARI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="💳 Kredit Karta Tahlili",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STIL
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ---- metric kartalar ---- */
.metric-box {
    background: linear-gradient(135deg, #1a1f2e 0%, #252b3d 100%);
    border: 1px solid #2e3650;
    border-radius: 14px;
    padding: 22px 24px;
    text-align: center;
    margin-bottom: 4px;
}
.metric-box .m-icon { font-size: 2rem; margin-bottom: 4px; }
.metric-box .m-label {
    font-size: 0.78rem;
    color: #8b95b0;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}
.metric-box .m-value {
    font-size: 1.85rem;
    font-weight: 700;
    color: #f0f4ff;
}
.metric-box .m-sub {
    font-size: 0.78rem;
    color: #4ade80;
    margin-top: 4px;
}
.metric-box.red   { border-color: #f87171; }
.metric-box.green { border-color: #4ade80; }
.metric-box.blue  { border-color: #60a5fa; }
.metric-box.amber { border-color: #fbbf24; }

/* ---- bo'lim sarlavhalari ---- */
.section-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #e2e8f0;
    border-left: 4px solid #3b82f6;
    padding-left: 12px;
    margin: 28px 0 16px;
}

/* ---- info kartalar ---- */
.info-card {
    background: #1a1f2e;
    border: 1px solid #2e3650;
    border-radius: 12px;
    padding: 18px 20px;
    margin-bottom: 12px;
}
.info-card h4 { color: #93c5fd; margin: 0 0 6px; font-size: 0.95rem; }
.info-card p  { color: #94a3b8; margin: 0; font-size: 0.88rem; }

/* ---- sidebar ---- */
[data-testid="stSidebar"] { background: #0f1117; border-right: 1px solid #1e2330; }
[data-testid="stSidebar"] .stSelectbox label { color: #94a3b8 !important; }

/* ---- asosiy fon ---- */
[data-testid="stAppViewContainer"] { background: #0d1117; }
[data-testid="block-container"] { padding-top: 1.5rem; }

/* ---- jadval ---- */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ---- ajratuvchi chiziq ---- */
hr { border-color: #1e2330 !important; }

/* ---- tugma ---- */
.stButton > button {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 32px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.2s;
    width: 100%;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(59,130,246,0.35);
}

/* ---- slider ---- */
.stSlider [data-baseweb="slider"] { color: #3b82f6; }

/* ---- tavsiya oynasi ---- */
.risk-box {
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 16px;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
}
.risk-high { background: rgba(239,68,68,0.15); border: 1px solid #ef4444; color: #fca5a5; }
.risk-low  { background: rgba(34,197,94,0.15); border: 1px solid #22c55e; color: #86efac; }
.risk-mid  { background: rgba(251,191,36,0.15); border: 1px solid #fbbf24; color: #fde68a; }

/* ---- jamoa kartasi ---- */
.team-card {
    background: linear-gradient(135deg, #1a1f2e, #252b3d);
    border: 1px solid #2e3650;
    border-radius: 14px;
    padding: 28px;
    text-align: center;
}
.team-card .avatar {
    width: 72px; height: 72px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    margin: 0 auto 12px;
}
.team-card h3 { color: #e2e8f0; margin: 0 0 4px; font-size: 1.05rem; }
.team-card p  { color: #64748b; margin: 0; font-size: 0.82rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PLOTLY MAVZU
# ─────────────────────────────────────────────
PLOTLY_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a3b8"),
    title_font=dict(size=15, color="#e2e8f0"),
    margin=dict(l=30, r=20, t=48, b=30),
)
COLORS = {
    "faol":   "#4ade80",
    "ketgan": "#f87171",
    "erkak":  "#60a5fa",
    "ayol":   "#f472b6",
    "seq":    px.colors.sequential.Blues_r,
    "qual":   ["#60a5fa","#f472b6","#fbbf24","#4ade80","#c084fc","#fb923c"],
}

# ─────────────────────────────────────────────
#  MA'LUMOT YUKLASH + O'ZBEK TARJIMA
# ─────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("BankChurners.csv")
    # keraksiz ustunlarni o'chirish
    drop_cols = [c for c in df.columns if "Naive_Bayes" in c or "CLIENTNUM" == c]
    df.drop(columns=drop_cols, inplace=True, errors="ignore")

    # O'zbek tarjimalari
    df["Holat"] = df["Attrition_Flag"].map({
        "Existing Customer": "Faol mijoz",
        "Attrited Customer": "Ketgan mijoz",
    })
    df["Jins"] = df["Gender"].map({"M": "Erkak", "F": "Ayol"})
    df["Yosh"] = df["Customer_Age"]
    df["Kredit_limiti"] = df["Credit_Limit"]
    df["Tranzaksiya_summasi"] = df["Total_Trans_Amt"]
    df["Tranzaksiya_soni"] = df["Total_Trans_Ct"]
    df["Revolving_balans"] = df["Total_Revolving_Bal"]
    df["Foydalanish_darajasi"] = df["Avg_Utilization_Ratio"]
    df["Karta_turi"] = df["Card_Category"]
    df["Munosabat_muddati"] = df["Months_on_book"]
    df["Bog_liq_mahsulotlar"] = df["Total_Relationship_Count"]

    # Ta'lim darajasi tarjimasi
    edu_map = {
        "Graduate": "Oliy ma'lumotli",
        "High School": "O'rta ta'lim",
        "Unknown": "Noma'lum",
        "Uneducated": "Ta'limsiz",
        "College": "Kollej",
        "Post-Graduate": "Magistr",
        "Doctorate": "Doktorant",
    }
    df["Talim"] = df["Education_Level"].map(edu_map).fillna(df["Education_Level"])

    # Oilaviy holat
    marital_map = {
        "Married": "Turmush qurgan",
        "Single": "Turmush qurmagan",
        "Unknown": "Noma'lum",
        "Divorced": "Ajrashgan",
    }
    df["Oilaviy_holat"] = df["Marital_Status"].map(marital_map).fillna(df["Marital_Status"])

    # Daromad toifasi
    income_map = {
        "Less than $40K": "< $40K",
        "$40K - $60K": "$40K–$60K",
        "$60K - $80K": "$60K–$80K",
        "$80K - $120K": "$80K–$120K",
        "$120K +": "> $120K",
        "Unknown": "Noma'lum",
    }
    df["Daromad"] = df["Income_Category"].map(income_map).fillna(df["Income_Category"])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("⚠️  **BankChurners.csv** fayli topilmadi!")
    st.info("CSV faylni `app.py` bilan bir papkaga joylashtiring.")
    st.stop()

# ─────────────────────────────────────────────
#  YON MENYU
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 24px;'>
        <div style='font-size:2.2rem;'>💳</div>
        <div style='font-size:1.1rem; font-weight:700; color:#e2e8f0; margin-top:6px;'>
            Kredit Karta
        </div>
        <div style='font-size:0.78rem; color:#64748b; margin-top:2px;'>
            Mijozlar tahlili tizimi
        </div>
    </div>
    """, unsafe_allow_html=True)

    sahifa = st.selectbox(
        "Bo'limni tanlang",
        ["🏠  Umumiy ko'rinish",
         "📊  Vizual tahlil",
         "🔍  Mijozlarni qidirish",
         "🔮  Xavfni baholash",
         "📋  Dataset",
         "👥  Jamoa"],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Yon menyu filtrlari
    st.markdown("**🎛️  Filtrlar**")
    jins_filter = st.multiselect(
        "Jins",
        options=["Erkak", "Ayol"],
        default=["Erkak", "Ayol"],
    )
    holat_filter = st.multiselect(
        "Mijoz holati",
        options=["Faol mijoz", "Ketgan mijoz"],
        default=["Faol mijoz", "Ketgan mijoz"],
    )
    karta_filter = st.multiselect(
        "Karta turi",
        options=sorted(df["Karta_turi"].unique()),
        default=sorted(df["Karta_turi"].unique()),
    )

# Filtr qo'llash
dff = df[
    df["Jins"].isin(jins_filter) &
    df["Holat"].isin(holat_filter) &
    df["Karta_turi"].isin(karta_filter)
].copy()

# ─────────────────────────────────────────────
#  YORDAMCHI FUNKSIYALAR
# ─────────────────────────────────────────────
def metric_card(icon, label, value, sub="", color="blue"):
    st.markdown(f"""
    <div class="metric-box {color}">
        <div class="m-icon">{icon}</div>
        <div class="m-label">{label}</div>
        <div class="m-value">{value}</div>
        {"<div class='m-sub'>" + sub + "</div>" if sub else ""}
    </div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

def apply_theme(fig, height=400):
    fig.update_layout(height=height, **PLOTLY_THEME)
    return fig

# ═══════════════════════════════════════════════
#  1. UMUMIY KO'RINISH
# ═══════════════════════════════════════════════
if "Umumiy" in sahifa:

    st.markdown("""
    <h1 style='color:#e2e8f0; font-size:2rem; margin-bottom:4px;'>
        💳 Kredit Karta Mijozlari Tahlili
    </h1>
    <p style='color:#64748b; font-size:1rem; margin-bottom:28px;'>
        Bank mijozlari ma'lumotlariga asoslangan interaktiv tahlil paneli
    </p>
    """, unsafe_allow_html=True)

    # ── KPI qatorlar ──────────────────────────────
    jami      = len(dff)
    faol_n    = (dff["Holat"] == "Faol mijoz").sum()
    ketgan_n  = (dff["Holat"] == "Ketgan mijoz").sum()
    churn_pct = round(ketgan_n / jami * 100, 1) if jami else 0
    ort_limit = f"${dff['Kredit_limiti'].mean():,.0f}"
    ort_trans = f"${dff['Tranzaksiya_summasi'].mean():,.0f}"

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: metric_card("👥", "Jami mijozlar",       f"{jami:,}",     color="blue")
    with c2: metric_card("✅", "Faol mijozlar",        f"{faol_n:,}",   color="green")
    with c3: metric_card("❌", "Ketgan mijozlar",      f"{ketgan_n:,}", sub=f"Churn: {churn_pct}%", color="red")
    with c4: metric_card("💰", "O'rt. kredit limiti",  ort_limit,       color="amber")
    with c5: metric_card("🧾", "O'rt. tranzaksiya",   ort_trans,       color="blue")

    st.markdown("---")

    # ── 2 ta asosiy grafik ────────────────────────
    section("📈 Asosiy ko'rsatkichlar")
    col1, col2 = st.columns(2)

    with col1:
        # Mijozlar holati — donut
        holat_counts = dff["Holat"].value_counts().reset_index()
        holat_counts.columns = ["Holat", "Soni"]
        fig = px.pie(
            holat_counts, names="Holat", values="Soni",
            title="Mijozlar holati ulushi",
            color="Holat",
            color_discrete_map={"Faol mijoz": COLORS["faol"], "Ketgan mijoz": COLORS["ketgan"]},
            hole=0.52,
        )
        fig.update_traces(textinfo="percent+label", textfont_size=13,
                          marker=dict(line=dict(color="#0d1117", width=2)))
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        # Yosh bo'yicha taqsimot — histogram
        fig = px.histogram(
            dff, x="Yosh", color="Holat", nbins=25,
            title="Yosh bo'yicha mijozlar taqsimoti",
            color_discrete_map={"Faol mijoz": COLORS["faol"], "Ketgan mijoz": COLORS["ketgan"]},
            barmode="overlay", opacity=0.78,
            labels={"Yosh": "Yosh", "count": "Mijozlar soni"},
        )
        fig.update_traces(marker_line_width=0)
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    # ── Ikkinchi qator ────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        # Jins bo'yicha holat — grouped bar
        jins_holat = dff.groupby(["Jins", "Holat"]).size().reset_index(name="Soni")
        fig = px.bar(
            jins_holat, x="Jins", y="Soni", color="Holat", barmode="group",
            title="Jins bo'yicha faol/ketgan mijozlar",
            color_discrete_map={"Faol mijoz": COLORS["faol"], "Ketgan mijoz": COLORS["ketgan"]},
            labels={"Soni": "Mijozlar soni", "Jins": "Jins"},
            text="Soni",
        )
        fig.update_traces(textposition="outside")
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col4:
        # Karta turi bo'yicha — horizontal bar
        karta_holat = dff.groupby(["Karta_turi", "Holat"]).size().reset_index(name="Soni")
        fig = px.bar(
            karta_holat, y="Karta_turi", x="Soni", color="Holat",
            barmode="stack", orientation="h",
            title="Karta turi bo'yicha holat",
            color_discrete_map={"Faol mijoz": COLORS["faol"], "Ketgan mijoz": COLORS["ketgan"]},
            labels={"Soni": "Soni", "Karta_turi": "Karta turi"},
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

# ═══════════════════════════════════════════════
#  2. VIZUAL TAHLIL
# ═══════════════════════════════════════════════
elif "Vizual" in sahifa:

    st.markdown("""
    <h1 style='color:#e2e8f0; font-size:2rem; margin-bottom:24px;'>
        📊 Chuqur vizual tahlil
    </h1>""", unsafe_allow_html=True)

    # ── Kredit limiti taqsimoti ──────────────────
    section("💰 Kredit limiti tahlili")
    col1, col2 = st.columns(2)

    with col1:
        fig = px.box(
            dff, x="Holat", y="Kredit_limiti", color="Holat",
            title="Holat bo'yicha kredit limiti",
            color_discrete_map={"Faol mijoz": COLORS["faol"], "Ketgan mijoz": COLORS["ketgan"]},
            labels={"Kredit_limiti": "Kredit limiti ($)", "Holat": ""},
            points="outliers",
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    with col2:
        fig = px.histogram(
            dff, x="Kredit_limiti", color="Jins", nbins=30,
            title="Jins bo'yicha kredit limiti taqsimoti",
            color_discrete_map={"Erkak": COLORS["erkak"], "Ayol": COLORS["ayol"]},
            barmode="overlay", opacity=0.75,
            labels={"Kredit_limiti": "Kredit limiti ($)", "count": "Mijozlar"},
        )
        st.plotly_chart(apply_theme(fig), use_container_width=True)

    # ── Tranzaksiyalar tahlili ───────────────────
    section("🧾 Tranzaksiya tahlili")
    col3, col4 = st.columns(2)

    with col3:
        fig = px.scatter(
            dff.sample(min(2000, len(dff)), random_state=1),
            x="Tranzaksiya_soni", y="Tranzaksiya_summasi",
            color="Holat", size="Kredit_limiti",
            title="Tranzaksiya soni vs Summasi",
            color_discrete_map={"Faol mijoz": COLORS["faol"], "Ketgan mijoz": COLORS["ketgan"]},
            labels={
                "Tranzaksiya_soni": "Tranzaksiya soni",
                "Tranzaksiya_summasi": "Tranzaksiya summasi ($)",
            },
            opacity=0.65,
        )
        st.plotly_chart(apply_theme(fig, 420), use_container_width=True)

    with col4:
        fig = px.violin(
            dff, y="Tranzaksiya_soni", x="Karta_turi", color="Holat",
            box=True, points=False,
            title="Karta turi bo'yicha tranzaksiyalar soni",
            color_discrete_map={"Faol mijoz": COLORS["faol"], "Ketgan mijoz": COLORS["ketgan"]},
            labels={"Tranzaksiya_soni": "Tranzaksiya soni", "Karta_turi": "Karta turi"},
        )
        st.plotly_chart(apply_theme(fig, 420), use_container_width=True)

    # ── Demografiya tahlili ──────────────────────
    section("👤 Demografik tahlil")
    col5, col6 = st.columns(2)

    with col5:
        edu_counts = dff["Talim"].value_counts().reset_index()
        edu_counts.columns = ["Talim", "Soni"]
        fig = px.bar(
            edu_counts.sort_values("Soni"), x="Soni", y="Talim",
            orientation="h", title="Ta'lim darajasi bo'yicha mijozlar",
            color="Soni", color_continuous_scale="Blues",
            labels={"Soni": "Mijozlar soni", "Talim": ""},
        )
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(apply_theme(fig, 380), use_container_width=True)

    with col6:
        daromad_order = ["< $40K","$40K–$60K","$60K–$80K","$80K–$120K","> $120K","Noma'lum"]
        dar_churn = (
            dff[dff["Holat"] == "Ketgan mijoz"]["Daromad"]
            .value_counts()
            .reindex(daromad_order, fill_value=0)
            .reset_index()
        )
        dar_churn.columns = ["Daromad", "Soni"]
        fig = px.bar(
            dar_churn, x="Daromad", y="Soni",
            title="Daromad toifasiga ko'ra ketgan mijozlar",
            color="Soni", color_continuous_scale="Reds",
            labels={"Soni": "Ketgan mijozlar", "Daromad": "Daromad toifasi"},
        )
        fig.update_coloraxes(showscale=False)
        st.plotly_chart(apply_theme(fig, 380), use_container_width=True)

    # ── Korrelyatsiya issiqlik xaritasi ─────────
    section("🗺️  Ko'rsatkichlar o'rtasidagi bog'liqlik")
    num_cols = ["Yosh", "Kredit_limiti", "Tranzaksiya_summasi",
                "Tranzaksiya_soni", "Revolving_balans", "Foydalanish_darajasi",
                "Munosabat_muddati", "Bog_liq_mahsulotlar"]
    uz_names = ["Yosh", "Kredit limiti", "Trans. summa",
                "Trans. soni", "Revolving balans", "Foydalanish %",
                "Munosabat muddati", "Bog'liq mahsulotlar"]
    corr = dff[num_cols].corr()
    corr.columns = uz_names
    corr.index   = uz_names
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=uz_names, y=uz_names,
        colorscale="RdBu", zmid=0,
        text=np.round(corr.values, 2),
        texttemplate="%{text}",
        textfont_size=10,
    ))
    fig.update_layout(title="Korrelyatsiya matritsasi", height=480, **PLOTLY_THEME)
    st.plotly_chart(fig, use_container_width=True)

# ═══════════════════════════════════════════════
#  3. MIJOZLARNI QIDIRISH
# ═══════════════════════════════════════════════
elif "Qidirish" in sahifa:

    st.markdown("""
    <h1 style='color:#e2e8f0; font-size:2rem; margin-bottom:24px;'>
        🔍 Mijozlarni qidirish va filtrlash
    </h1>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        jins_s = st.selectbox("Jins", ["Barchasi","Erkak","Ayol"])
    with c2:
        holat_s = st.selectbox("Holat", ["Barchasi","Faol mijoz","Ketgan mijoz"])
    with c3:
        karta_s = st.selectbox("Karta turi", ["Barchasi"] + sorted(dff["Karta_turi"].unique().tolist()))

    yosh_min, yosh_max = st.slider(
        "Yosh oralig'i", int(dff["Yosh"].min()), int(dff["Yosh"].max()),
        (int(dff["Yosh"].min()), int(dff["Yosh"].max())),
    )
    limit_min, limit_max = st.slider(
        "Kredit limiti oralig'i ($)",
        int(dff["Kredit_limiti"].min()), int(dff["Kredit_limiti"].max()),
        (int(dff["Kredit_limiti"].min()), int(dff["Kredit_limiti"].max())),
    )

    res = dff.copy()
    if jins_s  != "Barchasi": res = res[res["Jins"]  == jins_s]
    if holat_s != "Barchasi": res = res[res["Holat"] == holat_s]
    if karta_s != "Barchasi": res = res[res["Karta_turi"] == karta_s]
    res = res[(res["Yosh"] >= yosh_min) & (res["Yosh"] <= yosh_max)]
    res = res[(res["Kredit_limiti"] >= limit_min) & (res["Kredit_limiti"] <= limit_max)]

    st.markdown(f"""
    <div class='info-card'>
        <h4>🔎 Natija</h4>
        <p>Filtrlarga mos <strong style='color:#60a5fa;'>{len(res):,}</strong> ta mijoz topildi
        (jami {len(dff):,} dan).</p>
    </div>""", unsafe_allow_html=True)

    # Natijaviy ko'rsatkichlar
    if len(res) > 0:
        c1, c2, c3, c4 = st.columns(4)
        with c1: metric_card("👤","Topilgan mijozlar", f"{len(res):,}", color="blue")
        with c2: metric_card("💰","O'rt. kredit limiti", f"${res['Kredit_limiti'].mean():,.0f}", color="amber")
        with c3: metric_card("🧾","O'rt. tranzaksiya", f"${res['Tranzaksiya_summasi'].mean():,.0f}", color="green")
        with c4:
            ch = round((res["Holat"]=="Ketgan mijoz").mean()*100,1)
            metric_card("📉","Churn darajasi", f"{ch}%", color="red" if ch>20 else "green")

        section("📊 Filtrlangan ma'lumotlar tahlili")
        col1, col2 = st.columns(2)
        with col1:
            fig = px.histogram(
                res, x="Yosh", color="Holat", nbins=20,
                title="Yosh taqsimoti",
                color_discrete_map={"Faol mijoz":COLORS["faol"],"Ketgan mijoz":COLORS["ketgan"]},
            )
            st.plotly_chart(apply_theme(fig,320), use_container_width=True)
        with col2:
            fig = px.box(
                res, x="Karta_turi", y="Kredit_limiti", color="Holat",
                title="Karta turi bo'yicha kredit limiti",
                color_discrete_map={"Faol mijoz":COLORS["faol"],"Ketgan mijoz":COLORS["ketgan"]},
            )
            st.plotly_chart(apply_theme(fig,320), use_container_width=True)

        section("📋 Ma'lumotlar jadvali")
        show_cols = ["Jins","Yosh","Holat","Karta_turi","Kredit_limiti",
                     "Tranzaksiya_soni","Tranzaksiya_summasi","Talim","Daromad"]
        st.dataframe(
            res[show_cols].rename(columns={
                "Jins":"Jins","Yosh":"Yosh","Holat":"Holat",
                "Karta_turi":"Karta","Kredit_limiti":"Kredit limiti ($)",
                "Tranzaksiya_soni":"Trans. soni","Tranzaksiya_summasi":"Trans. summa ($)",
                "Talim":"Ta'lim","Daromad":"Daromad",
            }).reset_index(drop=True),
            use_container_width=True, height=380,
        )
    else:
        st.warning("Filtrlarga mos hech qanday mijoz topilmadi.")

# ═══════════════════════════════════════════════
#  4. XAVFNI BAHOLASH
# ═══════════════════════════════════════════════
elif "Xavf" in sahifa:

    st.markdown("""
    <h1 style='color:#e2e8f0; font-size:2rem; margin-bottom:6px;'>
        🔮 Mijozni yo'qotish xavfini baholash
    </h1>
    <p style='color:#64748b; margin-bottom:28px;'>
        Mijoz ma'lumotlarini kiriting va tizim bank bilan munosabatini davom
        ettirish ehtimolini taxmin qiladi.
    </p>""", unsafe_allow_html=True)

    col1, col2 = st.columns([1.2, 0.8])

    with col1:
        section("📝 Mijoz ma'lumotlari")

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            yosh_v = st.slider("👤 Mijoz yoshi", 18, 80, 42)
            karta_v = st.selectbox("💳 Karta turi", ["Blue","Silver","Gold","Platinum"])
            munosabat_v = st.slider("📅 Bank bilan munosabat (oy)", 1, 60, 36)
        with r1c2:
            kredit_v = st.number_input("💰 Kredit limiti ($)", 1000, 50000, 12000, step=500)
            daromad_v = st.selectbox("📈 Daromad toifasi", ["< $40K","$40K–$60K","$60K–$80K","$80K–$120K","> $120K"])
            mahsulot_v = st.slider("🔗 Bog'liq mahsulotlar soni", 1, 6, 3)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            trans_soni_v = st.number_input("🧾 Oxirgi yil tranzaksiyalar soni", 0, 200, 55)
            nofaol_v = st.slider("😴 Nofaol oylar soni (12 oyda)", 0, 6, 1)
        with r2c2:
            trans_summa_v = st.number_input("💵 Oxirgi yil tranzaksiya summasi ($)", 0, 20000, 4500, step=100)
            murojaat_v = st.slider("📞 Murojaatlar soni (12 oyda)", 0, 6, 2)

        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("🔮  Xavfni baholash"):
            # Balllar tizimi
            xavf_ball = 0

            if trans_soni_v < 30:      xavf_ball += 30
            elif trans_soni_v < 50:    xavf_ball += 15

            if trans_summa_v < 2000:   xavf_ball += 25
            elif trans_summa_v < 3500: xavf_ball += 12

            if nofaol_v >= 3:          xavf_ball += 20
            elif nofaol_v >= 2:        xavf_ball += 10

            if murojaat_v >= 4:        xavf_ball += 15
            elif murojaat_v >= 3:      xavf_ball += 8

            if mahsulot_v <= 2:        xavf_ball += 10
            if kredit_v > 15000 and trans_soni_v < 40: xavf_ball += 10

            # Natija
            with col2:
                section("📊 Baholash natijasi")

                if xavf_ball >= 55:
                    daraja = "YUQORI"
                    rang = "risk-high"
                    emoji = "🔴"
                    tavsiya = "Ushbu mijoz bankni tark etish xavfi **yuqori**. Darhol shaxsiy taklif va imtiyozlar bilan murojaat qiling."
                elif xavf_ball >= 30:
                    daraja = "O'RTA"
                    rang = "risk-mid"
                    emoji = "🟡"
                    tavsiya = "Ushbu mijozda **o'rta** xavf mavjud. Maxsus chegirmalar va xizmat sifatini oshirish tavsiya etiladi."
                else:
                    daraja = "PAST"
                    rang = "risk-low"
                    emoji = "🟢"
                    tavsiya = "Ushbu mijoz bank xizmatlaridan foydalanishni **davom ettirishi** kutilmoqda."

                st.markdown(f"""
                <div class="risk-box {rang}">
                    <div style="font-size:2.5rem; margin-bottom:8px;">{emoji}</div>
                    <div style="font-size:0.78rem; letter-spacing:0.1em; margin-bottom:4px;">XAVF DARAJASI</div>
                    <div style="font-size:2rem; font-weight:800;">{daraja}</div>
                    <div style="font-size:0.88rem; margin-top:8px; opacity:0.8;">Ball: {xavf_ball}/100</div>
                </div>""", unsafe_allow_html=True)

                # Omillar diagrammasi
                omillar = {
                    "Tranzaksiyalar soni": min(trans_soni_v/100, 1),
                    "Tranzaksiya summasi": min(trans_summa_v/15000, 1),
                    "Faollik darajasi": max(0, 1 - nofaol_v/6),
                    "Murojaatlar": max(0, 1 - murojaat_v/6),
                    "Mahsulotlar soni": min(mahsulot_v/6, 1),
                }
                fig = go.Figure(go.Bar(
                    x=list(omillar.values()),
                    y=list(omillar.keys()),
                    orientation="h",
                    marker=dict(
                        color=list(omillar.values()),
                        colorscale=[[0,"#ef4444"],[0.5,"#fbbf24"],[1,"#4ade80"]],
                    ),
                    text=[f"{v*100:.0f}%" for v in omillar.values()],
                    textposition="outside",
                ))
                fig.update_layout(
                    title="Omillar baholash natijasi",
                    xaxis=dict(range=[0,1.2], showticklabels=False),
                    height=260,
                    **PLOTLY_THEME,
                )
                st.plotly_chart(fig, use_container_width=True)

                st.markdown(f"""
                <div class="info-card">
                    <h4>💡 Tavsiya</h4>
                    <p>{tavsiya}</p>
                </div>""", unsafe_allow_html=True)

    if "xavf_ball" not in dir():
        with col2:
            st.markdown("""
            <div style='text-align:center; color:#64748b; padding:60px 20px;'>
                <div style='font-size:3rem; margin-bottom:12px;'>🎯</div>
                <p>Ma'lumotlarni kiriting va <br>"Xavfni baholash" tugmasini bosing</p>
            </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════
#  5. DATASET
# ═══════════════════════════════════════════════
elif "Dataset" in sahifa:

    st.markdown("""
    <h1 style='color:#e2e8f0; font-size:2rem; margin-bottom:24px;'>
        📋 Dataset va statistika
    </h1>""", unsafe_allow_html=True)

    section("ℹ️  Dataset haqida")
    st.markdown("""
    <div class='info-card'>
        <h4>💳 BankChurners Dataset</h4>
        <p>Ushbu dataset bankning kredit karta mijozlari haqidagi ma'lumotlarni o'z ichiga oladi.
        <strong>Asosiy maqsad</strong> — bankni tark etishi mumkin bo'lgan mijozlarni erta aniqlash
        va ularni saqlab qolish uchun tegishli chora-tadbirlar ko'rish.</p>
    </div>
    <div class='info-card'>
        <h4>📌 Muhim ko'rsatkichlar</h4>
        <p><code>Attrition_Flag</code> — mijoz holati (faol/ketgan) &nbsp;|&nbsp;
        <code>Credit_Limit</code> — kredit limiti &nbsp;|&nbsp;
        <code>Total_Trans_Ct</code> — tranzaksiya soni &nbsp;|&nbsp;
        <code>Avg_Utilization_Ratio</code> — kredit foydalanish darajasi</p>
    </div>""", unsafe_allow_html=True)

    # Asosiy statistika
    section("📊 Asosiy statistika")
    num_stat = dff[["Yosh","Kredit_limiti","Tranzaksiya_summasi",
                    "Tranzaksiya_soni","Revolving_balans"]].describe().T.round(1)
    num_stat.columns = ["Soni","O'rtacha","Std","Min","25%","Mediana","75%","Maks"]
    num_stat.index = ["Yosh","Kredit limiti ($)","Trans. summa ($)","Trans. soni","Revolving balans ($)"]
    st.dataframe(num_stat, use_container_width=True)

    section("🗃️  Barcha ma'lumotlar")
    qidiruv = st.text_input("🔍 Holat bo'yicha qidirish", placeholder="masalan: Faol mijoz")
    show_df = dff.copy()
    if qidiruv:
        mask = show_df.apply(lambda row: row.astype(str).str.contains(qidiruv, case=False).any(), axis=1)
        show_df = show_df[mask]

    disp_cols = ["Jins","Yosh","Talim","Oilaviy_holat","Daromad","Holat",
                 "Karta_turi","Kredit_limiti","Tranzaksiya_soni","Tranzaksiya_summasi"]
    st.dataframe(
        show_df[disp_cols].rename(columns={
            "Jins":"Jins","Yosh":"Yosh","Talim":"Ta'lim",
            "Oilaviy_holat":"Oilaviy holat","Daromad":"Daromad","Holat":"Holat",
            "Karta_turi":"Karta turi","Kredit_limiti":"Kredit limiti ($)",
            "Tranzaksiya_soni":"Trans. soni","Tranzaksiya_summasi":"Trans. summa ($)",
        }).reset_index(drop=True),
        use_container_width=True, height=440,
    )
    st.caption(f"Jami {len(show_df):,} ta yozuv ko'rsatilmoqda.")

# ═══════════════════════════════════════════════
#  6. JAMOA
# ═══════════════════════════════════════════════
elif "Jamoa" in sahifa:

    st.markdown("""
    <h1 style='color:#e2e8f0; font-size:2rem; margin-bottom:8px;'>
        👥 Loyiha jamoasi
    </h1>
    <p style='color:#64748b; margin-bottom:32px;'>
        Ushbu loyiha quyidagi jamoa a'zolari tomonidan tayyorlandi.
    </p>""", unsafe_allow_html=True)

    jamoalar = [
        {"ism": "Nargiza", "rang": "#f472b6", "emoji": "👩‍💻", "rol": "Ma'lumotlar tahlilchisi"},
        {"ism": "Munisa", "rang": "#60a5fa", "emoji": "👩‍🔬", "rol": "Modellashtirish mutaxassisi"},
        {"ism": "Maqsuda",  "rang": "#4ade80", "emoji": "👩‍🎨", "rol": "Vizualizatsiya dizayneri"},
    ]

    cols = st.columns(3)
    for col, a in zip(cols, jamoalar):
        with col:
            st.markdown(f"""
            <div class='team-card'>
                <div class='avatar' style='background:rgba(0,0,0,0.3); border: 2px solid {a["rang"]};'>
                    {a["emoji"]}
                </div>
                <h3>{a["ism"]}</h3>
                <p style='color:{a["rang"]}; font-weight:600; font-size:0.85rem;'>{a["rol"]}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='info-card'>
            <h4>🎯 Loyiha maqsadi</h4>
            <p>Bank kredit karta mijozlari ma'lumotlarini tahlil qilish va
            bankni tark etishi mumkin bo'lgan mijozlarni oldindan aniqlash
            orqali bank uchun qaror qabul qilishni qo'llab-quvvatlash.</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='info-card'>
            <h4>🛠️ Ishlatilgan texnologiyalar</h4>
            <p><strong style='color:#60a5fa;'>Python</strong> &nbsp;·&nbsp;
            <strong style='color:#f472b6;'>Streamlit</strong> &nbsp;·&nbsp;
            <strong style='color:#fbbf24;'>Pandas</strong> &nbsp;·&nbsp;
            <strong style='color:#4ade80;'>Plotly</strong></p>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-top:32px; padding: 24px;
                background: linear-gradient(135deg,#1a1f2e,#252b3d);
                border-radius:14px; border:1px solid #2e3650;'>
        <div style='font-size:1.8rem; margin-bottom:8px;'>🎓</div>
        <p style='color:#94a3b8; margin:0; font-size:0.95rem;'>
            Loyiha jamoasi tomonidan tayyorlandi &nbsp;·&nbsp; 2026-yil
        </p>
    </div>""", unsafe_allow_html=True)
