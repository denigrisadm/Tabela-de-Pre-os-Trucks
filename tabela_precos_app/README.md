# TABELA DE PREÇOS

Este é um sistema web simples para consulta de preços de veículos, desenvolvido com Flask (Python) para o backend e HTML/CSS/JavaScript para o frontend. Ele permite buscar veículos por modelo, variante ou UP, aplicar descontos dinamicamente e fazer upload de novas planilhas Excel para atualização dos dados.

## Funcionalidades

- **Busca de Veículos**: Pesquisa por modelo, variante ou UP, com resultados dinâmicos.
- **Descontos Dinâmicos**: Aplicação de descontos percentuais (0,5% a 3%) no preço de venda, com exibição do preço original e do preço com desconto.
- **Upload de Planilha**: Permite que o usuário faça upload de uma nova planilha Excel (`.xlsx`) para atualizar os dados de preços.
- **Download de Template**: Botão para baixar o template da planilha utilizada.
- **Interface Moderna**: Design responsivo com fundo azul corporativo, textos em branco e logotipos.

## Estrutura do Projeto

```
tabela_precos_app/
├── venv/                   # Ambiente virtual Python
├── src/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tabela_updated.py # Lógica do backend para busca e upload
│   │   └── dados_planilha.py # Dados da planilha convertidos para Python
│   ├── static/             # Arquivos estáticos (HTML, CSS, JS, imagens, planilha)
│   │   ├── index.html      # Frontend da aplicação
│   │   ├── logotipoMercedes.png
│   │   ├── logo-de-nigris-60-comercial-02-BRANCO].png
│   │   └── TabeladepreçoJulho25.25.xlsx # Planilha de exemplo
│   └── main.py             # Ponto de entrada da aplicação Flask
├── requirements.txt        # Dependências do Python
└── README.md               # Este arquivo
```

## Como Executar Localmente

1.  **Clone o repositório:**

    ```bash
    git clone <URL_DO_SEU_REPOSITORIO>
    cd tabela_precos_app
    ```

2.  **Crie e ative o ambiente virtual:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare os dados da planilha:**

    Certifique-se de que a planilha `TabeladepreçoJulho25.25.xlsx` esteja em `src/static/`. Se você tiver uma nova planilha, coloque-a lá.

    Execute o script `converter_planilha.py` (localizado na raiz do projeto) para gerar o arquivo `dados_planilha.py` que será usado pelo backend:

    ```bash
    python converter_planilha.py
    ```

    *Certifique-se de que o caminho da planilha no `converter_planilha.py` esteja correto: `excel_file = 'src/static/TabeladepreçoJulho25.25.xlsx'`*

5.  **Inicie a aplicação Flask:**

    ```bash
    python src/main.py
    ```

    A aplicação estará disponível em `http://localhost:5000`.

## Deploy no GitHub e Streamlit (Exemplo)

Este projeto é um aplicativo web Flask. Para deploy em plataformas como o Streamlit, que são mais focadas em Python puro e apps interativos, você precisaria adaptar a abordagem. Uma forma comum é usar o Streamlit para criar a interface e o Flask como uma API separada, ou reescrever a lógica de frontend em Streamlit.

**Para GitHub:**

1.  **Crie um novo repositório no GitHub.**
2.  **Inicialize o Git localmente e adicione os arquivos:**

    ```bash
    git init
    git add .
    git commit -m "Initial commit: Tabela de Preços App"
    git branch -M main
    git remote add origin <URL_DO_SEU_REPOSITORIO>
    git push -u origin main
    ```

**Para Streamlit (Adaptação Necessária):**

O Streamlit é ideal para criar aplicativos web interativos puramente em Python. Para usar este projeto no Streamlit, você precisaria reescrever a interface (`index.html`) e a lógica de interação (`JavaScript`) usando os componentes do Streamlit. O backend Flask (`tabela_updated.py`) poderia ser adaptado para ser uma função dentro do Streamlit ou ser exposto como uma API separada (o que exigiria um serviço de deploy para o Flask).

**Exemplo de como seria a estrutura para Streamlit (conceitual):**

```python
# app_streamlit.py

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
            preco_venda = preco_venda.replace("R$", "").replace(".", "").replace(",", "").strip()
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

if uploaded_file is not None:
    st.sidebar.success("Planilha carregada com sucesso!")
    dados_planilha = load_data(uploaded_file)
else:
    # Carregar planilha padrão se nenhuma for enviada
    default_excel_path = os.path.join(os.path.dirname(__file__), "src", "static", "TabeladepreçoJulho25.25.xlsx")
    if os.path.exists(default_excel_path):
        dados_planilha = load_data(default_excel_path)
    else:
        st.error("Nenhuma planilha padrão encontrada e nenhuma foi enviada.")
        dados_planilha = []

st.sidebar.markdown("--- ")
st.sidebar.download_button(
    label="⬇️ Baixar Template",
    data=open(os.path.join(os.path.dirname(__file__), "src", "static", "TabeladepreçoJulho25.25.xlsx"), "rb").read(),
    file_name="template_tabela_precos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


st.header("🔍 Buscar Veículo")
termo_busca = st.text_input("Digite o modelo, variante ou UP...", "").upper().strip()

resultados = []
if termo_busca and dados_planilha:
    for item in dados_planilha:
        if (termo_busca in item["MODELO"].upper() or 
            termo_busca in item["UP"].upper() or 
            termo_busca in item["VARIANTE"].upper()):
            resultados.append(item)

st.subheader(f"📋 Resultados da Busca ({len(resultados)} encontrado(s))")

if resultados:
    for i, resultado in enumerate(resultados):
        st.markdown(f"### {resultado['MODELO']}")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("UP", resultado["UP"])
        col2.metric("Variante", resultado["VARIANTE"])
        col3.metric("Tabela", resultado["TABELA"])
        col4.metric("Ano", resultado["ANO"])

        preco_venda_original = resultado["PREÇO VENDA"]
        preco_venda_atual = st.session_state.get(f'preco_venda_{i}', preco_venda_original)

        st.markdown(f"**Preço de Venda:** R$ {preco_venda_atual:,.2f}")

        descontos = [0.5, 1, 1.5, 2, 2.5, 3]
        cols_desconto = st.columns(len(descontos) + 1)

        for j, desconto_percentual in enumerate(descontos):
            if cols_desconto[j].button(f"{desconto_percentual}%"): # , key=f"btn_desc_{i}_{j}"
                novo_preco = preco_venda_original * (1 - desconto_percentual / 100)
                st.session_state[f'preco_venda_{i}'] = novo_preco
                st.experimental_rerun()
        
        if cols_desconto[len(descontos)].button("Reset"): # , key=f"btn_reset_{i}"
            st.session_state[f'preco_venda_{i}'] = preco_venda_original
            st.experimental_rerun()

        st.markdown("--- ")

else:
    st.info("Nenhum veículo encontrado. Tente um termo de busca diferente.")

```

**Observações sobre o Streamlit:**

-   O exemplo acima é uma adaptação conceitual. Você precisaria criar um arquivo `app_streamlit.py` e ajustar os caminhos dos arquivos.
-   O Streamlit lida com o estado da aplicação de forma diferente (usando `st.session_state`).
-   O `st.cache_data` é usado para otimizar o carregamento da planilha.
-   O estilo CSS é injetado diretamente via `st.markdown`.

## Contato

Para dúvidas ou suporte, entre em contato com o desenvolvedor.

