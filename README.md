# Aprendizado Profundo — Trabalho: Intro. Redes Neurais e Redes Convolucionais

Repositório: https://github.com/lucassmsantoss/aprendizado-profundo

Aluno: Lucas Medeiros
Disciplina: Aprendizado Profundo — PPgTI/IMD/UFRN
Docente: Prof. Josenalde Oliveira

Este repositório reúne as 3 tarefas solicitadas e o trabalho final da disciplina:

- **Tarefa 1** (`tarefa1/`): Estudo dirigido do TensorFlow Playground — experimentos reais de hiperparâmetros e respostas aos exercícios de fixação.
- **Tarefa 2** (`tarefa2/`): Otimização de hiperparâmetros do MNIST com Optuna, a partir do notebook base do professor.
- **Tarefa 3** (`tarefa3/`): Reprodução em PyTorch das arquiteturas CNN do artigo Silva Filho et al. (2022) sobre o Multiprova Corretor, aplicadas a subconjuntos do EMNIST (dígitos 1-5, V/F e letras A-E), com análise de parâmetros/tamanho dos modelos.
- **Trabalho Final** (`trabalho_final_recomendacao_consultorias/`): Propensão de contratação de consultoria — projeto individual completo (Data Product Canvas, notebook, modelo treinado e app de demonstração).

Um PDF único com as 3 tarefas consolidadas está em `relatorio_completo.pdf`.

## Notebooks

- Tarefa 2 — MNIST + Optuna: `tarefa2/tarefa2_mnist_optuna.ipynb` (já executado, com todos os
  outputs, gráficos e resultados reais salvos no próprio arquivo) — link Colab:
  https://colab.research.google.com/drive/1zFKRRcnSVH_FaU9bMy0xza6bvzjJmGZG?usp=sharing
- Tarefa 3 — CNNs PyTorch + EMNIST: `tarefa3/tarefa3_cnn_emnist_pytorch.ipynb` (já executado, com
  todos os outputs, gráficos e resultados reais salvos no próprio arquivo) — link Colab:
  https://colab.research.google.com/drive/1j0Qyu3_pJIpritZf15XOShYtwKJQGQu_?usp=sharing

## Trabalho Final — Propensão de Contratação de Consultoria

Na empresa que trabalho atendemos milhares de empresas por ano, mas o contato comercial é um recurso limitado.
Hoje não existe critério para decidir a quem oferecer uma consultoria: quem chuta acerta na
taxa-base da população, cerca de **2,5%** — uma contratação a cada 40 abordagens.

O projeto treina uma rede neural para responder uma pergunta binária — **esta empresa tem propensão
a contratar uma consultoria?** — usando 7 variáveis de perfil cadastral e histórico de atendimento
(atendimentos PJ, projetos atendidos, idade da empresa, segmento, município, tipo de
estabelecimento e porte). A saída é uma probabilidade, comparada com o **limiar padrão de 0,5**.

Duas arquiteturas são treinadas e comparadas no mesmo conjunto de teste: um **MLP com codificação
por frequência** das variáveis categóricas, e um **MLP com embeddings**, no qual a rede aprende um
vetor para cada município, segmento, porte e tipo de estabelecimento.

Os dois erros não custam o mesmo: um falso positivo é uma ligação que não converte, um falso
negativo é uma venda perdida que nunca aparece em relatório. Por isso o projeto é orientado a
**recall** da classe "Contratou" — é a métrica que o Optuna maximiza e que o `EarlyStopping`
monitora. O limiar fica fixo em 0,5 e o desbalanceamento é tratado pelos contra-pesos de classe,
comparados em um experimento com três configurações (sem peso, suave e balanceado). Junto do
recall, toda avaliação reporta quantas empresas o modelo mandou abordar, mais precisão, ganho sobre
o acaso, **MCC**, **Brier score**, ROC-AUC e PR-AUC.

- Data Product Canvas: `trabalho_final_recomendacao_consultorias/data_project_canvas_recomendacao_consultorias.png`
- Notebook: `trabalho_final_recomendacao_consultorias/trabalho_final_propensao_consultoria.ipynb`
  — abra e execute direto no Colab:
  https://colab.research.google.com/github/lucassmsantoss/aprendizado-profundo/blob/main/trabalho_final_recomendacao_consultorias/trabalho_final_propensao_consultoria.ipynb
- Modelo treinado (Keras) e pré-processador: `trabalho_final_recomendacao_consultorias/modelos/`
- App de demonstração (roda no localhost): `trabalho_final_recomendacao_consultorias/app/` —
  formulário com as 7 variáveis que aplica o modelo treinado em uma empresa por vez. Instruções em
  `app/COMO_RODAR.md`.
- Base de dados: `trabalho_final_recomendacao_consultorias/base_modelagem_anonimizada.xlsx`,
  incluída neste repositório (já anonimizada). O notebook lê o arquivo local se ele existir e,
  caso contrário, baixa automaticamente direto deste repositório público — funciona em qualquer
  ambiente (Colab, Kaggle, etc.) sem precisar de login ou permissão de Google Drive.
- Vídeo pitch (≤10 min, estilo pitch) explicando pipeline e arquitetura: [link a adicionar]

### Resultados no conjunto de teste

Base final com 207.611 empresas e 2,50% de contratantes, dividida em 70/15/15 de forma
estratificada. A arquitetura escolhida foi o MLP com codificação por frequência, com peso de classe
balanceado e os hiperparâmetros definidos por 20 trials de Optuna (3 camadas, 128 unidades
iniciais, sem BatchNorm, dropout 0,294, AdamW).

| métrica | resultado |
|---|---|
| recall da classe "Contratou" | **92,4%** — 720 dos 779 contratantes do teste |
| contratantes perdidos | 59 |
| empresas sinalizadas | 9.006 (28,9% da base) |
| precisão | 8,0% — 3,2x a taxa-base de 2,5% |
| contatos por contratação | 12,5 (contra 40 abordando sem critério) |
| ROC-AUC | 0,900 |
| MCC | 0,224 |

A ordenação é a parte mais forte do resultado: os 10% de maior probabilidade convertem a 15,35%,
**6,1 vezes o acaso**, e já contêm 61,4% de todos os contratantes. Nos 20% melhores estão 83,2%.

Uma ressalva que o próprio notebook registra: o contra-peso de classe infla as probabilidades
previstas (média de 26,6% contra uma taxa real de 2,5%, com Brier de 0,137). O número que a rede
devolve serve para **ordenar** empresas e para comparar com o limiar, não para ser lido como chance
real de contratação.
