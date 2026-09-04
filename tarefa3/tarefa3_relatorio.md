# Tarefa 3 — CNNs (PyTorch) para o Multiprova Corretor (EMNIST)

Aluno: Lucas Medeiros — Disciplina: Aprendizado Profundo — PPgTI/IMD/UFRN

Notebook: `tarefa3_cnn_emnist_pytorch.ipynb` (executado localmente em Python 3.13 / Windows,
PyTorch 2.14.0, CPU). Reprodução, em PyTorch, da melhor arquitetura de CNN de Silva Filho et al.
(2022) para o app Multiprova Corretor, aplicada a 3 subproblemas construídos a partir do EMNIST.

## 1. Arquitetura

`CNNMultiprova`: 4 blocos `Conv2d(3x3) → ReLU → MaxPool2d(2)` com 32→64→64→64 filtros, seguidos
de `Flatten → Linear(256, n_classes)`. Entrada: imagens EMNIST redimensionadas para 32×32, 1
canal. Treino: Adam (lr=1e-3), `CrossEntropyLoss`, batch size 128, até 12 épocas com early
stopping (paciência 3, monitorando perda de validação).

## 2. Subproblemas e resultados

**Digitos (1-5)** — split `digits` do EMNIST, mapeados para 5 classes (240.000 imagens de treino
originais → 102.000 treino / 18.000 validação / 20.000 teste após filtragem+split):

- Convergiu em 7 épocas (early stopping). **Acurácia de teste: 0.9975**.
- `classification_report`: precisão/recall/f1 = 1.00 em todas as 5 classes.

**V ou F** — split `letters`, filtrando apenas "v" (label 22) e "f" (label 6) → 2 classes
(8.160 treino / 1.440 validação / 1.600 teste):

- Convergiu em 11 épocas. **Acurácia de teste: 1.0000** (100%) — problema binário simples com
  bastante dado por classe, fácil de separar visualmente.

**Letras A-E** — split `letters`, filtrando "a" a "e" (labels 1-5) → 5 classes
(20.400 treino / 3.600 validação / 4.000 teste):

- Convergiu em 9 épocas. **Acurácia de teste: 0.9782**.
- `classification_report`: f1-score entre 0.97 (A) e 0.98 (demais); A tem o menor recall (0.95),
  provavelmente por confusão visual com outras letras manuscritas parecidas.

| Subproblema | Épocas até parar | Acc. teste |
|---|---|---|
| Dígitos (1-5) | 7 | 0.9975 |
| V ou F | 11 | 1.0000 |
| Letras (A-E) | 9 | 0.9782 |

## 3.1) Tabela: parâmetros treináveis e tamanho dos modelos exportados (.pt)

| Modelo | Parâmetros treináveis | Tamanho (MB) |
|---|---|---|
| Dígitos (1-5) | 93.957 | 0.363 |
| V ou F | 93.186 | 0.359 |
| Letras (A-E) | 93.957 | 0.363 |

Os três modelos têm praticamente o mesmo tamanho (a diferença de ~770 parâmetros entre os
modelos de 5 classes e o de 2 classes vem só da última camada densa, `Linear(256, n_classes)`).
Isso confirma que o custo do modelo é dominado pelas camadas convolucionais (compartilhadas na
arquitetura), não pela camada de saída — os modelos são bem enxutos (< 0.4 MB cada), compatíveis
com uso embarcado em um app mobile como o Multiprova Corretor.

## 3.2) Como o tamanho do modelo poderia ser reduzido?

1. **Reduzir a arquitetura**: menos filtros por camada (ex.: 16/32/32/32 em vez de 32/64/64/64)
   e/ou menos camadas — reduz diretamente o número de parâmetros, à custa de capacidade.
2. **Quantização (quantization)**: converter os pesos de float32 para int8 (ou float16),
   reduzindo o tamanho em até 4x com perda mínima de acurácia (`torch.quantization`, ou o
   conversor TFLite no caso de um modelo TensorFlow equivalente).
3. **Poda (pruning)**: remover pesos/filtros com magnitude próxima de zero, gerando uma rede
   esparsa que, combinada com formatos de armazenamento esparsos, reduz o tamanho real em disco.
4. **Convoluções separáveis em profundidade (depthwise separable)**: como no MobileNet, decompor
   uma convolução 3x3 completa em depthwise + pointwise (1x1), reduzindo parâmetros por camada.
5. **Destilação de conhecimento**: treinar uma rede "aluno" ainda menor para imitar as saídas
   dessas CNNs já treinadas ("professor"), mantendo desempenho próximo com menos parâmetros.
6. **Global Average Pooling** no lugar do `Flatten + Linear` final — no nosso caso a camada
   `Linear(256, n_classes)` já é pequena, mas em arquiteturas maiores essa troca costuma eliminar
   a maior parte dos parâmetros do modelo.
7. **Fatoração de baixo posto (low-rank factorization)** das matrizes de peso das convoluções.
8. **Formatos de exportação mais compactos**: ONNX ou TensorFlow Lite, que aplicam otimizações de
   grafo (fusão de camadas, remoção de operações redundantes) e permitem quantização integrada.

Como os modelos aqui já são pequenos (< 0.4 MB), a estratégia mais custo-benefício para um app
mobile como o Multiprova Corretor seria **quantização pós-treinamento para INT8** (redução de
~4x quase de graça, sem retreinar) combinada com **exportação para um formato compacto** (ONNX
Runtime Mobile ou TFLite), reservando poda/destilação/arquitetura menor para cenários com
restrição de memória ainda mais severa.
