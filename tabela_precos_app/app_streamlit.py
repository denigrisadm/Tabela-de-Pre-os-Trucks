import streamlit as st
import pandas as pd
import os

# Carregar dados da planilha (adaptado para Streamlit)
@st.cache_data
def load_data(file_path):
    df = pd.read_excel(file_path)
    data_list = []
    for _, row in df.iterrows():
        preco_venda = row["PREÇO VENDA"]
        if isinstance(preco_venda, str):
            # Remove R$, pontos e vírgulas, depois converte para int
            preco_venda = preco_venda.replace("R$", "").replace(".", "").replace(",", "").strip()
            # Verifica se a string resultante é um número antes de converter
            preco_venda = int(preco_venda) if preco_venda.isdigit() else 0
        else:
            preco_venda = int(preco_venda)
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

st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4, h5, h6 { color: white; }
    .stTextInput > div > div > input { background-color: rgba(255, 255, 255, 0.9); color: #333; }
    .stButton > button { background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white; }
    .stFileUploader > div > button { background: linear-gradient(45deg, #4834d4, #686de0); color: white; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("TABELA DE PREÇOS")
st.subheader("Sistema de Consulta de Preços de Veículos")

# Upload de planilha
st.sidebar.header("Importar Tabela")
uploaded_file = st.sidebar.file_uploader("Selecione uma nova planilha (.xlsx)", type=["xlsx"])

# Inicializa session_state para armazenar o estado da planilha
if 'dados_planilha' not in st.session_state:
    st.session_state.dados_planilha = []

if uploaded_file is not None:
    st.sidebar.success("Planilha carregada com sucesso!")
    st.session_state.dados_planilha = load_data(uploaded_file)
else:
    # Carregar planilha padrão se nenhuma for enviada ou se for a primeira vez
    if not st.session_state.dados_planilha:
        default_excel_path = os.path.join(os.path.dirname(__file__), "src", "static", "TabeladepreçoJulho25.25.xlsx")
        if os.path.exists(default_excel_path):
            st.session_state.dados_planilha = load_data(default_excel_path)
        else:
            st.error("Nenhuma planilha padrão encontrada e nenhuma foi enviada.")
            st.session_state.dados_planilha = []

st.sidebar.markdown("--- ")

# Botão para baixar o template
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
    st.sidebar.warning("Template da planilha não encontrado.")


st.header("🔍 Buscar Veículo")
termo_busca = st.text_input("Digite o modelo, variante ou UP...", "").upper().strip()

resultados = []
if termo_busca and st.session_state.dados_planilha:
    for item in st.session_state.dados_planilha:
        if (termo_busca in item["MODELO"].upper() or 
            termo_busca in item["UP"].upper() or 
            termo_busca in item["VARIANTE"].upper()):
            resultados.append(item)

st.subheader(f"📋 Resultados da Busca ({len(resultados)} encontrado(s))")

if resultados:
    for i, resultado in enumerate(resultados):
        st.markdown(f"### {resultado["MODELO"]}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("UP", resultado["UP"])
        col2.metric("Variante", resultado["VARIANTE"])
        col3.metric("Tabela", resultado["TABELA"])
        col4.metric("Ano", resultado["ANO"])

        preco_venda_original = resultado["PREÇO VENDA"]
        
        # Inicializa o preço atual para cada item na sessão
        if f'preco_venda_{i}' not in st.session_state:
            st.session_state[f'preco_venda_{i}'] = preco_venda_original

        preco_venda_atual = st.session_state[f'preco_venda_{i}']

        st.markdown(f"**Preço de Venda:** R$ {preco_venda_atual:,.2f}")

        descontos = [0.5, 1, 1.5, 2, 2.5, 3]
        cols_desconto = st.columns(len(descontos) + 1)

        for j, desconto_percentual in enumerate(descontos):
            if cols_desconto[j].button(f"{desconto_percentual}%", key=f"btn_desc_{i}_{j}"):
                novo_preco = preco_venda_original * (1 - desconto_percentual / 100)
                st.session_state[f'preco_venda_{i}'] = novo_preco
                st.experimental_rerun() # Recarrega a página para aplicar o desconto
        
        if cols_desconto[len(descontos)].button("Reset", key=f"btn_reset_{i}"):
            st.session_state[f'preco_venda_{i}'] = preco_venda_original
            st.experimental_rerun() # Recarrega a página para resetar o preço

        st.markdown("--- ")

else:
    st.info("Nenhum veículo encontrado. Tente um termo de busca diferente.")