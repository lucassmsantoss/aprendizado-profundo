# Tarefa 2 — Otimização de hiperparâmetros do MNIST (Optuna)

Aluno: Lucas Medeiros — Disciplina: Aprendizado Profundo — PPgTI/IMD/UFRN

Notebook: `tarefa2_mnist_optuna.ipynb` (executado localmente em Python 3.13 / Windows, TensorFlow
2.21.0, CPU). Base: notebook do professor `mnist_keras.ipynb`.

## 1. Metodologia

Utilizou-se a biblioteca **Optuna** (algoritmo TPE, `direction="maximize"`) para buscar a melhor
combinação de hiperparâmetros de uma MLP (rede densa) para classificação do MNIST, otimizando a
**acurácia de validação** (10% do conjunto de treino) como métrica objetivo. Espaço de busca:

- `n_layers`: número de camadas densas ocultas (1 a 3)
- `units`: número de neurônios por camada oculta (32, 64 ou 128)
- `activation`: função de ativação das camadas ocultas (relu ou tanh)
- `drop_rate`: taxa de dropout (0.0 a 0.5, contínuo)
- `learning_rate`: taxa de aprendizado do otimizador Adam (1e-4 a 1e-2, escala log)
- `batch_size`: tamanho do lote (32, 64 ou 128)

Cada trial treinou o modelo por 8 épocas, com 20 trials no total (`n_trials=20`).

## 2. Resultados da busca (20 trials)

| Trial | Acc. validação | batch_size | n_layers | units | activation | drop_rate | learning_rate |
|---|---|---|---|---|---|---|---|
| 0 | 0.9692 | 128 | 1 | 64 | relu | 0.499 | 0.002060 |
| 1 | 0.9650 | 64 | 1 | 32 | tanh | 0.029 | 0.004781 |
| 2 | 0.9715 | 128 | 3 | 32 | relu | 0.017 | 0.005653 |
| 3 | 0.9645 | 32 | 1 | 64 | tanh | 0.389 | 0.003944 |
| 4 | 0.9648 | 64 | 2 | 64 | relu | 0.458 | 0.000462 |
| 5 | 0.9228 | 64 | 3 | 32 | relu | 0.492 | 0.000621 |
| 6 | 0.9798 | 32 | 1 | 128 | relu | 0.254 | 0.000525 |
| **7** | **0.9808** | **128** | **2** | **128** | **relu** | **0.1125** | **0.002429** |
| 8 | 0.9775 | 32 | 1 | 128 | tanh | 0.230 | 0.003179 |
| 9 | 0.9753 | 128 | 1 | 64 | relu | 0.295 | 0.003128 |
| 10 | 0.9615 | 128 | 2 | 128 | tanh | 0.132 | 0.000183 |
| 11 | 0.9805 | 32 | 2 | 128 | relu | 0.188 | 0.000959 |
| 12 | 0.9802 | 32 | 2 | 128 | relu | 0.125 | 0.001351 |
| 13 | 0.9630 | 32 | 2 | 128 | relu | 0.143 | 0.009718 |
| 14 | 0.9782 | 128 | 2 | 128 | relu | 0.187 | 0.001166 |
| 15 | 0.9782 | 32 | 3 | 128 | relu | 0.093 | 0.000192 |
| 16 | 0.9803 | 128 | 2 | 128 | relu | 0.333 | 0.001074 |
| 17 | 0.9793 | 128 | 2 | 128 | relu | 0.066 | 0.001906 |
| 18 | 0.9735 | 32 | 3 | 128 | tanh | 0.209 | 0.000339 |
| 19 | 0.9420 | 64 | 2 | 32 | relu | 0.171 | 0.000113 |

**Melhor trial: nº 7**, com acurácia de validação **0.9808**, hiperparâmetros:
`batch_size=128, n_layers=2, units=128, activation=relu, drop_rate=0.1125, learning_rate=0.002429`.

## 3. Modelo final e avaliação no conjunto de teste

