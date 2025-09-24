import streamlit as st
import pandas as pd
import os

# Carregar dados da planilha
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    data_list = []
    for _, row in df.iterrows():
        preco_venda = row["PREÇO VENDA"]
        if isinstance(preco_venda, str):
            preco_venda = preco_venda.replace("R$", "").replace(".", "").replace(",", "").strip()
            preco_venda = float(preco_venda) if preco_venda.replace(".", "").isdigit() else 0.0
        else:
            preco_venda = float(preco_venda)
        data_list.append({
            "MODELO": str(row["MODELO"]),
            "UP": str(row["UP"]),
            "VARIANTE": str(row["VARIANTE"]),
            "TABELA": str(row["TABELA"]),
            "PREÇO VENDA": preco_venda,
            "ANO": str(row["ANO"])
        })
    return data_list

# --- Interface Streamlit ---
st.set_page_config(layout="wide", page_title="Tabela de Preços")

# Injetar CSS para identidade corporativa
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    html, body, [class*=


"css"] {
        font-family: 'Roboto', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }

    .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
        background: transparent;
    }

    h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: white !important;
        font-weight: 700;
    }

    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.95);
        color: #333;
        border: 2px solid #4CAF50;
        border-radius: 8px;
        font-size: 16px;
        padding: 10px;
    }

    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(45deg, #ee5a24, #ff6b6b);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }

    .stFileUploader > div > button {
        background: linear-gradient(45deg, #4834d4, #686de0);
        color: white;
        border: none;
        border-radius: 8px;
    }

    .stSidebar {
        background: rgba(30, 60, 114, 0.9);
    }

    .stSidebar .stMarkdown {
        color: white;
    }

    .metric-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .resultado-container {
        background: rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    .preco-venda {
        background: linear-gradient(45deg, #f39c12, #e67e22);
        color: white;
        padding: 10px 15px;
        border-radius: 8px;
        font-size: 18px;
        font-weight: bold;
        text-align: center;
        margin: 10px 0;
    }

    .desconto-info {
        background: rgba(46, 204, 113, 0.2);
        color: #2ecc71;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 14px;
        margin-top: 5px;
        border: 1px solid #2ecc71;
    }

    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        margin: 20px 0;
        padding: 20px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
    }

    .logo-container img {
        max-height: 60px;
        filter: brightness(1.1);
    }

    .status-info {
        background: rgba(46, 204, 113, 0.2);
        color: #2ecc71;
        padding: 10px 15px;
        border-radius: 8px;
        text-align: center;
        margin: 15px 0;
        border: 1px solid #2ecc71;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Cabeçalho com logos
st.markdown(
    """
    <div class="logo-container">
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==" alt="Mercedes Logo" style="max-height: 60px;">
        <div style="text-align: center;">
            <h1 style="margin: 0; color: white; font-size: 2.5rem;">TABELA DE PREÇOS</h1>
            <p style="margin: 5px 0 0 0; color: rgba(255,255,255,0.8); font-size: 1.1rem;">Sistema de Consulta de Preços de Veículos</p>
        </div>
        <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==" alt="De Nigris Logo" style="max-height: 60px;">
    </div>
    """,
    unsafe_allow_html=True
)

# Inicializar session_state
if 'dados_planilha' not in st.session_state:
    st.session_state.dados_planilha = []

if 'precos_com_desconto' not in st.session_state:
    st.session_state.precos_com_desconto = {}

if 'descontos_aplicados' not in st.session_state:
    st.session_state.descontos_aplicados = {}

# Sidebar para upload
st.sidebar.header("📁 Importar Tabela")
uploaded_file = st.sidebar.file_uploader("Selecione uma nova planilha (.xlsx)", type=["xlsx"])

if uploaded_file is not None:
    st.sidebar.success("✅ Planilha carregada com sucesso!")
    st.session_state.dados_planilha = load_data(uploaded_file)
    # Limpar preços com desconto quando nova planilha é carregada
    st.session_state.precos_com_desconto = {}
    st.session_state.descontos_aplicados = {}
else:
    # Carregar planilha padrão se nenhuma for enviada
    if not st.session_state.dados_planilha:
        default_excel_path = os.path.join(os.path.dirname(__file__), "src", "static", "TabeladepreçoJulho25.25.xlsx")
        if os.path.exists(default_excel_path):
            st.session_state.dados_planilha = load_data(default_excel_path)
        else:
            st.error("❌ Nenhuma planilha padrão encontrada e nenhuma foi enviada.")
            st.session_state.dados_planilha = []

st.sidebar.markdown("---")

# Botão para baixar template
def get_template_excel():
    template_path = os.path.join(os.path.dirname(__file__), "src", "static", "TabeladepreçoJulho25.25.xlsx")
    if os.path.exists(template_path):
        with open(template_path, "rb") as f:
            return f.read()
    return None

template_data = get_template_excel()
if template_data:
    st.sidebar.download_button(
        label="⬇️ Baixar Template",
        data=template_data,
        file_name="template_tabela_precos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.sidebar.warning("⚠️ Template da planilha não encontrado.")

# Status do sistema
if st.session_state.dados_planilha:
    st.markdown(
        f"""
        <div class="status-info">
            ✅ Sistema pronto • {len(st.session_state.dados_planilha)} veículos carregados
        </div>
        """,
        unsafe_allow_html=True
    )

# Seção de busca
st.markdown("## 🔍 Buscar Veículo")
termo_busca = st.text_input("Digite o modelo, variante ou UP...", "", placeholder="Ex: ACCELO, UPA, 02037T...")

# Buscar resultados
resultados = []
if termo_busca and st.session_state.dados_planilha:
    termo_busca_upper = termo_busca.upper().strip()
    for item in st.session_state.dados_planilha:
        if (termo_busca_upper in item["MODELO"].upper() or 
            termo_busca_upper in item["UP"].upper() or 
            termo_busca_upper in item["VARIANTE"].upper()):
            resultados.append(item)

# Exibir resultados
st.markdown(f"## 📋 Resultados da Busca")
if termo_busca:
    st.markdown(f"**{len(resultados)} resultado(s) encontrado(s) para '{termo_busca}'**")
else:
    st.markdown("**Digite um termo de busca para ver os resultados**")

if resultados:
    for i, resultado in enumerate(resultados):
        # Criar chave única para cada resultado
        resultado_key = f"{resultado['MODELO']}_{resultado['UP']}_{resultado['VARIANTE']}"
        
        st.markdown(
            f"""
            <div class="resultado-container">
                <h3 style="color: white; margin-top: 0;">{resultado['MODELO']}</h3>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Métricas em colunas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                f"""
                <div class="metric-container">
                    <strong>UP:</strong><br>{resultado['UP']}
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div class="metric-container">
                    <strong>Variante:</strong><br>{resultado['VARIANTE']}
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f"""
                <div class="metric-container">
                    <strong>Tabela:</strong><br>{resultado['TABELA']}
                </div>
                """,
                unsafe_allow_html=True
            )
        with col4:
            st.markdown(
                f"""
                <div class="metric-container">
                    <strong>Ano:</strong><br>{resultado['ANO']}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Preço de venda
        preco_original = resultado["PREÇO VENDA"]
        preco_atual = st.session_state.precos_com_desconto.get(resultado_key, preco_original)
        desconto_aplicado = st.session_state.descontos_aplicados.get(resultado_key, 0)
        
        if desconto_aplicado > 0:
            economia = preco_original - preco_atual
            st.markdown(
                f"""
                <div class="preco-venda">
                    <div style="text-decoration: line-through; opacity: 0.7; font-size: 14px;">
                        Preço de Venda: R$ {preco_original:,.2f}
                    </div>
                    <div style="font-size: 20px; margin-top: 5px;">
                        Preço de Venda: R$ {preco_atual:,.2f}
                    </div>
                </div>
                <div class="desconto-info">
                    Desconto de {desconto_aplicado}% aplicado (-R$ {economia:,.2f})
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="preco-venda">
                    Preço de Venda: R$ {preco_atual:,.2f}
                </div>
                """,
                unsafe_allow_html=True
            )

        # Botões de desconto
        st.markdown("**Aplicar Desconto:**")
        descontos = [0.5, 1, 1.5, 2, 2.5, 3]
        cols_desconto = st.columns(len(descontos) + 1)

        for j, desconto_percentual in enumerate(descontos):
            with cols_desconto[j]:
                if st.button(f"{desconto_percentual}%", key=f"btn_desc_{resultado_key}_{j}"):
                    novo_preco = preco_original * (1 - desconto_percentual / 100)
                    st.session_state.precos_com_desconto[resultado_key] = novo_preco
                    st.session_state.descontos_aplicados[resultado_key] = desconto_percentual
                    st.rerun()
        
        with cols_desconto[len(descontos)]:
            if st.button("Reset", key=f"btn_reset_{resultado_key}"):
                if resultado_key in st.session_state.precos_com_desconto:
                    del st.session_state.precos_com_desconto[resultado_key]
                if resultado_key in st.session_state.descontos_aplicados:
                    del st.session_state.descontos_aplicados[resultado_key]
                st.rerun()

        st.markdown("---")

elif termo_busca:
    st.info("🔍 Nenhum veículo encontrado. Tente um termo de busca diferente.")
else:
    st.info("💡 Digite um modelo, variante ou UP para buscar veículos.")
