# App de demonstração (localhost)

Interface simples para aplicar o modelo treinado em uma empresa por vez: preenche as 7 variáveis,
a rede devolve a probabilidade de contratação e a decisão no limiar de 0,5.

## O que o app usa

Os dois arquivos salvos pelo notebook na seção 13, que precisam estar na pasta `modelos/`:

```
trabalho_final_recomendacao_consultorias/
├── modelos/
│   ├── propensao_consultoria.keras    <- a rede treinada
│   └── propensao_artefatos.joblib     <- pré-processador, limiar, taxa-base, hiperparâmetros
└── app/
    ├── app.py
    └── requirements.txt
```

O app não lê a base de dados. As listas de municípios, segmentos, portes e tipos de estabelecimento
saem do próprio pré-processador — são exatamente as categorias que o modelo viu no treino.

## Passo a passo

Abra o terminal dentro da pasta `app` e rode:

```bash
pip install -r requirements.txt
streamlit run app.py
```

O Streamlit abre o navegador em `http://localhost:8501`. Para encerrar, `Ctrl+C` no terminal.

## Se der erro ao carregar

- **"Não encontrei os arquivos do modelo em modelos/"** — o notebook não chegou até a seção 13, ou
  os arquivos ficaram em outra pasta. Basta copiá-los para `modelos/`.
- **Erro de desserialização no `.joblib`** — os artefatos foram salvos com o `dill`, por isso ele
  está no `requirements.txt`. Confirme que a instalação incluiu o pacote.
- **Aviso de versão do scikit-learn** — é só aviso. Aparece quando a versão local é diferente da do
  ambiente em que o modelo foi treinado e não impede a previsão.

## O que mostrar na apresentação

1. Uma empresa com pouco histórico de atendimento — a probabilidade fica baixa e o app não sinaliza.
2. A mesma empresa com mais atendimentos e projetos — a probabilidade sobe e cruza o limiar.
3. A barra lateral, que mostra a arquitetura escolhida, o contra-peso de classe, o limiar e a
   taxa-base de 2,5%.
4. O expansor "O que foi enviado para a rede", que mostra o vetor depois do pré-processamento —
   é onde se vê o `log1p`, a padronização e a codificação por frequência agindo.

A legenda embaixo do resultado já registra a ressalva que vale repetir em voz alta: o contra-peso
infla as probabilidades, então o número serve para ordenar empresas e comparar com o limiar, não
para ser lido como chance real de contratação.