O modelo final foi reconstruído com os melhores hiperparâmetros do trial 7 e treinado por 25
épocas (mais que as 8 usadas durante a busca).

**Arquitetura final:** `Flatten(784) → Dense(128, relu) → Dropout(0.1125) → Dense(128, relu) →
Dropout(0.1125) → Dense(10, softmax)`. **Total de parâmetros treináveis: 118.282** (≈462 KB).

**Resultado no conjunto de TESTE (10.000 imagens, nunca vistas):**

- **Acurácia de teste: 0.9788**
- **Perda (loss) de teste: 0.1058**

`classification_report` (teste):

| Classe | precisão | recall | f1-score | suporte |
|---|---|---|---|---|
| 0 | 0.99 | 0.99 | 0.99 | 980 |
| 1 | 0.99 | 0.99 | 0.99 | 1135 |
| 2 | 0.98 | 0.98 | 0.98 | 1032 |
| 3 | 0.97 | 0.98 | 0.98 | 1010 |
| 4 | 0.99 | 0.97 | 0.98 | 982 |
| 5 | 0.96 | 0.98 | 0.97 | 892 |
| 6 | 0.98 | 0.98 | 0.98 | 958 |
| 7 | 0.97 | 0.98 | 0.98 | 1028 |
| 8 | 0.99 | 0.96 | 0.97 | 974 |
| 9 | 0.96 | 0.98 | 0.97 | 1009 |
| **acurácia geral** | | | **0.98** | 10000 |

A rede não sofreu overfitting relevante: a acurácia de treino final (~0.99, ver curvas) e a de
teste (0.9788) ficam próximas, e a curva de perda de validação (ver `curvas_treinamento.png`)
estabiliza sem disparar, o que é coerente com o dropout de ~0.11 aplicado entre as camadas.
A classe com pior desempenho (5, recall 0.98/precisão 0.96) reflete a confusão clássica do MNIST
entre dígitos visualmente parecidos (5/3, 5/6), visível na matriz de confusão (`matriz_confusao.png`).

## 4. Comentário sobre o ajuste final e sua qualidade

Observando os 20 trials, o padrão é claro: os melhores resultados (acc. validação > 0.978)
concentram-se em `n_layers=1 ou 2`, `units=128` e `activation=relu`, com `learning_rate` entre
~5e-4 e ~2.5e-3, e `batch_size` de 32 ou 128. Isso é coerente com a teoria:

- **Mais unidades por camada (128) e poucas camadas** já bastam para o MNIST, um problema
  relativamente simples; `n_layers=3` não trouxe ganho consistente (trials 2, 5, 15, 18 variam
  bastante), sinal de que a profundidade extra não é bem aproveitada em só 8 épocas de busca.
- **ReLU superou tanh** de forma quase sistemática entre os melhores trials — a tanh (trials 1,
  3, 8, 10, 18) tende a saturar mais e converge mais devagar nesse regime de poucas épocas.
- **Learning rates muito baixos** (~1e-4, trials 10, 15, 19) e **muito altos** (~1e-2, trial 13)
  tiveram desempenho pior — o primeiro caso por não convergir a tempo, o segundo por
  instabilidade no treino. A faixa "doce" ficou entre ~5e-4 e ~2.5e-3.
- O **dropout** ótimo encontrado (0.1125) é moderado-baixo — sugere que, no MNIST, uma
  regularização mais leve já é suficiente, diferente de um problema com mais overfitting.

A busca convergiu para uma região estável de hiperparâmetros: os trials 7, 11, 12, 16 (todos com
`units=128`, `n_layers=2`, `relu`, learning rate entre 0.001 e 0.0024) têm desempenho muito
próximo (0.980–0.981), o que indica um ótimo estável e não um pico isolado de ruído estatístico.
O ganho sobre a configuração mais fraca da busca (trial 5, 0.9228) é de mais de 5 pontos
percentuais de acurácia de validação, obtido de forma sistemática via busca automática — e o
resultado final no teste (0.9788) confirma que o ajuste generaliza bem, sem overfitting aos dados
de validação usados durante a busca.
