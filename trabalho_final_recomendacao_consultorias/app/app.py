"""
Demonstracao do modelo de propensao a contratacao de consultoria.

Roda local, em cima dos arquivos salvos pelo notebook:
  modelos/propensao_consultoria.keras   -> a rede treinada
  modelos/propensao_artefatos.joblib    -> pre-processador + configuracao usada no treino

Para executar:
  streamlit run app.py
"""

import os

import numpy as np
import pandas as pd
import streamlit as st

# as listas de opcoes e o pre-processador vem dos artefatos, nao estao escritos aqui
PASTA_APP = os.path.dirname(os.path.abspath(__file__))
PASTA_MODELOS = os.path.join(os.path.dirname(PASTA_APP), 'modelos')
CAMINHO_MODELO = os.path.join(PASTA_MODELOS, 'propensao_consultoria.keras')
CAMINHO_ARTEFATOS = os.path.join(PASTA_MODELOS, 'propensao_artefatos.joblib')

ROTULOS = {
    'Qtd de atendimentos PJ': 'Atendimentos PJ ja realizados',
    'Qtd de projetos atendidos': 'Projetos em que a empresa participou',
    'idade_empresa_meses': 'Idade da empresa (meses)',
    'ds_sebrae_segmento': 'Segmento',
    'nm_municipio': 'Municipio',
    'ds_tipo_estabelecimento': 'Tipo de estabelecimento',
    'sg_porte': 'Porte',
}

st.set_page_config(page_title='Propensao a contratar consultoria', layout='wide')


def carregar_artefatos(caminho):
    """mesma leitura do notebook: tenta joblib e cai pro dill, que foi quem deu conta
    de serializar o transformador customizado"""
    import joblib
    try:
        return joblib.load(caminho)
    except Exception:
        import dill
        with open(caminho, 'rb') as arquivo:
            return dill.load(arquivo)


@st.cache_resource(show_spinner='Carregando modelo...')
def carregar_tudo():
    """carrega uma unica vez; o Streamlit reusa em toda interacao da pagina"""
    from tensorflow import keras
    modelo = keras.models.load_model(CAMINHO_MODELO, compile=False)
    artefatos = carregar_artefatos(CAMINHO_ARTEFATOS)
    return modelo, artefatos


def opcoes_por_variavel(artefatos):
    """as categorias que o modelo viu no treino. No modelo base elas estao no mapa de
    frequencias; no modelo com embeddings, no mapa de indices."""
    if artefatos['tipo_modelo'].startswith('Base'):
        codificador = artefatos['pre_processador'].named_transformers_['cat'].named_steps['frequencia']
        mapas = codificador.freq_maps_
    else:
        _, codificador = artefatos['artefatos_embeddings']
        mapas = codificador.mapas_
    return {coluna: sorted(str(c) for c in mapas[coluna]) for coluna in mapas}


def montar_entrada(linha, artefatos):
    """transforma a empresa digitada no formato que a rede espera"""
    numericas = artefatos['features_numericas']
    categoricas = artefatos['features_categoricas']
    df = pd.DataFrame([linha])[numericas + categoricas]

    if artefatos['tipo_modelo'].startswith('Base'):
        return artefatos['pre_processador'].transform(df).values.astype('float32')

    pipeline_num, codificador = artefatos['artefatos_embeddings']
    entradas = codificador.transform(df)
    entradas['numericas'] = pipeline_num.transform(df[numericas]).astype('float32')
    return entradas


st.title('Esta empresa tem propensao a contratar uma consultoria?')
st.caption(
    'Demonstracao do modelo treinado no trabalho final de Aprendizado Profundo. '
    'A rede recebe as 7 variaveis de perfil e atendimento e devolve a probabilidade de contratacao.'
)

if not os.path.exists(CAMINHO_MODELO) or not os.path.exists(CAMINHO_ARTEFATOS):
    st.error(
        'Nao encontrei os arquivos do modelo em `modelos/`. Rode o notebook ate a secao 13 '
        '(Salvando o modelo) antes de abrir o app.'
    )
    st.stop()

