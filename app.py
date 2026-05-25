import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
from datetime import datetime
import base64
import os
from dotenv import load_dotenv

# =========================================================
# CARREGAR SENHAS
# local  → senha.env
# deploy → Streamlit Secrets (Settings → Secrets)
# =========================================================

load_dotenv("senha.env")

def get_senha(chave: str) -> str:
    try:
        return str(st.secrets[chave]).strip()
    except Exception:
        return os.getenv(chave, "").strip()

USUARIOS = {
    "sac01":       get_senha("SAC01"),
    "sac02":       get_senha("SAC02"),
    "qualidade01": get_senha("QUALIDADE01"),
    "qualidade02": get_senha("QUALIDADE02"),
}

# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Coleta SAC Cini",
    page_icon="🚚",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# =========================================================
# HELPERS
# =========================================================

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #09111F 0%, #111B36 50%, #182850 100%);
    color: white;
}

.block-container {
    padding-top: 1rem;
    padding-left: 2rem;
    padding-right: 2rem;
}

.logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin-top: 0px;
    margin-bottom: 10px;
}

.logo-pulsando {
    width: 90px;
    height: auto;
    animation: pulseGlow 2.5s infinite, floating 3s ease-in-out infinite;
    filter: drop-shadow(0 0 10px #00AEEF) drop-shadow(0 0 25px rgba(0,174,239,0.5));
}

.login-box {
    background: rgba(255,255,255,0.05);
    padding: 35px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 50px;
}

.titulo {
    font-size: 38px;
    font-weight: 800;
    color: white;
    text-align: center;
    margin-top: 10px;
}

.subtitulo {
    color: #8FA7D8;
    font-size: 15px;
    text-align: center;
    margin-bottom: 20px;
}

.stTextInput input {
    background: rgba(255,255,255,0.08);
    color: white;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.10);
    padding: 12px;
}

[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 0 20px rgba(0,0,0,0.35), inset 0 0 15px rgba(255,255,255,0.02);
}

.stButton button {
    background: #00AEEF;
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 22px;
    font-weight: 700;
    font-size: 15px;
    width: 100%;
}

.stButton button:hover {
    background: #008FC4;
}

a {
    color: #00AEEF !important;
    text-decoration: none !important;
    font-weight: 700;
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 12px;
    border: 1px solid rgba(255,255,255,0.08);
}

@keyframes pulseGlow {
    0%   { transform: scale(1); }
    50%  { transform: scale(1.05); }
    100% { transform: scale(1); }
}

