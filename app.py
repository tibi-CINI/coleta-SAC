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
# =========================================================

load_dotenv("senha.env")

USUARIOS = {

    "sac01": os.getenv("SAC01", "").strip(),
    "sac02": os.getenv("SAC02", "").strip(),
    "qualidade01": os.getenv("QUALIDADE01", "").strip(),
    "qualidade02": os.getenv("QUALIDADE02", "").strip()

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
# SESSION
# =========================================================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# =========================================================
# LOGO
# =========================================================

def get_base64_image(image_path):

    try:

        with open(image_path, "rb") as img_file:

            return base64.b64encode(
                img_file.read()
            ).decode()

    except:

        return ""

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp{

    background:
    linear-gradient(
        135deg,
        #09111F 0%,
        #111B36 50%,
        #182850 100%
    );

    color:white;

}

.block-container{

    padding-top:1rem;
    padding-left:2rem;
    padding-right:2rem;

}

/* LOGIN */

.login-box{

    background:rgba(255,255,255,0.05);

    padding:40px;

    border-radius:24px;

    border:1px solid rgba(255,255,255,0.08);

    margin-top:40px;

}

/* LOGO */

.logo-container{

    display:flex;
    justify-content:center;
    align-items:center;

    width:100%;

}

.logo-pulsando{

    width:120px;
    height:auto;

    animation:
        pulseGlow 2.5s infinite,
        floating 3s ease-in-out infinite;

    filter:
        drop-shadow(0 0 10px #00AEEF)
        drop-shadow(0 0 25px rgba(0,174,239,0.5));

}

/* TITULOS */

.titulo{

    font-size:40px;
    font-weight:800;
    color:white;
    text-align:center;
    margin-top:15px;

}

.subtitulo{

    color:#8FA7D8;
    font-size:15px;
    text-align:center;
    margin-bottom:25px;

}

/* INPUTS */

.stTextInput input{

    background:rgba(255,255,255,0.08);

    color:white;

    border-radius:12px;

    border:1px solid rgba(255,255,255,0.10);

    padding:12px;

}

/* BOTÕES */

.stButton button{

    background:#00AEEF;

    color:white;

    border:none;

    border-radius:12px;

    padding:12px 22px;

    font-weight:700;

    font-size:15px;

    width:100%;

}

.stButton button:hover{

    background:#008FC4;

}

/* KPI */

[data-testid="stMetric"]{

    background:rgba(255,255,255,0.05);

    padding:20px;

    border-radius:18px;

    border:1px solid rgba(255,255,255,0.08);

}

/* CARD */

.card{

    background:rgba(255,255,255,0.05);

    padding:18px;

    border-radius:18px;

    margin-bottom:12px;

    border:1px solid rgba(255,255,255,0.08);

}

/* LINKS */

a{

    color:white !important;
    text-decoration:none !important;

}

@keyframes pulseGlow {

    0%{
        transform:scale(1);
    }

    50%{
        transform:scale(1.05);
    }

    100%{
        transform:scale(1);
    }

}

@keyframes floating {

    0%{
        transform:translateY(0px);
    }

    50%{
        transform:translateY(-5px);
    }

    100%{
        transform:translateY(0px);
    }

}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logado:

    col1, col2, col3 = st.columns([1,1.5,1])

    with col2:

        st.markdown("""
        <div class="login-box">
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="logo-container">
            <img src="data:image/png;base64,{get_base64_image('logo.png')}" class="logo-pulsando">
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class='titulo'>
            🚚 COLETA SAC CINI
        </div>

        <div class='subtitulo'>
            Sistema operacional de coletas SAC
        </div>
        """, unsafe_allow_html=True)

        usuario = st.text_input(
            "👤 Usuário"
        )

        senha = st.text_input(
            "🔒 Senha",
            type="password"
        )

        if st.button("🚀 ENTRAR"):

            usuario = usuario.strip().lower()
            senha = senha.strip()

            senha_correta = USUARIOS.get(usuario)

            if senha_correta and senha == senha_correta:

                st.session_state.logado = True
                st.session_state.usuario = usuario

                st.success("✅ Login realizado com sucesso!")

                st.rerun()

            else:

                st.error("❌ Usuário ou senha inválidos!")

        st.markdown("</div>", unsafe_allow_html=True)

    st.stop()

# =========================================================
# HEADER
# =========================================================

col1, col2, col3 = st.columns([1,4,1])

with col1:

    st.markdown(f"""
    <div class="logo-container">
        <img src="data:image/png;base64,{get_base64_image('logo.png')}" class="logo-pulsando">
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown(f"""
    <div class='titulo'>
        🚚 COLETA SAC CINI
    </div>

    <div class='subtitulo'>
        Usuário conectado: {st.session_state.usuario}
    </div>
    """, unsafe_allow_html=True)

with col3:

    if st.button("🚪 SAIR"):

        st.session_state.logado = False
        st.session_state.usuario = ""

        st.rerun()

st.divider()

# =========================================================
# IMPORTAR PLANILHA
# =========================================================

arquivo = st.file_uploader(

    "📥 Importar planilha COLETA SAC",
    type=["xlsx"]

)

# =========================================================
# PROCESSAMENTO
# =========================================================

if arquivo:

    try:

        df = pd.read_excel(
            arquivo,
            sheet_name="cini"
        )

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
            "DATA ENTRADA AMOSTRA"

        ]

        df = df[colunas]

        # STATUS

        df["STATUS"] = np.where(

            df["DATA ENTRADA AMOSTRA"].notna(),

            "COLETADO",

            "AGUARDANDO"

        )

        # ENDEREÇO

        df["ENDERECO_COMPLETO"] = (

            df["ENDEREÇO"].fillna("").astype(str) + ", " +
            df["BAIRRO"].fillna("").astype(str) + ", " +
            df["CIDADE"].fillna("").astype(str) + " - " +
            df["ESTADO"].fillna("").astype(str)

        )

        # MAPS

        df["GOOGLE MAPS"] = (

            "https://www.google.com/maps/search/?api=1&query="
            +
            df["ENDERECO_COMPLETO"].str.replace(" ", "+")

        )

        # KPI

        total = len(df)

        aguardando = len(
            df[df["STATUS"] == "AGUARDANDO"]
        )

        coletado = len(
            df[df["STATUS"] == "COLETADO"]
        )

        cidades = df["CIDADE"].nunique()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("TOTAL", total)
        c2.metric("AGUARDANDO", aguardando)
        c3.metric("COLETADO", coletado)
        c4.metric("CIDADES", cidades)

        st.divider()

        # FILTROS

        cidades_filtro = st.multiselect(

            "🏙️ Filtrar cidade",

            sorted(
                df["CIDADE"]
                .dropna()
                .astype(str)
                .unique()
            )

        )

        if cidades_filtro:

            df = df[
                df["CIDADE"].astype(str).isin(cidades_filtro)
            ]

        status_filtro = st.multiselect(

            "🚦 Filtrar status",

            ["AGUARDANDO", "COLETADO"],

            default=["AGUARDANDO", "COLETADO"]

        )

        df = df[
            df["STATUS"].isin(status_filtro)
        ]

        st.divider()

        # TABELA

        st.subheader("📋 Lista de Coletas")

        st.dataframe(

            df,

            use_container_width=True,

            height=500

        )

        st.divider()

        # ROTAS

        st.subheader("🗺️ Rotas de Coleta")

        for _, row in df.iterrows():

            status_cor = (
                "#00FF9D"
                if row["STATUS"] == "COLETADO"
                else "#FFD93D"
            )

            st.markdown(f"""
            <div class="card">

                <div style="
                    font-size:18px;
                    font-weight:700;
                    color:white;
                    margin-bottom:8px;
                ">
                    👤 {row['NOME DO CONSUMIDOR']}
                </div>

                <div style="color:#8FA7D8;">

                    📦 Produto: {row['PRODUTO']}<br>
                    📍 Cidade: {row['CIDADE']}<br>
                    🏪 Estabelecimento: {row['NOME DO ESTABELECIMENTO']}<br>
                    📞 Telefone: {row['TELEFONE CONSUMIDOR']}<br>

                </div>

                <div style="
                    margin-top:10px;
                    font-weight:700;
                    color:{status_cor};
                ">
                    🚦 {row['STATUS']}
                </div>

                <br>

                <a href="{row['GOOGLE MAPS']}" target="_blank"
                style="
                    background:#00AEEF;
                    padding:10px 18px;
                    border-radius:10px;
                    color:white;
                    font-weight:700;
                ">
                    🗺️ Abrir Google Maps
                </a>

            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # PDF

        st.subheader("📄 Exportação PDF")

        if st.button("📄 GERAR PDF"):

            pdf = FPDF()

            pdf.add_page()

            pdf.set_font("Arial", "B", 16)

            pdf.cell(190, 10, "COLETA SAC CINI", 0, 1, "C")

            pdf.ln(10)

            pdf.set_font("Arial", "", 10)

            for _, row in df.iterrows():

                pdf.multi_cell(

                    0,
                    8,

                    f"""
Cliente: {row['NOME DO CONSUMIDOR']}
Produto: {row['PRODUTO']}
Cidade: {row['CIDADE']}
Telefone: {row['TELEFONE CONSUMIDOR']}
Status: {row['STATUS']}
Endereco: {row['ENDERECO_COMPLETO']}
                    """

                )

                pdf.ln(4)

            pdf_output = pdf.output(dest="S")

            st.download_button(

                label="⬇️ DOWNLOAD PDF",

                data=bytes(pdf_output),

                file_name=f"coletas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",

                mime="application/pdf"

            )

    except Exception as erro:

        st.error(f"❌ Erro: {erro}")