modelo, artefatos = carregar_tudo()
opcoes = opcoes_por_variavel(artefatos)
LIMIAR = float(artefatos['limiar'])
TAXA_BASE = float(artefatos['taxa_base'])

with st.sidebar:
    st.header('Modelo em uso')
    st.write(f"**Arquitetura:** {artefatos['tipo_modelo']}")
    st.write(f"**Contra-peso de classe:** {artefatos['modo_peso']}")
    st.write(f"**Limiar de decisao:** {LIMIAR:.2f}")
    st.write(f"**Taxa-base da populacao:** {TAXA_BASE*100:.2f}%")
    st.divider()
    st.caption('Hiperparametros escolhidos pelo Optuna')
    st.json(artefatos['melhores_hiperparametros'], expanded=False)

st.subheader('Dados da empresa')

with st.form('empresa'):
    col_esq, col_dir = st.columns(2)

    with col_esq:
        atendimentos = st.number_input(ROTULOS['Qtd de atendimentos PJ'],
                                       min_value=0, max_value=20000, value=4, step=1)
        projetos = st.number_input(ROTULOS['Qtd de projetos atendidos'],
                                   min_value=0, max_value=500, value=1, step=1)
        idade = st.number_input(ROTULOS['idade_empresa_meses'],
                                min_value=0, max_value=1200, value=60, step=1)
        st.caption(f'{idade / 12:.1f} anos de empresa')

    with col_dir:
        segmento = st.selectbox(ROTULOS['ds_sebrae_segmento'], opcoes['ds_sebrae_segmento'])
        municipio = st.selectbox(ROTULOS['nm_municipio'], opcoes['nm_municipio'])
        tipo = st.selectbox(ROTULOS['ds_tipo_estabelecimento'], opcoes['ds_tipo_estabelecimento'])
        porte = st.selectbox(ROTULOS['sg_porte'], opcoes['sg_porte'])

    enviado = st.form_submit_button('Calcular propensao', type='primary')

if enviado:
    linha = {
        'Qtd de atendimentos PJ': atendimentos,
        'Qtd de projetos atendidos': projetos,
        'idade_empresa_meses': idade,
        'ds_sebrae_segmento': segmento,
        'nm_municipio': municipio,
        'ds_tipo_estabelecimento': tipo,
        'sg_porte': porte,
    }

    entrada = montar_entrada(linha, artefatos)
    probabilidade = float(modelo.predict(entrada, verbose=0).ravel()[0])
    sinalizar = probabilidade >= LIMIAR

    st.subheader('Resultado')
    col_prob, col_decisao = st.columns([1, 2])

    with col_prob:
        st.metric('Probabilidade prevista', f'{probabilidade*100:.1f}%')
        st.progress(min(probabilidade, 1.0))

    with col_decisao:
        if sinalizar:
            st.success(
                f'**Sinalizar para contato.** A probabilidade prevista ({probabilidade*100:.1f}%) '
                f'passou do limiar de {LIMIAR*100:.0f}%.'
            )
        else:
            st.info(
                f'**Nao sinalizar agora.** A probabilidade prevista ({probabilidade*100:.1f}%) '
                f'ficou abaixo do limiar de {LIMIAR*100:.0f}%.'
            )

    st.caption(
        'O treino usou contra-peso de classe, o que empurra as probabilidades para cima: '
        'o valor serve para ordenar empresas e para comparar com o limiar, nao para ser lido '
        f'como chance real de contratacao (a taxa observada na base e de {TAXA_BASE*100:.2f}%).'
    )

    with st.expander('O que foi enviado para a rede'):
        st.dataframe(pd.DataFrame([linha]).T.rename(columns={0: 'valor'}))
        if isinstance(entrada, np.ndarray):
            st.caption(f'Vetor de entrada apos o pre-processamento: {entrada.shape}')
            st.dataframe(pd.DataFrame(entrada, columns=[
                c.split('__')[-1] for c in
                artefatos['pre_processador'].get_feature_names_out()
            ]).T.rename(columns={0: 'valor padronizado'}))