@keyframes floating {
    0%   { transform: translateY(0px); }
    50%  { transform: translateY(-5px); }
    100% { transform: translateY(0px); }
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logado:

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:

        st.markdown('<div class="login-box">', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{get_base64_image('logo.png')}" class="logo-pulsando">
        </div>
        <div class="titulo">🚚 COLETA SAC CINI</div>
        <div class="subtitulo">Sistema operacional de coletas SAC</div>
        """, unsafe_allow_html=True)

        usuario = st.text_input("👤 Usuário")
        senha   = st.text_input("🔒 Senha", type="password")

        if st.button("🚀 ENTRAR"):

            usuario_norm = usuario.strip().lower()
            senha_norm   = senha.strip()

            if usuario_norm in USUARIOS and USUARIOS[usuario_norm] == senha_norm:
                st.session_state.logado  = True
                st.session_state.usuario = usuario_norm
                st.success("✅ Login realizado com sucesso!")
                st.rerun()
            else:
                if usuario_norm not in USUARIOS:
                    st.error(f"❌ Usuário '{usuario_norm}' não encontrado.")
                else:
                    st.error("❌ Senha incorreta.")

        st.markdown('</div>', unsafe_allow_html=True)

    st.stop()

# =========================================================
# HEADER
# =========================================================

col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    st.markdown(f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{get_base64_image('logo.png')}" class="logo-pulsando">
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="titulo">🚚 COLETA SAC CINI</div>
    <div class="subtitulo">Usuário conectado: {st.session_state.usuario}</div>
    """, unsafe_allow_html=True)

with col3:
    st.write("")
    if st.button("🚪 SAIR"):
        st.session_state.logado  = False
        st.session_state.usuario = ""
        st.rerun()

st.divider()

# =========================================================
# UPLOAD
# =========================================================

arquivo = st.file_uploader("📥 Importar planilha COLETA SAC", type=["xlsx"])

# =========================================================
# PROCESSAMENTO
# =========================================================

if arquivo:

    try:

        df = pd.read_excel(arquivo, sheet_name="cini")

        colunas = [
            "Nº",
            "Título",
            "PRODUTO",
            "NOME DO CONSUMIDOR",
            "TIPO DE ESTABELECIMENTO",
            "NOME DO ESTABELECIMENTO",
            "BAIRRO DO ESTABELECIMENTO",
            "DATA COMPRA",
            "LOTE",
            "DATA PRODUÇÃO",
            "VALIDADE",
            "HORÁRIO",
            "QUANTIDADE COMPRADA",
            "QUANTIDADE COM DEFEITO",
            "WHATSAPP DO CONSUMIDOR",
            "TELEFONE CONSUMIDOR",
            "CIDADE",
            "ESTADO",
            "BAIRRO",
            "ENDEREÇO",
            "CEP",
            "DATA AGENDADA DE TROCA",
            "PERÍODO PARA RECEBIMENTO DO REPRESENTANTE",
            "DATA ENTRADA AMOSTRA",
        ]

        faltando = [c for c in colunas if c not in df.columns]

        if faltando:
            st.error(f"❌ Colunas não encontradas: {faltando}")
            st.stop()

        df = df[colunas]

        # STATUS
        df["STATUS"] = np.where(
            df["DATA ENTRADA AMOSTRA"].notna(),
            "COLETADO",
            "AGUARDANDO"
        )

        # ENDEREÇO COMPLETO
        df["ENDERECO_COMPLETO"] = (
            df["ENDEREÇO"].fillna("").astype(str) + ", " +
            df["BAIRRO"].fillna("").astype(str)   + ", " +
            df["CIDADE"].fillna("").astype(str)   + " - " +
            df["ESTADO"].fillna("").astype(str)
        )

        # GOOGLE MAPS
        df["GOOGLE MAPS"] = (
            "https://www.google.com/maps/search/?api=1&query=" +
            df["ENDERECO_COMPLETO"].astype(str).str.replace(" ", "+")
        )

        # ── KPIs ──────────────────────────────────────────────

        total      = len(df)
        aguardando = len(df[df["STATUS"] == "AGUARDANDO"])
        coletado   = len(df[df["STATUS"] == "COLETADO"])
        cidades    = df["CIDADE"].nunique()

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("TOTAL",      total)
        c2.metric("AGUARDANDO", aguardando)
        c3.metric("COLETADO",   coletado)
        c4.metric("CIDADES",    cidades)

        st.divider()

        # ── FILTROS ───────────────────────────────────────────

        cidades_filtro = st.multiselect(
            "🏙️ Filtrar cidade",
            sorted(df["CIDADE"].dropna().astype(str).unique())
        )

        if cidades_filtro:
            df = df[df["CIDADE"].astype(str).isin(cidades_filtro)]

        status_filtro = st.multiselect(
            "🚦 Filtrar Status",
            ["AGUARDANDO", "COLETADO"],
            default=["AGUARDANDO", "COLETADO"]
        )

        df = df[df["STATUS"].isin(status_filtro)]

        st.divider()

        # ── TABELA ────────────────────────────────────────────

        st.subheader("📋 Lista de Coletas")
        st.dataframe(df, use_container_width=True, height=500)

        st.divider()

        # ── ROTAS ─────────────────────────────────────────────

        st.subheader("🗺️ Rotas de Coleta")

        for _, row in df.iterrows():

            status_cor = "#00FF9D" if row["STATUS"] == "COLETADO" else "#FFD93D"

            st.markdown(f"""
            <div class="card">
                <div style="font-size:18px;font-weight:700;color:white;margin-bottom:8px;">
                    👤 {str(row['NOME DO CONSUMIDOR'])}
                </div>
                <div style="color:#8FA7D8;">
                    📦 Produto: {str(row['PRODUTO'])}<br>
                    📍 Cidade: {str(row['CIDADE'])}<br>
                    🏪 Estabelecimento: {str(row['NOME DO ESTABELECIMENTO'])}<br>
                    📞 Telefone: {str(row['TELEFONE CONSUMIDOR'])}<br>
                </div>
                <div style="margin-top:10px;font-weight:700;color:{status_cor};">
                    🚦 {str(row['STATUS'])}
                </div>
                <br>
                <a href="{str(row['GOOGLE MAPS'])}" target="_blank"
                   style="background:#00AEEF;color:white;padding:10px 18px;border-radius:10px;
                          text-decoration:none;font-weight:700;">
                    🗺️ Abrir Google Maps
                </a>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # ── PDF ───────────────────────────────────────────────

        st.subheader("📄 Exportação PDF")

        if st.button("📄 GERAR PDF DE PENDÊNCIAS"):

            df_pdf = df[df["STATUS"] == "AGUARDANDO"]

            if len(df_pdf) == 0:
                st.warning("⚠️ Não existem pendências.")

            else:

                pdf = FPDF()
                pdf.set_auto_page_break(False)

                for _, row in df_pdf.iterrows():

                    pdf.add_page()

                    # ── cabeçalho ──
                    pdf.set_fill_color(10, 16, 32)
                    pdf.rect(0, 0, 210, 32, "F")
                    pdf.set_text_color(255, 255, 255)
                    pdf.set_font("Arial", "B", 22)
                    pdf.set_xy(12, 9)
                    pdf.cell(0, 10, "COLETA SAC CINI")
                    pdf.set_font("Arial", "", 10)
                    pdf.set_xy(12, 20)
                    pdf.cell(0, 10, "Relatorio operacional de coleta")

                    # ── caixa de conteúdo ──
                    pdf.set_draw_color(210, 210, 210)
                    pdf.rect(10, 40, 190, 190)
                    pdf.set_text_color(0, 0, 0)

                    # cliente
                    pdf.set_xy(15, 50)
                    pdf.set_font("Arial", "B", 13)
                    pdf.cell(35, 8, "Cliente:")
                    pdf.set_font("Arial", "", 13)
                    pdf.multi_cell(135, 8, str(row["NOME DO CONSUMIDOR"]))

                    # produto
                    pdf.set_xy(15, 75)
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(45, 8, "Produto:")
                    pdf.set_font("Arial", "", 12)
                    pdf.multi_cell(120, 8, str(row["PRODUTO"]))

                    # quantidade
                    pdf.set_xy(15, 95)
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(45, 8, "Quantidade:")
                    pdf.set_font("Arial", "", 12)
                    pdf.cell(80, 8, str(row["QUANTIDADE COM DEFEITO"]))

                    # telefone
                    pdf.set_xy(15, 110)
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(45, 8, "Telefone:")
                    pdf.set_font("Arial", "", 12)
                    pdf.cell(100, 8, str(row["TELEFONE CONSUMIDOR"]))

                    # endereço
                    pdf.set_xy(15, 125)
                    pdf.set_font("Arial", "B", 12)
                    pdf.cell(45, 8, "Endereco:")
                    pdf.set_font("Arial", "", 12)
                    pdf.multi_cell(130, 8, str(row["ENDERECO_COMPLETO"]))

                # fpdf2 retorna bytearray — converte para bytes
                pdf_output = pdf.output()
                pdf_bytes  = bytes(pdf_output) if isinstance(pdf_output, bytearray) else pdf_output

                st.download_button(
                    label="⬇️ DOWNLOAD PDF",
                    data=pdf_bytes,
                    file_name=f"coletas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )

    except Exception as erro:
        st.error(f"❌ Erro ao processar planilha: {erro}")