import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import base64
import os
from dotenv import load_dotenv
from fpdf import FPDF

# =========================================================
# CONFIG PAGINA
# =========================================================

st.set_page_config(
    page_title="Coleta SAC Cini",
    page_icon="🚚",
    layout="wide"
)

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
# SESSION
# =========================================================

if "logado" not in st.session_state:
    st.session_state.logado = False

if "usuario" not in st.session_state:
    st.session_state.usuario = ""

# =========================================================
# FUNÇÃO LOGO
# =========================================================

def get_base64_image(image_path):

    try:

        caminho_absoluto = os.path.join(
            os.path.dirname(__file__),
            image_path
        )

        with open(caminho_absoluto, "rb") as img_file:

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

    margin-top:60px;

    box-shadow:
        0 0 30px rgba(0,0,0,0.35);

}

/* TITULOS */

.titulo{

    font-size:42px;
    font-weight:800;
    color:white;

}

.subtitulo{

    color:#8FA7D8;
    font-size:15px;

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

    border-radius:14px;

    padding:12px 22px;

    font-weight:700;

    font-size:15px;

    width:100%;

}

.stButton button:hover{

    background:#0094D1;

}

/* KPIS */

[data-testid="stMetric"]{

    background:rgba(255,255,255,0.05);

    padding:20px;

    border-radius:18px;

    border:1px solid rgba(255,255,255,0.08);

}

/* CARDS */

.card{

    background:rgba(255,255,255,0.05);

    padding:20px;

    border-radius:20px;

    margin-bottom:15px;

    border:1px solid rgba(255,255,255,0.08);

}

/* TABELA */

[data-testid="stDataFrame"]{

    border-radius:18px;
    overflow:hidden;

}

</style>

