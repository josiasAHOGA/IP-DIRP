import streamlit as st
import pandas as pd
import io
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# ── Configuration ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ABMed – Programmation des Inspections",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Global */
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

/* Header bandeau */
.abmed-header {
    background: linear-gradient(135deg, #003366 0%, #0055a4 60%, #1a78c2 100%);
    color: white;
    padding: 1.2rem 2rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.5rem;
    box-shadow: 0 4px 16px rgba(0,51,102,0.25);
}
.abmed-header h1 { margin: 0; font-size: 1.6rem; font-weight: 700; }
.abmed-header p  { margin: 0; font-size: 0.85rem; opacity: 0.85; }
.badge-initiale {
    background: rgba(255,255,255,0.2);
    border: 2px solid rgba(255,255,255,0.5);
    border-radius: 50%;
    width: 58px; height: 58px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.5rem; font-weight: 900; flex-shrink: 0;
}

/* Connexion */
.login-box {
    max-width: 420px;
    margin: 80px auto;
    background: white;
    border-radius: 16px;
    padding: 2.5rem;
    box-shadow: 0 8px 32px rgba(0,51,102,0.15);
    border-top: 5px solid #003366;
}
.login-box h2 { color: #003366; text-align: center; margin-bottom: 0.5rem; }
.login-subtitle { color: #666; text-align: center; font-size: 0.9rem; margin-bottom: 1.5rem; }

/* KPI cards */
.kpi-card {
    background: white;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    border-left: 5px solid #003366;
    margin-bottom: 0.5rem;
}
.kpi-card .kpi-value { font-size: 2rem; font-weight: 800; color: #003366; }
.kpi-card .kpi-label { font-size: 0.8rem; color: #888; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-card.green  { border-left-color: #1a9e5f; }
.kpi-card.orange { border-left-color: #e07b00; }
.kpi-card.red    { border-left-color: #c0392b; }
.kpi-card.blue   { border-left-color: #0055a4; }

/* Mission badge */
.mission-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}
.role-principal { background: #003366; color: white; }
.role-co        { background: #0055a4; color: white; }
.role-reserve   { background: #e07b00; color: white; }

/* Section titles */
.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #003366;
    border-bottom: 2px solid #e8eef5;
    padding-bottom: 0.4rem;
    margin: 1.2rem 0 0.8rem 0;
}

/* Table styling */
.dataframe { font-size: 0.82rem !important; }
</style>
""", unsafe_allow_html=True)

# ── Data Loading ───────────────────────────────────────────────────────────────
DATA_FILE = Path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "book5.xlsx"))
if not DATA_FILE.exists():
    DATA_FILE = Path("book5.xlsx")MOIS_SHEETS = ["Avril", "Mai", "Juin", "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]

@st.cache_data
def load_data():
    xl = pd.read_excel(DATA_FILE, sheet_name=None, header=None)

    # ── Charge par inspecteur ──────────────────────────────────────
    df_c = xl["Charge par inspecteur"].copy()
    # row 1 = headers (row 0 is empty)
    df_c.columns = df_c.iloc[1]
    df_c = df_c.iloc[2:].reset_index(drop=True)
    df_c = df_c.dropna(subset=["Inspecteur"])
    df_c.rename(columns={
        "Inspecteur": "Initiale",
        "Groupe": "Groupe",
        "P": "P",
        "Co": "Co",
        "R": "R",
        "Total missions sans reserve": "Total_sans_R",
        "Total missions": "Total",
        "VT (P+Co)": "VT",
        "IC = 2P+Co+R": "IC",
        "ICR = IC + VT/5": "ICR",
    }, inplace=True)
    inspecteurs = df_c[["Initiale", "Groupe", "P", "Co", "R",
                         "Total_sans_R", "Total", "VT", "IC", "ICR"]].dropna(subset=["Initiale"])

    # ── Missions mensuelles ────────────────────────────────────────
    def _norm_col(cs):
        if cs == "Mois": return "Mois"
        if cs == "Semaine": return "Semaine"
        if cs == "Période": return "Periode"
        if cs == "Zone": return "Zone"
        if cs == "Type_Inspection": return "Type_Inspection"
        if cs == "Sous_Type": return "Sous_Type"
        if "Département" in cs or "Department" in cs: return "Departement"
        if cs == "Volume": return "Volume"
        if "Structure" in cs: return "Structures"
        if "Principal" in cs: return "IP"
        if "Co_Inspecteur_1" in cs: return "Co1"
        if "Co_Inspecteur_2" in cs: return "Co2"
        if "Co_Inspecteur_3" in cs: return "Co3"
        if "Reserve" in cs: return "Reserve"
        if "Observation" in cs: return "Observation"
        return cs

    all_missions = []
    for sheet in MOIS_SHEETS:
        if sheet not in xl:
            continue
        df_m = xl[sheet].copy()
        header_idx = None
        for i, row in df_m.iterrows():
            if any(str(v).strip() == "Mois" for v in row.values if pd.notna(v)):
                header_idx = i
                break
        if header_idx is None:
            continue
        df_m.columns = df_m.iloc[header_idx]
        df_m = df_m.iloc[header_idx + 1:].reset_index(drop=True)
        df_m = df_m.dropna(how="all")
        df_m.columns = [_norm_col(str(c).strip()) for c in df_m.columns]
        keep = [c for c in ["Mois","Semaine","Periode","Zone","Type_Inspection",
                              "Sous_Type","Departement","Volume","Structures",
                              "IP","Co1","Co2","Co3","Reserve","Observation"] if c in df_m.columns]
        df_m = df_m[keep].copy()
        if "Mois" in df_m.columns:
            df_m["Mois"] = df_m["Mois"].ffill()
        df_m = df_m[df_m["Mois"].notna()]
        all_missions.append(df_m)

    missions = pd.concat(all_missions, ignore_index=True) if all_missions else pd.DataFrame()

    # ── Congés ────────────────────────────────────────────────────
    df_cg = xl["Congés"].copy()
    df_cg.columns = df_cg.iloc[1]
    df_cg = df_cg.iloc[2:].reset_index(drop=True)
    df_cg = df_cg.dropna(subset=["Initiales"])
    df_cg.rename(columns={
        "Mois": "Mois", "Date_Debut": "Date_Debut", "Date_Fin_Indicative": "Date_Fin",
        "Inspecteur": "Nom_Complet", "Initiales": "Initiale",
        "Entité": "Entite", "Zone_Impact": "Zone_Impact",
        "Durée": "Duree", "Observation": "Observation"
    }, inplace=True)
    conges = df_cg

    return inspecteurs, missions, conges

inspecteurs_df, missions_df, conges_df = load_data()

VALID_INITIALES = set(inspecteurs_df["Initiale"].dropna().str.strip().str.upper().tolist())

# ── Session state ──────────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "initiale" not in st.session_state:
    st.session_state.initiale = ""

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE CONNEXION
# ═══════════════════════════════════════════════════════════════════════════════
def page_login():
    st.markdown("""
    <div style="text-align:center;margin-top:30px;margin-bottom:10px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Flag_of_Benin.svg/40px-Flag_of_Benin.svg.png" width="40"/>
    </div>
    <div class="login-box">
        <h2>🏥 ABMed</h2>
        <p class="login-subtitle">Agence Béninoise du Médicament<br>Plateforme de programmation des inspections</p>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("### Connexion Inspecteur")
        st.caption("Renseignez vos initiales pour accéder à votre tableau de bord")
        initiale_input = st.text_input(
            "Vos initiales",
            placeholder="Ex : JA, IG, SH...",
            max_chars=4,
            label_visibility="collapsed"
        ).strip().upper()
        col_btn, col_info = st.columns([1, 1])
        with col_btn:
            if st.button("🔐 Accéder", use_container_width=True, type="primary"):
                if initiale_input in VALID_INITIALES:
                    st.session_state.logged_in = True
                    st.session_state.initiale = initiale_input
                    st.rerun()
                else:
                    st.error("Initiales non reconnues. Vérifiez et réessayez.")
        st.markdown("---")
        st.caption(f"**Inspecteurs enregistrés :** {len(VALID_INITIALES)} | Données 2026")


# ═══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════════════════════
def get_missions_inspecteur(init):
    """Retourne toutes les missions où l'inspecteur apparaît (IP, Co, Réserve)."""
    if missions_df.empty:
        return pd.DataFrame()
    df = missions_df.copy()
    cols_role = {}
    for col in ["IP", "Co1", "Co2", "Co3"]:
        if col in df.columns:
            cols_role[col] = "Principal" if col == "IP" else "Co-inspecteur"
    if "Reserve" in df.columns:
        cols_role["Reserve"] = "Réserve/Urgence"

    rows = []
    for _, row in df.iterrows():
        role_found = None
        for col, role in cols_role.items():
            val = str(row.get(col, "")).strip().upper()
            if val == init:
                role_found = role
                break
        if role_found:
            r = row.to_dict()
            r["Mon_Role"] = role_found
            rows.append(r)
    return pd.DataFrame(rows)


def get_conges_inspecteur(init):
    if conges_df.empty:
        return pd.DataFrame()
    return conges_df[conges_df["Initiale"].str.strip().str.upper() == init].copy()


def get_charge_inspecteur(init):
    row = inspecteurs_df[inspecteurs_df["Initiale"].str.strip().str.upper() == init]
    if row.empty:
        return None
    return row.iloc[0]


def couleur_role(role):
    if role == "Principal":
        return "role-principal"
    elif role == "Co-inspecteur":
        return "role-co"
    return "role-reserve"


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE PRINCIPALE (dashboard)
# ═══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    init = st.session_state.initiale
    charge = get_charge_inspecteur(init)
    missions_perso = get_missions_inspecteur(init)
    conges_perso = get_conges_inspecteur(init)
    groupe = charge["Groupe"] if charge is not None else "—"

    # ── Header ────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="abmed-header">
        <div class="badge-initiale">{init}</div>
        <div>
            <h1>Tableau de bord – Inspecteur {init}</h1>
            <p>Groupe : <strong>{groupe}</strong> &nbsp;|&nbsp; Agence Béninoise du Médicament &nbsp;|&nbsp; Programmation 2026</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Sidebar ───────────────────────────────────────────────────
    with st.sidebar:
        st.markdown(f"### 👤 {init} — {groupe}")
        st.markdown("---")
        page = st.radio("Navigation", [
            "📊 Mes statistiques",
            "📅 Mes missions",
            "🏖️ Mes congés",
            "🌍 Vue globale",
            "👥 Équipe",
        ])
        st.markdown("---")
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.initiale = ""
            st.rerun()

    # ════════════════════════════════════════════════
    if page == "📊 Mes statistiques":
        page_stats(init, charge, missions_perso, conges_perso)
    elif page == "📅 Mes missions":
        page_missions(init, missions_perso)
    elif page == "🏖️ Mes congés":
        page_conges(init, conges_perso)
    elif page == "🌍 Vue globale":
        page_globale()
    elif page == "👥 Équipe":
        page_equipe(init)


# ── Statistiques personnelles ──────────────────────────────────────────────────
def page_stats(init, charge, missions_perso, conges_perso):
    st.markdown('<p class="section-title">📊 Mes indicateurs de charge</p>', unsafe_allow_html=True)

    if charge is not None:
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(f"""<div class="kpi-card blue">
                <div class="kpi-value">{int(charge['Total']) if pd.notna(charge['Total']) else '—'}</div>
                <div class="kpi-label">Total missions</div></div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""<div class="kpi-card green">
                <div class="kpi-value">{int(charge['P']) if pd.notna(charge['P']) else '—'}</div>
                <div class="kpi-label">En principal (P)</div></div>""", unsafe_allow_html=True)
        with c3:
            st.markdown(f"""<div class="kpi-card orange">
                <div class="kpi-value">{int(charge['Co']) if pd.notna(charge['Co']) else '—'}</div>
                <div class="kpi-label">En co-inspecteur (Co)</div></div>""", unsafe_allow_html=True)
        with c4:
            st.markdown(f"""<div class="kpi-card red">
                <div class="kpi-value">{int(charge['R']) if pd.notna(charge['R']) else '—'}</div>
                <div class="kpi-label">Réserve/Urgence (R)</div></div>""", unsafe_allow_html=True)

        c5, c6, c7 = st.columns(3)
        with c5:
            st.metric("IC (Indice de charge)", f"{int(charge['IC']) if pd.notna(charge['IC']) else '—'}")
        with c6:
            st.metric("ICR (IC + VT/5)", f"{charge['ICR']:.1f}" if pd.notna(charge.get('ICR')) else "—")
        with c7:
            st.metric("VT (Visites totales)", f"{int(charge['VT']) if pd.notna(charge['VT']) else '—'}")
    else:
        st.info("Données de charge non disponibles.")

    # ── Répartition par rôle ───────────────────────────────────────────────────
    if not missions_perso.empty:
        st.markdown('<p class="section-title">Répartition de mes missions par rôle</p>', unsafe_allow_html=True)
        role_counts = missions_perso["Mon_Role"].value_counts().reset_index()
        role_counts.columns = ["Rôle", "Nombre"]
        fig = px.pie(role_counts, names="Rôle", values="Nombre",
                     color_discrete_sequence=["#003366", "#0055a4", "#e07b00"],
                     hole=0.4)
        fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=280)
        st.plotly_chart(fig, use_container_width=True)

        # ── Par mois ──────────────────────────────────────────────────────────
        st.markdown('<p class="section-title">Répartition mensuelle</p>', unsafe_allow_html=True)
        if "Mois" in missions_perso.columns:
            ordre_mois = ["AVRIL","MAI","JUIN","JUILLET","AOUT","SEPTEMBRE","OCTOBRE","NOVEMBRE","DECEMBRE"]
            m_counts = missions_perso.groupby(["Mois", "Mon_Role"]).size().reset_index(name="N")
            m_counts["Mois_upper"] = m_counts["Mois"].str.upper()
            m_counts["Ordre"] = m_counts["Mois_upper"].apply(
                lambda x: ordre_mois.index(x) if x in ordre_mois else 99)
            m_counts = m_counts.sort_values("Ordre")
            fig2 = px.bar(m_counts, x="Mois", y="N", color="Mon_Role",
                          barmode="stack",
                          color_discrete_map={
                              "Principal": "#003366",
                              "Co-inspecteur": "#0055a4",
                              "Réserve/Urgence": "#e07b00"
                          }, labels={"N": "Missions", "Mon_Role": "Rôle"})
            fig2.update_layout(margin=dict(t=10, b=10), height=280)
            st.plotly_chart(fig2, use_container_width=True)

    # ── Congés ────────────────────────────────────────────────────
    if not conges_perso.empty:
        st.markdown('<p class="section-title">🏖️ Mes périodes de congé</p>', unsafe_allow_html=True)
        for _, row in conges_perso.iterrows():
            debut = str(row.get("Date_Debut", "")).split(" ")[0]
            fin = str(row.get("Date_Fin", "")).split(" ")[0]
            obs = str(row.get("Observation", "")).strip()
            mois = str(row.get("Mois", "")).strip()
            duree = str(row.get("Duree", "")).strip()
            st.markdown(f"""
            <div style="background:#fff8e7;border-left:4px solid #e07b00;border-radius:8px;
                        padding:0.7rem 1rem;margin-bottom:0.5rem;">
                <strong>{mois}</strong> : {debut} → {fin} &nbsp;
                <span style="color:#e07b00;font-size:0.8rem;">({duree})</span><br>
                <small style="color:#666;">{obs}</small>
            </div>""", unsafe_allow_html=True)


# ── Mes missions ───────────────────────────────────────────────────────────────
def page_missions(init, missions_perso):
    st.markdown('<p class="section-title">📅 Calendrier de mes missions</p>', unsafe_allow_html=True)

    if missions_perso.empty:
        st.info("Aucune mission trouvée pour cet inspecteur.")
        return

    # Filtres
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        mois_dispo = ["Tous"] + sorted(missions_perso["Mois"].dropna().unique().tolist()) if "Mois" in missions_perso.columns else ["Tous"]
        filtre_mois = st.selectbox("Mois", mois_dispo)
    with col_f2:
        roles_dispo = ["Tous"] + missions_perso["Mon_Role"].unique().tolist()
        filtre_role = st.selectbox("Rôle", roles_dispo)
    with col_f3:
        zones_dispo = ["Toutes"] + missions_perso["Zone"].dropna().unique().tolist() if "Zone" in missions_perso.columns else ["Toutes"]
        filtre_zone = st.selectbox("Zone", zones_dispo)

    df = missions_perso.copy()
    if filtre_mois != "Tous":
        df = df[df["Mois"] == filtre_mois]
    if filtre_role != "Tous":
        df = df[df["Mon_Role"] == filtre_role]
    if filtre_zone != "Toutes" and "Zone" in df.columns:
        df = df[df["Zone"] == filtre_zone]

    st.caption(f"{len(df)} mission(s) affichée(s)")

    for _, row in df.iterrows():
        role = row.get("Mon_Role", "")
        mois = str(row.get("Mois", "")).strip()
        sem = str(row.get("Semaine", "")).strip()
        periode = str(row.get("Periode", "")).strip()
        zone = str(row.get("Zone", "")).strip()
        stype = str(row.get("Sous_Type", "")).strip()
        dept = str(row.get("Departement", "")).strip()
        vol = row.get("Volume", "")
        structures = str(row.get("Structures", "")).strip()
        obs = str(row.get("Observation", "")).strip()

        badge_cls = couleur_role(role)
        structures_html = structures.replace("\n", "<br>") if structures not in ["nan", ""] else "—"

        st.markdown(f"""
        <div style="background:white;border-radius:12px;padding:1rem 1.2rem;
                    margin-bottom:0.8rem;box-shadow:0 2px 10px rgba(0,0,0,0.07);
                    border-left:5px solid {'#003366' if role=='Principal' else '#0055a4' if role=='Co-inspecteur' else '#e07b00'};">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                <span style="font-weight:700;color:#003366;">{mois} · {sem} ({periode})</span>
                <span class="mission-badge {badge_cls}">{role}</span>
            </div>
            <div style="display:flex;gap:2rem;margin-bottom:0.5rem;flex-wrap:wrap;">
                <span>📍 <strong>Zone :</strong> {zone}</span>
                <span>🏷️ <strong>Type :</strong> {stype}</span>
                <span>🗺️ <strong>Dép. :</strong> {dept if dept not in ['nan',''] else '—'}</span>
                <span>🔢 <strong>Volume :</strong> {int(vol) if str(vol) not in ['nan','','0.0'] else '—'}</span>
            </div>
            <div style="font-size:0.82rem;color:#444;background:#f5f8fc;
                        border-radius:6px;padding:0.5rem 0.8rem;margin-bottom:0.3rem;">
                <strong>Structures :</strong> {structures_html}
            </div>
            {'<div style="font-size:0.8rem;color:#888;font-style:italic;">💬 ' + obs + '</div>' if obs not in ['nan',''] else ''}
        </div>
        """, unsafe_allow_html=True)


# ── Mes congés ─────────────────────────────────────────────────────────────────
def page_conges(init, conges_perso):
    st.markdown('<p class="section-title">🏖️ Mes périodes de congé</p>', unsafe_allow_html=True)
    if conges_perso.empty:
        st.success("Aucun congé enregistré pour vous.")
        return
    cols_show = [c for c in ["Mois","Date_Debut","Date_Fin","Duree","Zone_Impact","Observation"] if c in conges_perso.columns]
    st.dataframe(conges_perso[cols_show].reset_index(drop=True), use_container_width=True)


# ── Vue globale ────────────────────────────────────────────────────────────────
def page_globale():
    st.markdown('<p class="section-title">🌍 Vue globale des inspections 2026</p>', unsafe_allow_html=True)

    if missions_df.empty:
        st.info("Données non disponibles.")
        return

    # Totaux par mois
    if "Mois" in missions_df.columns and "Volume" in missions_df.columns:
        df_g = missions_df.copy()
        df_g["Volume"] = pd.to_numeric(df_g["Volume"], errors="coerce").fillna(0)
        by_mois = df_g.groupby("Mois")["Volume"].sum().reset_index()
        ordre = ["AVRIL","MAI","JUIN","JUILLET","AOUT","SEPTEMBRE","OCTOBRE","NOVEMBRE","DECEMBRE"]
        by_mois["Ordre"] = by_mois["Mois"].str.upper().apply(lambda x: ordre.index(x) if x in ordre else 99)
        by_mois = by_mois.sort_values("Ordre")
        fig = px.bar(by_mois, x="Mois", y="Volume",
                     color_discrete_sequence=["#003366"],
                     labels={"Volume": "Structures inspectées", "Mois": "Mois"},
                     title="Volume d'inspections par mois")
        fig.update_layout(height=320, margin=dict(t=40,b=10))
        st.plotly_chart(fig, use_container_width=True)

    # Répartition par type
    col_a, col_b = st.columns(2)
    with col_a:
        if "Sous_Type" in missions_df.columns:
            st.markdown("**Par type de structure**")
            st.dataframe(
                missions_df["Sous_Type"].value_counts().reset_index().rename(
                    columns={"index": "Type", "Sous_Type": "Missions"}),
                use_container_width=True, height=200)
    with col_b:
        if "Zone" in missions_df.columns:
            st.markdown("**Par zone**")
            st.dataframe(
                missions_df["Zone"].value_counts().reset_index().rename(
                    columns={"index": "Zone", "Zone": "Missions"}),
                use_container_width=True, height=200)

    # Tableau complet filtrable
    st.markdown('<p class="section-title">Détail de toutes les missions</p>', unsafe_allow_html=True)
    cols_show = [c for c in ["Mois","Semaine","Periode","Zone","Type_Inspection","Sous_Type",
                               "Departement","Volume","IP","Co1","Reserve","Observation"]
                 if c in missions_df.columns]
    st.dataframe(missions_df[cols_show].reset_index(drop=True), use_container_width=True, height=400)


# ── Vue équipe ─────────────────────────────────────────────────────────────────
def page_equipe(init_courant):
    st.markdown('<p class="section-title">👥 Tableau de charge de l\'équipe</p>', unsafe_allow_html=True)

    df_e = inspecteurs_df.copy()
    df_e["ICR_num"] = pd.to_numeric(df_e["ICR"], errors="coerce")
    max_icr = df_e["ICR_num"].max()

    cols_show = [c for c in ["Initiale","Groupe","P","Co","R","Total","IC","ICR"] if c in df_e.columns]
    df_display = df_e[cols_show].copy()
    df_display["Vous"] = df_display["Initiale"].apply(lambda x: "⬅️ vous" if str(x).strip().upper() == init_courant else "")

    st.dataframe(
        df_display.sort_values("ICR", ascending=False).reset_index(drop=True),
        use_container_width=True,
        height=500
    )

    # Graphique comparaison ICR
    st.markdown('<p class="section-title">Comparaison ICR (Indice de charge pondéré)</p>', unsafe_allow_html=True)
    df_e_sorted = df_e.sort_values("ICR_num", ascending=True)
    colors = ["#e07b00" if str(x).strip().upper() == init_courant else "#003366"
              for x in df_e_sorted["Initiale"]]
    fig = go.Figure(go.Bar(
        x=df_e_sorted["ICR_num"],
        y=df_e_sorted["Initiale"],
        orientation="h",
        marker_color=colors,
        text=df_e_sorted["ICR_num"],
        textposition="outside"
    ))
    fig.update_layout(
        height=max(300, len(df_e) * 22),
        margin=dict(l=10, r=40, t=10, b=10),
        xaxis_title="ICR",
        yaxis_title="Inspecteur",
        plot_bgcolor="white",
        xaxis=dict(gridcolor="#eee")
    )
    st.plotly_chart(fig, use_container_width=True)

    # Congés équipe
    st.markdown('<p class="section-title">🏖️ Congés de l\'équipe</p>', unsafe_allow_html=True)
    cols_cg = [c for c in ["Mois","Initiale","Nom_Complet","Date_Debut","Date_Fin","Duree","Zone_Impact","Observation"]
               if c in conges_df.columns]
    st.dataframe(conges_df[cols_cg].reset_index(drop=True), use_container_width=True, height=300)


# ═══════════════════════════════════════════════════════════════════════════════
# ROUTING
# ═══════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    page_login()
else:
    page_dashboard()
