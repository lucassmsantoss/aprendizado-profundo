# Aprendizado Profundo — Trabalho: Intro. Redes Neurais e Redes Convolucionais

Repositório: https://github.com/lucassmsantoss/aprendizado-profundo

Aluno: Lucas Medeiros
Disciplina: Aprendizado Profundo — PPgTI/IMD/UFRN
Docente: Prof. Josenalde Oliveira

Este repositório reúne as 3 tarefas solicitadas e o trabalho final da disciplina:

- **Tarefa 1** (`tarefa1/`): Estudo dirigido do TensorFlow Playground — experimentos reais de hiperparâmetros e respostas aos exercícios de fixação.
- **Tarefa 2** (`tarefa2/`): Otimização de hiperparâmetros do MNIST com Optuna, a partir do notebook base do professor.
- **Tarefa 3** (`tarefa3/`): Reprodução em PyTorch das arquiteturas CNN do artigo Silva Filho et al. (2022) sobre o Multiprova Corretor, aplicadas a subconjuntos do EMNIST (dígitos 1-5, V/F e letras A-E), com análise de parâmetros/tamanho dos modelos.
- **Trabalho Final** (`trabalho_final_recomendacao_consultorias/`): Recomendação de Consultorias Sebrae RN — projeto individual completo (Data Product Canvas, notebook, modelos treinados).

Um PDF único com as 3 tarefas consolidadas está em `relatorio_completo.pdf`.

## Notebooks

- Tarefa 2 — MNIST + Optuna: `tarefa2/tarefa2_mnist_optuna.ipynb` (já executado, com todos os
  outputs, gráficos e resultados reais salvos no próprio arquivo) — link Colab:
  https://colab.research.google.com/drive/1zFKRRcnSVH_FaU9bMy0xza6bvzjJmGZG?usp=sharing
- Tarefa 3 — CNNs PyTorch + EMNIST: `tarefa3/tarefa3_cnn_emnist_pytorch.ipynb` (já executado, com
  todos os outputs, gráficos e resultados reais salvos no próprio arquivo) — link Colab:
  https://colab.research.google.com/drive/1j0Qyu3_pJIpritZf15XOShYtwKJQGQu_?usp=sharing

## Trabalho Final — Recomendação de Consultorias Sebrae RN

Projeto individual que usa a base de empresas atendidas pelo Sebrae/RN (enriquecida com dados da
Receita Federal) para prever, em duas etapas encadeadas: (1) a propensão de uma empresa contratar
uma nova consultoria (Rede 1, binária), e (2) qual tema de consultoria recomendar para quem tem
propensão (Rede 2, multiclasse, avaliada via Recall@2/@3).

- Data Product Canvas: `trabalho_final_recomendacao_consultorias/data_project_canvas_recomendacao_consultorias.png`
- Notebook (Rede 1 + Rede 2, com pré-processamento, tuning via Optuna, avaliação, discussão e
  limitações): `trabalho_final_recomendacao_consultorias/trabalho_final_recomendacao_consultorias.ipynb`
  — link Colab: [link a adicionar após rodar no Colab]
- Modelos treinados (Keras): `trabalho_final_recomendacao_consultorias/modelos/`
- Base de dados: `trabalho_final_recomendacao_consultorias/base_modelagem_anonimizada.xlsx`,
  incluída neste repositório (já anonimizada). O notebook lê o arquivo local se ele existir e,
  caso contrário, baixa automaticamente direto deste repositório público — funciona em qualquer
  ambiente (Colab, Kaggle, etc.) sem precisar de login ou permissão de Google Drive (ver célula
  de configuração, seção 1 do notebook).
- Vídeo pitch (≤10 min, estilo pitch) explicando pipeline e arquitetura: [link a adicionar]

**Resultados principais:** Rede 1 — recall macro 0,85 e ROC-AUC 0,92 no teste; Rede 2 — recall
macro 0,27, Recall@2 0,61 e Recall@3 0,75 no teste. Detalhes, discussão e limitações no notebook
(seções 8 a 10).