""", unsafe_allow_html=True)

# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logado:

    col1, col2, col3 = st.columns([1,1.5,1])

    with col2:

        st.markdown(
            '<div class="login-box">',
            unsafe_allow_html=True
        )

        logo_base64 = get_base64_image("logo.png")

        if logo_base64:

            st.markdown(f"""

            <div style="
                display:flex;
                justify-content:center;
                margin-bottom:20px;
            ">

                <img
                    src="data:image/png;base64,{logo_base64}"
                    style="
                        width:100px;
                        height:auto;
                    "
                >

            </div>

            """, unsafe_allow_html=True)

        st.markdown("""

        <div style="text-align:center;">

            <div class='titulo'>
                🚚 COLETA SAC CINI
            </div>

            <div class='subtitulo'>
                Sistema operacional de coletas SAC
            </div>

        </div>

        """, unsafe_allow_html=True)

        usuario = st.text_input("👤 Usuário")

        senha = st.text_input(
            "🔒 Senha",
            type="password"
        )

        if st.button("🚀 ENTRAR"):

            usuario = usuario.strip().lower()
            senha = senha.strip()

            if usuario in USUARIOS and USUARIOS[usuario] == senha:

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

col1, col2, col3 = st.columns([1,5,1])

with col1:

    logo_base64 = get_base64_image("logo.png")

    if logo_base64:

        st.markdown(f"""

        <div style="
            display:flex;
            justify-content:center;
            align-items:center;
            margin-top:10px;
        ">

            <img
                src="data:image/png;base64,{logo_base64}"
                style="
                    width:90px;
                    height:auto;
                "
            >

        </div>

        """, unsafe_allow_html=True)

with col2:

    st.markdown("""

    <div style="padding-top:15px;">

        <div style="
            font-size:42px;
            font-weight:800;
            color:white;
            line-height:1;
        ">

            🚚 COLETA SAC CINI

        </div>

        <div style="
            color:#8FA7D8;
            font-size:15px;
            margin-top:8px;
        ">

            Sistema operacional de coletas SAC

        </div>

    </div>

    """, unsafe_allow_html=True)

    st.caption(
        f"Usuário conectado: {st.session_state.usuario}"
    )

with col3:

    st.write("")

    if st.button("🚪 SAIR"):

        st.session_state.logado = False
        st.session_state.usuario = ""

        st.rerun()

st.divider()

# =========================================================
# IMPORTAÇÃO
# =========================================================

arquivo = st.file_uploader(
    "📥 Importar planilha COLETA SAC",
    type=["xlsx"]
)

# =========================================================
# CLASSE PDF
# =========================================================

class PDF(FPDF):

    def header(self):

        self.set_fill_color(2, 21, 43)

        self.rect(
            0,
            0,
            210,
            30,
            "F"
        )

        caminho_logo = os.path.join(
            os.path.dirname(__file__),
            "logo.png"
        )

        if os.path.exists(caminho_logo):

            self.image(
                caminho_logo,
                x=12,
                y=6,
                w=16
            )

        self.set_text_color(255,255,255)

        self.set_font(
            "Helvetica",
            "B",
            20
        )

        self.set_xy(34,8)

        self.cell(
            0,
            8,
            "COLETA SAC CINI",
            ln=True
        )

        self.set_font(
            "Helvetica",
            "",
            9
        )

        self.set_x(34)

        self.cell(
            0,
            5,
            "Relatorio operacional de coleta"
        )

        self.ln(22)

    def footer(self):

        self.set_y(-15)

        self.set_font(
            "Helvetica",
            "I",
            8
        )

        self.set_text_color(120,120,120)

        self.cell(
            0,
            10,
            f"Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            align="C"
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

        faltando = [

            c for c in colunas
            if c not in df.columns

        ]

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

        # ENDEREÇO

        df["ENDERECO_COMPLETO"] = (

            df["ENDEREÇO"].fillna("").astype(str) + ", " +
            df["BAIRRO"].fillna("").astype(str) + ", " +
            df["CIDADE"].fillna("").astype(str) + " - " +
            df["ESTADO"].fillna("").astype(str)

        )

        # GOOGLE MAPS

        df["GOOGLE MAPS"] = (

            "https://www.google.com/maps/search/?api=1&query="
            +
            (
                df["ENDERECO_COMPLETO"]
                .fillna("")
                .astype(str)
                .str.replace(" ", "+")
                .str.replace(",", "")
                .str.replace("++", "+")
            )

        )

        # KPIS

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
            sorted(df["CIDADE"].dropna().astype(str).unique())
        )

        if cidades_filtro:

            df = df[
                df["CIDADE"].astype(str).isin(cidades_filtro)
            ]

        status_filtro = st.multiselect(
            "🚦 Filtrar Status",
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

        for i, row in df.iterrows():

            status_cor = (
                "#00FF9D"
                if row["STATUS"] == "COLETADO"
                else "#FFD93D"
            )

            st.markdown(f"""

            <div class="card">

                <div style="
                    font-size:20px;
                    font-weight:700;
                    margin-bottom:10px;
                ">

                    👤 {str(row['NOME DO CONSUMIDOR'])}

                </div>

                <div style="
                    color:#B7C7EA;
                    line-height:1.8;
                ">

                    📦 Produto:
                    {str(row['PRODUTO'])}<br>

                    📍 Cidade:
                    {str(row['CIDADE'])}<br>

                    🏪 Estabelecimento:
                    {str(row['NOME DO ESTABELECIMENTO'])}<br>

                    📞 Telefone:
                    {str(row['TELEFONE CONSUMIDOR'])}<br>

                </div>

                <div style="
                    margin-top:10px;
                    font-weight:700;
                    color:{status_cor};
                ">

                    🚦 {str(row['STATUS'])}

                </div>

                <div style="margin-top:15px;">

                    <a
                        href="{str(row['GOOGLE MAPS'])}"
                        target="_blank"
                        style="
                            background:#00AEEF;
                            color:white;
                            padding:10px 16px;
                            border-radius:10px;
                            text-decoration:none;
                            font-weight:700;
                            display:inline-block;
                        "
                    >

                        🗺️ Abrir Google Maps

                    </a>

                </div>

            </div>

            """, unsafe_allow_html=True)

        st.divider()

        # PDF

        st.subheader("📄 Exportação PDF")

        if st.button("📄 GERAR PDF DE PENDÊNCIAS"):

            df_pdf = df[
                df["STATUS"] == "AGUARDANDO"
            ]

            if len(df_pdf) == 0:

                st.warning("⚠️ Não existem pendências.")

            else:

                pdf = PDF()

                pdf.set_auto_page_break(
                    auto=True,
                    margin=20
                )

                for i, row in df_pdf.iterrows():

                    pdf.add_page()

                    pdf.set_draw_color(220,220,220)

                    pdf.rect(
                        10,
                        38,
                        190,
                        170
                    )

                    pdf.set_text_color(25,25,25)

                    pdf.set_font(
                        "Helvetica",
                        "B",
                        12
                    )

                    y = 50

                    campos = [

                        ("Cliente:", row["NOME DO CONSUMIDOR"]),
                        ("Produto:", row["PRODUTO"]),
                        ("Quantidade:", str(row["QUANTIDADE COM DEFEITO"])),
                        ("Telefone:", str(row["TELEFONE CONSUMIDOR"])),
                        ("Endereco:", row["ENDERECO_COMPLETO"])

                    ]

                    for titulo, valor in campos:

                        pdf.set_xy(18, y)

                        pdf.cell(
                            38,
                            8,
                            titulo
                        )

                        pdf.set_font(
                            "Helvetica",
                            "",
                            12
                        )

                        pdf.set_xy(58, y)

                        pdf.multi_cell(
                            125,
                            8,
                            str(valor)
                        )

                        pdf.set_font(
                            "Helvetica",
                            "B",
                            12
                        )

                        y += 18

                    y += 15

                    pdf.set_xy(18, y)

                    pdf.cell(
                        0,
                        8,
                        "[ ] Coletado"
                    )

                    y += 14

                    pdf.set_xy(18, y)

                    pdf.cell(
                        0,
                        8,
                        "[ ] Recebido no estabelecimento"
                    )

                    y += 60

                    pdf.line(
                        60,
                        y,
                        150,
                        y
                    )

                    pdf.set_font(
                        "Helvetica",
                        "",
                        10
                    )

                    pdf.set_xy(70, y+2)

                    pdf.cell(
                        70,
                        8,
                        "Assinatura Responsavel",
                        align="C"
                    )

                pdf_bytes = bytes(
                    pdf.output(dest="S")
                )

                st.download_button(

                    label="⬇️ BAIXAR PDF",

                    data=pdf_bytes,

                    file_name=f"coletas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",

                    mime="application/pdf"

                )

    except Exception as erro:

        st.error(f"❌ Erro ao processar planilha: {erro}")